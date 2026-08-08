# Capability Status

## Capability
Hebrew and English runtime localization

## Current phase
Controlled execution — remaining bilingual runtime paths

## Overall status
In progress; locale-isolated target-bank slice deployed

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Active | Continue remaining localized MCP/entity/workstream paths | Next execution slice |
| QA | Complete for target-bank slice | Target isolation, empty initialization, English-write rejection, and rollback verified | Final acceptance |
| Architecture/Product | Approved | Two physical empty databases; no migration | Complete |
| UX | Pending | Review consolidated bilingual UI | Slice 3 acceptance |
| Product | Pending | Review behavior at checkpoints | Final acceptance |

## Latest change since previous review
Checkpoint 006 deploys two physical target-bank instances. Both active databases are empty, future writes are locale-routed, and English writes containing Hebrew are rejected.

## Current blockers
None for the target-bank slice.

## Current risks
Active MCP data localization, target-bank presentation, entity metadata defaults, workstream metadata, legacy v1, and mutable-state locale isolation remain pending.

## Next expected artifact
Implementation of the remaining English MCP/entity/workstream data paths identified in checkpoint 004.

## Artifact links
- Capability brief: `capability-brief.md`
- Developer review: `developer-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-006.md`
- Handoff: `handoff-summary.md`

## Gate checklist
- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current; remote issues will be created when publishing the first checkpoint.
