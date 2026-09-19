# Final Handoff

## Capability

Playback deployment recovery

## Goal

Restore staged playback and prevent deployments from deleting mutable UI state.

## Final behavior

The live API returns playback stage 1 again. Future deployments preserve scenario runs, workstreams, investigations, and saved questions, while distributing the v2.1 manifest and keeping the service on v2.1.

## Files changed

- `llm_investigation_orchestrator_serbia_poc/mcp_server/remote_deploy_ui.py`
- `llm_investigation_orchestrator_serbia_poc/scenario_manifests/brnjak-engineering-assessment-v1.json`
- `llm_investigation_orchestrator_serbia_poc/app.js`

## Tests/checks

Focused playback suite passed: 19 tests. Python compilation, JavaScript syntax validation, and production API smoke checks passed.

## Known limitation

The current server state was already missing `scenario_runs` and `workstreams`; the inspected staged-playback backup contained the manifest only. Recover older mutable state only from a separately validated backup.

## Suggested durable documentation update

Add the deployment invariant to `docs/architecture.md`: UI code/assets may be deployed, but runtime state directories are server-owned and must never be replaced or removed by the deployer.
