# Investigation Selection Execution Plan

## Review gate

- Product behavior was clarified and implementation authorized by the user on 2026-08-04.
- Active means the currently selected investigation.
- All other investigations remain available in the selector.
- No workstream lifecycle, API, data-model, architecture, or permission change is in scope.

## Implementation approach

1. Separate the selector search query from the active investigation name.
2. Show the complete investigation registry when the selector opens.
3. Keep exact ID equality as the single active-row rule.
4. Load workstreams and memory for the explicitly selected investigation only.
5. Retain the latest-investigation fallback only during initial bootstrap for legacy desktop continuity.
6. Ignore stale asynchronous results after a later selection.

## Files

- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/test_workstream_ui.py`
- capability decision, status, checkpoint, and handoff artifacts

## Validation

- JavaScript syntax check.
- Focused workstream UI, API, and scenario playback tests.
- `git diff --check`.
- Manual browser validation remains required before deployment.

## Rollback

Revert this slice. No persisted schema or server data migration is involved.
