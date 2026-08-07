(() => {
  "use strict";

  const $ = (selector) => document.querySelector(selector);
  const els = {
    datePicker: $("#date-picker"),
    dayCount: $("#day-count"),
    weekCount: $("#week-count"),
    themeToggle: $("#theme-toggle"),
    programProgress: $("#program-progress"),
    progressBar: $("#program-progress-bar"),
    streak: $("#streak"),
    weeklyHours: $("#weekly-hours"),
    weekPhase: $("#week-phase"),
    todayKicker: $("#today-kicker"),
    todayTheme: $("#today-theme"),
    todayFocus: $("#today-focus"),
    themeDot: $("#theme-dot"),
    taskStack: $("#task-stack"),
    restPanel: $("#rest-panel"),
    sessionTime: $("#session-time"),
    sessionDeliverable: $("#session-deliverable"),
    sessionRing: $("#session-ring"),
    sessionPercent: $("#session-percent"),
    checkinNote: $("#checkin-note"),
    checkinFeedback: $("#checkin-feedback"),
    saveCheckin: $("#save-checkin"),
    roadmap: $("#roadmap-track"),
    phaseSelect: $("#phase-select"),
    sprintCount: $("#sprint-count"),
    sprintList: $("#sprint-list"),
    noteInput: $("#note-input"),
    saveNote: $("#save-note"),
    noteList: $("#note-list"),
    toast: $("#toast"),
    settingsDialog: $("#settings-dialog"),
    settingsOpen: $("#settings-open"),
    settingsForm: $("#settings-form"),
    startDate: $("#start-date"),
    targetRole: $("#target-role"),
    weeklyGoal: $("#weekly-goal"),
    saveSettings: $("#save-settings"),
    exportProgress: $("#export-progress"),
  };

  const colorMap = {
    violet: "#9986ff", cyan: "#5bd2ce", amber: "#edc36a", rose: "#ef839e",
    blue: "#79a6ff", green: "#66d9a8", indigo: "#a68cf3", pink: "#ee88c6", orange: "#ef9a64",
  };
  let state = { data: null, selectedEnergy: null };
  let toastTimer;

  function showToast(message) {
    window.clearTimeout(toastTimer);
    els.toast.textContent = message;
    els.toast.classList.add("show");
    toastTimer = window.setTimeout(() => els.toast.classList.remove("show"), 2900);
  }

  async function api(url, options = {}) {
    const hasBody = options.body !== undefined;
    const response = await fetch(url, {
      ...options,
      headers: { ...(hasBody ? { "Content-Type": "application/json" } : {}), ...(options.headers || {}) },
    });
    const type = response.headers.get("content-type") || "";
    const body = type.includes("application/json") ? await response.json() : await response.text();
    if (!response.ok) throw new Error(body.error || "Something went wrong. Please try again.");
    return body;
  }

  function minutesLabel(minutes) {
    const hours = Math.floor(minutes / 60);
    const remainder = minutes % 60;
    return hours ? `${hours}h ${String(remainder).padStart(2, "0")}m` : `${remainder}m`;
  }

  function cleanDate(value) {
    return new Date(`${value}T12:00:00`).toLocaleDateString(undefined, { weekday: "long", month: "short", day: "numeric" });
  }

  function phaseColor(color) { return colorMap[color] || colorMap.violet; }

  function renderTask(block, date) {
    const label = document.createElement("label");
    label.className = `task-item ${block.complete ? "is-complete" : ""}`;
    const checkbox = document.createElement("input");
    checkbox.className = "task-check";
    checkbox.type = "checkbox";
    checkbox.checked = block.complete;
    checkbox.setAttribute("aria-label", `Mark ${block.label} complete`);
    checkbox.addEventListener("change", async () => {
      checkbox.disabled = true;
      try {
        const result = await api("/api/completion", { method: "POST", body: JSON.stringify({ date, block_id: block.id, completed: checkbox.checked }) });
        state.data.today = result.today;
        state.data.stats = result.stats;
        renderStats();
        renderToday();
        showToast(checkbox.checked ? "Block completed. Nicely measured." : "Block reopened.");
      } catch (error) {
        checkbox.checked = !checkbox.checked;
        showToast(error.message);
      } finally {
        checkbox.disabled = false;
      }
    });
    const copy = document.createElement("span");
    copy.className = "task-copy";
    const title = document.createElement("span"); title.className = "task-title"; title.textContent = block.label;
    const detail = document.createElement("span"); detail.className = "task-detail"; detail.textContent = block.detail;
    copy.append(title, detail);
    const duration = document.createElement("span"); duration.className = "task-duration"; duration.textContent = minutesLabel(block.minutes);
    label.append(checkbox, copy, duration);
    return label;
  }

  function renderToday() {
    const today = state.data.today;
    const { week } = today;
    els.dayCount.textContent = `Day ${String(today.day_number).padStart(3, "0")}`;
    els.weekCount.textContent = `Week ${String(week.week).padStart(2, "0")}`;
    els.weeklyHours.textContent = `${week.weekly_hours}h`;
    els.weekPhase.textContent = `Phase ${week.phase}`;
    els.todayTheme.textContent = today.theme;
    els.todayFocus.textContent = today.focus;
    els.themeDot.style.background = phaseColor(week.color);
    els.themeDot.style.boxShadow = `0 0 0 5px color-mix(in srgb, ${phaseColor(week.color)}, transparent 83%)`;
    els.sessionTime.textContent = minutesLabel(today.minutes);
    els.sessionDeliverable.textContent = today.deliverable;

    let kicker = `${today.day_name} · Week ${week.week} · ${cleanDate(today.date)}`;
    if (today.is_before_start) kicker = `Your program begins ${cleanDate(state.data.settings.start_date)}`;
    if (today.is_after_program) kicker = "You completed the planned two-year arc";
    els.todayKicker.textContent = kicker;

    const done = today.completed_count;
    const percent = Math.round((done / today.blocks.length) * 100);
    els.sessionPercent.textContent = `${percent}%`;
    els.sessionRing.style.strokeDashoffset = String(113.1 - (113.1 * percent / 100));

    const specialDay = today.is_rest_day || today.is_before_start || today.is_after_program;
    els.restPanel.hidden = !specialDay;
    els.taskStack.hidden = specialDay;
    if (specialDay) {
      const heading = els.restPanel.querySelector("strong");
      const paragraph = els.restPanel.querySelector("p");
      if (today.is_before_start) {
        heading.textContent = "Your runway begins soon";
        paragraph.textContent = "Use this time to make the setup frictionless: choose a workspace, reserve five modest slots, and arrive rested on day one.";
      } else if (today.is_after_program) {
        heading.textContent = "The roadmap is complete";
        paragraph.textContent = "Keep the practices that give you energy: a light maintenance rhythm, thoughtful applications, and recovery around live interviews.";
      } else {
        heading.textContent = "Intentional recovery day";
        paragraph.textContent = "Rest is training infrastructure. A ten-minute recall or a walk is optional; guilt is not on the plan.";
      }
      return;
    }
    els.taskStack.replaceChildren(...today.blocks.map((block) => renderTask(block, today.date)));
  }

  function renderStats() {
    const { stats, today } = state.data;
    els.programProgress.textContent = `${stats.program_progress}%`;
    els.progressBar.style.width = `${Math.max(stats.program_progress, 1)}%`;
    els.streak.textContent = stats.streak;
    els.weekPhase.textContent = today.week.phase_name;
  }

  function renderCheckin() {
    const checkin = state.data.checkin;
    state.selectedEnergy = checkin?.energy || null;
    els.checkinNote.value = checkin?.note || "";
    document.querySelectorAll("[data-energy]").forEach((button) => {
      button.classList.toggle("active", Number(button.dataset.energy) === state.selectedEnergy);
      button.setAttribute("aria-pressed", String(Number(button.dataset.energy) === state.selectedEnergy));
    });
  }

  function renderRoadmap() {
    const currentPhase = state.data.today.week.phase;
    els.roadmap.replaceChildren(...state.data.phases.map((phase, index) => {
      const card = document.createElement("article");
      card.className = `phase-card ${currentPhase === index + 1 ? "active" : ""}`;
      card.style.setProperty("--phase-color", phaseColor(phase.color));
      const week = document.createElement("p"); week.className = "phase-week"; week.textContent = `W${String(phase.first_week).padStart(2, "0")}–${String(phase.last_week).padStart(2, "0")}`;
      const dot = document.createElement("div"); dot.className = "phase-number";
      const title = document.createElement("h3"); title.textContent = phase.name;
      const outcome = document.createElement("p"); outcome.textContent = phase.outcome;
      card.append(week, dot, title, outcome);
      return card;
    }));
  }

  function renderPhaseOptions() {
    const oldValue = els.phaseSelect.value;
    els.phaseSelect.replaceChildren();
    const all = new Option("All sprints", "all");
    els.phaseSelect.add(all);
    state.data.phases.forEach((phase, index) => els.phaseSelect.add(new Option(`Phase ${index + 1}: ${phase.name}`, String(index + 1))));
    els.phaseSelect.value = oldValue || String(state.data.today.week.phase);
  }

  function renderCurriculum() {
    const selection = els.phaseSelect.value || "all";
    const sprints = selection === "all" ? state.data.curriculum : state.data.curriculum.filter((sprint) => sprint.phase === Number(selection));
    els.sprintCount.textContent = `${sprints.length} SPRINT${sprints.length === 1 ? "" : "S"}`;
    els.sprintList.replaceChildren(...sprints.map((sprint) => {
      const item = document.createElement("article"); item.className = "sprint-item"; item.style.setProperty("--sprint-color", phaseColor(sprint.color));
      const number = document.createElement("div"); number.className = "sprint-number"; number.textContent = `W${String(sprint.week).padStart(2, "0")}`;
      const inner = document.createElement("div");
      const phase = document.createElement("p"); phase.className = "sprint-phase"; phase.textContent = `Phase ${sprint.phase} · ${sprint.weekly_hours}h/week`;
      const title = document.createElement("h3"); title.textContent = sprint.title;
      const focus = document.createElement("p"); focus.className = "sprint-focus"; focus.textContent = sprint.focus;
      const deliverable = document.createElement("p"); deliverable.className = "sprint-deliverable";
      const bold = document.createElement("b"); bold.textContent = "Evidence: ";
      deliverable.append(bold, document.createTextNode(sprint.deliverable));
      inner.append(phase, title, focus, deliverable); item.append(number, inner); return item;
    }));
  }

  function renderNotes() {
    if (!state.data.notes.length) {
      const empty = document.createElement("p"); empty.className = "empty-notes"; empty.textContent = "No ledger entries yet. Capture what changed your thinking today.";
      els.noteList.replaceChildren(empty); return;
    }
    els.noteList.replaceChildren(...state.data.notes.map((note) => {
      const item = document.createElement("article"); item.className = "note-item";
      const when = document.createElement("span"); when.className = "note-date";
      when.textContent = new Date(note.created_at).toLocaleDateString(undefined, { month: "short", day: "numeric" });
      const body = document.createElement("p"); body.textContent = note.body; item.append(when, body); return item;
    }));
  }

  function renderSettings() {
    const config = state.data.settings;
    els.startDate.value = config.start_date;
    els.targetRole.value = config.target_role;
    els.weeklyGoal.value = config.weekly_goal;
  }

  function renderAll({ rebuildOptions = false } = {}) {
    renderStats(); renderToday(); renderCheckin(); renderRoadmap();
    if (rebuildOptions) renderPhaseOptions();
    renderCurriculum(); renderNotes(); renderSettings();
  }

  async function loadData(dateValue, options = {}) {
    const parameter = dateValue ? `?date=${encodeURIComponent(dateValue)}` : "";
    try {
      state.data = await api(`/api/bootstrap${parameter}`);
      if (!dateValue && state.data.today.is_before_start) {
        els.datePicker.value = state.data.settings.start_date;
        return loadData(state.data.settings.start_date, options);
      }
      els.datePicker.value = state.data.today.date;
      renderAll(options);
    } catch (error) { showToast(error.message); }
  }

  function setupEvents() {
    els.datePicker.addEventListener("change", () => loadData(els.datePicker.value));
    els.phaseSelect.addEventListener("change", renderCurriculum);
    document.querySelectorAll("[data-energy]").forEach((button) => button.addEventListener("click", () => {
      state.selectedEnergy = Number(button.dataset.energy);
      renderCheckin();
      const messages = ["Keep it very small today—one block is enough.", "Reduce scope; protect the habit.", "A steady session is the whole assignment.", "Good energy: do the planned blocks, no bonus marathon.", "Strong day: use it for quality, then stop on time."];
      els.checkinFeedback.textContent = messages[state.selectedEnergy - 1];
    }));
    els.saveCheckin.addEventListener("click", async () => {
      if (!state.selectedEnergy) { showToast("Pick an energy level first."); return; }
      try {
        await api("/api/checkin", { method: "POST", body: JSON.stringify({ date: state.data.today.date, energy: state.selectedEnergy, note: els.checkinNote.value }) });
        state.data.checkin = { energy: state.selectedEnergy, note: els.checkinNote.value };
        showToast("Check-in saved. The plan can flex with you.");
      } catch (error) { showToast(error.message); }
    });
    els.saveNote.addEventListener("click", async () => {
      const body = els.noteInput.value.trim(); if (!body) { showToast("Write a short observation first."); return; }
      try {
        const result = await api("/api/notes", { method: "POST", body: JSON.stringify({ body }) });
        state.data.notes.unshift(result.note); state.data.notes = state.data.notes.slice(0, 6); els.noteInput.value = ""; renderNotes(); showToast("Added to your learning ledger.");
      } catch (error) { showToast(error.message); }
    });
    els.settingsOpen.addEventListener("click", () => els.settingsDialog.showModal());
    els.settingsForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      try {
        const result = await api("/api/settings", { method: "POST", body: JSON.stringify({ start_date: els.startDate.value, target_role: els.targetRole.value, weekly_goal: els.weeklyGoal.value, theme: document.body.classList.contains("light") ? "light" : "dark" }) });
        state.data.settings = result.settings; els.settingsDialog.close(); showToast("Plan settings saved."); loadData(els.datePicker.value, { rebuildOptions: true });
      } catch (error) { showToast(error.message); }
    });
    els.exportProgress.addEventListener("click", () => { window.location.assign("/api/export"); });
    els.themeToggle.addEventListener("click", async () => {
      const light = !document.body.classList.contains("light"); document.body.classList.toggle("light", light);
      try { await api("/api/settings", { method: "POST", body: JSON.stringify({ theme: light ? "light" : "dark" }) }); if (state.data) state.data.settings.theme = light ? "light" : "dark"; } catch (error) { showToast(error.message); }
    });
  }

  async function boot() {
    setupEvents();
    await loadData(null, { rebuildOptions: true });
    if (state.data?.settings.theme === "light") document.body.classList.add("light");
  }
  boot();
})();
