# Checkpoint 002 - Runtime and semantic compatibility

## Completed

- Added optional `v2.1`, `v2_1`, and `v21` dataset selection to the MCP and UI servers.
- Kept the default and deployed selection on V2.
- Expanded deterministic semantic aliases to cover every varied public confirmation phrase and bumped the cache version to v11.
- Added a repeatable semantic fusion smoke test.

## Validation

- MCP loaders: V1 10,000 rows; V2 14,800 rows; V2.1 14,800 rows.
- UI loader: V2.1 14,800 rows and build label `serbia-poc-v2.1`.
- V2.1 projection contains no evaluator truth fields.
- All 600 positive public confirmations emit the expected semantic object concept.
- All 300 truth chains: 600/600 public confirmations recovered in the top 20 after canonical location, entity, and truth-window filtering with the UAV record as semantic seed.
- Existing V2 semantic regression runner completed successfully with the v11 vocabulary.
- Python compilation and whitespace checks passed.

## Production status

Not deployed and not selected. Production remains on V2 pending a separate release decision.

## Remaining limitation

V2.1 provides area-level shared-object truth. It does not add observation-level coordinates, so Moshe must retain canonical-location precision and uncertainty in any target artifact.
