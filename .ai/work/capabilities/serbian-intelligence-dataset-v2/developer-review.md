# Developer Review

## Status

AI-authored implementation review; Product authorized generation. Human review required before application activation.

## Recommended approach

- Add one deterministic generator under `data/`.
- Read v1 as immutable input and write only `_v2` outputs.
- Preserve canonical runtime projection schema.
- Store richer UAV observations in a separate JSONL linked by record/event/location/entity identifiers.
- Validate distributions and referential integrity in the generator.

## Technical risks

- Large checked-in generated files.
- Encoding consistency for Hebrew CSV/JSONL.
- Accidental v1 overwrite.
- Runtime semantics where `event_id` currently represents record identity in the projection.

## Test strategy

- Hash v1 files before and after generation.
- Run generator twice and compare v2 hashes.
- Validate counts, unique IDs, field sets, event ranges, source perspective, and references.
- Sample chronology and UAV observation linkage.

## Execution slices

1. Generator and schemas.
2. Generation and automated validation.
3. Human scenario/quality review before activation.
