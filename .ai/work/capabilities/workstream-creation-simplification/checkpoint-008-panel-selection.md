# Checkpoint 008 — Workstream panel selection

## Scope

- Seen/unchanged workstreams use grey rather than green.
- New/updated workstreams use green rather than blue.
- Selecting a presentable workstream appends its summary to chat and automatically loads its map and
  timeline-capable result layers.

## UX behavior

The map becomes the active view after selection. Raw indication layers are also available in the
timeline. A target-only layer remains map/table-only because it has no timestamp capability. The
existing show/hide button remains available in the chat summary.

## Validation status

Implementation complete.

- JavaScript syntax check passed.
- Focused workstream UI suite: 28 passed.
- Full app/backend suite: 129 passed.
- Diff whitespace check passed.

## Publishing status

Branch: `codex/workstream-panel-interaction` at `31fb95c`.

The bilingual production UI was patched semantically rather than overwritten. Live cache versions are
`styles.css?v=133` and `app.js?v=146`; the UI service is active and the Hebrew health check passed.
Rollback backup: `/opt/serbia-poc-ui-backups/workstream-panel-interaction-20260809T163215Z`.

Merge requires product validation.
