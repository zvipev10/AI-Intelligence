# Checkpoint 001 - V2.1 evidence generation

## Completed

- Added a deterministic V2.1 generator that treats V2 artifacts as immutable input.
- Generated 14,800 V2.1 records, including the unchanged 3,800 UAV observations and 11,000 public-source records.
- Created 300 evaluator-known target objects with 900 positive evidence records.
- Every positive chain contains one UAV anchor and two public confirmations from distinct public platforms.
- Added approximate, range, and explicitly uncertain public count language.
- Added 100 hard-negative records sharing the canonical area and target-like terminology while differing in affiliation.
- Added evaluator-only fusion labels and a target-truth JSONL; truth identifiers do not appear in raw or runtime projection data.

## Validation

- Deterministic double regeneration passed.
- V2 byte hashes remained unchanged.
- Row IDs are unique and entity/location references resolve.
- Truth-leakage scan passed.
- Object distribution spans convoys, armored vehicles, roadblocks, observation posts, helicopters, logistics trucks, and engineering activity.

## Review findings

- Initial count-language generation did not reach the uncertain-count variant. The generator now varies language across the full chain set; validation reports 200 approximate, 229 range, and 171 uncertain public confirmations.
- Canonical location remains area-level. Evaluator truth asserts a shared synthetic object inside the area but does not imply an observation-level coordinate.

## Next slice

Add optional V2.1 runtime dataset selection and smoke-test the current MCP semantic loader without switching production.
