# PRD: DeskQueue wait management

## Problem

Lobby wait time at two clinics averages 34 minutes. 18% of arrivals leave before check-in (front-desk log, last quarter). The current process is a paper clipboard; the next patient is shouted. Root cause: no visible queue, no SLA, no handoff when a clinician is running late.

This is not “we need an app”. The need is **arrivals know their place and staff can pull the next patient without shouting**, so walk-outs drop.

## Stakeholders (RACI)

| Stakeholder | Interest | Influence | RACI |
|-------------|----------|-----------|------|
| Clinic ops manager | Walk-outs, complaints | High | Accountable |
| Front-desk clerk | Speed of check-in | High | Responsible |
| Clinician | Next-patient pull | Medium | Consulted |
| Patient | Fair wait, privacy | Medium | Consulted (sample of 12 interviews) |
| Privacy officer | PHI in the lobby | High | Consulted |
| IT | Integration with the EHR | Medium | Informed |

## Success

- Baseline walk-out rate 18%. Target 10% in 60 days after change.
- Median wait (clip-time to room) from 34 min to ≤ 25 min.
- Privacy: no full names on a public display.

Owner: ops manager. Review: day 30 and day 60. Data: front-desk log + EHR rooming timestamps.

## Constraints and assumptions

- Hard: privacy policy forbids full names on a lobby screen; no new vendor this fiscal year without RFQ.
- Preference (not a need): mobile app.
- Assumption (validate by week 2): 70% of arrivals have a smartphone. Expires if the sample of 12 does not hold.

## Options

| Option | Value to problem | Cost / risk / time | Fit |
|--------|------------------|--------------------|-----|
| Do nothing | None | Walk-outs continue | Reject |
| Numbered tickets + wall display of numbers only | High | Low, 2 weeks, no PHI | Recommended first slice |
| Clipboard process change only (script + SLA) | Medium | Tiny | Complement |
| Custom mobile app + AI wait prediction | Unproven | High, PHI, RFQ | Deferred |

Weighted scoring: value 40%, time 25%, privacy risk 25%, cost 10%. Tickets+display 8.2; process-only 6.4; app 4.1.

## Must / Should / Could / Won't (MoSCoW)

- Must: issue a queue number; display next number; clerk marks done; no PHI on display.
- Should: SMS “you are next” if the patient opted in.
- Could: predicted wait.
- Won't: social login, in-lobby video ads, AI triage.

## User stories + acceptance

As a clerk I want to issue the next number so that arrivals have a place in line.
Given a patient at the desk, When the clerk hits next, Then a unique number is printed and the wall display lists it as waiting.

As a clinician I want to pull the next number so that we stop shouting names.
Given waiting numbers, When the clinician pulls next, Then the display shows that number as called and the clerk log records the timestamp.

Traces: OBJ-walkout → REQ-queue-number → story clerk-issue → UAT-U01.
Traces: OBJ-wait → REQ-pull-next → story clinician-pull → UAT-U02.

## Process (as-is / to-be)

As-is: arrive → clipboard name → wait in chairs → name shouted → room. Exceptions: late clinician, two surnames the same, interpreter needed.

To-be: arrive → number → wait → number called → room. Same exceptions; interpreter flagged on the clerk ticket, not the wall.

## Data and decisions

Entity: Visit {number, state: waiting|called|done|no-show, timestamps}. Decision: call next = oldest waiting number not marked done. No patient name on Visit as displayed.

## Life cycle

Status: proposed → approved (ops manager) → implemented → measured. Fortnightly refinement. Dropped items go to Won't with date.

## Out of scope

Mobile app, AI prediction, EHR write-back in slice 1. EHR read of appointment roster is Could after the 60-day review.
