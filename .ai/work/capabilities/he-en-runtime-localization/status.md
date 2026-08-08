# Capability Status

## Capability
Hebrew and English runtime localization

## Current phase
Controlled execution — deployment consistency fix deployed

## Overall status
In progress; MCP locale runtime, target-bank isolation, locale-isolated workstreams, unified staged playback, and header locale/status deployment consistency fix deployed

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | Complete for checkpoint 011 | Hand off deployed locale/status fix | Final acceptance |
| QA | Ready | Review checkpoint 011 production smoke evidence | Final acceptance |
| Architecture/Product | Approved by execution request | Locale-keyed runtime implemented | Complete for Section 1 design |
| UX | Pending | Review consolidated bilingual UI | Slice 3 acceptance |
| Product | Pending | Review behavior at checkpoints | Final acceptance |

## Latest change since previous review
Checkpoint 011 is deployed: the VM now has matching merged `main` frontend assets for the header language toggle and system status indicators. The regression was deployment drift: newer indicator markup was deployed without the matching status-rendering JS/styles. Production checks verified `renderSystemStatuses`, `datasetStatusIndicator`, `status-indicator` styles, compact `E`/`ע` language slider markup, and active UI service.

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
- Latest checkpoint: `checkpoint-011.md`
- Handoff: `handoff-summary.md`

## Gate checklist
- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current; remote issues will be created when publishing the first checkpoint.
