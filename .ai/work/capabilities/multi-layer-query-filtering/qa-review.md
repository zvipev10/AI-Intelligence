# QA Review

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Related issue
GitHub issue: #7. Local issue body: `issues/040-qa-planning.md`.

## Review status
Approved for Slice 4 readiness.

## Role action

| Role | Status | Required action | Due before |
|---|---|---|---|
| QA | Complete for Slice 4 readiness | Canonical fixture, manual validation scope, regression priority, and browser expectations are approved. | Done |

## What changed since previous review
QA planning has been approved using conservative defaults so Slice 4 implementation can proceed with clear validation expectations.

## Context reviewed
- `capability-brief.md`
- `developer-review.md`
- `execution-plan.md`
- `checkpoint-001.md`

## Acceptance criteria review
The current acceptance criteria cover layer selection, independent selected layers, per-layer filters, empty value blocking, contains matching, AND logic, draft/apply behavior, filter editing/removal, and active filter display.

## Test strategy
Use manual browser validation for MVP. Add helper-level automated tests only if a local test harness is already practical without distracting from delivery.

## Approved QA readiness decisions
- Canonical review environment: deployed VM at `http://151.145.93.180/`.
- Canonical data state: current API-loaded dataset served by the VM at the time of Slice 4 validation.
- Required layer fixture:
  - event source `טלגרם`
  - at least one additional event-source layer
  - Entities layer
  - Locations layer
- Required browser/viewports:
  - phone `360x800`
  - phone `390x844`
  - tablet `768x1024`
  - one desktop viewport
- Required screenshots for review checkpoints:
  - mobile filter window open
  - applied filter with non-zero filtered results
  - applied filter with zero results
  - desktop or tablet filtered presentation state
- Console expectation: no browser console errors or warnings during required validation flows.
- Regression priority: preserve existing layer selection, tabs, visibility, close, raw overlay controls, table scrolling, map rendering, and timeline rendering.

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
- Deployed VM at `http://151.145.93.180/`.
- Local app server for development smoke before VM deployment.
- Browser capable of running the POC UI.
- Known API dataset state for repeatable validation.

## Open questions
None for Slice 4 readiness. The canonical fixture and screenshot expectations are approved above.

## QA recommendation
Approve QA readiness for Slice 4 implementation. Slice 4 acceptance still requires executing the approved validation checklist against the implemented behavior.
