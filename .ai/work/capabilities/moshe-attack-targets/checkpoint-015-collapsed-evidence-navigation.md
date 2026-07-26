# Checkpoint 015 — Collapsed evidence navigation

## Outcome

- The `מזהי ראיות` section is collapsed by default.
- Every evidence layer inside the section is also collapsed by default.
- Opening an evidence layer:
  - materializes that layer;
  - activates its declared map or timeline view;
  - restores and displays the results table;
  - selects that evidence layer in the results table.
- Closing the evidence layer hides its presented layer.

## Scope

- Frontend interaction and styling only.
- No MCP, shared result contract, agent instruction, target-bank, or SQLite change.
- Requested results remain independent and manual.

## Validation

- JavaScript syntax passes on Node 22.
- 48 shared UI, routing, profile, pipeline, and catalog API tests pass.
- 39 MCP, fusion, target-bank, migration, catalog, and boundary tests pass.
- Total automated regressions: 87.
- Deployed HTML serves `styles.css?v=90` and `app.js?v=111`.
- General gateway, Moshe gateway, and UI services are active; UI restart count is zero.

## Deployment

- VM: `151.145.93.180`
- Rollback backup: `/home/ubuntu/deploy-backups/evidence-collapse-table-20260724T150000Z`
- No database migration or write was performed.

## Review state

Implementation, regression testing, deployment, and served-asset verification are complete. Product visual acceptance is pending.

