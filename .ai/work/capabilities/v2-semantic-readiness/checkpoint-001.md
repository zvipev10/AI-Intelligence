# Checkpoint 001 — Structured V2 Semantic Fields

## Completed

- Extended the V2 runtime projection with collection family, UAV observation/mission ids, normalized object class, estimated count, movement, direction, and geolocation/identification confidence.
- Regenerated only V2 artifacts.
- Preserved a stable schema: non-UAV rows have empty structured observation fields.

## Validation

- 14,800 unique projection records.
- 3,800 UAV rows with populated object/count/movement fields.
- Every UAV projection object/count/movement value matches the dedicated UAV JSONL by record id.
- All non-UAV rows have empty object/count fields.
- Generator checks passed, including V1 input hashes unchanged.
- Projection contains 18 runtime columns and passes exact-schema validation.

## Review

Slice 1 complete. Continue to semantic indexing and concept features.
