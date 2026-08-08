# Capability Status

## Capability
Hebrew and English runtime localization

## Current phase
Planning review — complete English MCP runtime and workstreams

## Overall status
In progress; locale-isolated target-bank slice deployed

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Pending approval | Implement Section 1 MCP runtime, then Section 4 workstream isolation | Checkpoint 007 gate |
| QA | Complete for target-bank slice | Target isolation, empty initialization, English-write rejection, and rollback verified | Final acceptance |
| Architecture/Product | Action required | Approve checkpoint 007 runtime and workstream architecture | Before coding |
| UX | Pending | Review consolidated bilingual UI | Slice 3 acceptance |
| Product | Pending | Review behavior at checkpoints | Final acceptance |

## Latest change since previous review
Checkpoint 007 plans a complete locale-keyed MCP runtime and physically isolated workstream stores. English workstreams start empty; legacy untagged workstreams remain Hebrew-owned.

## Current blockers
None for the target-bank slice.

## Current risks
Active MCP data localization, target-bank presentation, entity metadata defaults, workstream metadata, legacy v1, and mutable-state locale isolation remain pending.

## Next expected artifact
Human approval of `checkpoint-007.md`, followed by Section 1 implementation.

## Artifact links
- Capability brief: `capability-brief.md`
- Developer review: `developer-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-007.md`
- Handoff: `handoff-summary.md`

## Gate checklist
- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current; remote issues will be created when publishing the first checkpoint.
