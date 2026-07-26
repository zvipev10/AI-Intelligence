# Developer / Architecture Review — Indication Artifact

## Status

AI-authored recommendation — pending human Development/Architecture approval.

## Scope reviewed

The artifact foundation and manual chat flow only. Agent execution, assessment execution, and target-bank mutation are excluded.

## Feasibility

Feasible by extending the existing workstream component. Workstream documents already contain empty `artifacts`, `activity`, and `attention_requests` arrays, are written atomically, and are investigation-scoped. Investigation Memory and the SQLite target bank do not need to change.

## Recommended state model

Keep a generic artifact envelope in `workstream.artifacts`:

```json
{
  "artifact_id": "artifact_...",
  "artifact_type": "target_assessment_lead",
  "status": "proposed",
  "revision": 1,
  "content": {},
  "created_by": {"participant_id": "analyst-1", "kind": "human"},
  "created_at_utc": "ISO-8601",
  "updated_at_utc": "ISO-8601",
  "revisions": []
}
```

`content` is validated by an artifact-type registry. The first registered type is `target_assessment_lead`; reusable workstream persistence and routing must not encode Hebrew UX copy or target-bank operations.

The first artifact content contains:

- `lead_statement`;
- `indications`;
- `supporting_signals`;
- `contradictions`;
- `assessment_questions`;
- `gaps`;
- `assigned_to`;
- optional annotation.

Each indication uses a stable reference:

```json
{
  "indication_id": "indication_...",
  "source_reference": {
    "kind": "layer_record",
    "layer_id": "catalog-layer-id",
    "record_id": "stable-record-id"
  },
  "observed_claim": "bounded source-derived text",
  "relevance": "why it matters to the lead",
  "role": "supports",
  "annotation": "",
  "added_by": {"participant_id": "analyst-1", "kind": "human"},
  "added_at_utc": "ISO-8601",
  "state": "active"
}
```

## Revision and concurrency contract

- Every mutation supplies `expected_revision`.
- The server rejects stale writes with `409 Conflict` and returns the current revision.
- Accepted mutations append an immutable revision entry containing actor, action, timestamp, previous revision, and a bounded change summary.
- Removing an indication marks it `removed`; it does not erase history.
- Server owns artifact, indication, revision IDs and timestamps.
- Archived workstreams reject artifact mutations.

## Proposed API

- `GET /api/workstreams/{workstream_id}/artifacts`
- `POST /api/workstreams/{workstream_id}/artifacts`
- `GET /api/workstreams/{workstream_id}/artifacts/{artifact_id}`
- `POST /api/workstreams/{workstream_id}/artifacts/{artifact_id}/revisions`

The create request supplies `artifact_type`, initial content, and actor. Revision requests supply `expected_revision`, actor, action, and action-specific payload.

Supported MVP actions:

- `accept_proposal`
- `reject_proposal`
- `add_indication`
- `remove_indication`
- `update_annotation`
- `request_completion`
- `send_to_assessment`

`send_to_assessment` changes status to `ready_for_assessment`; it does not call an agent or target API in this slice.

## Validation rules

- One non-closed `target_assessment_lead` per workstream.
- At least one active indication for an accepted artifact.
- Every indication references a stable record/item in the workstream's explicitly attached layer.
- Reference existence and layer membership are checked through the existing layer/catalog resolver.
- Bounded strings, arrays, and payload sizes.
- Valid participant attribution.
- Only a human participant may perform `send_to_assessment`.
- Status transitions are allow-listed.
- Target-bank APIs are never called from artifact routes.

## Likely affected code

- `llm_investigation_orchestrator_serbia_poc/server.py`
- new focused module for artifact validation and mutations, rather than further expanding `server.py`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- focused server/API and UI-regression tests

## Technical risks

- Layer records do not all expose one uniform stable-record identifier.
- Whole-workstream JSON writes require explicit revision conflict handling.
- Storing source text snapshots may drift from source truth; references should remain authoritative.
- Client-supplied actor identity is demo-only and is not production authorization.
- Generic artifact infrastructure may become over-engineered if the first validator contract is too abstract.

## Recommended implementation slices

1. Generic artifact envelope, validator registry, revision engine, API, and tests.
2. Manual chat interaction and source-record selection with UI regression tests.
3. Agent contribution tools and Moshe prompt/routing changes.
4. Assessment execution and target-candidate handoff.

Each slice changes an interface or product behavior and must stop at a checkpoint.

## Blocking questions

1. Confirm that the existing layer/catalog resolver can validate every record reference required by the demo.
2. Confirm that demo actor attribution may remain client-supplied until authentication exists.

## Recommendation

Continue to execution planning after the two blocking assumptions are explicitly accepted and UX/QA reviews are accepted.

