# Evals

Three planted fixtures plus expected score **floors/ceilings**. The agent still classifies evidence. These files measure whether a competent pass lands in the right band (a stated-solution brief scores low on problem/options/value; a solid PRD scores high on those). Scanner planted-dir detection skips `evals/` and `tests/fixtures/` so fixtures are not treated as product docs of this skill.

## Fixtures

| Dir | Planted | Expected |
|-----|---------|----------|
| `fixtures/stated-solution` | “We need a mobile app” with no problem, no stakeholders, no options | Problem, options, value, elicitation **ceilings** (must be low) |
| `fixtures/solid-prd` | Problem, RACI, MoSCoW, options, metrics, AC, traceability | Problem, stakeholders, value, options, requirements **floors** (must be high) |
| `fixtures/gold-plated-backlog` | Dozens of stories, no value, no non-goals, everything Must | Scope, classification, value **ceilings** |

## Run (after an agent audit)

```bash
python3 scripts/score_report.py ba-audit-report.md --json report.json
python3 scripts/compare-eval.py evals/expected/stated-solution.json report.json
```

Baseline (fail only on new low principle scores):

```bash
python3 scripts/compare-eval.py --baseline previous.json report.json
```

CI does **not** spawn coding agents. CI tests the scanner, `score_report.py`, the renderer, and the compare-eval contract.
