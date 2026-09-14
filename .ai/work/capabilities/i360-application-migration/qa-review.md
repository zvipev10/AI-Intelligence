# QA review: I360 application migration

## Review status

Ready for planning. Detailed test cases should be finalized after live field mapping.

## Test strategy

- Provider contract tests with fixed local fixtures and recorded/redacted I360 responses.
- Differential tests that run the same representative queries through local and I360 providers and compare functional outcomes.
- Live integration tests using ordinary users with own, shared, and denied records.
- Existing non-Workstream regression suite for frontend contracts, routing, presentation, object viewer, targets, and MCP reasoning.
- Focused browser tests for map/list/timeline selection and degraded states.

## Required cases

- text, semantic, time, source, entity, radius, bounding-box, and polygon queries;
- paging, sort stability, caps, warnings, missing capabilities, and empty results;
- original/translated text, transcript/OCR fallback, media authorization, and expired URLs;
- stable citations through search, detail, saved layers, memory, and target evidence;
- permission differences between search, direct GET, context, entities, and media;
- Hebrew and English queries plus RTL display;
- I360 timeout, 401, 403, 404, 429, and 5xx handling;
- provider rollback without data corruption;
- simultaneous writes if mutable state moves to I360.

## Regression exclusions

Workstream and playback test suites are not migration acceptance gates. Existing unrelated behavior should not be intentionally changed.
