# Checkpoint 004 — Moshe General-Chat Integration

## Scope completed

- Added non-persisting MCP tools for preparing indication proposals and interpreting later proposal decisions.
- Restricted the tools to resolved `REC-...` evidence and an optional read-only `TGT-...` subject.
- Added Moshe instructions for natural-language interpretation, proposal-before-write, ambiguous confirmation, and the assessment-handoff boundary.
- Passed bounded, server-owned active-workstream context into Moshe turns.
- Normalized successful proposal/action audit output into the shared agent result.
- Staged proposals in browser conversation state without artifact mutation.
- Applied confirmed create/revision actions through the Slice 1 artifact service only after a distinct later user turn.
- Kept persistence in the app server and independently revalidated the workstream, actor, layer, references, revision, and action.
- Returned success and conflicts in ordinary chat without adding a proposal panel, buttons, or dedicated artifact surface.
- Removed the mandatory workstream layer attachment; each indication is now resolved and attributed canonically by `REC-...`.
- Extended the existing indicator-to-chat flow to display the active lead statement, indications, gaps, questions, revision, and assessment status.
- Added natural-language evaluation fixtures and focused MCP, pipeline, bridge, profile, UI, and regression tests.

## Validation

- Python compilation passed for the server, result pipeline, artifact service, MCP server, and Moshe profile provisioning.
- Main test discovery: 56 tests passed.
- Focused MCP workstream-tool tests: 3 tests passed.
- `git diff --check` passed.

## Review findings

### Blocking issues

None found by automated implementation review.

### Non-blocking limitations

- The pending proposal remains browser-memory-only and is lost on refresh, as approved for the MVP.
- When more than one active workstream exists, the current chat bridge does not guess which workstream should receive a proposal; the existing chat selection flow remains the disambiguation mechanism.
- Human attribution remains the existing synthetic single-user participant contract, not production authentication.
- Natural-language fixtures define acceptance cases but require deployment-level evaluation against the running Moshe profile in final validation.

## Required checkpoint reviewers

- Product
- Development/Architecture
- UX
- QA/Security

## Recommendation

Approve Slice 2 for merge, then run final validation issue #43 against the deployed demo and stale dataset before closing the parent capability.

## VM deployment

Deployed PR #46 head commit `28b35d4` to the demo VM using a state-preserving, file-scoped deployment.

- UI service: active.
- Moshe gateway service: active.
- `/api/status`: dataset `v2.1`, 14,800 rows.
- Public application: HTTP 200 after the existing HTTPS-to-HTTP redirect.
- Public `app.js`: contains `workstreamArtifactHtml` and no `starting_source`.
- VM UI server: contains the artifact service and confirmed-action bridge.
- VM MCP server and Moshe profile: expose both workstream proposal/decision tools.
- Rollback backup: `/opt/serbia-poc-ui-backups/workstream-slice2-20260726T182421Z`.

Deployment correction:

- The first scoped deployment omitted `index.html`, leaving the VM `+` menu without the already-implemented `מעקב` entry even though the new JavaScript was present.
- The deployment contract now includes `index.html` and verifies both the rendered menu entry and the Slice 2 JavaScript.
- The cache key was advanced to `app.js?v=112`.
- Corrected deployment backup: `/opt/serbia-poc-ui-backups/workstream-slice2-20260726T184041Z`.
