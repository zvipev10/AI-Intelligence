# Checkpoint 006 — Target workstream results toggle

## Outcome

Target-only workstreams now expose the same show/hide-results control as raw-record-based
workstreams. The correction is deployed for product validation and remains unmerged.

## Root cause

The presentation API already returned target layers from root-level `target_ids`, but the UI's
`workstreamHasPresentation` predicate only recognized active artifact indications. Therefore, the
shared results button and toggle handler were never rendered for target-only workstreams.

## Correction

- A workstream is presentable when it has at least one non-empty root `target_id` or an active
  target-assessment indication.
- Both cases continue to use the existing presentation endpoint and visibility toggle.
- No target-specific control, state, or presentation path was added.

## Verification

- JavaScript syntax: passed.
- Focused UI/workstream tests: 37 passed.
- Full application/backend suite: 126 passed.
- Hebrew target-only production workstream is eligible and returns one target layer.
- English target-only production workstream is eligible and returns one target layer.
- Both returned layers contain `TGT-F2CA47CB9859`.

Interactive automated browser clicking was blocked by the production server's self-signed
certificate. The deployed asset, workstream payloads, presentation responses, and existing toggle
handler were verified independently.

## Deployment

- Backup: `/opt/serbia-poc-ui-backups/workstream-target-toggle-20260809T142447Z`
- UI service: active.
- v2.1 health: 200, 14,800 rows.

## Merge status

Do not merge until the user validates the deployed control.

