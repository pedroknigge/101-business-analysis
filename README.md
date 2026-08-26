# 101-business-analysis

**Solve the right problem, choose the best-supported option, and verify measurable value** — for a repo, PRD, feature request, idea, process, or predetermined “we need an app”.

```bash
npx skills add pedroknigge/101-business-analysis -g -y
```

```
    ┌─────────────────────────────────┐
    │  problem ≠ requested feature    │
    │  stakeholders · value · options │
    │  requirements that can be tested│
    │  did the outcome actually move? │
    └─────────────────────────────────┘
         b u s i n e s s  a n a l y s i s
              ── 101 analyzer ──
         question the problem, not the epic
```

Pre-1.0 (`0.2.0`). An outcome-first Business Analysis skill with an optional deterministic audit scorer. Not a BABOK certification and not a project-manager replacement.

By default, the agent frames the real decision, separates the problem from the requested solution, examines evidence, and compares credible options. Only after the decision gate is ready does it define the minimum outcome-testing change and close the loop with a value-realization plan. It does not force a score or create report files for ordinary BA work.

Ask explicitly for an audit, score, rank, maturity review, or BA audit report to run the 15-principle audit. `scripts/artifact_scanner.py` inventories evidence, `scripts/score_report.py` validates Decision Readiness and recomputes overall (simple average) and rank, and the HTML renderer styles the Markdown. The separate Decision Readiness gate prevents a good average from masking an unresolved problem, option choice, or value measure.

Ranks stay English: **Excellent** · **Good** · **Fair** · **Poor**.

Install once. It lands in every coding agent the [Skills CLI](https://github.com/vercel-labs/skills) finds (Grok, Claude Code, Cursor, Codex, Windsurf, Copilot, Gemini CLI, and 70+ more).

## 📦 Install (all your agents, all projects)

```bash
npx skills add pedroknigge/101-business-analysis -g -y
```

`-g` = global (home directory, every project). Omit it to install only in the current repo. `-y` skips prompts. The CLI auto-detects installed agents and **symlinks** them to one copy, so updates are a single pull.

This repo is a valid Agent Skill (`SKILL.md` at the root) per [agentskills.io](https://agentskills.io/specification).

## 🔄 Update

```bash
npx skills update 101-business-analysis -g -y
```

Or update every installed skill:

```bash
npx skills update -g -y
```

## 🧭 Use

In any supported agent:

- `/101-business-analysis`
- “analiza como BA”
- “business analysis 101”
- “cuáles son los requisitos de verdad”
- “is this the problem or the feature?”
- “stakeholder and value review”

Point it at a project path, a PRD, or paste the request. Decision support is the default: it answers in chat, scales depth to the decision, and does not score unless asked.

For the deterministic audit, ask to “audit and score” the subject. Deep is the audit default; say “quick” (or an equivalent such as “rápido”) for a shorter audit. If the host can spawn parallel agents, Deep may fan out independent principle groups; Decision Readiness, overall, and rank are each determined **once** by the coordinator and `score_report.py` as appropriate.

The skill body is English. The report **narrative** matches the user’s language; section titles, principle names, and rank tokens stay English so the scorer can parse the file.

An explicit audit returns in chat by default. When report files are requested, it writes Markdown + JSON at the subject root (HTML opens only on an interactive TTY):

- `ba-audit-report.md` — 📋 evidence report
- `ba-audit-report.json` — 🧮 computed overall / rank / scores
- `ba-audit-report.html` — 🖥 styled twin

`scripts/score_report.py` recomputes the math. `scripts/compare-eval.py --baseline` diffs new low scores.

Planted fixtures: `evals/`. Worked HTML: `docs/example-report.html`.

## ⚡ One-off without installing

```bash
npx skills use pedroknigge/101-business-analysis
```

## 📁 Manual copy (no Node)

```bash
git clone https://github.com/pedroknigge/101-business-analysis.git ~/.grok/skills/101-business-analysis
```

Symlink or copy that folder into the skills directory of each agent you use (`~/.claude/skills/`, `~/.cursor/skills/`, `~/.codex/skills/`, `~/.agents/skills/`, …). Prefer `npx skills add` so updates stay one command.

Source of truth for this checkout is this repo — not a host `~/.grok/skills` copy.

## 🗂 Layout

```
101-business-analysis/
├── SKILL.md                      # Agent prompt
├── README.md
├── CHANGELOG.md
├── VERSION
├── LICENSE
├── action.yml                    # Composite: score_report.py
├── scripts/
│   ├── artifact_scanner.py       # BA artifacts + keyword signals
│   ├── score_report.py           # Readiness validation + overall/rank; --json
│   ├── compare-eval.py           # expected.json vs report JSON; --baseline
│   ├── report_parse.py           # Shared markdown parse (not HTML)
│   ├── report_theme.py           # HTML CSS theme
│   └── render-report.py          # Markdown → HTML (no scores)
├── evals/                        # Planted fixtures + expected manifests
├── tests/
├── references/
│   ├── principles.md             # Definitions (only home)
│   ├── scoring.md                # Formula, scale, rank bands
│   ├── techniques.md             # Elicitation / modeling catalog
│   ├── report_template.md        # Report skeleton
│   ├── skill-discovery.md        # Install path / upgrade
│   └── example-report.md         # Worked report
└── docs/adr/
    └── 0001-html-render-does-not-score.md
```

Python **3.9+**. Scripts are stdlib only.

```bash
python3 -m py_compile scripts/artifact_scanner.py scripts/score_report.py scripts/compare-eval.py scripts/render-report.py scripts/report_parse.py scripts/report_theme.py
python3 -m unittest discover -s tests -v
```

## 📐 Contract (do not restate numbers here)

| Fact | Home |
|------|------|
| Outcome-first behavior and Decision Readiness | `SKILL.md` |
| Principle definitions, indicators, anti-patterns, per-principle anchors | `references/principles.md` |
| 0–10 scale, simple-average overall, rank bands | `references/scoring.md` |
| Techniques catalog | `references/techniques.md` |
| Report skeleton | `references/report_template.md` |
| Report format | `SKILL.md` |
| Decision Readiness validation + overall / rank recompute | `scripts/score_report.py` |
| HTML render | `scripts/render-report.py` |
| HTML render does not score | `docs/adr/0001-html-render-does-not-score.md` |
| One worked report | `references/example-report.md` (`docs/example-report.html`) |
| Planted evals | `evals/` |
| Floors / ceilings / baseline | `scripts/compare-eval.py` |
| Install path / upgrade | `references/skill-discovery.md` |

## 🔗 Related skills

- Architecture-principle ranking → `arquitectura-software-analyzer`
- Production-readiness / anti-vibe / listo para prod → `vibe-proof-auditor`
- Docs vs code / AGENTS.md hub → `documentation-manager`
- Platform/stack at scale → `scale-stack-framework`

## 📜 License

MIT
