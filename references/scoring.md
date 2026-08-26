# Scoring

Single home for the **0–10 scale**, **overall formula**, and **rank bands**. Principle definitions and per-principle evidence anchors live in `references/principles.md`. Techniques live in `references/techniques.md`. Report shape lives in `references/report_template.md`. Architecture ranking and production gates are out of scope (use `arquitectura-software-analyzer` / `vibe-proof-auditor`).

Do not copy these numbers into `SKILL.md`. Agents must not invent weights, ranks, or overall arithmetic.

## Fifteen scored principles

Integer **0–10** per principle. The agent classifies evidence; `scripts/score_report.py` does not invent principle scores.

| # | Canonical name |
|---|----------------|
| 1 | Problem Definition |
| 2 | Stakeholder Engagement |
| 3 | Value & Success Criteria |
| 4 | Constraints & Assumptions |
| 5 | Elicitation Completeness |
| 6 | Requirements Quality |
| 7 | Classification & Prioritization |
| 8 | Solution Options Evaluation |
| 9 | Traceability |
| 10 | Process Modeling |
| 11 | Data & Decision Modeling |
| 12 | Scope Discipline |
| 13 | Collaboration & Communication |
| 14 | Solution Evaluation |
| 15 | Requirements Life Cycle |

All 15 are required. Missing principles are a census error (`score_report.py` exits 1). Do not drop a principle as N/A to raise the average. If evidence is thin, **score conservatively** and note it — do not invent files, stakeholders, or metrics.

BABOK knowledge areas are covered by these principles (not scored as a second card): Planning & Monitoring → 15; Elicitation & Collaboration → 5, 13; Requirements Life Cycle Management → 9, 15; Strategy Analysis → 1, 3, 4, 8; Requirements Analysis & Design Definition → 6, 7, 10, 11, 12; Solution Evaluation → 14.

## Scale (principle 0–10)

| Score | Meaning |
|-------|---------|
| 9–10 | Exemplary |
| 7–8 | Strong |
| 5–6 | Adequate with gaps |
| 3–4 | Significant issues |
| 0–2 | Major violations / absent |

Per-principle “what 9 vs 2 looks like” stays in `references/principles.md`. This table is the shared language for the integer.

## Overall (simple average — the contract)

`overall = (sum of the 15 integer scores) / 15` to **one decimal**, **half up**.

There are **no weights**. Optional or “light” weighting is **not used**. Agents must not reweight Problem Definition, Value, or any other principle. Context (Agile vs Waterfall, idea vs regulated program) may change the **prose** and how strictly anchors are applied; it must not change the formula.

`scripts/score_report.py` recomputes overall from the 15 integers. The renderer does not.

## Rank bands

Rank tokens are English even when the narrative is in another language. Do not invent aliases. Section titles, header keys, and scorecard principle names also stay English so `scripts/score_report.py` can parse the file.

| Overall | Rank |
|---------|------|
| ≥ 8.5 | Excellent |
| 7.0–8.4 | Good |
| 5.5–6.9 | Fair |
| ≤ 5.4 | Poor |

Edges (inclusive): **8.5** Excellent, **7.0** Good, **5.5** Fair, **5.4** Poor.

## Evidence coverage (optional)

If the scorecard’s evidence cell for a principle is non-empty, that principle is **covered**.

`coverage = covered / 15`, published as an integer percent, half up.

Missing evidence → score conservatively and say so. Coverage is **not** a rank input. If the header omits Evidence coverage, `score_report.py` does not fail for that.

## Score census (optional)

Count how many of the 15 fall in 9–10 / 7–8 / 5–6 / 3–4 / 0–2. Report-only; not an input to overall.

## Worked example

`references/example-report.md` (ShiftSwap). Fifteen integers sum to **96** → `overall = 96 / 15 = 6.4` → **Fair**.
