# Report Template for Business Analysis 101

Use this exact structure. Section titles, header keys, principle names, and rank tokens stay **English** (the scorer parses them). Write the narrative (verdict, evidence, recommendations, roadmap) in the language of the request. Rank tokens: `Excellent` / `Good` / `Fair` / `Poor` — `references/scoring.md`. Numbers live only in `references/` — never invent them.

```markdown
# Business Analysis 101 Report

**Project:** [path or brief label]
**Date:** [today]
**Audit mode:** [Deep / Quick]
**Subject type:** [repo / spec / brief / process / decision]
**Cadence:** [Waterfall / Agile / mixed / unknown]
**Overall Score:** X.X / 10
**Rank:** [Excellent | Good | Fair | Poor]
**Evidence coverage:** NN%

## Executive Summary
- 3 strengths
- 3 critical weaknesses
- 1–2 sentence verdict (copy the Rank header computed by `score_report.py`; do not invent a second rank)

## Starting Questions
1. Real problem/opportunity:
2. Who cares and why:
3. Success (measurable):
4. Constraints:
5. Possible ways:
6. Best value given constraints:
7. How we will know it worked:

Unknown stays unknown.

## Quantitative Snapshot
(From artifact_scanner.py — real output only)
- Subject type / files / docs
- Artifact counts
- Keyword hits
- Gaps the scanner flagged

## Score census
| Band | Count |
|------|-------|
| 9–10 | |
| 7–8 | |
| 5–6 | |
| 3–4 | |
| 0–2 | |

Counts must sum to 15.

## Scorecard

| # | Principle | Score (0-10) | Key Evidence | Recommendation |
|---|-----------|--------------|--------------|----------------|
| 1 | Problem Definition | | | |
| 2 | Stakeholder Engagement | | | |
| 3 | Value & Success Criteria | | | |
| 4 | Constraints & Assumptions | | | |
| 5 | Elicitation Completeness | | | |
| 6 | Requirements Quality | | | |
| 7 | Classification & Prioritization | | | |
| 8 | Solution Options Evaluation | | | |
| 9 | Traceability | | | |
| 10 | Process Modeling | | | |
| 11 | Data & Decision Modeling | | | |
| 12 | Scope Discipline | | | |
| 13 | Collaboration & Communication | | | |
| 14 | Solution Evaluation | | | |
| 15 | Requirements Life Cycle | | | |

Scores are integers 0–10. Empty evidence → score conservatively; do not invent files. `scripts/score_report.py` recomputes overall and rank from this table.

## BA Artifacts
### Problem statement
### Stakeholder map
| Stakeholder | Interest | Influence | RACI |
|-------------|----------|-----------|------|
### Requirements inventory (gaps)
### Options compared
| Option | Value to problem | Cost / risk / time | Fit |
|--------|------------------|--------------------|-----|
### Assumptions & decisions

## Strengths
## Weaknesses & Risks
## Prioritized Roadmap
### P0 – Quick Wins (high leverage, low effort)
### P1
### P2 – Strategic
(For each item: what / why / effort S-M-L / suggested technique from `references/techniques.md`)

## Cadence Notes
(Waterfall vs Agile: what changes in batch size, not in the questions.)

## Follow-ups
```
