# Capability Status

## Capability
Hebrew and English runtime localization

## Current phase
Controlled execution — MCP runtime deployed, recovery required

## Overall status
In progress; MCP code deployed but production semantic acceptance blocked

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Blocked on VM recovery | Upload prebuilt semantic cache, deploy final revision, rerun production QA | Checkpoint 008 recovery |
| QA | Complete for target-bank slice | Target isolation, empty initialization, English-write rejection, and rollback verified | Final acceptance |
| Architecture/Product | Approved by execution request | Locale-keyed runtime implemented | Complete for Section 1 design |
| UX | Pending | Review consolidated bilingual UI | Slice 3 acceptance |
| Product | Pending | Review behavior at checkpoints | Final acceptance |

## Latest change since previous review
Checkpoint 008 implements the locale-keyed MCP runtime and deploys its code/assets. The first production English hybrid-index build exhausted VM resources; SSH recovery and final semantic verification remain.

## Current blockers
The VM accepts TCP port 22 but does not complete SSH banners after semantic-index resource exhaustion. Oracle console reboot/process termination is required.

## Current risks
The final production server revision and prebuilt English cache are not uploaded. Workstream localization, legacy v1, and remaining mutable-state isolation remain pending.

## Next expected artifact
VM recovery followed by checkpoint-008 production semantic verification.

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
