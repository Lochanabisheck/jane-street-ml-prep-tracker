# Signal / Prep

A source-informed, two-year Jane Street machine-learning-engineering preparation tracker. It starts at two focused hours a weekday, builds intensity gradually, preserves weekends and consolidation weeks, and stores progress locally in SQLite.

The curriculum is informed by the supplied Interview Query guide, not an official Jane Street hiring specification. It emphasizes the themes surfaced in that guide: probability/Bayesian reasoning, streaming and time-series ML, reliable software and ML systems, functional-programming literacy, and clear discussion of assumptions and trade-offs.

## What’s included

- 104 specific weekly sprints from 2027-01-04 through 2028-12-31 (start date is editable).
- Daily three-block sessions, weekday-only, starting at 2h and stepping up gradually to 3–3.25h.
- Recovery-week language, weekend rest, energy check-ins, learning notes, and CSV export.
- Progress persistence via a local SQLite database—no account or external service required.
- Dark/light theme, mobile layout, roadmap, detailed curriculum filter, and interview reasoning flow.

## Run locally

Requires Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. Your data is saved to `tracker.db` beside the app. Set `DATABASE_PATH` to use another persistent location.

## Put it on GitHub and deploy

GitHub stores the source code, but GitHub Pages cannot run Flask or SQLite. Use GitHub as the repository, then connect it to a Python host such as Render, Railway, or Fly.io.

1. Create an empty GitHub repository and push this folder.
2. In Render, select **New → Web Service** and connect the repository.
3. Use build command `pip install -r requirements.txt` and start command `gunicorn app:app`.
4. Add a persistent disk and set `DATABASE_PATH` to a path on that disk (for example `/var/data/tracker.db`). Without persistent storage, progress resets whenever the service restarts.

For multi-user hosting, replace SQLite with a managed Postgres database and add authentication; the current app is intentionally a single-user private tracker.

## Source used

- Supplied HTML: *Jane Street Machine Learning Engineer Interview Guide for 2026* (Interview Query), canonical URL: <https://www.interviewquery.com/interview-guides/jane-street-machine-learning>

The website and curriculum intentionally avoid promises of employment. Interview processes and open roles change, so verify current details directly from the employer before applying.
