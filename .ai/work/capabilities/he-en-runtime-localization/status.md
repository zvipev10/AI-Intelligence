# Capability Status

## Capability
Hebrew and English runtime localization

## Current phase
Checkpoint review — Slice 1 data remediation complete

## Overall status
In progress

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Paused at gate | Await review, then implement the MCP locale boundary | Checkpoint 002 acceptance |
| QA | Active | Review clean-English projections and runtime smoke evidence | Checkpoint 002 acceptance |
| UX | Pending | Review consolidated bilingual UI | Slice 3 acceptance |
| Product | Pending | Review behavior at checkpoints | Final acceptance |

## Latest change since previous review
Checkpoint 002 regenerated the v2/v2.1 English projections and verified zero Hebrew matches in all six runtime assets and 14,800 runtime-loaded rows.

## Current blockers
None for Slice 1. Production deployment credentials are not required yet.

## Current risks
Legacy v1/recorded-run localization, module-global MCP state, semantic cache isolation, and production deployment remain pending.

## Next expected artifact
QA/product acceptance of `checkpoint-002.md`, followed by the MCP locale-boundary slice.

## Artifact links
- Capability brief: `capability-brief.md`
- Developer review: `developer-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-002.md`
- Handoff: `handoff-summary.md`

## Gate checklist
- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current; remote issues will be created when publishing the first checkpoint.
