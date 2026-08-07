"""Source-informed two-year curriculum for the preparation tracker.

The saved Interview Query guide is used as a directional input, not as an
official job specification. The schedule focuses on the guide's recurring
themes: statistical thinking, robust coding, online/time-series reasoning,
ML systems, functional-programming literacy, and clear communication.
"""

from __future__ import annotations


PHASES = [
    {
        "name": "Build the operating system",
        "weeks": range(1, 9),
        "color": "violet",
        "hours": 2.0,
        "outcome": "A sustainable practice rhythm, Python fluency, and probability language.",
        "topics": [
            ("Baseline & environment", "Set a humane cadence; audit Python, math, and interview gaps.", "Write your learning contract and a tiny clean-code kata."),
            ("Python for reliable data work", "Functions, iterators, testing, profiling, and numerical types.", "Ship a tested streaming-statistics utility."),
            ("Counting & conditional probability", "Combinatorics, Bayes' rule, conditional independence, simulation.", "Explain three probability puzzles aloud."),
            ("Random variables & distributions", "Expectation, variance, covariance, common discrete/continuous distributions.", "Build a Monte Carlo notebook with tests."),
            ("Statistical estimation", "Sampling, bias, variance, confidence intervals, bootstrap.", "Implement bootstrap intervals from scratch."),
            ("Linear algebra for ML", "Vectors, projections, eigen intuition, gradients, numerical conditioning.", "Derive and code least squares two ways."),
            ("Algorithms I", "Arrays, hash maps, heaps, complexity, invariants, edge cases.", "Complete four timed fundamentals with written reviews."),
            ("Recovery & consolidation", "Deliberate review, error log, spaced recall, first mock conversation.", "Publish a one-page fundamentals map."),
        ],
    },
    {
        "name": "Reason precisely",
        "weeks": range(9, 17),
        "color": "cyan",
        "hours": 2.25,
        "outcome": "Confident statistical reasoning and clear algorithmic implementation.",
        "topics": [
            ("Inference essentials", "Hypothesis tests, p-values, power, multiple comparisons.", "Explain when not to use a p-value."),
            ("Regression foundations", "OLS assumptions, regularization, residual diagnostics.", "Build a regression diagnostic checklist."),
            ("Classification & calibration", "Log loss, ROC/AUC limits, Brier score, thresholds, imbalance.", "Compare calibrated and uncalibrated models."),
            ("Trees & ensembles", "Bias/variance, bagging, boosting, feature leakage.", "Defend a model choice under a latency budget."),
            ("Bayesian foundations", "Priors, posteriors, conjugacy, credible intervals.", "Solve and narrate three posterior updates."),
            ("Monte Carlo & uncertainty", "Sampling, variance reduction, simulation diagnostics.", "Implement a Monte Carlo estimator and error bar."),
            ("Algorithms II", "Two pointers, binary search, trees, graphs, recursion.", "Complete four medium problems with invariant notes."),
            ("First deep review", "Mixed retrieval, first 45-minute coding + ML concept rehearsal.", "Record and score a mock interview."),
        ],
    },
    {
        "name": "Model with judgment",
        "weeks": range(17, 27),
        "color": "amber",
        "hours": 2.5,
        "outcome": "You can start with a baseline, validate it honestly, and explain every trade-off.",
        "topics": [
            ("Experimental discipline", "Baselines, leakage, train/validation/test, reproducibility.", "Write an experiment card template."),
            ("Time-aware validation", "Walk-forward splits, embargoes, drift, non-stationarity.", "Build a time-series cross-validation splitter."),
            ("Feature engineering", "Missingness, transformations, robust scaling, feature contracts.", "Create a documented feature pipeline."),
            ("Causal thinking", "Confounding, interventions, selection bias, counterfactual framing.", "Critique a misleading observational result."),
            ("Online learning", "Incremental updates, exploration/exploitation, regret intuition.", "Implement an online mean and bandit simulation."),
            ("State-space models", "Filtering, Kalman intuition, latent state, observation noise.", "Code a simple 1D Kalman filter."),
            ("Gaussian processes", "Kernels, posterior prediction, uncertainty, computational costs.", "Explain a kernel choice and its failure mode."),
            ("Bayesian logistic regression", "Posterior approximation, uncertainty-aware classification.", "Compare point estimates and posterior predictions."),
            ("Model critique week", "Interpretability, calibration, latency, risk, and monitoring.", "Present baseline → evidence → iteration in 6 minutes."),
            ("Consolidation", "Retrieval practice and a lower-load reset.", "Refine your error log and next-quarter plan."),
        ],
    },
    {
        "name": "Build for streams",
        "weeks": range(27, 39),
        "color": "rose",
        "hours": 2.75,
        "outcome": "You can code and reason about dynamic, noisy, latency-sensitive systems.",
        "topics": [
            ("Rolling statistics", "Sliding windows, moving z-scores, numerical stability.", "Implement a rolling mean/variance API."),
            ("Streaming quantiles", "Approximate summaries, memory constraints, error trade-offs.", "Explain exact vs approximate quantiles."),
            ("Reservoir sampling", "Uniform sampling from an unknown-length stream.", "Prove and implement reservoir sampling."),
            ("Exponential smoothing", "EMA, adaptation rate, noise, initialization bias.", "Benchmark EWMA under simulated drift."),
            ("Change detection", "CUSUM intuition, thresholds, false alarms, response plans.", "Build a toy drift alarm."),
            ("Anomalies & robust estimators", "Outliers, median/MAD, robust losses.", "Compare mean and robust estimators."),
            ("Time series modeling", "AR/MA intuition, stationarity, autocorrelation, residuals.", "Validate a forecasting baseline correctly."),
            ("Evaluation under shift", "Backtests, leakage, delayed labels, rolling metrics.", "Produce a time-aware evaluation report."),
            ("Latency engineering", "Complexity, caching, vectorization, memory, profiling.", "Optimize one slow path with a measured result."),
            ("Streaming design rehearsal", "Clarify requirements, choose data contracts, plan failures.", "Whiteboard a low-latency signal pipeline."),
            ("Integrated mini-project", "From stream ingestion to monitored baseline.", "Ship a small, testable streaming ML service."),
            ("Recovery & review", "Lower cognitive load; retrieve key ideas without cramming.", "Run a 45-minute mixed mock."),
        ],
    },
    {
        "name": "Engineer dependable ML",
        "weeks": range(39, 51),
        "color": "blue",
        "hours": 3.0,
        "outcome": "A production-minded mental model for data, deployment, reliability, and model risk.",
        "topics": [
            ("Data contracts", "Schemas, freshness, quality checks, idempotency.", "Specify a feature contract and failure policy."),
            ("Feature platforms", "Offline/online parity, backfills, point-in-time correctness.", "Design a feature store at a whiteboard."),
            ("Serving architecture", "Batch vs online inference, queues, caching, fallbacks.", "Choose an architecture under a latency SLO."),
            ("Model versioning", "Artifacts, lineage, reproducibility, safe rollbacks.", "Document a rollback runbook."),
            ("Monitoring", "Data drift, prediction drift, calibration, alert fatigue.", "Build a monitoring spec with response owners."),
            ("Testing ML systems", "Unit, integration, data, shadow, and property-based tests.", "Add tests to your streaming project."),
            ("Distributed data", "Partitions, joins, consistency, backpressure, replay.", "Explain a late-event handling strategy."),
            ("Distributed training", "Data parallelism, checkpoints, cost/throughput trade-offs.", "Sketch a reliable training workflow."),
            ("Security & safety", "Access control, secrets, auditability, incident thinking.", "Threat-model one small ML pipeline."),
            ("System design: feature store", "Freshness, dedupe, invalidation, serving, observability.", "Complete a timed 45-minute design."),
            ("System design: signal service", "Streaming ingestion to guarded low-latency serving.", "Present an end-to-end trade-off narrative."),
            ("Portfolio polish", "Make one project readable, reproducible, and measurable.", "Publish architecture, tests, and results."),
        ],
    },
    {
        "name": "Think in functional systems",
        "weeks": range(51, 63),
        "color": "green",
        "hours": 3.0,
        "outcome": "Functional-programming literacy and stronger collaboration in coding interviews.",
        "topics": [
            ("Functional essentials", "Pure functions, immutability, composition, types as design.", "Refactor a Python module into pure functions."),
            ("Recursion & ADTs", "Recursive data, algebraic data types, pattern matching.", "Solve tree and list problems recursively."),
            ("OCaml orientation", "Syntax, let bindings, lists, options, variants.", "Implement small data transformations in OCaml."),
            ("OCaml modules & tests", "Interfaces, modules, functors at a conceptual level.", "Read and explain a small typed module."),
            ("Algorithms under constraints", "Heaps, min queues, union-find, memory/time budgets.", "Implement a constant-time-min queue or equivalent."),
            ("Numerical reliability", "Overflow, precision, stable formulas, deterministic tests.", "Audit and improve a numerical function."),
            ("Debugging conversations", "Reproduce, isolate, hypothesize, test, communicate.", "Run a paired-debugging rehearsal."),
            ("Project narrative I", "Problem, constraints, baseline, evidence, iteration.", "Create a project story deck (six slides or notes)."),
            ("Project narrative II", "Failures, counterfactuals, limitations, next steps.", "Practice answering ten project follow-ups."),
            ("Behavioral evidence", "Feedback, conflict, humility, curiosity, mentoring.", "Write six concise STAR evidence cards."),
            ("Mock loop", "Coding + ML + project discussion + behavioral.", "Run a four-part mock with feedback."),
            ("Recovery & planning", "Reduce load and turn feedback into a new queue.", "Choose three high-leverage corrections."),
        ],
    },
    {
        "name": "Create evidence",
        "weeks": range(63, 77),
        "color": "indigo",
        "hours": 3.25,
        "outcome": "A credible portfolio and repeatable interview performance—not just more reading.",
        "topics": [
            ("Capstone framing", "Choose a meaningful streaming/uncertainty project with a small scope.", "Write a one-page project proposal."),
            ("Data & assumptions", "Data provenance, target definition, leakage risks, ethics.", "Create a data card and assumption ledger."),
            ("Baseline implementation", "Simple model, correct time split, reproducible environment.", "Ship the first measurable baseline."),
            ("Evaluation & calibration", "Metrics, uncertainty, robustness, error slices.", "Write a focused evaluation report."),
            ("Iteration by evidence", "Hypothesis-driven improvement; no blind tuning.", "Run and document two controlled iterations."),
            ("Serving prototype", "Interface, latency budget, tests, graceful degradation.", "Demo an inference path with timing."),
            ("Observability", "Dashboards, logs, drift, alert response.", "Add a monitored simulation or report."),
            ("Architecture story", "Data flow, model loop, risks, decision log.", "Draw and narrate the complete architecture."),
            ("Documentation sprint", "README, onboarding, design choices, limitations.", "Publish a recruiter-readable project README."),
            ("Coding pattern review", "Revisit weak patterns from error log.", "Complete three quality timed problems."),
            ("Probability clinic", "Targeted puzzle practice and derivation explanation.", "Explain five problems without notes."),
            ("ML depth clinic", "Targeted model, inference, or calibration weaknesses.", "Teach one topic in a five-minute recording."),
            ("Full mock I", "Technical interview plus project deep dive.", "Capture feedback and one measurable improvement."),
            ("Recovery & polish", "Light review and portfolio cleanup.", "Make your project demo frictionless."),
        ],
    },
    {
        "name": "Turn readiness into interviews",
        "weeks": range(77, 93),
        "color": "pink",
        "hours": 3.25,
        "outcome": "High-quality repetitions that preserve energy while improving interview readiness.",
        "topics": [
            ("Interview inventory", "Map evidence to coding, ML, systems, and collaboration.", "Build a simple readiness matrix."),
            ("Coding simulation I", "45-minute implementation, edge cases, complexity narration.", "Do two reviewed coding simulations."),
            ("ML simulation I", "Baseline, validation, calibration, uncertainty, trade-offs.", "Do two structured ML concept simulations."),
            ("System simulation I", "Real-time features, freshness, rollout, monitoring.", "Do one timed systems design."),
            ("Probability simulation I", "Conditional probability and expected-value reasoning aloud.", "Do five puzzles with assumption checks."),
            ("Coding simulation II", "Streaming and numerical problems under constraints.", "Do two reviewed coding simulations."),
            ("ML simulation II", "Shift, drift, online updates, and evaluation.", "Do two structured ML concept simulations."),
            ("System simulation II", "Serving latency, failure modes, rollback, observability.", "Do one timed systems design."),
            ("Project defense", "Defend every major decision with evidence and alternatives.", "Complete a hostile-but-kind project review."),
            ("Behavioral collaboration", "Clarify, disagree productively, invite feedback, learn.", "Practice six behavioral prompts aloud."),
            ("Application materials", "Resume, project bullets, role-tailored story, referrals.", "Finish a concise one-page resume."),
            ("Network with integrity", "Learn from people; no transactional volume targets.", "Prepare three thoughtful outreach notes."),
            ("Full mock II", "Three back-to-back rounds with recovery afterward.", "Write a post-mock correction plan."),
            ("Targeted repair I", "Repair the single largest bottleneck.", "Re-test the weak area."),
            ("Targeted repair II", "Repair the second-largest bottleneck.", "Re-test the weak area."),
            ("Rest & retrieval", "Lower load, sleep, and confidence-building recall.", "Run a light no-notes review."),
        ],
    },
    {
        "name": "Apply, adapt, sustain",
        "weeks": range(93, 105),
        "color": "orange",
        "hours": 3.0,
        "outcome": "A sustainable final mile: applications, refined practice, and recovery around interviews.",
        "topics": [
            ("Application sprint", "Tailor materials, verify role fit, track conversations.", "Submit only roles you can explain your fit for."),
            ("Coding refresh", "Core patterns and clear implementations—not volume grinding.", "Create a ten-problem confidence set."),
            ("Probability refresh", "High-yield derivations, estimation, simulation checks.", "Create a personal probability formula sheet."),
            ("ML refresh", "Validation, calibration, uncertainty, baseline → iteration stories.", "Create concise ML answer frameworks."),
            ("Systems refresh", "Feature/data/model life cycle, latency, failure and rollback.", "Create a systems design checklist."),
            ("Live interview buffer", "Adjust plan around active interviews and feedback.", "Turn real feedback into one bounded practice task."),
            ("Full mock III", "End-to-end rehearsal under realistic time and fatigue limits.", "Complete a full loop with a recovery day."),
            ("Portfolio audit", "Remove noise; make impact, evidence, and trade-offs obvious.", "Polish one project and resume bullet set."),
            ("Communication polish", "Assumptions first, structure, decision, caveat, next step.", "Record two answers and self-review."),
            ("Targeted repair III", "Work the remaining limiting skill deliberately.", "Demonstrate one clean improvement."),
            ("Interview-ready maintenance", "Short high-value repetitions and quality rest.", "Choose a 4-week maintenance rhythm."),
            ("Two-year retrospective", "Celebrate evidence, capture lessons, and plan the next chapter.", "Write your personal operating manual."),
        ],
    },
]


def build_curriculum():
    """Return the 104-week program as plain JSON-friendly dictionaries."""
    weeks = []
    for phase_index, phase in enumerate(PHASES, start=1):
        for index, (title, focus, deliverable) in enumerate(phase["topics"]):
            week_number = phase["weeks"].start + index
            weeks.append(
                {
                    "week": week_number,
                    "phase": phase_index,
                    "phase_name": phase["name"],
                    "color": phase["color"],
                    "title": title,
                    "focus": focus,
                    "deliverable": deliverable,
                    "weekly_hours": round(phase["hours"] * 5, 2),
                    "daily_hours": phase["hours"],
                }
            )
    return weeks


CURRICULUM = build_curriculum()


def daily_blocks(week: dict, weekday: int):
    """Return a five-day, recovery-aware session plan for a curriculum week."""
    minutes = int(week["daily_hours"] * 60)
    learning = max(35, round(minutes * 0.38 / 5) * 5)
    practice = max(40, round(minutes * 0.42 / 5) * 5)
    reflection = minutes - learning - practice
    labels = [
        ("Monday", "Learn the frame", "Read/derive the core idea; state assumptions in your own words."),
        ("Tuesday", "Implement deliberately", "Build a small, tested artifact; keep an edge-case list."),
        ("Wednesday", "Reason under constraints", "Solve one timed prompt and narrate time, memory, and statistical trade-offs."),
        ("Thursday", "Apply & explain", "Use the idea in a small scenario; explain baseline, evidence, and limitations."),
        ("Friday", "Retrieve & review", "Practice from memory; update your error log and choose next week’s focus."),
    ]
    day_name, day_focus, day_prompt = labels[weekday]
    if weekday == 4:
        learning = max(25, learning - 15)
        practice = max(30, practice - 15)
        reflection = minutes - learning - practice
    return {
        "day_name": day_name,
        "day_focus": day_focus,
        "theme": week["title"],
        "focus": week["focus"],
        "deliverable": week["deliverable"],
        "minutes": minutes,
        "blocks": [
            {"id": "learn", "label": "Concept", "minutes": learning, "detail": day_prompt},
            {"id": "build", "label": "Practice", "minutes": practice, "detail": "Work directly on: " + week["deliverable"]},
            {"id": "reflect", "label": "Close the loop", "minutes": reflection, "detail": "Log one insight, one uncertainty, and your next smallest step."},
        ],
    }
