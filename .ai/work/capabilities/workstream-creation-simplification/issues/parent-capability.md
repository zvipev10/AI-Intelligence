# [Capability] Evidence-first workstream creation

## Capability

Simplify Moshe's workstream creation by resolving supplied target and raw-record identifiers,
investigating their context, and inferring required workstream fields before asking the user.

## Current phase

Phase 1 — product definition

## Overall status

Draft — pending human product approval

## Operational status

See `.ai/work/capabilities/workstream-creation-simplification/status.md`.

## User problem

Moshe currently asks users to provide title, objective, and responsibility even when a supplied
target or raw-record ID gives him enough context to derive them.

## MVP scope

- Evidence-first resolution of one or more `TGT-*` and `REC-*` identifiers.
- Automatic inference of title, objective, and Moshe's responsibility.
- One focused question only for blocking ambiguity.
- Raw-record expansion toward existing or eligible candidate target context.
- Preservation of protected target-bank persistence boundaries.
- Focused automated and evaluation coverage.

## Acceptance criteria

- [ ] A valid target-only request creates a fully populated workstream without a metadata questionnaire.
- [ ] Multiple supplied targets are all resolved before creation or clarification.
- [ ] Raw records trigger existing-target lookup and related-evidence discovery.
- [ ] Inferred title, objective, and responsibility are grounded in resolved context.
- [ ] Only one focused blocking question is asked when inference is unsafe.
- [ ] Unresolved or conflicting IDs are disclosed.
- [ ] Raw-record expansion cannot silently bypass protected target-bank writes.
- [ ] Persistent and runtime Moshe instructions remain aligned.
- [ ] Automated tests and evaluation cases cover the accepted flows.

## Child tasks

- [ ] Product review: approve behavior and target-persistence boundary
- [ ] Developer review: validate tools and enforcement approach
- [ ] UX review: approve inferred summary and question fallback
- [ ] QA review: approve test matrix and safety regression coverage
- [ ] Execution plan: define reviewed implementation slices
- [ ] Slice 1 implementation: instructions, guard if required, and tests
- [ ] Slice 1 review: checkpoint approval
- [ ] Final QA: offline and live example validation
- [ ] Final handoff: publish acceptance and remaining risks

## Artifacts

- Capability brief: `.ai/work/capabilities/workstream-creation-simplification/capability-brief.md`
- Status: `.ai/work/capabilities/workstream-creation-simplification/status.md`
- Decisions: pending
- Developer review: pending
- UX review: pending
- QA review: pending
- Execution plan: pending
- Checkpoints: pending
- Handoff: pending

## Closure rule

Keep this parent issue open until all required child tasks are closed, acceptance criteria are
satisfied, final QA is complete, and final handoff is published.
