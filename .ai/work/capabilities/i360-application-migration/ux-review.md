# UX review: I360 application migration

## Review status

Ready for planning. Part 1 preserves the data exploration UI and disables chat investigation. Part 2 restores chat, live progress, cancellation, saved answers, and agent failure states. Final copy and degraded-state behavior require human UX acceptance.

## Preserved flows

- open or create an investigation;
- search through chat and existing controls;
- inspect results on the map, timeline, catalog, and object viewer;
- open source text and media;
- save questions/layers and revisit investigation context;
- create and inspect target candidates.

## Part 1 search interaction

The current application has no global evidence-search field. `promptInput` is an investigation-agent composer; `investigationInput` selects investigations; `layerSelectorSearch` finds catalog layers; table and layer filters only narrow records already loaded.

Part 1 adds a dedicated I360 evidence-search control outside the chat panel. It provides query text, text/semantic mode, and supported structured filters. A submission creates a standard result layer so the existing map, timeline, table, filtering, object-view, and save interactions can be reused. The chat panel remains disabled until Part 2 rather than changing meaning between releases.

## Required new states

- authentication expired or I360 unavailable;
- semantic search unavailable because embeddings are missing;
- geographic operation unavailable;
- partial/incomplete result with an explanation and retry/refinement action;
- source detail or media denied by permissions;
- item removed or no longer visible since it was cited;
- saved state references evidence the current user cannot access.

Warnings must be visible near the affected result and must not be presented as “no evidence found.” Existing bilingual and RTL behavior remains required.

## Exclusions

Workstream and scenario playback are not part of this migration flow or its UX acceptance.
