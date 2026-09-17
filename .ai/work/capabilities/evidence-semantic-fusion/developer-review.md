# Developer review

Status: Ready for implementation; user explicitly approved execution.

## Approach

- Add a reusable semantic object-class resolver backed by `semantic_index.CONCEPT_FEATURES` / `concept_weights`.
- Use it from `project_event`, live fusion preparation, and catalog generation.
- Change batch correlation to rolling, connected temporal components within an entity/location/object-class group.
- Add catalog-backed reads to `EvidenceStore` so SQLite remains the writable overlay while the deployment seed remains readable.

## Risks

- Over-classification: only mapped object concepts may resolve a class; structured classes remain authoritative.
- Duplicate reads: repository results must deduplicate deterministic evidence IDs.
- Locale: IDs and canonical Hebrew class values remain stable; only summaries are localized.
- Performance: catalog loading must be lazy and cached.

## Test strategy

- Unit tests for semantic class resolution.
- Catalog regression for rolling-window fusion and Ibar Bridge chains.
- Repository tests for catalog fallback plus SQLite override.
- Existing evidence, assessment, catalog, and profile tests.
