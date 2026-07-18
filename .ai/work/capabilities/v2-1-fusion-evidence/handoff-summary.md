# V2.1 Fusion Evidence Handoff

## Outcome

V2.1 is ready as the evaluation corpus for Moshe. It corrects V2's independently sampled public/UAV evidence without modifying V1 or V2.

## Dataset contract

- 14,800 runtime records.
- 3,800 UAV observations and 11,000 public-source records.
- 300 positive shared-object truth chains.
- One UAV anchor plus two distinct public platforms per positive chain.
- 900 positive evidence records and 100 hard negatives.
- Public confirmations vary object terminology and count certainty.
- Runtime records use canonical area locations, not observation coordinates.

## Truth isolation

`fusion_target_truth_v2_1.jsonl` and the additional evaluator-label columns are test-only. Moshe and runtime retrieval must use only the raw/projection, entity, location, and UAV artifacts.

## Runtime selection

Set `INTELLIGENCE_POC_DATASET_VERSION=v2.1` to load V2.1 locally. Production remains on V2.

## Next capability

Implement the global `attack targets` layer and Moshe's command-driven investigation workflow: area/time search, geographic grouping, semantic linkage, source independence, duplicate-target lookup, candidate persistence, and separate human approval.
