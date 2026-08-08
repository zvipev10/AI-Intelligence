# Capability Status

## Capability
Hebrew and English runtime localization

## Current phase
Controlled execution — workstream localization next

## Overall status
In progress; MCP locale runtime and target-bank isolation deployed

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Ready | Implement Section 4 locale-isolated workstreams | Next execution checkpoint |
| QA | Complete for target-bank slice | Target isolation, empty initialization, English-write rejection, and rollback verified | Final acceptance |
| Architecture/Product | Approved by execution request | Locale-keyed runtime implemented | Complete for Section 1 design |
| UX | Pending | Review consolidated bilingual UI | Slice 3 acceptance |
| Product | Pending | Review behavior at checkpoints | Final acceptance |

## Latest change since previous review
Checkpoint 008 is complete: the final server and prebuilt English semantic cache are deployed, English payload scans pass, and semantic locale isolation is verified in production.

## Current blockers
None for Section 1.

## Current risks
Workstream localization, legacy v1, and remaining mutable-state isolation remain pending. Semantic caches should continue to be built off-host for this low-memory VM.

## Next expected artifact
Section 4 workstream-isolation implementation checkpoint.

## Artifact links
- Capability brief: `capability-brief.md`
- Developer review: `developer-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-008.md`
- Handoff: `handoff-summary.md`

## Gate checklist
- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current; remote issues will be created when publishing the first checkpoint.
