# QA Review

## Capability

Annotated investigation memory

## Related issue

`issues/parent-capability.md`

## Review status

Draft — pending human QA approval.

## Acceptance criteria review

The approved scope is testable if it specifies bounded comment/geometry limits, a source-unavailable state, and saved-investigation-only visibility.

## Test strategy

- Unit tests for comments/artifacts and schema compatibility.
- UI regression tests for each action, screen, localization, disabled state, and cache/version updates.
- Polygon-control behavior tests.
- Manual browser verification in Hebrew and English, desktop and narrow layout.

## Happy path tests

- Save chat and layer with/without comment.
- Save table object and viewer object with a comment.
- Complete, select, and save a polygon with a comment.
- Open Memory and verify all categories, comments, timestamps, and original details.
- Reload the investigation and verify persisted entries still render.

## Edge and negative tests

- Empty, whitespace-only, max-length, and over-limit comments.
- Invalid/non-closed/oversized polygon payloads.
- No active saved investigation, draft investigation, network failure, timeout, and cancel.
- Missing object on reload retains context-only entry.
- Duplicate object/polygon saves with different comments are retained separately.
- Existing v1 memory without artifacts loads/restores existing layers unchanged.

## Regression areas

- Existing chat/layer save buttons and draft-create continuation.
- Layer restoration and agent memory injection.
- Object viewer docking, Table interactions, MapLibre markers, drawing cancellation, basemap changes, and locale switching.

## QA recommendation

Approve after exact comment and polygon vertex limits are set in the execution plan, and after a manual accessibility check covers polygon-save access.

