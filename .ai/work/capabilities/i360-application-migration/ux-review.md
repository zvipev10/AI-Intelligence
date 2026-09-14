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
