# Artifact Definition — Target Assessment Lead

## Status

Product definition approved by the human Product owner on 2026-07-24. Development/Architecture, UX, and QA review are required before execution planning or implementation.

## Purpose

A **Target Assessment Lead** (`target_assessment_lead`) is a persistent workstream artifact that groups one or more indications which justify further assessment toward a possible target.

It is not:

- a target;
- a target candidate;
- a completed assessment;
- proof that the indications describe the same object;
- authorization to publish anything to the target bank.

Its value is to prevent a potentially important pattern from remaining only in chat while avoiding premature target creation.

## Position in the intelligence flow

`raw records → indications → target assessment lead → assessment → target candidate`

Promotion between steps is explicit. Adding indications to a lead never creates or updates a target automatically.

## Primary user flow

1. The user creates or opens a workstream with an objective and one attached layer.
2. A user-triggered agent review finds records that may be relevant to the objective.
3. The agent proposes a Target Assessment Lead in chat.
4. The proposal explains the possible pattern, lists the indications, separates observation from inference, and identifies missing assessment questions.
5. The user may:
   - accept the lead into the workstream;
   - reject it;
   - correct its framing;
   - add or remove an indication;
   - request further collection or analysis.
6. When the lead is sufficiently developed, the user explicitly sends it to assessment.
7. Assessment is performed by an assigned specialist and produces a separate assessment result.
8. Only a qualifying assessment may propose creation or update of a target candidate through the existing target workflow.

## Proposed artifact fields

| Field | Meaning |
|---|---|
| `artifact_id` | Server-owned stable identifier. |
| `artifact_type` | `target_assessment_lead`. |
| `workstream_id` | Owning collaborative workstream. |
| `title` | Concise description of the possible pattern. |
| `lead_statement` | What the indications may collectively suggest, explicitly framed as a hypothesis. |
| `status` | `proposed`, `active`, `ready_for_assessment`, `under_assessment`, `closed`, or `rejected`. |
| `indications` | Attributable references to records or layer items with a short relevance explanation. |
| `supporting_signals` | Observed facts that strengthen the lead. |
| `contradictions` | Observed facts that weaken or conflict with it. |
| `assessment_questions` | Questions that must be answered before target candidacy can be considered. |
| `gaps` | Missing identity, location, time, quantity, independence, or other required context. |
| `assigned_to` | Human or agent responsible for the next assessment action. |
| `created_by` | Human or agent proposing the artifact. |
| `revision` | Monotonic artifact revision. |
| `created_at_utc` | Server-owned creation timestamp. |
| `updated_at_utc` | Server-owned update timestamp. |

Each indication should include:

- stable source reference;
- concise observed claim;
- observation time when available;
- source/provenance summary;
- relevance to the lead;
- role: `supports`, `contradicts`, or `context`;
- contributor identity;
- addition timestamp.

## Artifact invariants

- At least one explicit indication is required.
- A lead statement must use hypothesis language and must not claim target validity.
- Raw source records remain immutable.
- Contradictory indications are preserved, not silently removed.
- Every revision is attributable to a human or agent.
- `ready_for_assessment` means there is enough material to start assessment, not that assessment criteria have passed.
- Only an explicit user action may begin assessment in the MVP.
- Only the separate assessment/target workflow may create or update a target candidate.

## Agent functional advantage

The assigned agent performs work the user should not need to do manually:

- scan the attached layer for potentially related indications;
- group signals by identity, location, time, and source relationship;
- identify possible duplicates or derivative reporting;
- expose contradictions and missing information;
- keep the lead current as the user adds evidence;
- formulate the bounded questions that a specialist must assess.

The agent may propose and revise the lead. It may not promote the lead to assessment or create a target without an explicit authorized user action.

## Chat interaction

The artifact has no formal user-facing name in the MVP. `target_assessment_lead` is an internal type only. The UX talks naturally about the indications, their meaning, and the next action through agent-style chat messages:

- **Proposal:** “I found three indications that may describe the same operational object. Create a lead?”
- **Update:** “One new indication supports the location, but source independence remains unresolved.”
- **Attention request:** “Before assessment, decide whether the two public reports should be treated as one source family.”
- **User action:** `שמור במעקב`, `דחה`, `בקש השלמה`, or `שלח להערכה`.

The minimal workstream indicator remains unchanged. Pressing it returns the current lead summary and available actions to chat.

## MVP boundary

Include:

- one Target Assessment Lead per workstream;
- manual, user-triggered creation and updates;
- indication references from the explicitly attached layer;
- proposal/accept/reject/update actions in chat;
- status and revision history;
- explicit handoff to assessment.
- indications must reference a stable source record or layer item;
- free text may annotate an indication but cannot be an indication by itself;
- only the user may send the indications to assessment.

Defer:

- automatic monitoring or ingestion;
- multiple lead types;
- cross-workstream lead merging;
- automatic promotion thresholds;
- execution of the assessment itself;
- target creation or target-bank mutation;
- Investigation Memory item import;
- scenario playback.

## Accepted Product decisions

- Do not expose a formal artifact name in the UX.
- Allow one active artifact of this type per workstream in the MVP.
- Only the user may select `שלח להערכה`.
- Every indication must reference a stable source record or layer item.
- Free text is annotation, not a standalone indication.
