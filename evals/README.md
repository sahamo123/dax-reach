# Behavioral Evaluation

These are realistic task cases, not automated keyword checks. Use the same model, tools, input artifacts, and task prompt when comparing this package against upstream-only or no-skill baselines. Give the executing model the request and raw artifacts, but keep the reviewer rubric separate.

Cases and review criteria: [cases.json](cases.json).

For each run record package commit, host/model identifier when exposed, tools available, date, exact input, raw output, reviewer, and findings. Evaluate usefulness, factual support, completed deliverables, appropriate scope, and accurate limitations. A failure involving fabricated evidence or unauthorized publication should be recorded separately from writing quality.

Suggested comparative protocol: run each case in each condition at least three times, randomize output order for review, and report per-case observations and variability. This is a proposed protocol; no aggregate benchmark results are implied. Don't merge structural/unit-test passes into behavioral scores.

Use synthetic examples only. Do not submit real forms, publish sites, contact third parties, or incur API charges during these offline cases.
