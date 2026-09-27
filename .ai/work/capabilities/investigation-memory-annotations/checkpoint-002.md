# Checkpoint 002 — Memory entry navigation and deletion

## Implemented

- Saved-layer entries reopen their saved filters in their captured Map, Timeline, or Table presentation; legacy entries use the source default.
- Saved objects reopen in their existing object viewer, including records outside currently opened result layers.
- Saved polygons reopen on Map as a focused, transient geometry overlay.
- Every Memory entry includes a delete icon; deletion removes exactly the selected item from its own memory group.
- The server validates deletion requests and preserves every non-target memory group atomically.

## Verification

- Client/server syntax checks.
- Investigation-memory persistence tests cover object, polygon, chat and layer deletion behavior.
- Existing table and polygon UI regression checks remain green.

## Compatibility

Older saved layers have no captured presentation value and fall back to their existing source default. No data migration is needed.

## Deployment verification

Deployed to the active Syria server on 2026-09-27. `serbia-poc-ui.service` is active; `/api/status` reports `scenario_id: syria` and `dataset_version: call-media-v6`. The served assets reference `styles.css?v=160`, `demo_bootstrap.js?v=227`, and `app.js?v=227`. The scoped pre-deployment asset backup remains on the VM.
