# QA Review

## Status

Test plan accepted for this execution by explicit user request.

## Required checks

- Generator deterministic regeneration and V1 immutability checks.
- Projection schema and 14,800 unique rows.
- Exactly 3,800 populated UAV structured records.
- Object/count values match the dedicated UAV observation JSONL by record id.
- Public-event serialization preserves structured values.
- Concept-feature unit probes for every requested family.
- Semantic synonym retrieval and exact-count retrieval against V2.
- V1 loader regression.
- Index manifest/cache invalidation and measured build/search time.

## Review recommendation

Proceed in two checkpoints: data contract, then semantic implementation/validation.
