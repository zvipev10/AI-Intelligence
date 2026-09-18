# Final Handoff — mobile agent-run recovery

## Goal

Prevent false Hermes steps after app resume and keep analyst-expanded live steps open while new steps arrive.

## Final behavior

Returning to the app waits briefly for the original request. Recovery starts only if that request remains unsettled, and recovery status is not represented as a research step. Live step refreshes restore the analyst's expanded disclosure state.

## Files changed

- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/test_mobile_run_recovery.py`
- frontend asset-version contract tests and source manifest
- capability status, plan, QA, checkpoint, and handoff artifacts

## Decisions

- Preserve existing request-ID recovery.
- Use a 2.5-second resume grace period.
- Treat recovery as transport behavior, not an agent research step.
- Preserve disclosure state by visible step number during append-only live polling.

## Known limitations

Expanded state is preserved within the current response only; reopening a saved run starts with its normal collapsed presentation.

## Release note

Fixed mobile/desktop resume behavior for active agent runs and prevented open research steps from collapsing when new live steps arrive.

