# Checkpoint 018 — Global playback Next correction

## Checkpoint status

Implemented; pending Product/QA review and deployment.

## Problem

The playback visibility policy was global, but playback status and transitions
looked up scenario runs by the selected investigation. Switching investigations
left the global Next button available while the server attempted to create a
second run and returned `Another scenario run is already active`.

## Accepted behavior

- One active scenario run supplies the staged playback clock for all investigations.
- Investigation selection changes investigation and workstream context only.
- Status, mode, reset, and Next resolve the same active global run.
- Pressing Next after switching investigations advances the existing run once.

## What changed

- Replaced investigation-scoped run lookup with active-global-run lookup in the
  playback status and mode handlers.
- Made Next resolve the run referenced by the active visibility policy, with the
  active global run as a recovery fallback.
- Preserved the selected investigation ID as request/UI context without changing
  run ownership or creating another run.
- Added an automated cross-investigation regression test.

## Tests/checks run

- `python -m unittest test_scenario_playback`: 16 tests passed.
- `python -m unittest discover -p 'test_*.py'`: 132 tests passed.
- Python compilation: passed.
- `git diff --check`: passed.

## Risks

- Playback remains process-global, so concurrent users share the same scenario
  clock; this is an existing accepted limitation.
- Deployment smoke should confirm the production visibility policy references the
  same run returned before and after an investigation switch.

## Review request

Product/QA should verify that switching investigations preserves the timeframe and
that one press of Next advances it without a conflict message or duplicate run.
