# Developer Review

## Capability

Cellular Calls raw data source

## Related issue

Draft: `issues/developer-review.md`

## Review status

Pending human review

## Role action

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | AI-prepared draft | Approve or request changes | Coding |

## What changed since previous review

Initial technical review.

## Reviewer / input source

AI-prepared draft pending human approval.

## Context reviewed

Dynamic raw layer creation, CSV event projection, public MCP event projection, object viewer media routing, UAV-specific viewer behavior, dataset generator, and existing viewer CSS.

## Product requirements understood

Add tens of raw cellular-call records, expose both parties and recording, create a repeated Side A trail through the three scenario locations, and preserve existing raw-layer behavior.

## Feasibility

Feasible without a new service or layer type. Existing source-type grouping creates the catalog layer automatically, and the viewer already supports audio media.

## Likely affected files/services

- `data/generate_serbian_intelligence_v2_1.py`
- V2.1 projected Hebrew/English CSV artifacts
- New `assets/audio/cellular_calls/*.wav` assets or deterministic generator
- `mcp_server/server.py` public event projection
- `static/app.js` record classification and dedicated viewer rendering
- `static/styles.css` responsive call-party and recording presentation
- Dataset/API/UI test files

## Existing patterns to follow

- Dynamic `events:<source_type>` catalog layers.
- Locale-specific CSV projection.
- UAV specialized viewer as the routing pattern, without copying its visual design.
- Generic `audio_url` media support.

## Implementation options

### Option 1

Add call columns to the shared projected-event schema and render a specialized viewer when `source_type` matches the cellular source. Generate one deterministic WAV per call. Recommended.

### Option 2

Store call details in a secondary JSON document and expose only a reference from events. This adds unnecessary joining and a parallel contract.

## Recommended approach

Option 1. Extend events additively, keep blank call fields for other sources, preserve dynamic catalog behavior, and add a single call-specific viewer branch.

## Technical risks

- Schema consumers that assume an exact column set.
- Audio URL/mime handling on deployment.
- Duplicated party fields if generic metadata is not filtered.
- Phone/IMEI rendering as numeric values may lose formatting; keep them as strings.

## Data/API considerations

- Add explicit call fields and expose them through `public_event()`.
- Use `timestamp_utc` as the canonical start timestamp while also displaying it as call start time.
- Add duration, sector IDs, recording URL, and transcript.
- Preserve all existing event IDs and generator determinism.

## Security/permissions considerations

Use synthetic identifiers and generated audio only. Mark them as simulation data. Do not include real voices or PII.

## Performance considerations

Twenty-four small compressed-equivalent WAV assets are acceptable for demo scale; use `preload="metadata"` to avoid loading all recordings. Only one record viewer plays audio at a time.

## Test strategy

Generator invariants, schema/API contract tests, asset validation, layer-catalog test, viewer unit/render tests, and mobile RTL/LTR visual verification.

## Acceptance criteria improvements

Assert the repeated identity appears exactly three times in each requested location and nowhere else; assert Side B and sector differ for every linked record.

## Proposed execution slices

### Slice 1

Dataset schema, deterministic call records, audio generation, and contract tests.

### Slice 2

MCP/public projection and search/object retrieval tests.

### Slice 3

Specialized viewer, responsive styles, localization, and regression tests.

## Required review gates before coding

Product scope, developer feasibility, UX viewer, QA coverage, and synthetic-data acknowledgement.

## Blocking questions before execution planning

- Is generated non-speech audio with transcript acceptable?
- Is the sector-within-canonical-location model the intended meaning?

## Open questions for Product / UX / QA / Architecture / Security

Whether the transcript is always visible or collapsed beneath the recording player.
