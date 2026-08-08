# Capability Status

## Capability
Hebrew and English runtime localization

## Current phase
Controlled execution — staged playback title removed

## Overall status
In progress; MCP locale runtime, target-bank isolation, locale-isolated workstreams, unified staged playback, header locale/status deployment consistency fix, Next button visibility fix, and title removal deployed

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Complete for checkpoint 013 | Hand off deployed title removal | Final acceptance |
| QA | Ready | Review checkpoint 013 production smoke evidence | Final acceptance |
| Architecture/Product | Approved by execution request | Locale-keyed runtime implemented | Complete for Section 1 design |
| UX | Pending | Review consolidated bilingual UI | Slice 3 acceptance |
| Product | Pending | Review behavior at checkpoints | Final acceptance |

## Latest change since previous review
Checkpoint 013 is deployed: the visible `Staged playback` / `ניגון מדורג` title was removed from the header. The timeframe, Moshe playback status, and Next button remain. Production checks verified the title strings and unused `intelligenceModeSelect` element are absent, public `index.html` references `app.js?v=143`, and the UI service is active.

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
- Latest checkpoint: `checkpoint-013.md`
- Handoff: `handoff-summary.md`

## Gate checklist
- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current; remote issues will be created when publishing the first checkpoint.
