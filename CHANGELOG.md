# Changelog

Public numbering is **0.1.0**. First productized release of the Agent Skill.

## 0.1.0

Portable GitHub product, deterministic scoring contract, and evals/HTML/action packaging.

- Scanner path is portable: `python3 <this-skill>/scripts/artifact_scanner.py <path> --json` (also `--text`, `--stdin`). Agents never hardcode `~/.claude/skills/…`. Host dirs include `~/.agents/skills/`, `~/.claude/skills/`, `~/.grok/skills/`, or the clone.
- `SKILL.md` frontmatter: MIT, Python 3.9+, version `0.1.0`, English use-when plus bilingual triggers.
- When NOT to use: architecture ranking → `arquitectura-software-analyzer`; production-readiness → `vibe-proof-auditor`; docs vs code → `documentation-manager`; stack at scale → `scale-stack-framework`; full webapp spec from a one-liner → `mega-webapp-generator`.
- Deep is default. Quick only when the user explicitly asks for a short pass (`quick`, or an equivalent such as `rápido`). File count does not switch modes.
- Seven starting questions are answered **before** scoring. A stated solution is a hypothesis, not the problem.
- Skill body is English. Report narrative matches the request language; section titles, principle names, and rank tokens stay English. No auto-commit.
- Skill discovery announces installed version/path and suggests `npx skills update` when local < published 0.1.0. No silent auto-patch.
- One home per fact: overall formula, rank bands, 0–10 scale, and “simple average is the contract” live only in `references/scoring.md`. Principle definitions stay in `references/principles.md`. Techniques in `references/techniques.md`. Report skeleton in `references/report_template.md`.
- `scripts/score_report.py` recomputes overall (mean of the 15 integers, one decimal, half up) and rank. Does not invent principle scores. Exit 0/1/2. `--json` writes structured JSON.
- Reports land at the subject root: `ba-audit-report.md`, `.json`, `.html`. HTML via `scripts/render-report.py` (styles only; does not score). Open HTML only on an interactive TTY with `CI` unset.
- Tests (`unittest`, stdlib) for the scanner, scorer, renderer, and compare-eval.
- `evals/`: planted `stated-solution`, `solid-prd`, `gold-plated-backlog` fixtures plus floor/ceiling manifests. `scripts/compare-eval.py` checks those bounds and `--baseline` diffs new low scores. CI does not spawn agents.
- Composite action `ba-score` (`action.yml`) runs `score_report.py`.
- Worked example: `references/example-report.md` and `docs/example-report.html`.
- ADR `docs/adr/0001-html-render-does-not-score.md`.
- Install: `npx skills add pedroknigge/101-business-analysis -g -y`.
