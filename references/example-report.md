# Business Analysis 101 Report

**Project:** `/Users/demo/shiftswap`
**Date:** 2026-08-25
**Audit mode:** Deep
**Subject type:** repo
**Cadence:** Agile
**Overall Score:** 6.4 / 10
**Rank:** Fair
**Evidence coverage:** 100%

Worked example for the formula in `references/scoring.md` (ShiftSwap, fictional ops team that asked for a mobile shift-swap app). Integers sum to 96 → 96 / 15 = 6.4 → Fair.

## Executive Summary

- Strengths: as-is swimlane in `docs/process-as-is.md`; stories in `docs/stories.md` use Given/When/Then; standup notes name payroll, union steward, and shift leads.
- Weaknesses: success is “app launched”; options paper is missing (process/policy never scored); no out-of-scope list; no plan to measure overtime after release.
- Verdict: competent Agile backlog on a real process, still anchored to a predetermined mobile app. Problem and process are ahead of value and options.

## Starting Questions

1. Real problem/opportunity: Overtime cost and coverage gaps when swaps are arranged on WhatsApp and payroll is told after the fact (`docs/process-as-is.md`, finance note in `docs/stakeholders.md`).
2. Who cares and why: Shift leads (coverage), employees (fairness), payroll (correct hours), union steward (policy), finance (overtime). IT is a delivery party, not the owner.
3. Success (measurable): Stated as “launch the app in Q3”. Overtime $ and late payroll corrections are mentioned, not baselined.
4. Constraints: Union swap rules; payroll cutoff T+1; no budget for a vendor this year (`docs/stakeholders.md`). “Must be mobile” is a preference treated as a constraint.
5. Possible ways: Mobile app (chosen); improve WhatsApp template + payroll form; policy that swaps need lead approval by T-12h; do nothing.
6. Best value given constraints: Unknown — options were not scored. Policy + form is the cheap hypothesis.
7. How we will know it worked: No owner, no baseline, no review date. UAT is “tap through the screens”.

## Quantitative Snapshot

- Subject type: repo (scanner)
- Files: docs + README; artifact counts include process, user_stories, stakeholders, acceptance
- Keyword hits: problem, stakeholder, requirement, gherkin, process, constraint
- Gaps flagged: no options / alternatives signal; no out-of-scope; no outcome-validation signal

## Score census

| Band | Count |
|------|-------|
| 9–10 | 0 |
| 7–8 | 7 |
| 5–6 | 7 |
| 3–4 | 1 |
| 0–2 | 0 |

## Scorecard

| # | Principle | Score (0-10) | Key Evidence | Recommendation |
|---|-----------|--------------|--------------|----------------|
| 1 | Problem Definition | 8 | `docs/process-as-is.md` names WhatsApp workarounds and overtime leakage | Keep; stop restating the app as the problem in the README |
| 2 | Stakeholder Engagement | 7 | `docs/stakeholders.md` lists leads, payroll, union; no RACI | Add RACI for approve-swap vs inform-payroll |
| 3 | Value & Success Criteria | 5 | README success = “app in Q3”; overtime mentioned, no baseline | Pull last quarter overtime $ and late-correction count |
| 4 | Constraints & Assumptions | 6 | Union rules and payroll cutoff are real; “must be mobile” is not | Split hard vs preference; log the mobile assumption |
| 5 | Elicitation Completeness | 6 | Process doc + stories; no observation of a live swap | Shadow one weekend swap; capture exceptions |
| 6 | Requirements Quality | 8 | `docs/stories.md` Given/When/Then for request/approve/notify | Add rules for denied swaps and cutoff misses |
| 7 | Classification & Prioritization | 7 | MoSCoW on stories; Must still includes push notifications | Cut notify-all from Must; keep approve-by-cutoff |
| 8 | Solution Options Evaluation | 4 | Only the app is in `README.md`; policy/form not scored | One-page options: app vs form vs policy vs do-nothing |
| 9 | Traceability | 5 | Stories map to AC; no link to an objective id | OBJ-overtime → REQ-approve-cutoff → story → UAT |
| 10 | Process Modeling | 8 | As-is swimlane with WhatsApp, lead, payroll; to-be sketched | Add exception path: swap after cutoff |
| 11 | Data & Decision Modeling | 6 | “Shift” and “swap” used consistently; eligibility rules in prose | Decision table: who may swap with whom |
| 12 | Scope Discipline | 5 | No out-of-scope; chat and calendar sync crept into Could | Write non-goals; freeze chat/calendar |
| 13 | Collaboration & Communication | 8 | Same terms in process + stories; finance can read the as-is | Keep; publish the options table in the same language |
| 14 | Solution Evaluation | 5 | UAT = screen walkthrough; no overtime review | 30-day post-release: overtime $ vs baseline |
| 15 | Requirements Life Cycle | 8 | Fortnightly refinement notes in `docs/stories.md` | Add status: proposed / approved / dropped |

## BA Artifacts

### Problem statement

Weekend coverage is arranged in WhatsApp. Approved swaps reach payroll late or not at all, so overtime is paid on the wrong person and vacant slots are filled at premium rates. The need is **timely, policy-compliant swap approval that payroll can trust** — not a mobile app as such.

### Stakeholder map

| Stakeholder | Interest | Influence | RACI |
|-------------|----------|-----------|------|
| Shift lead | Coverage | High | Accountable (approve) |
| Employee | Fair swaps | Medium | Responsible (request) |
| Payroll | Correct hours | High | Consulted / informed |
| Union steward | Policy | High | Consulted |
| Finance | Overtime $ | Medium | Informed |
| IT | Delivery | Medium | Responsible (build, if built) |

### Requirements inventory (gaps)

- Must: request, lead approve/deny before cutoff, payroll-ready record — present.
- Should: notify both parties — present, possibly over-scoped.
- Missing: denied-swap path, post-cutoff exception, eligibility rules as a table.
- Creep: in-app chat, calendar sync.

### Options compared

| Option | Value to problem | Cost / risk / time | Fit |
|--------|------------------|--------------------|-----|
| Do nothing | None | Overtime continues | Reject |
| Policy + paper/form | High if leads actually approve | Low cost, culture risk | Not scored by the team |
| WhatsApp template + payroll sheet | Medium | Tiny | Not scored |
| Custom mobile app | Unproven | High | Chosen without comparison |

### Assumptions & decisions

- Assumption: staff will install and use a new app (untested).
- Decision logged: Agile delivery, two-week slices (`docs/stories.md`).
- Missing decision: why not the form.

## Strengths

- `docs/process-as-is.md` is a real as-is, not a UI flow.
- Stories carry acceptance criteria a tester can execute.
- Union and payroll are in the stakeholder list, not only “users”.

## Weaknesses & Risks

- Predetermined solution — option 8 is the hole the rest of the analysis falls into.
- No baseline overtime, so the app can “succeed” while the cost does not move.
- Gold-plating path: chat and calendar in the same MVP conversation.

## Prioritized Roadmap

### P0 – Quick Wins (high leverage, low effort)

- One-page options (S). Why: principle 8 is the binding constraint. Technique: weighted scoring.
- Baseline overtime $ and late payroll corrections (S). Why: value is currently “launch”.

### P1

- Eligibility decision table (S). Why: union rules are constraints, not UI.
- RACI + out-of-scope list (S). Why: stakeholders exist; ownership of approve vs inform does not.

### P2 – Strategic

- 30-day outcome review against overtime (M). Why: solution evaluation.
- Only if options still pick software: first slice = approve-by-cutoff record payroll can import (M). Why: scope discipline.

## Cadence Notes

Agile refinement is already happening. That does not replace an options paper. Keep stories small; freeze chat/calendar until the outcome moves.

## Follow-ups

- Stakeholder workshop (60 min): score four options.
- Observation: one weekend swap.
- Traceability stub: OBJ-overtime → Must stories.
