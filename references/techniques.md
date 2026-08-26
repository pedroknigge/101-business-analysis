# Techniques

Catalog of techniques the agent may **recommend** in the report. Definitions and scores live in `references/principles.md` / `references/scoring.md`. Do not score techniques. Pick the smallest set that closes the gap.

## Elicitation & collaboration

| Technique | Use when | Avoid when |
|-----------|----------|------------|
| Interview | Need depth, political context, unstated needs | Many equivalent users (use a sample + survey) |
| Workshop / facilitation | Alignment across conflicting groups | Sponsor wants a private decision first |
| Observation / job shadowing | Stated process ≠ real process | Access is blocked; then say so |
| Document analysis | Legacy rules live in SOPs, contracts, tickets | Docs are the only source (confirm with people) |
| Survey | Volume, ranking, geographic spread | You need why, not just what |
| Prototype / wireframe | Validate UX or a misunderstood flow | Treating the mock as the approved solution |
| Interface analysis | System-to-system or API contracts | Human process is the real bottleneck |

## Analysis & modeling

| Technique | Use when |
|-----------|----------|
| Process model (BPMN, swimlanes, value stream) | Handoffs, delays, as-is vs to-be |
| Use case / user story + acceptance criteria | Capabilities the solution must have |
| Conceptual / logical data model | Shared meaning of entities; reporting; integrations |
| Decision table / decision model | Complex business rules, eligibility, pricing |
| Root-cause (5 Whys, fishbone) | Stated request is a symptom |
| Stakeholder map + RACI | Unclear ownership or missing voices |
| Impact analysis + risk / RAID | Change hits other processes, systems, or regs |

## Prioritization & options

| Technique | Use when |
|-----------|----------|
| MoSCoW | Need a shared language for must / should / could / won’t |
| Kano | Distinguish delighters from basics |
| Weighted scoring | Compare solution options against explicit criteria |
| Cost of delay | Sequencing a backlog under a value constraint |
| Buy vs build vs change-process vs do-nothing | The request jumped to “build an app” |

## Cadence

- **Waterfall / traditional:** detailed requirements up front; still question the problem; still keep traceability.
- **Agile:** same skills, smaller slices — backlog refinement, stories, acceptance criteria, continuous prioritization, frequent validation.

The underlying questions do not change. The level of detail and the batch size do.
