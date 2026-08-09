# Playback reevaluation audit

## Finding

The Next-slice workstream reevaluation capability still exists and has not been deleted. It advances
the visible timeframe, reevaluates active workstreams asynchronously, persists new indications and
target layers, and returns them to the UI.

Production run `run_20260809_082815_3e4d00c9` contains a completed revision-3 reevaluation with new
records, an updated workstream artifact, and both indication and target result layers. This proves the
backend path has executed successfully in production.

## Confirmed display gap

The UI polls and renders the result while the browser remains on the page and observes the transition
from `running` to `completed`. On page refresh or reopening the investigation after completion,
`fetchInvestigationPlayback()` does not rehydrate and render the already stored completed assessment.
The persisted update can therefore appear missing even though it remains in the scenario run and
workstream artifact.

## Operating conditions

- Reevaluation runs only after Next slice, not for the initial baseline.
- At least one active workstream must match the investigation and locale.
- The final slice cannot advance further.
- Processing is asynchronous, so results appear only after reevaluation completes.

## Recommendation

Add completed-assessment recovery to the initial playback fetch in a separate corrective slice. No
playback code was changed during this audit.

