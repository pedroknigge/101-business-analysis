# Report Template for Business Analysis 101

Use this exact structure in explicit audit mode. Section titles, header keys, principle names, and rank tokens stay **English** (the scorer parses them). Write the narrative (readiness, verdict, evidence, recommendations, roadmap) in the language of the request. Rank tokens: `Excellent` / `Good` / `Fair` / `Poor` — `references/scoring.md`. Audit constants live only in `references/`; business baselines and targets must come from evidence or be labeled proposed.

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
- 1–2 sentence diagnostic verdict (copy the Rank header computed by `score_report.py`; do not invent a second rank or infer decision readiness from it)

## Decision Readiness

| Outcome | Conclusion | Evidence | Critical unknown / next evidence |
|---------|------------|----------|----------------------------------|
| Right problem | Validated / Provisional / Unknown | | |
| Best available option | Recommended: … / Not decision-ready | | |
| Measurable value | Realized / Measurement-ready / Measurable with gaps / Not measurable / Unknown | | |

This gate is non-numeric. A high Rank cannot override an unresolved row. `Realized` requires post-delivery outcome evidence; `Measurement-ready` requires a baseline or baseline plan, target, owner, data source, review point, and action if the target misses. Use `Measurable with gaps` when the outcome is plausible but one or more of those elements is unresolved; reserve `Not measurable` for cases with no observable outcome.

## Starting Questions
1. Real problem/opportunity:
2. Who cares and why; decision owner:
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

Scores are integers 0–10. Empty evidence → score conservatively; do not invent files. `scripts/score_report.py` validates Decision Readiness and recomputes overall and rank from this table.

## BA Artifacts
### Problem statement
### Stakeholder map
| Stakeholder | Interest | Influence | RACI |
|-------------|----------|-----------|------|
Decision owner: [role / Unknown]
### Requirements inventory (gaps and outcome trace)
If `Not decision-ready`, inventory existing requirements and evidence gaps only. Do not create implementation requirements or a solution backlog.

| Requirement / gap | Stakeholder need | Measurable outcome / ID | Acceptance evidence | Priority / status |
|-------------------|------------------|-------------------------|---------------------|-------------------|
### Options compared
Decision criteria: [derived from desired value, hard constraints, feasibility, and risk]

| Option | Expected value | Constraints / feasibility | Cost / time / risk | Evidence & uncertainty | Decision rationale |
|--------|----------------|---------------------------|--------------------|------------------------|--------------------|
### Recommendation and rationale
Recommended option or `Not decision-ready`; material trade-offs; rejected alternatives; confidence; what could reverse the decision.
### Value realization plan
| Outcome | Baseline / baseline plan | Target | Owner | Data source | Review point | Action if missed |
|---------|--------------------------|--------|-------|-------------|--------------|------------------|
### Assumptions & decisions

## Strengths
## Weaknesses & Risks
## Prioritized Roadmap
If `Not decision-ready`, include only discovery, evidence, option-comparison, and measurement actions. Do not include implementation slices.
### P0 – Quick Wins (high leverage, low effort)
### P1
### P2 – Strategic
(For each item: what / why / effort S-M-L / suggested technique from `references/techniques.md`)

## Cadence Notes
(Waterfall vs Agile: what changes in batch size, not in the questions.)

## Follow-ups
```
