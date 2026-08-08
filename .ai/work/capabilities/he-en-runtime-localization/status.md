# Capability Status

## Capability
Hebrew and English runtime localization

## Current phase
Controlled execution — Slice 1

## Overall status
In progress

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Active | Implement and verify localized data/MCP boundary | Checkpoint 001 |
| QA | Active | Review locale isolation and fallback tests | Checkpoint 001 acceptance |
| UX | Pending | Review consolidated bilingual UI | Slice 3 acceptance |
| Product | Pending | Review behavior at checkpoints | Final acceptance |

## Latest change since previous review
Initialized capability artifacts from the supplied implementation plan and audited latest `main` plus the English WIP.

## Current blockers
None for Slice 1. Production deployment credentials are not required yet.

## Current risks
English WIP divergence, module-global MCP state, semantic cache isolation, and untranslated generated content.

## Next expected artifact
`checkpoint-001.md`

## Artifact links
- Capability brief: `capability-brief.md`
- Developer review: `developer-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: pending
- Handoff: pending

## Gate checklist
- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current; remote issues will be created when publishing the first checkpoint.

