# Checkpoint 001 — Table presentation implemented

User-authorized implementation complete; deployment and live qualification next. Parent #67, implementation #75.

The same raw-records table becomes full-height in the Table tab, preserving filters, record links, selected layer and Map/Timeline overlay minimization. Geometry-free raw layers default to Table; explicit chronology remains Timeline. Legacy evidence view aliases to Table. Agent instructions (English/Hebrew), MCP presentation/catalog schemas, audit parsing, saved-memory reconstruction and frontend recommendations support Table.

Validation: focused Python pipeline/scenario/media tests pass (37); new Syria catalog/presentation test passes; MCP 74 tests, 72 pass and 2 skipped. Node table mode, geometry-free record links, empty state, legacy restoration, catalog recovery, and media tests pass. Full UI suite baseline has eight previously recorded failures; final regression rerun pending after updating asset version assertion. A mistaken test module invocation was corrected to discovery; no implementation test error is hidden.

Review: no blocking implementation findings. No dataset/schema/dependency changes. Browser interaction was not manually verified. Release uses existing drain/stop/restart and rollback controls, Syria network-v1 unchanged.
