# Saved Questions Feature Plan

Date: 2026-06-30

## Purpose

Replace the current recorded-question replay feature with a user-facing **Saved Questions** capability.

The analyst should be able to save any completed investigation result and later reopen it with full presentation functionality:

- Original analyst question
- Final agent answer
- Investigation steps
- Step explanations
- Tool outputs
- Event IDs
- Event/location/entity layers
- Map, timeline, and table presentation data
- Usage/performance metadata when available

Loading a saved question should not call Hermes. It should restore the saved investigation artifact.

## Current Recorded Replay Limitation

The existing `recorded_runs/` feature is demo-oriented:

- Recordings are prepared manually or by developer scripts.
- Steps are replayed with artificial timing.
- It is not a natural user workflow.
- It does not let the analyst decide which live investigation result should be preserved.

Saved Questions should become the product feature. Recorded runs can remain temporarily as legacy/demo data until removed.

## Data Model

Store one JSON file per saved question.

Suggested directory:

```text
llm_investigation_orchestrator_serbia_poc/saved_questions/
```

VM path:

```text
/opt/serbia-poc-ui/saved_questions/
```

Suggested JSON shape:

```json
{
  "id": "saved_20260630_153012_abcd",
  "schema_version": 1,
  "title": "optional user title",
  "question": "original analyst question",
  "saved_at_utc": "2026-06-30T12:30:12Z",
  "source_run_id": "run_...",
  "result": {
    "run_id": "run_...",
    "answer": "...",
    "recommended_view": "map",
    "view_reason": "...",
    "event_ids": [],
    "answer_event_ids": [],
    "investigation_steps": [],
    "events": [],
    "usage": {},
    "performance": {}
  }
}
```

Critical rule: save the full `result` object returned by `/api/investigate`, not only the answer text.

The full result is needed because the UI presentation is reconstructed from:

- `result.answer`
- `result.event_ids`
- `result.investigation_steps[].event_ids`
- `result.investigation_steps[].map_locations`
- `result.investigation_steps[].aggregate_groups`
- `result.investigation_steps[].location_layers`
- `result.investigation_steps[].entity_layers`
- `result.recommended_view`
- `result.view_reason`

## Backend API

Add endpoints to `llm_investigation_orchestrator_serbia_poc/server.py`.

```text
GET    /api/saved-questions
GET    /api/saved-question?id=<id>
POST   /api/saved-question
DELETE /api/saved-question?id=<id>
```

### GET /api/saved-questions

Returns metadata only, not full saved result payloads.

Example:

```json
{
  "saved_questions": [
    {
      "id": "saved_20260630_153012_abcd",
      "title": "מוקדי חיכוך",
      "question": "באילו אזורים יש ריכוז חריג של דיווחים?",
      "saved_at_utc": "2026-06-30T12:30:12Z",
      "source_run_id": "run_...",
      "recommended_view": "map",
      "step_count": 5
    }
  ]
}
```

### GET /api/saved-question

Returns the complete saved object for restoration.

### POST /api/saved-question

Body:

```json
{
  "title": "optional title",
  "question": "...",
  "result": {}
}
```

Validation:

- `question` must be a non-empty string.
- `result` must be an object.
- `result.answer` must be present.
- `result.investigation_steps` should be an array, or default to `[]`.
- Generate server-side `id`.
- Generate server-side `saved_at_utc`.
- Reject path traversal.
- Write UTF-8 JSON.

### DELETE /api/saved-question

Deletes one saved question by ID.

Validation:

- ID must match a strict pattern such as `^[A-Za-z0-9_.-]+$`.
- Delete only inside `saved_questions/`.

## Frontend UX

Replace the current recorded-question UX with Saved Questions.

### Save Action

Add a `שמור` action near the question input or near the final answer actions.

Behavior:

- Enabled only after a successful live answer exists.
- Saves `state.lastPrompt` and `state.lastResult`.
- Optional title:
  - First implementation can auto-title from the first 60 chars of the question.
  - Later implementation can open a small title dialog.

### Saved Questions Modal

Reuse the current recorded questions modal structure, but rename it:

- Tooltip: `שאלות שמורות`
- Modal title: `שאלות שמורות`

Each item should show:

- Title
- Question preview
- Saved time
- Recommended view
- Step count
- Buttons:
  - `פתח`
  - `מחק`

### Opening A Saved Question

Loading should not call Hermes.

Expected behavior:

1. Append the analyst question to the chat.
2. Restore the saved investigation steps.
3. Render the final answer.
4. Allow final `הצג תוצאות`.
5. Allow per-step `הצג תוצאות`.
6. Preserve all layer behavior:
   - event layers
   - location layers
   - entity layers
   - timeline/group aggregations
   - close/hide layer tabs

Use the existing `applyHermesResult` path where possible.

Recommended first behavior:

- Load immediately.
- Do not replay steps with artificial delay.

Optional later behavior:

- Add `הצג כתהליך` to replay steps progressively for demo mode.

## Migration From Recorded Runs

Do not remove recorded endpoints in the first implementation.

Recommended staged approach:

1. Add saved-question endpoints and UI.
2. Keep `recorded_runs/` endpoints temporarily.
3. Rename UI affordances from recorded to saved.
4. After saved questions are verified, decide whether to:
   - migrate existing recordings into `saved_questions/`, or
   - keep them as developer/demo fixtures only, or
   - remove them completely.

## Deployment Notes

VM service user must be able to write:

```text
/opt/serbia-poc-ui/saved_questions/
```

Deployment should create the directory and set ownership to the UI service user if needed.

The saved files are runtime-generated user artifacts. Decide before implementation whether to:

- keep them only on VM disk,
- include sample saved questions in git,
- or exclude runtime saved questions from git with `.gitignore`.

Recommended:

- Commit only the empty directory marker or documentation.
- Do not commit user-generated saved question JSON files by default.

## Security And Robustness

For the POC, file-based storage is enough.

Still required:

- Strict ID validation.
- No user-controlled paths.
- JSON size guard if needed.
- Atomic write pattern:
  - write temporary file
  - rename to final path
- Defensive parsing when listing saved files.
- Skip corrupt saved files instead of failing the whole list endpoint.

## Compatibility With Entity/Location Layers

The saved result must preserve the new normalized presentation data:

- `location_layers`
- `entity_layers`
- `map_locations`
- `aggregate_groups`
- event objects with `entity_id`, `entity_name`, `location_id`, `location_name`

This is why saving the full result object is mandatory.

If future schema changes occur, use `schema_version` for migration.

## Acceptance Tests

Local:

1. Run a live investigation.
2. Save it.
3. Reset the UI.
4. Open Saved Questions.
5. Load the saved question.
6. Verify final answer appears.
7. Press final `הצג תוצאות`.
8. Verify map/table/timeline layers are restored.
9. Press per-step `הצג תוצאות`.
10. Verify step-specific layers are restored.
11. Delete the saved question.
12. Verify it disappears from the modal and JSON file is removed.

VM:

1. Deploy code.
2. Verify `saved_questions/` exists and is writable.
3. Save from public HTTPS UI.
4. Reload browser.
5. Open saved question.
6. Verify no Hermes run is triggered for loading.

## Files Expected To Change During Implementation

Backend:

```text
llm_investigation_orchestrator_serbia_poc/server.py
```

Frontend:

```text
llm_investigation_orchestrator_serbia_poc/index.html
llm_investigation_orchestrator_serbia_poc/app.js
llm_investigation_orchestrator_serbia_poc/styles.css
```

Docs:

```text
PROJECT_HANDOFF.md
llm_investigation_orchestrator_serbia_poc/README.md
```

Optional:

```text
llm_investigation_orchestrator_serbia_poc/.gitignore
llm_investigation_orchestrator_serbia_poc/saved_questions/.gitkeep
```
