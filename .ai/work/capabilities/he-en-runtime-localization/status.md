# Capability Status

## Capability
Hebrew and English runtime localization

## Current phase
Controlled execution — Next button visibility fix deployed

## Overall status
In progress; MCP locale runtime, target-bank isolation, locale-isolated workstreams, unified staged playback, header locale/status deployment consistency fix, and Next button visibility fix deployed

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Complete for checkpoint 012 | Hand off deployed Next button fix | Final acceptance |
| QA | Ready | Review checkpoint 012 production smoke evidence | Final acceptance |
| Architecture/Product | Approved by execution request | Locale-keyed runtime implemented | Complete for Section 1 design |
| UX | Pending | Review consolidated bilingual UI | Slice 3 acceptance |
| Product | Pending | Review behavior at checkpoints | Final acceptance |

## Latest change since previous review
Checkpoint 012 is deployed: the frontend no longer tries to auto-create the staged baseline during page-load playback fetch. It stores the API payload and renders Next from top-level `next_stage` when no run exists. Production checks verified both Hebrew and English `/api/playback` responses expose the first staged timeframe and deployed `index.html` references `app.js?v=142`.

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
- Latest checkpoint: `checkpoint-012.md`
- Handoff: `handoff-summary.md`

## Gate checklist
- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current; remote issues will be created when publishing the first checkpoint.
