# QA Review

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Related issue
GitHub issue: #7. Local issue body: `issues/040-qa-planning.md`.

## Review status
Pending human review.

## Role action

| Role | Status | Required action | Due before |
|---|---|---|---|
| QA | Action needed before acceptance | Confirm canonical test fixture, manual validation scope, and any required regression priority. | Slice 4 completion |

## What changed since previous review
QA planning has been backfilled from the brief, developer review, execution plan, and Slice 1 checkpoint. It still needs human QA approval.

## Context reviewed
- `capability-brief.md`
- `developer-review.md`
- `execution-plan.md`
- `checkpoint-001.md`

## Acceptance criteria review
The current acceptance criteria cover layer selection, independent selected layers, per-layer filters, empty value blocking, contains matching, AND logic, draft/apply behavior, filter editing/removal, and active filter display.

## Test strategy
Use manual browser validation for MVP. Add helper-level automated tests only if a local test harness is already practical without distracting from delivery.

## Happy path tests
- Select Entities.
- Select Locations.
- Select at least two event-source layers.
- Confirm each layer opens as a tab.
- Add one filter to a layer and Apply.
- Add multiple filters to one layer and confirm AND behavior.
- Switch layers and confirm filters remain independent.

## Edge cases
- No layers available.
- No event-source layers available.
- Layer search returns no matches.
- Selected layer has no rows.
- Selected layer has no discoverable fields.
- Applying filters returns no rows.
- Hebrew and English contains matching.
- Field exists on some rows but not others.
- Contains matching over objects, arrays, nulls, and numbers.

## Negative tests
- Apply with an empty filter value.
- Row-loading API failure.
- Layer catalog API failure.
- Close a layer with draft filters.
- Close a layer with applied filters.

## Regression areas
- Existing chat/agent result loading.
- Existing raw overlay open/close/minimize/resize.
- Existing layer tab selection.
- Existing layer X close action.
- Existing layer visibility action.
- Map and timeline rendering.

## Automation suggestions
- Add helper tests for field discovery, value stringification, text normalization, AND matching, and draft/applied filter transitions if a JS test harness is available.
- Keep API smoke checks for `/api/layers` and selected layer row endpoints.

## Test data needs
- Entity metadata rows.
- Location metadata rows.
- Event rows from at least two `source_type` values.
- Hebrew and English text values for contains matching.
- A layer/filter combination expected to return zero rows.

## Environment needs
- Local app server.
- Browser capable of running the POC UI.
- Known API dataset state for repeatable validation.

## Open questions
- Which API-loaded dataset state should QA treat as the canonical manual fixture?
- Should screenshots be required for Product/UX review checkpoints?

## QA recommendation
QA planning is adequate as a draft, but human QA should approve fixtures and validation expectations before Slice 4 is accepted.
