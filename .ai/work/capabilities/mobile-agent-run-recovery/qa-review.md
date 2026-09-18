# QA Review — resume recovery and live-step disclosure state

## Status

Ready for final validation.

## Required checks

- Direct request completes within the resume grace period: no recovery request and no synthetic step.
- Direct request fails: cached-result recovery still completes the run.
- Direct request remains stalled after resume: recovery begins after the grace period.
- Expanded step remains open as new live steps are appended.
- No change to chat auto-scroll behavior.
- Frontend asset version and source manifest are current.

## Recommendation

Approve after focused unit/contract tests and production smoke verification pass.

