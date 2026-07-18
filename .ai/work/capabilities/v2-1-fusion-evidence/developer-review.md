# Developer Review

## Status

Approved for execution by explicit user direction on 2026-07-18.

## Recommended approach

Build V2.1 deterministically from immutable V2 artifacts. Select high-value opposition UAV observations as truth anchors, bind unused public records with compatible event/location/entity/time to each anchor, and rewrite only their public narrative and evaluator labels. Preserve all runtime field names and record counts.

Add a separate evaluator-only truth JSONL and additional evaluator CSV columns. Runtime consumers must not load either truth field set.

## Risks

- Truth leakage into raw or projection files.
- Public confirmations that repeat exact UAV wording and make fusion trivial.
- Reusing one public record in multiple chains.
- Dense synthetic records producing unlabelled accidental matches.
- Encoding regressions in Hebrew text.

## Test strategy

- Deterministic regeneration and hash comparison.
- V1/V2 immutability hashes.
- Exact row, source-family, and UAV counts.
- Chain cardinality, source-platform independence, event/location/entity/time agreement.
- Truth-leakage scan of raw and runtime projection files.
- Hard-negative cardinality and non-overlap.
- UTF-8 round-trip and loader smoke tests.

## Execution slices

1. V2.1 generator and evaluator truth model.
2. Generated artifacts and automated validation.
3. Runtime compatibility review and handoff to Moshe implementation.
