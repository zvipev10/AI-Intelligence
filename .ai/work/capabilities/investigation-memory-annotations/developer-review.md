# Developer Review

## Capability

Annotated investigation memory

## Related issue

`issues/parent-capability.md`

## Review status

Approved by product-owner delegation on 2026-09-27.

## Reviewer / input source

AI-prepared draft; the product owner explicitly approved the developer, UX, and QA recommendations and authorized implementation on 2026-09-27.

## Context reviewed

- `app.js`: existing chat/layer memory saves, table, object viewer, view routing, and polygon-control initialization.
- `server.py`: schema-v1 memory persistence, atomic writes, existing two POST endpoints, restoration, and bounded agent context.
- `polygon_draw.js`: completed polygons are currently in-memory map features only.

## Feasibility

Feasible without a new service or dependency. It requires additive persisted state, one new validated endpoint for artifacts, comment fields on existing save payloads, a reusable client modal, and click selection for drawn polygons.

## Recommended approach

1. Preserve `memory.chat_summaries` and `memory.layers`; add `memory.artifacts: []` while accepting missing artifacts from existing saved investigations.
2. Add optional bounded `analyst_comment` to chat/layer items and to every artifact.
3. Add one `POST /api/investigation-memory/artifact` endpoint. The server validates artifact kind, stable object identity/provenance or closed polygon coordinates, bounded labels/comments, and writes atomically through the existing memory writer.
4. Add a shared client-side `openMemoryCommentDialog()` flow. It calls the existing save endpoint for chat/layer or the new artifact endpoint for table rows, viewer objects, and polygons.
5. Make `PolygonDrawControl` assign a stable client polygon ID, expose completed polygon selection, and call back to the app; preserve drawing/marker behavior.
6. Add a workspace-only Memory button and dedicated overlay/screen. It is independent of `activateView()` and does not become a fourth result presentation. Render the current persisted chat/layer/artifact entries read-only.
7. Extend bounded agent normalization so comments/artifact summaries are available, without implying that annotations prove a conclusion.

## Likely affected files/services

- `app.js`, `index.html`, `styles.css`, `polygon_draw.js`
- `server.py`
- memory and UI regression tests
- `docs/product.md` and `docs/architecture.md` after final acceptance

## Technical risks

- Event identity differs by object kind; require a canonical record/entity/evidence/assessment identifier or fail closed.
- Polygons need coordinate/vertex limits and closed-ring validation server-side.
- Agent context needs bounded comments and artifacts to prevent unbounded prompt growth.
- Existing layer restore must ignore artifacts it cannot present rather than failing all memory load.

## Test strategy

- Server unit tests for comment normalization, artifact validation, old schema compatibility, and atomic persistence.
- Client regression tests for all save entry points, Memory button/screen, modal cancellation, and locale labels.
- Polygon-control tests for select-after-complete and no selection during drawing.
- Manual bilingual browser checks and deployed API/source verification.

## Proposed execution slices

1. Memory schema/API and comment dialog for existing chat/layer saves.
2. Object row/viewer saves and read-only Memory screen.
3. Polygon selection/save, full regression, deployment, and handoff.

## Required review gates before coding

- Human developer approval of additive memory contract and endpoint.
- Human UX approval of the screen/dialog/map flow.
- Human QA approval of persistence and map interaction coverage.

