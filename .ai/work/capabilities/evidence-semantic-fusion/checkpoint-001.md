# Checkpoint 001 — semantic evidence fusion

## Status

Implementation is complete locally and committed on `codex/evidence-semantic-fusion`. It has not been pushed, merged, or deployed because publishing to the external remote requires explicit user authorization.

## Implemented

- Added shared semantic object-class normalization backed by the existing semantic index concept vocabulary.
- Applied normalization to `prepare_evidence`, live fused-evidence preparation, and catalog generation.
- Removed the additional ambiguity persistence block from live evidence preparation as requested.
- Replaced fixed six-hour catalog buckets with bounded eight-hour rolling groups.
- Added the deployment catalog as a read seed beneath the SQLite writable overlay used by Talia.
- Updated Talia to search fused evidence first, create missing evidence through existing tools, and keep one phenomenon per evidence object.
- Updated deployment configuration to align agent profiles with dataset v2.1 and the shared evidence catalog.

## Validation

- Evidence catalog tests: passed.
- MCP evidence/fusion/target/semantic tests: 36 passed.
- Assessment tests: 5 passed.
- Full v2.1 catalog build: 5,283 rows, including 783 fused objects.
- Ibar Bridge validation produced separate fused objects:
  - armored vehicle: `EVD-FUSED-CE661784179B3B88BCB9`
  - helicopter: `EVD-FUSED-FDF2C6DAD2CC106E7BD2`
  - engineering activity: `EVD-FUSED-C1E6F848E654359BD98C`
- One broader UI evidence test batch has one pre-existing asset-version mismatch: the test expects `app.js?v=187`, while current `index.html` uses `v=190`. This task does not modify either file.
- Profile unit tests could not run in the bundled Python runtime because PyYAML is unavailable; the modified files compile successfully.

## Review findings

### Blocking issues

None found in the scoped evidence behavior.

### Non-blocking comments

- The helicopter group also contains `REC-V2-007693`, a second compatible UAV observation inside the rolling window. This is visible in provenance and increases the group from three to four records.
- Catalog JSON remains the deployment seed artifact, but it is no longer invisible to Talia; SQLite remains the writable overlay.

### Recommendation

Continue to commit/push and then deploy both the UI catalog rebuild and MCP/profile changes together.
