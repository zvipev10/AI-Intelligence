# Capability Status

## Capability
Hebrew and English runtime localization

## Current phase
Controlled execution — collapsed steps and final-result presentation restored

## Overall status
In progress; MCP locale runtime, target-bank isolation, locale-isolated workstreams, unified staged playback, header locale/status deployment consistency fix, Next button visibility fix, title removal, collapsed step details, and automatic final-result presentation deployed

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Complete for checkpoint 014 | Hand off restored collapsed steps and final-result presentation | Final acceptance |
| QA | Ready | Review checkpoint 014 production smoke evidence and run manual browser smoke | Final acceptance |
| Architecture/Product | Approved by execution request | Locale-keyed runtime implemented | Complete for Section 1 design |
| UX | Pending | Review consolidated bilingual UI | Slice 3 acceptance |
| Product | Pending | Review behavior at checkpoints | Final acceptance |

## Latest change since previous review
Checkpoint 014 is deployed: collapsed investigation-step details and automatic final-result map/timeline presentation were restored from the previously implemented feature branches. Production checks verified the deployed assets contain the disclosure UI, final-result presenter, and updated cache keys.

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
- Latest checkpoint: `checkpoint-014.md`
- Handoff: `handoff-summary.md`

## Gate checklist
- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current; remote issues will be created when publishing the first checkpoint.
