# Checkpoint 012 — Requested-result layers

## Approved product behavior

`הצג תוצאות` presents only data that directly answers the user's request. Supporting evidence and intermediate tool output remain outside the final requested-result layers. The final answer text is unchanged. Evidence-layer links are deferred to a later slice.

## Implementation

- Added the shared read-only `present_requested_results` tool to both agent allowlists.
- The agent selects canonical event, location, entity, target, or prior aggregate-result IDs.
- The MCP backend validates identifiers and materializes canonical rows.
- Aggregate rows must have been returned by an earlier `aggregate_events` call in the same run.
- The final backend response exposes a separate `requested_result_layers` collection.
- Only the last successful explicit selection is authoritative.
- `הצג תוצאות` reads only `requested_result_layers`; legacy layers and investigation-step results cannot populate it.
- The button is absent when no requested result was selected.
- One layer is the instructed default; multiple layers are allowed only when the user explicitly requested multiple result types.

## Non-goals

- No change to final answer wording.
- No change to investigation-step presentation.
- No implementation of the proposed linked evidence-layer list under `מזהי ראיות`.

## Validation

- 33 shared backend, profile, result-pipeline, and UI tests pass on Linux.
- 33 MCP, target-bank, fusion, schema, and boundary tests pass on Linux.
- JavaScript syntax and Python compilation pass.
- A live General Agent request for only `REC-V2-004481` returned one `events` layer containing only that record.
- A live Moshe request for targets containing `REC-V2-009058` returned one `attack_targets` layer containing only `TGT-70C964B0ECC0` and `TGT-5D4598097339`.
- Both live responses returned zero legacy layers.
- Both agent gateways and the UI service are active.
- SQLite remained unchanged at 12 targets and 43 evidence links; integrity is `ok`.

## Deployment

- VM: `151.145.93.180`
- Code/config rollback backup: `/home/ubuntu/deploy-backups/requested-result-layers-20260724T090000Z`
- Database backup: `/opt/serbia-poc/backups/attack_targets/attack_targets-pre-requested-results-20260724T090000Z.db`

## Review state

Implementation and production verification complete; user acceptance pending.
