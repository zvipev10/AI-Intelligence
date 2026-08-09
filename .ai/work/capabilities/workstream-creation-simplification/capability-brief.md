# Capability Brief

## Capability name

Evidence-first workstream creation

## Capability slug

`workstream-creation-simplification`

## Parent issue

Pending remote issue creation; draft body is in `issues/parent-capability.md`.

## Current status

Product definition drafted; human product approval is required before role reviews or implementation.
See `status.md` for the operational owner, blocker, and next action.

## User problem

Moshe currently treats workstream creation like a form. For a concise request such as
`צור מעקב אחר TGT-F2CA47CB9859`, he asks the user to supply a title, objective, and owner
responsibility even though he can resolve the referenced intelligence object and derive those
fields himself.

The user wants Moshe to investigate first and ask only when a consequential ambiguity remains.

## Business goal

Reduce workstream-creation friction so a user can start a useful, fully populated workstream from
one or more target IDs or raw-record IDs in a single request whenever the available evidence is
sufficient.

## Target users

Analysts creating collaborative workstreams through Moshe in chat.

## Proposed behavior

Moshe follows an evidence-first completion policy:

1. Parse every supplied `TGT-*` and `REC-*` identifier.
2. Resolve all supplied identifiers with the available MCP tools before asking for metadata.
3. When one or more targets are supplied:
   - retrieve each target's canonical details and supporting evidence;
   - use that context to derive a concise workstream title and objective;
   - infer Moshe's functional responsibility from the work to be performed;
   - create the workstream in the same turn when the identifiers resolve and the intent is clear.
4. When one or more raw records are supplied:
   - retrieve each record and check whether it already belongs to an existing target;
   - search for related evidence and assess whether the records support one or more target
     candidates;
   - use existing targets and/or eligible derived candidate context to populate the workstream;
   - do not silently persist a new target-bank record as a side effect of workstream creation.
5. Fill title, objective, and responsibility from verified context. Do not ask the user to provide
   those fields merely because they were omitted.
6. Ask one short, focused question only when Moshe cannot safely resolve a supplied identifier,
   multiple materially different workstream intents remain, or a required field cannot be inferred
   without inventing facts.
7. If some supplied identifiers resolve and others do not, state the unresolved identifiers and ask
   whether to proceed with the resolved subset; do not silently drop input.

## MVP scope

- Moshe instruction changes for evidence-first workstream creation.
- Runtime instruction parity with the persistent Moshe profile.
- Target-seeded and raw-record-seeded creation flows.
- Automated prompt/contract tests covering proactive lookup, field inference, and minimal questions.
- Evaluation cases using one target, multiple targets, one raw record, multiple raw records, mixed
  identifiers, unresolved identifiers, and ambiguous intent.

## Non-goals

- Changing the workstream persistence schema.
- Adding a separate creation form.
- Automatically approving or persisting a newly derived target-bank candidate as a hidden side
  effect of creating a workstream.
- Inventing unsupported evidence, locations, entities, source groups, or confidence.
- Removing confirmation requirements from protected artifact or target-bank decisions.

## Acceptance criteria

- Given `צור מעקב אחר TGT-F2CA47CB9859`, Moshe resolves the target, derives title, objective, and
  responsibility, and creates the workstream without asking the user for those three fields when
  the target exists and supplies adequate context.
- Given multiple valid `TGT-*` IDs, Moshe resolves all of them and creates one coherent workstream
  when their relationship supports one clear objective.
- Given a `REC-*` ID, Moshe checks existing target membership and searches for relevant additional
  evidence before deciding what target context belongs in the workstream.
- Given raw records with evidence for a new target candidate, Moshe may prepare and describe the
  candidate context but does not persist a target-bank record without the separately required
  authorization.
- Moshe never asks for title, objective, or responsibility if those values can be derived from
  resolved evidence.
- Moshe asks no more than one focused question per turn, and only for a blocking ambiguity.
- Unresolved and conflicting identifiers are surfaced explicitly.
- The structured `prepare_workstream_creation` handoff remains the only workstream persistence
  path and still requires non-empty title, objective, and responsibility.
- Existing indication-proposal confirmation boundaries and target-bank safety checks remain intact.
- Hebrew and English runtime instructions remain behaviorally aligned where both are supported.

## Edge cases

- Target ID does not exist or is not visible to the current investigation.
- Record ID does not exist, maps to several existing targets, or contains insufficient evidence.
- Several targets imply unrelated objectives.
- Mixed `TGT-*` and `REC-*` input contains duplicates or contradictions.
- Retrieval is truncated, unavailable, or returns low-confidence candidate preparation.
- User explicitly supplies a title, objective, or responsibility that conflicts with resolved data.

## Technical constraints

- The current workstream schema requires title, objective, and responsibility.
- Both `moshe_profile/SOUL.md` and the server-injected Moshe runtime instruction must remain aligned.
- Existing tools must be reviewed to confirm that target IDs can be resolved with enough detail and
  that raw-record expansion can run within the current Moshe allowlist.
- Target persistence must continue to honor `prepare_target_candidate`, duplicate checking, and
  `persistence_eligible=true`.

## UX notes

- Prefer visible progress phrased as investigation, not a metadata questionnaire.
- The creation response should briefly state what Moshe inferred and which IDs grounded it.
- When a question is unavoidable, explain the exact ambiguity rather than listing generic required
  fields.

## QA notes

- Test tool-call ordering, not only final answer text.
- Assert that identifier resolution occurs before any clarification question.
- Assert that the creation handoff contains evidence-grounded non-empty fields.
- Add regression coverage proving that raw-record workstream creation does not bypass target-bank
  persistence protections.

## Risks

- An instruction-only change may be unreliable if the current tool contract does not expose enough
  target context or enforce lookup-before-question behavior.
- Broad retrieval from raw records may increase latency and token/tool usage.
- Inferring responsibility too aggressively may misstate what Moshe will do in the workstream.
- The phrase "create new targets around raw records" can mean either derive candidate context or
  persist targets; this brief assumes derivation/preparation, with persistence remaining protected.

## Open questions

- Should a raw-record-seeded request be allowed to persist an eligible new target candidate in the
  same turn, or should it only prepare the candidate context for later explicit approval?
- When supplied targets are unrelated, should Moshe propose multiple workstreams or ask which scope
  the user intended?
- What retrieval/time budget should bound raw-record expansion during creation?

## Missing inputs

- Human product approval of the proposed behavior and target-persistence boundary.
- Developer confirmation that existing MCP tools provide sufficient target detail and raw-record
  expansion for deterministic field inference.
- UX and QA review of the one-question fallback and mixed/unresolved identifier behavior.

## Required reviewers

- Product
- Development
- UX
- QA/Security

## Required child issues

- [ ] Product review
- [ ] Developer review
- [ ] UX review
- [ ] QA/Security review
- [ ] Execution planning

## Proposed execution checkpoints

1. Approve product semantics and the target-persistence boundary.
2. Review tool coverage and decide whether instruction-only enforcement is sufficient.
3. Approve UX copy and QA matrix.
4. Implement profile/runtime instructions and focused tests.
5. Run offline evaluation, deploy, and validate the example request live.

## Handoff to developer

Questions for developer:

- Which existing tool should resolve full `TGT-*` context during creation?
- Can current raw-record tools discover and prepare new candidate context without expanding Moshe's
  permissions?
- Should lookup-before-question be enforced only in instructions, or with a server-side orchestration
  guard?
- How should latency and partial tool failure be represented?

Expected developer output:

- feasibility notes
- likely affected files/services
- implementation options
- recommended approach
- technical risks
- test strategy
- proposed execution slices
