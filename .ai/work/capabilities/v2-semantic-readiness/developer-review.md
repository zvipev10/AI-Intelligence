# Developer Review

## Status

Ready for execution under explicit user direction.

## Approach

1. Extend the V2 projection contract rather than joining the separate UAV JSONL at runtime.
2. Keep empty structured fields on non-UAV rows for one stable CSV schema.
3. Include structured field labels/values in `SemanticEventIndex.event_text`.
4. Expand deterministic multilingual concept features; do not depend on an external model.
5. Validate with focused synonym/count probes plus existing loader/search regression checks.

## Risks

- Larger projection and index-build cost.
- Concept overmatching across generic military terms.
- Exact count matching may be mistaken for identity evidence; counts remain supporting signals only.
- Existing public rows lack structured object annotations.

## Rollback

Revert the V2 projection fields, semantic concept version, and generated V2 artifacts. V1 remains untouched.
