# Capability Status

## Capability
Hebrew and English runtime localization

## Current phase
Architecture review — locale-isolated target banks

## Overall status
In progress

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Pending approval | Implement the two-database target-bank split after checkpoint 005 approval | Checkpoint 005 gate |
| QA | Pending | Validate isolation, migration, English-write rejection, and rollback | Implementation checkpoint |
| Architecture/Product | Action required | Approve the physical DB split and migration behavior | Before coding/migration |
| UX | Pending | Review consolidated bilingual UI | Slice 3 acceptance |
| Product | Pending | Review behavior at checkpoints | Final acceptance |

## Latest change since previous review
Checkpoint 005 defines two physical target-bank instances. Existing 21 Hebrew targets move to the Hebrew DB; the English DB starts empty and rejects Hebrew presentation/evidence text.

## Current blockers
None for Slice 1. Production deployment credentials are not required yet.

## Current risks
Active MCP data localization, target-bank presentation, entity metadata defaults, workstream metadata, legacy v1, and mutable-state locale isolation remain pending.

## Next expected artifact
Human approval of `checkpoint-005.md`, followed by controlled implementation and a separately reviewed production migration.

## Artifact links
- Capability brief: `capability-brief.md`
- Developer review: `developer-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-005.md`
- Handoff: `handoff-summary.md`

## Gate checklist
- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current; remote issues will be created when publishing the first checkpoint.
