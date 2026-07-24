# Execution Plan

## Capability

Collaborative Scenario Playback — Phase 1 persistent workstream foundation

## Related issues

- Parent: #25
- Phase 1 implementation: #30
- Planning PR: #24

## Plan status

Approved for Phase 1 implementation by the human Product owner on 2026-07-24.

## Prerequisite review gate

- Product brief: ready for Phase 1.
- Product scope decision: approved; memory-item selection removed.
- Developer/Architecture review: AI-authored recommendation; unresolved broader decisions do not affect the isolated persistence shell.
- UX review: AI-authored recommendation; Phase 1 uses a minimal shell and must stop for UX review before richer artifact interaction.
- QA review: AI-authored recommendation; Phase 1 includes focused persistence/API tests.
- Blocking questions accepted as Phase 1 assumptions by explicit instruction to start implementation.

## Goal

Persist and reopen a minimal unit of shared human-agent work independently from chat, scenario playback, and Investigation Memory item selection.

## Approved scope

- Create, list, load, update, reopen, and archive workstreams.
- Associate every workstream with one `investigation_id`.
- Store title, objective, status, participants, initial responsibility assignments, and an optional generic starting-source reference.
- Initialize empty `artifacts`, `activity`, and `attention_requests` arrays for later slices.
- Validate identifiers, enums, and bounded text/list inputs.
- Use server-owned IDs, timestamps, and atomic writes.
- Add focused server/API tests.

## Non-goals

- Selecting or importing Investigation Memory items.
- Scenario manifests, stages, visibility, advance, or reset.
- Agent execution or triggers.
- Artifact contribution/revision semantics.
- Human decision requests.
- Production authentication or authorization.
- A full workstream management UI.

## Proposed approach

- Add a separate server-side workstream store rather than extending Investigation Memory documents.
- Store one normalized JSON document per workstream in a dedicated directory.
- Expose constrained collection/item endpoints.
- Add a minimal investigation-scoped browser entry and workstream shell only if it can be reviewed independently.
- Preserve existing Investigation Memory APIs and files unchanged.

## Data/API changes

Proposed document fields:

- `schema_version`
- `workstream_id`
- `investigation_id`
- `title`
- `objective`
- `status`
- `starting_source`
- `participants`
- `assignments`
- `artifacts`
- `activity`
- `attention_requests`
- `created_at_utc`
- `updated_at_utc`
- `archived_at_utc`

Proposed endpoints:

- `GET /api/workstreams?investigation_id=...`
- `POST /api/workstreams`
- `GET /api/workstreams/{workstream_id}`
- `PUT /api/workstreams/{workstream_id}`
- `POST /api/workstreams/{workstream_id}/archive`

Exact route shape may adapt to the existing simple HTTP server.

## Test plan

- Create/load/list/update/archive happy paths.
- Invalid and path-traversal identifiers.
- Missing required fields and invalid state transitions.
- Server-owned ID/timestamp enforcement.
- Atomic-write behavior.
- Investigation-scoped listing.
- Empty future-facing containers remain normalized.
- Existing Investigation Memory tests and relevant UI regressions.

## Execution slices

### Slice 1 — Persistence and API foundation

Goal:
Implement normalized storage and constrained APIs with focused tests.

Risk:
Medium; introduces a new server-side state model and API.

Reviewer:
Development/Architecture and QA.

Stop after slice?
Yes. Publish checkpoint and request review before adding UI behavior.

### Slice 2 — Minimal workstream UI shell

Goal:
Create/reopen/archive an investigation-associated workstream and display objective, participants, responsibilities, and status.

Risk:
Medium; changes product behavior and UX.

Reviewer:
Product, UX, QA.

Stop after slice?
Yes.

## Stop conditions

- Any need to alter Investigation Memory schema or behavior.
- Any need to define scenario-stage or artifact-revision semantics.
- Any authorization decision beyond the current demo boundary.
- Existing investigation or memory regressions.

## Rollback/fallback

The store and endpoints are additive. UI exposure can remain disabled while persistence is reviewed. Removing the dedicated workstream directory configuration and routes restores prior behavior without migrating Investigation Memory.

## Required approval before implementation

The human Product owner explicitly approved the revised Phase 1 boundary and instructed implementation to begin on 2026-07-24.
