# Capability Status

## Capability
Record and knowledge entity viewers

## Current phase and overall status
Phase 6 — side-viewer refinement merged, deployed, and smoke-validated.

## Who needs to act now
No role action is required. Hands-on product/UX acceptance is an optional follow-up.

## Latest change
The centered modal is now a Hebrew-left/English-right edge drawer. UAV records include a source-level raw-video section that can be shared across records from the same mission.

## Current blockers
None. No playable UAV asset exists in the repository, so the designed disconnected state is expected.

## Current risks
Hands-on browser acceptance was not requested. Current media references without URLs render as unavailable.

## Next expected artifact
None required. See the completed deployment record in `checkpoint-002.md`.

## Parent issue
https://github.com/zvipev10/AI-Intelligence/issues/48 — open through final acceptance.

## Child issues
| Issue | Roles | Purpose | Status | Blocking |
|---|---|---|---|---|
| [49](https://github.com/zvipev10/AI-Intelligence/issues/49) | Product, Development, UX, QA | Review capability and establish planning readiness | Open | Yes |

## Artifact links
- [Capability brief](capability-brief.md)
- [Handoff](handoff-summary.md)
- [Checkpoint 001](checkpoint-001.md)

## Publishing
Viewer refinement is on remote `main` at `4688544`. Production serves `app.js?v=179` and `styles.css?v=148`; rollback is `/home/ubuntu/deploy-backups/viewer-side-drawer-4688544`. Parent and review issues remain open pending repository administration.
