# Execution Plan — Annotated Investigation Memory

## Approval gate

Product scope and developer, UX, and QA recommendations were approved by explicit product-owner delegation on 2026-09-27.

## Implementation approach

Use the existing investigation-memory file/API contract and add an optional `analyst_comment` field to chat/layer entries plus an additive `artifacts` list. Artifacts represent one captured object or one closed polygon. The browser uses one reusable comment dialog for every save entry point. Memory is a workspace-only overlay/screen, separate from Map, Timeline, and Table.

## API/data contract

- Existing `POST /api/investigation-memory/chat-summary` and `/layer` accept optional `comment`.
- New `POST /api/investigation-memory/artifact` accepts a validated `object` or `polygon` artifact plus optional `comment`.
- Comments are normalized and limited to 1200 characters.
- Polygon rings are closed and limited to 200 positions; coordinates must be finite longitude/latitude values.
- Existing memory files without `artifacts` load as an empty artifact list.

## Execution slices

### Slice 1 — Persistence contract and shared comment dialog

Add comment normalization/persistence for chat/layer saves, artifact validation/persistence, and the reusable client modal. Add server and client regression coverage.

### Slice 2 — Object capture and Memory screen

Add table-row/viewer object save actions and a workspace-only Memory button/overlay that renders existing chat, layer, object, and polygon items read-only.

### Slice 3 — Polygon capture, QA, and release

Extend the polygon control with completed-polygon selection and app callback, connect it to the shared save flow, run bilingual/regression checks, deploy, and publish handoff.

## Risks and mitigations

- Old memory files: default `artifacts` to an empty list.
- Overlarge/unsafe payloads: validate and bound all fields server-side.
- Map conflict: ignore polygon selection while drawing and stop the click event when selecting a completed polygon.
- Agent context growth: include bounded artifact/comment summaries only.

## Rollback

The release is limited to client UI assets plus `server.py`. Retain the pre-release static asset backup and service health checks; old persisted memory files remain valid.
