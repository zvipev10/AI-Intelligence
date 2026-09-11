# Capability Brief — Agent catalog-layer opening

## Status
Approved for end-to-end delivery by the user on 2026-09-11.

## Problem
Commands such as “open the Telegram layer” are misrouted as saved-memory
presentation. Invalid memory IDs are silently discarded, so the agent answers
without opening a layer.

## Approved behavior
- Distinguish catalog-layer navigation from saved-memory presentation and data search.
- Resolve only server-provided catalog IDs and localized labels.
- Return a structured catalog-layer action through the agent result envelope.
- Let the browser open the layer through the existing `openCatalogLayer` path,
  activate it, switch to the requested view, and redraw all presentations.
- Return explicit errors for invalid or ambiguous catalog IDs.
- Keep filtered analytical requests on `search_events` plus requested results.

## Non-goals
- Fuzzy semantic catalog matching inside the browser.
- Replacing saved-memory presentation.
- Treating unfiltered catalog navigation as an intelligence search.

## Acceptance criteria
1. “Open Telegram layer” resolves to the canonical Telegram catalog ID.
2. The catalog row endpoint is fetched and the visible selected tab appears.
3. The map redraws with both regular and eligible symbology markers.
4. Invalid catalog IDs are rejected rather than silently ignored.
5. Saved-memory and filtered-search flows remain unchanged.
6. Automated and production browser acceptance pass with rollback documented.

