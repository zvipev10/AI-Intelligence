# Checkpoint 001 — Annotated Investigation Memory

## Implemented

- Optional, bounded analyst comments for existing chat and layer saves.
- Additive object and polygon artifacts through the investigation-memory API.
- Table-row and object-viewer save controls.
- Click-to-save completed polygons, using the same comment dialog.
- Investigation-only Memory screen with chat, layer, object, area, timestamps, and comments.
- Agent-context inclusion for annotations without making Memory a new presentation.

## Verification

- JavaScript syntax checks for `app.js` and `polygon_draw.js`.
- Python compile check for `server.py`.
- `test_investigation_registry.py`, `test_member_ui_regression.py`, and `test_results_table.py`: 24 passing tests.
- `test_results_table_ui.cjs` and `test_polygon_draw.cjs`: passing.
- `git diff --check`: passing.

## Release scope

Client assets, `server.py`, tests, and durable product/architecture documentation. No migration is required: legacy investigation memory files load with an empty `artifacts` list.
