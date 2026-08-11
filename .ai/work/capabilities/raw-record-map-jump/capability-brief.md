# Capability Brief

## Capability name

Raw record to map jump

## Capability slug

`raw-record-map-jump`

## Parent issue

Local draft: `issues/parent-capability.md`

## Current status

Pending human review. See `status.md`.

## User problem

An analyst inspecting a raw record in the results table cannot move directly to its geographic context. They must manually switch to the map and find the matching location among aggregated markers.

## Business goal

Make raw evidence spatially inspectable in one action while preserving the analyst's current result layers and filters.

## Target users

Intelligence analysts reviewing event/raw-record result layers.

## Proposed behavior

Each raw event row with a resolvable location exposes a bilingual “Show on map” pin action. Activating it:

1. switches to the map view;
2. centers and zooms the map on the record's canonical location;
3. opens an event-specific tooltip showing the selected record, not only the existing aggregate-location tooltip;
4. leaves the results layer, filters, sorting, and table state intact.

The event tooltip should show record ID, time, entity, location, and summary. Keyboard activation and an accessible label are required.

## MVP scope

- Raw event rows only (`events` layers).
- Canonical coordinates from `LOCATIONS[event.location_id]`, with event coordinates as a fallback if available.
- Dedicated pin action rather than making the full row clickable.
- Map centering, sensible detail zoom, and event-specific popup.
- Hebrew and English labels.

## Non-goals

- Navigation from aggregate, entity, location-metadata, or target-candidate rows.
- Changing marker aggregation.
- Persisting the focused record across reloads.
- Adding new backend APIs or data-model fields.

## Acceptance criteria

- A raw event with a resolvable location has a visible, keyboard-accessible map action.
- Activating the action switches to the map and centers on the event location.
- The opened popup identifies the exact selected record and shows its core details.
- Existing table sorting and filtering still work with the action column.
- Repeated jumps replace the previous focused popup without accumulating popups.
- A record without resolvable coordinates does not offer an active jump action.
- Hebrew and English UI text are correct.

## Edge cases

- The event layer is currently hidden.
- Several records share one aggregated location marker.
- The map has not finished initializing.
- The table is minimized or filtered/sorted.
- The location ID is unknown and the event has no coordinates.
- Popup text contains untrusted dataset content and must remain escaped.

## Technical constraints

- Current map rendering clears and recreates markers in `renderMap()`.
- Current event markers aggregate by location and their popup is location-level.
- The result table is rendered as HTML and subsequently enhanced with column sorting/filtering.
- The implementation should remain client-side in `app.js` and `styles.css`; no API change is expected.

## UX notes

- Use a compact pin icon button in a dedicated action column.
- Keep the table visible after switching to the map so the analyst can continue reviewing rows.
- Use an event-specific popup anchored at the selected coordinates.
- Do not overload the existing aggregate marker popup with one arbitrarily selected record.

## QA notes

- Validate both locales and keyboard activation.
- Validate a shared-location case to ensure the selected record, rather than a neighboring event, is shown.
- Regression-check table sorting/filtering column indexes and ordinary map fit behavior.

## Risks

- Automatic `renderMap()` calls could close the focused popup unless its lifecycle is explicit.
- Adding a table column can affect the current generic sort/filter enhancement.
- A hidden source layer may create ambiguity over whether the event marker itself should become visible.

## Open questions

- Proposed assumption: jumping does not change the layer's visibility; it opens a standalone event popup even if the aggregate marker is hidden.
- Proposed detail zoom: preserve a closer current zoom, otherwise zoom to approximately 13.

## Missing inputs

- Human confirmation of the proposed standalone event-popup behavior and hidden-layer assumption.

## Required reviewers

- Product/user acceptance
- Development
- UX
- QA

## Required child issues

- [ ] Product review
- [ ] Developer review
- [ ] UX review
- [ ] QA review
- [ ] Execution planning

## Proposed execution checkpoints

1. Review and approve interaction contract.
2. Implement event-row action and focused-popup lifecycle.
3. Run focused automated checks and browser acceptance.
4. Deploy only after explicit deployment request or acceptance.

## Handoff to developer

Questions for developer:
- What is the safest popup lifecycle alongside `renderMap()` marker recreation?
- Should the focused record be stored in UI state so a map rerender can restore its popup?
- Which existing tests can be extended without coupling to exact translated column text?

Expected developer output:
- feasibility notes
- likely affected files/services
- implementation options
- recommended approach
- technical risks
- test strategy
- proposed execution slices
