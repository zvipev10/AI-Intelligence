# Checkpoint 005 — Conversational Workstream UX Corrections

## Scope completed

- Removed duplicate open-summary rendering by replacing an earlier message for the same workstream.
- Limited the `מעקב` plus-menu option and composer entry to the selected Moshe conversation.
- Replaced the local draft/preview/approve flow with a structured Moshe creation handoff.
- Kept the composer active while information is incomplete so Moshe can ask follow-up questions.
- Persisted a complete creation handoff in the same turn through server-owned validation.
- Added a compact upper-bar workstream status and selection menu.
- Kept detailed summaries and archive actions in chat after selection.
- Added public deployment checks for the new menu, creation contract, styles, and Moshe tool.

## Validation

- Main test discovery: 76 tests passed.
- MCP test discovery: 44 tests passed, 1 skipped.
- Python compilation passed.
- `git diff --check` passed.
- Browser validation confirmed:
  - the general chat plus menu does not show `מעקב`;
  - the Moshe chat plus menu does show `מעקב`;
  - tracking mode opens without approval controls.

## Review findings

### Blocking issues

None found in local validation.

### Non-blocking limitations

- Real-agent clarification quality depends on the deployed Moshe profile and requires demo-environment validation.
- Artifact promotion and archiving retain their existing explicit protected-decision behavior; this checkpoint changes initial workstream creation only.

## Recommendation

Deploy to the demo VM and run one incomplete and one complete Moshe creation conversation before product acceptance.

## VM deployment

- Deployed commit `108f7b4` to the demo VM.
- UI service: active.
- Moshe gateway service: active.
- Dataset: `v2.1`, 14,800 rows.
- Public HTML uses `app.js?v=114` and `styles.css?v=114`.
- Public UI contains the upper-bar `workstreamMenu`.
- Public JavaScript contains `workstream_creation_requested` and no local pending-draft or creation-confirmation controls.
- Deployed MCP server and Moshe profile expose `prepare_workstream_creation`.
- Rollback backup: `/opt/serbia-poc-ui-backups/workstream-slice2-20260726T194238Z`.
