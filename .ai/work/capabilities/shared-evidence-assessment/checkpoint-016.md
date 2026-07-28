# Checkpoint 016 — Minimal next-stage playback and Moshe reevaluation

## Checkpoint status

Implemented and pending Product acceptance.

## Handoff

Next role: Product owner.

Required action: review the single-button interaction and approve or request
changes.

Do not proceed to deployment until the owner explicitly approves it.

## Approved slice

- One `Next stage` button in the existing workstream update.
- A tooltip showing the next stage's timeframe.
- The first press releases the first configured stage; each later press releases
  one additional stage.
- Every successful release triggers Moshe exactly once for that run revision.
- Moshe sees cumulative visible evidence and the newly released timeframe.
- No scenario picker, playback panel, reset UI, or separate completion UI.

## What changed

- Added workstream playback status and next-stage endpoints.
- Added server-derived next-stage timeframe metadata.
- Added durable per-revision Moshe claims to prevent duplicate triggers.
- Added the single button, tooltip, processing-disabled state, and Moshe
  response rendering to the existing workstream message.
- At the final stage, the button is absent because there is no next timeframe.

## API surface

- `GET /api/workstreams/{workstream_id}/playback`
- `POST /api/workstreams/{workstream_id}/playback/next`

## Tests/checks run

- Full Python discovery: 95 tests passed.
- Focused scenario and workstream UI tests: 27 passed.
- JavaScript syntax check: passed.
- Python compilation: passed.
- `git diff --check`: passed.

## Review findings

No blocking issue was found within the approved boundary.

The durable claim provides at-most-once triggering. If the process fails after
the claim but before Moshe finishes, the stage remains released and the UI
reports the failure; it does not automatically run Moshe again.

Prepared-scenario selection remains automatic and dataset-compatible because
the approved UI contains no picker.

## Not completed

- VM deployment and production smoke validation.

## Recommendation

Approve checkpoint 016, then explicitly authorize deployment.
