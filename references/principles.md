# Business Analysis Principles — Detailed Reference

Only home for **principle definitions**, indicators, anti-patterns, detection guidance, and **per-principle** 0–10 anchors.

Overall formula, rank bands, the shared 0–10 scale language, and “simple average is the contract” live in `references/scoring.md`. Techniques live in `references/techniques.md`. Do not invent weights or overall arithmetic here.

Aligned with BABOK knowledge areas without scoring them as a second card. Context (Agile vs Waterfall, idea vs regulated program) changes prose, not the formula.

---

## 1. Problem Definition

**Definition**: The underlying need or opportunity — why something is not working, or why a change is worth making. Distinct from the **stated request** and from any predetermined solution.

**Why it matters**: Solutions fail when they treat symptoms. A BA who accepts “build X” without a problem statement is documenting a guess.

**Good indicators**:
- Problem stated as a gap in outcomes (cost, risk, time, quality, revenue, compliance), not as a system.
- Root-cause work (5 Whys, fishbone, incident/ticket patterns) is visible.
- As-is pain is evidenced (metrics, quotes, observed workarounds).

**Anti-patterns**:
- “We need an app / dashboard / AI” with no failure of the current way of working.
- Problem restated as the sponsor’s favorite feature list.
- Multiple unrelated problems bundled as one initiative.

**Detection**: Scanner `keyword_hits.problem`; README/PRD opening; first user message. Ask: if we shipped the requested thing tomorrow, which business number moves?

**Scoring**:
- 9–10: Root cause named, evidenced, and separated from the solution idea.
- 5–6: A plausible problem exists but is still mixed with the solution.
- 0–2: Only a stated solution; need is absent or invented.

---

## 2. Stakeholder Engagement

**Definition**: Anyone who affects or is affected by the change is identified, with interest, influence, and how they will be involved (RACI, interviews, not “ comms later”).

**Why it matters**: Ignoring a key stakeholder is one of the most common causes of failed delivery. Late objections look like “changing requirements”.

**Good indicators**:
- Named roles (sponsor, end user, operator, regulator, downstream system owner), not “the business”.
- RACI or equivalent for decisions vs consult vs inform.
- Conflicting interests are written down, not smoothed over.

**Anti-patterns**:
- Only the requester is in the room.
- “Users” as a single persona when jobs differ (clerk vs manager vs auditor).
- IT and vendor treated as non-stakeholders.

**Detection**: Scanner `stakeholders` / `persona` / `raci`; org titles in the brief. Missing names → conservative score.

**Scoring**:
- 9–10: Map + engagement plan; conflicts explicit.
- 5–6: Core names present; operators or downstream missing.
- 0–2: No stakeholders, or only “we”.

---

## 3. Value & Success Criteria

**Definition**: The benefit the business expects, stated so someone can later say whether it happened. Analysis without a value focus becomes documentation for its own sake.

**Why it matters**: Prioritization, option choice, and “done” are undefined without it.

**Good indicators**:
- Baseline + target (e.g. overtime hours, cycle time, error rate, conversion) with owner and timebox.
- Leading vs lagging measures distinguished.
- Non-financial value (risk, compliance, employee time) is still measurable.

**Anti-patterns**:
- Success = “the app launched” or “stories accepted”.
- Vanity metrics with no link to the problem.
- KPI theater (copied OKRs that this change cannot move).

**Detection**: Scanner `okrs` / `value` / `kpi`. Briefs that only list features score low.

**Scoring**:
- 9–10: Measurable outcomes tied to the problem, with baseline or a plan to get one.
- 5–6: Qualitative success (“easier”, “faster”) without numbers.
- 0–2: No outcome; success is shipping.

---

## 4. Constraints & Assumptions

**Definition**: Limits that are real (time, budget, regulation, technology, culture, contracts) and beliefs that are not yet proven. Both are visible and challengeable.

**Why it matters**: Hidden assumptions become late surprises. Fake constraints (we must use X) masquerade as needs.

**Good indicators**:
- Assumptions log with owner and expiry (when we will validate).
- Constraints labeled hard vs preference.
- Regulatory or cultural constraints sourced (policy, law, union, brand).

**Anti-patterns**:
- “No constraints” on a real business change.
- Solution technology listed as a need (“must be a mobile app”).
- Silent assumption that current headcount / data quality / process compliance holds.

**Detection**: Scanner `constraint` / `assumption`. ADRs that smuggle “must” without a source.

**Scoring**:
- 9–10: Hard vs preference split; assumptions owned and dated.
- 5–6: Some constraints named; assumptions implicit.
- 0–2: None, or every preference treated as a law.

---

## 5. Elicitation Completeness

**Definition**: Stated **and** unstated needs are sought, using more than one technique when the subject warrants it. Elicitation is discovery, not a transcript of the first meeting.

**Why it matters**: Users describe workarounds. Sponsors describe politics. Operators describe exceptions. One source is a sample of one.

**Good indicators**:
- Mix of techniques (interview + observation or document analysis + workshop).
- Exceptions, errors, volumes, and “what we actually do on Fridays” captured.
- Open questions listed rather than filled with guesses.

**Anti-patterns**:
- Single email treated as the requirements set.
- No attempt to find unstated needs.
- Workshop that rubber-stamps a pre-drawn solution.

**Detection**: Multiple evidence sources vs one brief. Scanner gaps on stakeholder + process + requirement together.

**Scoring**:
- 9–10: Several techniques; unstated needs and exceptions present.
- 5–6: One solid source; likely gaps named.
- 0–2: Stated request copied forward.

---

## 6. Requirements Quality

**Definition**: Each requirement is a capability the solution must have, or a condition it must meet — clear, complete enough to implement, feasible, and testable. Bad requirements are expensive rework.

**Why it matters**: Ambiguity is paid for in build, test, and production.

**Good indicators**:
- Atomic, unambiguous statements; defined terms (glossary).
- Acceptance criteria (Given/When/Then or equivalent) on capabilities that will be built.
- Feasibility challenged (data exists? process owner exists?).

**Anti-patterns**:
- “Make it intuitive / world-class / like X”.
- Requirements that mix UI chrome with business rules.
- Copy-pasted stories without acceptance criteria.

**Detection**: Scanner `requirement` / `gherkin` / `story_template`. Count vague adjectives.

**Scoring**:
- 9–10: Testable, glossaried, feasible; few weasel words.
- 5–6: Mix of good stories and slogans.
- 0–2: Feature list or slogans only.

---

## 7. Classification & Prioritization

**Definition**: Requirements (and wants) are classified and ordered with an explicit method — MoSCoW, Kano, weighted scoring, cost of delay — so trade-offs are decisions, not feelings.

**Why it matters**: Everything-is-Must is not a priority. The BA helps stakeholders choose.

**Good indicators**:
- Wants vs needs vs constraints labeled.
- A Must set that could actually ship as a first slice.
- Ranking criteria agreed (value, risk, dependency), not HiPPO order.

**Anti-patterns**:
- Flat backlog of equal stories.
- Must-have for every requester.
- Priority = recency of the last meeting.

**Detection**: Scanner `moscow` / prioritization artifacts. Gold-plated backlogs score low here **and** on Scope Discipline.

**Scoring**:
- 9–10: Method visible; Must is small; criteria explicit.
- 5–6: Informal P0/P1 without criteria.
- 0–2: No priority, or everything is P0.

---

## 8. Solution Options Evaluation

**Definition**: The BA evaluates means of satisfying the need (process change, policy, buy, build, do nothing) against criteria — not merely documenting one predetermined idea.

**Why it matters**: The most expensive architecture is the one that solves the wrong problem. “Build the app” is an option, not an analysis.

**Good indicators**:
- At least two real alternatives plus do-nothing.
- Criteria: cost, risk, time, strategic fit, feasibility, value to the problem.
- Recommendation with what was rejected and why.

**Anti-patterns**:
- Options that are only UI variants of the same build.
- Vendor demo accepted as the business case.
- Do-nothing omitted so the change looks inevitable.

**Detection**: Scanner `options`. Stated-solution briefs without alternatives score low.

**Scoring**:
- 9–10: Compared options, including process/policy/do-nothing; recommendation tied to value.
- 5–6: One alternative mentioned, weakly scored.
- 0–2: Single predetermined solution.

---

## 9. Traceability

**Definition**: A requirement can be followed from business objective → requirement → design/story → test → outcome. Orphan features and orphan tests are visible.

**Why it matters**: Scope changes and defects need a line back to why the work exists. Without it, gold-plating hides.

**Good indicators**:
- IDs or explicit links (obj-03 → REQ-12 → story → AC → test).
- Each Must maps to at least one test or observable outcome.
- Dropped requirements are marked dropped, not silently gone.

**Anti-patterns**:
- Stories with no parent objective.
- Tests that check UI widgets, not the business rule.
- Traceability matrix as theatre (IDs that nothing uses).

**Detection**: Scanner `trace` / `traceability`. Even a small table beats a vibe.

**Scoring**:
- 9–10: Working chain from objective to test/outcome.
- 5–6: Partial links (stories ↔ AC only).
- 0–2: No chain.

---

## 10. Process Modeling

**Definition**: Current and future ways of working are made visible — steps, actors, handoffs, waits, exceptions — so the change is a process change, not only a screen change.

**Why it matters**: Software dropped onto a broken process automates the waste. Handoffs are where value dies.

**Good indicators**:
- As-is and to-be (swimlane, BPMN, value stream) with actors named.
- Volumes, SLAs, exception paths.
- Policy/manual steps called out, not hidden in “the system does it”.

**Anti-patterns**:
- UI flow mistaken for the business process.
- Happy path only.
- To-be drawn with no as-is (so no delta).

**Detection**: Scanner `process` / `.bpmn` / as-is / to-be. For briefs, a numbered as-is in prose counts.

**Scoring**:
- 9–10: As-is and to-be with actors, exceptions, and a clear delta.
- 5–6: Partial flow; missing exceptions or as-is.
- 0–2: No process; only features.

---

## 11. Data & Decision Modeling

**Definition**: Shared meaning of the things the business talks about (entities, states, relationships) and the rules that decide outcomes (decision tables, eligibility, pricing). Conceptual/logical first; physical schema is not the model.

**Why it matters**: Arguments about “what is an order / a customer / a shift” are requirements arguments. Hidden rules become code folklore.

**Good indicators**:
- Glossary aligned with a conceptual model.
- Decision tables for non-trivial rules.
- States and allowed transitions named.

**Anti-patterns**:
- Database tables treated as the business language.
- Rules only in Slack or in a developer’s head.
- Same term, three meanings.

**Detection**: Scanner `data` / glossary / decision table. Code-only schemas without a business glossary score mid at best.

**Scoring**:
- 9–10: Conceptual model + key decisions tabulated; terms defined.
- 5–6: Partial glossary or implied entities.
- 0–2: No shared language.

---

## 12. Scope Discipline

**Definition**: The work is bounded. Non-goals, out-of-scope, and deferred wants are explicit. Gold-plating (adding unnecessary requirements) is treated as a defect in the analysis.

**Why it matters**: Unbounded analysis produces unbounded delivery. Value concentrates in a small Must set.

**Good indicators**:
- Out-of-scope list with owners of the “later”.
- First slice that could still prove the outcome.
- Requirements challenged with “does this serve the problem?”.

**Anti-patterns**:
- Feature factory: more stories as progress.
- “While we’re at it” bundled into Must.
- Scope = whatever fits the sprint after the fact.

**Detection**: Scanner `scope` / `out of scope` / `non-goal`. Huge backlogs with no non-goals score low.

**Scoring**:
- 9–10: Tight Must, explicit non-goals, gold-plating called out.
- 5–6: Some trimming; still a wide first slice.
- 0–2: Unbounded or clearly gold-plated.

---

## 13. Collaboration & Communication

**Definition**: The BA is understood by both business and technical audiences. Decisions, open questions, and disagreements are written so the next person can continue.

**Why it matters**: A brilliant model that only the BA understands is not analysis. Misaligned language is rework.

**Good indicators**:
- Same terms in the problem statement, stories, and engineering notes.
- Visuals used where prose fails (one process picture, one options table).
- Open questions owned; no silent “we’ll see”.

**Anti-patterns**:
- Jargon dump at the business, or feature dump at engineering.
- Analysis trapped in a private chat.
- Status reports that hide unresolved conflict.

**Detection**: Tone of existing docs; presence of a shared artifact vs only tickets. Thin briefs can still score mid if the *request* is already bilingual and honest.

**Scoring**:
- 9–10: Shared language, visible decisions, both audiences served.
- 5–6: One audience well served; the other guessing.
- 0–2: Opaque, oral-only, or conflicting stories in circulation.

---

## 14. Solution Evaluation

**Definition**: Whether the delivered change solved the business problem and returned the expected value — not whether tickets closed. Includes support during implementation and after release.

**Why it matters**: Requirements that are never validated against outcomes are a one-time document exercise. BABOK Solution Evaluation lives here.

**Good indicators**:
- Pre-delivery plan with baseline or baseline plan, target, owner, data source, review point, and action if the target misses.
- Post-delivery observed outcome delta and an explicit continue / adapt / stop decision.
- UAT against acceptance criteria that map to the problem.
- Rollback / learn path if the outcome misses.

**Anti-patterns**:
- Done = deployed.
- No baseline, so “improvement” cannot be shown.
- UAT as a click-through of screens.

**Detection**: Scanner `validation` / UAT / outcome. Pre-delivery subjects score on the *plan*, not on retrofitted metrics.

**Scoring**:
- 9–10: Measurement plan tied to the original value with baseline or baseline plan, target, owner, data source, review point, and action if the target misses; post-delivery subjects also show the observed delta and continue / adapt / stop decision.
- 5–6: UAT or “we’ll look at usage” without a baseline.
- 0–2: No idea how to know it worked.

---

## 15. Requirements Life Cycle

**Definition**: Analysis is an ongoing discovery process: planning the BA work, maintaining requirements as they change, and retiring what is obsolete. Not a one-shot BRD.

**Why it matters**: Businesses change while you build. A frozen document that nobody updates is fiction. A never-ending discovery with no baseline is also failure.

**Good indicators**:
- Cadence named (backlog refinement, change control, review board).
- Versioning / status on requirements (proposed, approved, implemented, retired).
- BA work itself estimated and monitored (what will we elicit next, with whom).

**Anti-patterns**:
- “The spec is done” on day 1 of a six-month build.
- Endless workshops with no baseline.
- Changes absorbed as “the developers already know”.

**Detection**: Evidence of iteration (changelog of requirements, refinement notes) vs a single static dump. Agile cadence without change control still needs a baseline.

**Scoring**:
- 9–10: Planned BA work, statused requirements, change path.
- 5–6: Informal updates; no status model.
- 0–2: One-time document, or chaos with no baseline.

---

## How to use this reference in audit mode

1. Answer the seven starting questions from `SKILL.md` first.
2. State the non-numeric Decision Readiness conclusions; do not derive them from scores.
3. For each principle, gather evidence (scanner JSON, files, quoted brief).
4. Score an **integer 0–10** from the anchors here. Overall and rank come from `references/scoring.md` via `scripts/score_report.py`.
5. Cite real paths or quotes. Do not invent stakeholders or KPIs.
6. When principles conflict (speed vs elicitation completeness), name the trade-off in prose. Do not reweight.
