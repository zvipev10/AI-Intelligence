# Capability Status

## Capability
Hebrew and English runtime localization

## Current phase
Controlled execution — unified staged playback ready for deployment

## Overall status
In progress; MCP locale runtime, target-bank isolation, locale-isolated workstreams, and unified staged playback implemented locally

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Active | Deploy checkpoint 010 and run production smoke | Final acceptance |
| QA | Ready after deployment | Review checkpoint 010 local and production smoke evidence | Final acceptance |
| Architecture/Product | Approved by execution request | Locale-keyed runtime implemented | Complete for Section 1 design |
| UX | Pending | Review consolidated bilingual UI | Slice 3 acceptance |
| Product | Pending | Review behavior at checkpoints | Final acceptance |

## Latest change since previous review
Checkpoint 010 is implemented locally: playback now uses one staged flow, baseline visibility starts at dataset beginning through the first slice boundary, Moshe reevaluation is skipped on baseline creation, UI/data layer rows are filtered by active `visible_timeframe`, and the historical/real-time selector distinction was removed from the UI.

## Current blockers
None for deployment.

## Current risks
The active playback visibility policy is process/global, so production smoke must restore the previous `active_visibility.json` after test calls. Explicit scenario-run IDs remain directly addressable by ID, although investigation-level playback lookup is locale-filtered. Semantic caches should continue to be built off-host for this low-memory VM.

## Next expected artifact
Checkpoint 010 production smoke evidence / final bilingual acceptance review.

## Artifact links
- Capability brief: `capability-brief.md`
- Developer review: `developer-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-010.md`
- Handoff: `handoff-summary.md`

## Gate checklist
- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current; remote issues will be created when publishing the first checkpoint.
