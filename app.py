from __future__ import annotations

import csv
import io
import json
import os
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

from flask import Flask, Response, jsonify, render_template, request

from curriculum import CURRICULUM, PHASES, daily_blocks


BASE_DIR = Path(__file__).resolve().parent
DATABASE = Path(os.environ.get("DATABASE_PATH", BASE_DIR / "tracker.db"))

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


def db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with db_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS completions (
                work_date TEXT NOT NULL,
                block_id TEXT NOT NULL,
                completed_at TEXT NOT NULL,
                PRIMARY KEY (work_date, block_id)
            );
            CREATE TABLE IF NOT EXISTS checkins (
                work_date TEXT PRIMARY KEY,
                energy INTEGER NOT NULL,
                note TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                body TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        defaults = {
            "start_date": "2027-01-04",
            "target_role": "Machine Learning Engineer",
            "weekly_goal": "Show up five times; finish less, learn more.",
            "theme": "dark",
        }
        for key, value in defaults.items():
            conn.execute("INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)", (key, value))


def settings():
    with db_connection() as conn:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
    return {row["key"]: row["value"] for row in rows}


def date_for_request():
    payload = request.get_json(silent=True) if request.is_json else {}
    raw = request.args.get("date") or (payload or {}).get("date")
    if raw:
        try:
            return date.fromisoformat(raw)
        except ValueError:
            pass
    return date.today()


def date_context(target: date):
    config = settings()
    start = date.fromisoformat(config["start_date"])
    raw_day = (target - start).days
    bounded_day = min(max(raw_day, 0), 727)
    week_index = min(bounded_day // 7, len(CURRICULUM) - 1)
    week = CURRICULUM[week_index]
    weekday = bounded_day % 7
    active = 0 <= raw_day < 728
    return {
        "target": target,
        "start": start,
        "raw_day": raw_day,
        "day_number": bounded_day + 1,
        "week": week,
        "weekday": weekday,
        "active": active,
    }


def completion_summary():
    with db_connection() as conn:
        rows = conn.execute("SELECT work_date, block_id FROM completions").fetchall()
    return {(row["work_date"], row["block_id"]) for row in rows}


def progress_stats(completed=None):
    completed = completion_summary() if completed is None else completed
    total_blocks = len(CURRICULUM) * 5 * 3
    return {
        "completed_blocks": len(completed),
        "total_blocks": total_blocks,
        "streak": streak(completed),
        "program_progress": round(len(completed) / total_blocks * 100, 1),
    }


def streak(completions):
    completed_days = {date.fromisoformat(work_date) for work_date, _ in completions}
    run = 0
    cursor = date.today()
    while cursor in completed_days or (cursor.weekday() >= 5 and run > 0):
        if cursor.weekday() < 5 and cursor in completed_days:
            run += 1
        cursor -= timedelta(days=1)
    return run


def serialize_day(target: date):
    context = date_context(target)
    plan = daily_blocks(context["week"], min(context["weekday"], 4))
    rest_day = context["weekday"] >= 5
    work_date = target.isoformat()
    completed = completion_summary()
    for block in plan["blocks"]:
        block["complete"] = (work_date, block["id"]) in completed
    plan.update(
        {
            "date": work_date,
            "day_number": context["day_number"],
            "week": context["week"],
            "is_rest_day": rest_day,
            "is_before_start": context["raw_day"] < 0,
            "is_after_program": context["raw_day"] >= 728,
            "completed_count": sum(block["complete"] for block in plan["blocks"]),
        }
    )
    return plan


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/bootstrap")
def bootstrap():
    target = date_for_request()
    config = settings()
    completed = completion_summary()
    with db_connection() as conn:
        notes = conn.execute("SELECT id, body, created_at FROM notes ORDER BY id DESC LIMIT 6").fetchall()
        checkin = conn.execute("SELECT energy, note FROM checkins WHERE work_date = ?", (target.isoformat(),)).fetchone()
    return jsonify(
        {
            "settings": config,
            "today": serialize_day(target),
            "stats": progress_stats(completed),
            "checkin": dict(checkin) if checkin else None,
            "notes": [dict(row) for row in notes],
            "curriculum": CURRICULUM,
            "phases": [
                {"name": p["name"], "outcome": p["outcome"], "color": p["color"], "first_week": p["weeks"].start, "last_week": p["weeks"].stop - 1}
                for p in PHASES
            ],
        }
    )


@app.route("/api/completion", methods=["POST"])
def toggle_completion():
    payload = request.get_json(silent=True) or {}
    work_date = payload.get("date")
    block_id = payload.get("block_id")
    completed = bool(payload.get("completed"))
    if not work_date or block_id not in {"learn", "build", "reflect"}:
        return jsonify({"error": "A valid date and session block are required."}), 400
    try:
        date.fromisoformat(work_date)
    except ValueError:
        return jsonify({"error": "Date must use YYYY-MM-DD."}), 400
    with db_connection() as conn:
        if completed:
            conn.execute(
                "INSERT OR REPLACE INTO completions(work_date, block_id, completed_at) VALUES (?, ?, ?)",
                (work_date, block_id, datetime.utcnow().isoformat(timespec="seconds")),
            )
        else:
            conn.execute("DELETE FROM completions WHERE work_date = ? AND block_id = ?", (work_date, block_id))
    return jsonify({"ok": True, "today": serialize_day(date.fromisoformat(work_date)), "stats": progress_stats()})


@app.route("/api/checkin", methods=["POST"])
def save_checkin():
    payload = request.get_json(silent=True) or {}
    work_date = payload.get("date") or date.today().isoformat()
    energy = payload.get("energy")
    note = (payload.get("note") or "").strip()[:500]
    if not isinstance(energy, int) or energy not in range(1, 6):
        return jsonify({"error": "Energy must be a number from 1 to 5."}), 400
    with db_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO checkins(work_date, energy, note, created_at) VALUES (?, ?, ?, ?)",
            (work_date, energy, note, datetime.utcnow().isoformat(timespec="seconds")),
        )
    return jsonify({"ok": True})


@app.route("/api/notes", methods=["POST"])
def add_note():
    payload = request.get_json(silent=True) or {}
    body = (payload.get("body") or "").strip()[:1200]
    if not body:
        return jsonify({"error": "Write a short note first."}), 400
    with db_connection() as conn:
        cursor = conn.execute("INSERT INTO notes(body, created_at) VALUES (?, ?)", (body, datetime.utcnow().isoformat(timespec="seconds")))
    return jsonify({"ok": True, "note": {"id": cursor.lastrowid, "body": body, "created_at": datetime.utcnow().isoformat(timespec="seconds")}})


@app.route("/api/settings", methods=["POST"])
def save_settings():
    payload = request.get_json(silent=True) or {}
    allowed = {"start_date", "target_role", "weekly_goal", "theme"}
    updates = {key: str(value).strip()[:220] for key, value in payload.items() if key in allowed}
    if "start_date" in updates:
        try:
            date.fromisoformat(updates["start_date"])
        except ValueError:
            return jsonify({"error": "Start date must use YYYY-MM-DD."}), 400
    if "theme" in updates and updates["theme"] not in {"dark", "light"}:
        return jsonify({"error": "Theme must be dark or light."}), 400
    if not updates:
        return jsonify({"error": "No editable settings were supplied."}), 400
    with db_connection() as conn:
        for key, value in updates.items():
            conn.execute("INSERT OR REPLACE INTO settings(key, value) VALUES (?, ?)", (key, value))
    return jsonify({"ok": True, "settings": settings()})


@app.route("/api/export")
def export_progress():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["date", "block", "completed_at"])
    with db_connection() as conn:
        rows = conn.execute("SELECT work_date, block_id, completed_at FROM completions ORDER BY work_date, block_id").fetchall()
    for row in rows:
        writer.writerow([row["work_date"], row["block_id"], row["completed_at"]])
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=ml-prep-progress.csv"})


@app.route("/health")
def health():
    return {"status": "ok", "weeks": len(CURRICULUM)}


init_db()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
