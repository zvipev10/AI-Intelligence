# UX Review

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Related issue
GitHub issue: #6. Local issue body: `issues/030-ux-review.md`.

## Review status
Changes requested after Product review of `checkpoint-002.md`.

## Role action

| Role | Status | Required action | Due before |
|---|---|---|---|
| UX | Waiting on Development | Review the corrected selector/control/table styling after Product's Slice 1 UX comments are implemented. | Slice 2 starts |

## What changed since previous review
Product reviewed Slice 1 and said the selector correction looks good, with three UX comments before Slice 2: make the selector almost half as wide, make the selector and other map-top components transparent, and make the results table slightly transparent in the same visual direction.

## Context reviewed
- `capability-brief.md`
- `developer-review.md`
- `execution-plan.md`
- `checkpoint-001.md`

## User flow
Users select layers from a compact search/autocomplete affordance. Selecting a result opens that layer in the existing results panel as an opened layer tab. Once filter UI is implemented, users open filters from the layer tab, edit draft filters, and Apply changes per layer.

## UI states
- Compact selector idle state.
- Selector focused/searching state with matching results.
- No matching layer result state.
- Opened layer tab selected/active state.
- Opened layer tab with unapplied filter changes.
- Opened layer tab with applied filters.

## Empty states
- No layers available.
- No event-source layers available.
- No selector search matches.
- Selected layer has no rows.
- Applied filters return no matching rows.

## Error states
- Layer catalog load fails.
- Selected layer row load fails.
- Filter Apply blocked by empty value.

## Disabled/loading states
- Selector loading catalog.
- Selected layer loading rows.
- Apply disabled or blocked when draft filters are invalid.

## Copy / terminology
MVP uses raw field names for filter fields. Avoid section labels such as "Data layers", "Layer selection", or available-layer counts around the selector.

## Accessibility notes
- Selector should be keyboard reachable.
- Autocomplete results should have clear focus and selection behavior.
- Filter validation should be visible inline, not only color-based.

## UX edge cases
- Compact selector should not obscure map/timeline investigation content.
- Compact selector should be almost half the current width from `checkpoint-002.md`.
- Selector, map-top controls, and results table should use a transparent/translucent treatment while preserving readability.
- Filter action, visibility action, and X close action must remain visually distinct.
- Layer close should not feel like filter editing.
- Unapplied filter changes should be visible enough to prevent accidental confusion.

## Product questions
No current blocking Product questions. Product has requested three Slice 1 UX styling changes before approval.

## Developer questions
- Can the selector wrapper/header/count be removed without changing the API-backed catalog and row loading behavior?
- Should the corrected selector be placed on the map surface or remain above the presentation area as a compact line?
- Can the selector width, map-top transparency, and results-table transparency be changed with CSS-only updates and no API/catalog behavior changes?

## Review recommendation
Request changes for Slice 1. Do not continue to Slice 2 until Product's three UX styling comments are implemented and reviewed.
