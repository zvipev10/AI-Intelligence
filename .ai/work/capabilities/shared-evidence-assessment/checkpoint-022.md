# Checkpoint 022 — Initial time-slice reset control

## Summary

The real-time playback header now includes a reload-style control beside Next.
It resets the single global scenario run to its initial time slice.

## Behavior

- The reset button is visible only in real-time mode.
- It uses the existing global playback mode endpoint with `reset: true`.
- Both playback controls are disabled while Moshe is processing.
- The button has a localized tooltip and accessible label.
- Failures are reported in the conversation without changing mode.

## Scope

No API, persistence, data-model, or architecture changes.

## Deployment

Implementation validation passed:

- JavaScript syntax check passed.
- Focused playback/header UI suite: 33 tests passed.
- Full Python discovery: 141 tests passed.

Localized VM deployment is pending.
