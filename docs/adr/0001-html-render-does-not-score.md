# ADR 0001: HTML render is style, not scores

The renderer (`scripts/render-report.py`) turns `ba-audit-report.md` into HTML.

It must not compute, round, or invent principle scores, overall, or rank tokens. Those live in `references/scoring.md` and are already in the markdown. `scripts/score_report.py` is the only arithmetic.

Artifacts land at the subject root, next to the markdown.
