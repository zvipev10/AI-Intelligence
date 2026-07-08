# [QA] Multi-Layer Query Filtering Test Planning

## Purpose
Define manual validation scope, test data needs, and regression coverage.

GitHub issue: #7

## Required action
QA has confirmed the canonical dataset and approved the validation checklist for Slice 4 readiness.

## Owner role
QA.

## Inputs
- `qa-review.md`
- `capability-brief.md`
- `execution-plan.md`
- `checkpoint-001.md`

## Expected output
QA-approved test fixture and validation checklist.

## Blocking
No longer blocking Slice 4 implementation. Slice 4 acceptance still requires executing the approved validation checklist.

## QA readiness decisions
- Canonical review environment: deployed VM at `http://151.145.93.180/`.
- Canonical data state: current API-loaded dataset served by the VM at the time of Slice 4 validation.
- Required layer fixture: `טלגרם`, at least one additional event-source layer, Entities, and Locations.
- Required browser/viewports: `360x800`, `390x844`, `768x1024`, and one desktop viewport.
- Screenshots required for mobile filter open, non-zero filtered results, zero-result filtered state, and desktop/tablet filtered presentation.
- Console expectation: no browser console errors or warnings during required validation flows.
- Regression priority: layer selector, tabs, visibility, close, raw overlay controls, table scrolling, map rendering, and timeline rendering.

## Completion criteria
- [x] Canonical API-loaded dataset identified.
- [x] Manual happy path checks approved.
- [x] Edge cases approved.
- [x] Regression areas approved.
- [x] Browser validation expectations confirmed.

## Related artifacts
- `qa-review.md`
- `execution-plan.md`

## Parent capability
#3 / `000-parent-capability.md`
