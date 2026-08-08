# Capability Status

## Capability
Hebrew and English runtime localization

## Current phase
Controlled execution — unified staged playback deployed

## Overall status
In progress; MCP locale runtime, target-bank isolation, locale-isolated workstreams, and unified staged playback deployed

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Complete for checkpoint 010 | Hand off deployed staged playback | Final acceptance |
| QA | Ready | Review checkpoint 010 local and production smoke evidence | Final acceptance |
| Architecture/Product | Approved by execution request | Locale-keyed runtime implemented | Complete for Section 1 design |
| UX | Pending | Review consolidated bilingual UI | Slice 3 acceptance |
| Product | Pending | Review behavior at checkpoints | Final acceptance |

## Latest change since previous review
Checkpoint 010 is deployed: playback now uses one staged flow, baseline visibility starts at dataset beginning through the first slice boundary, Moshe reevaluation is skipped on baseline creation, UI/data layer rows are filtered by active `visible_timeframe`, and the historical/real-time selector distinction was removed from the UI. Production smoke verified English TikTok rows respect the baseline timeframe and restored the previous inactive global visibility policy.

## Current blockers
None for checkpoint 010.

## Current risks
The active playback visibility policy is process/global. Explicit scenario-run IDs remain directly addressable by ID, although investigation-level playback lookup is locale-filtered. Semantic caches should continue to be built off-host for this low-memory VM.

## Next expected artifact
Final bilingual acceptance review / next localization slice.

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
