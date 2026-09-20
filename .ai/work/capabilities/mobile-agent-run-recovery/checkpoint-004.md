# Checkpoint 004 — remove focus-triggered completion race

## Trigger

Production v195 showed the generic agent-run failure after switching away and returning on both desktop and mobile, even though the backend had completed the same run with a valid answer and six steps.

## Root cause

Focus and `pageshow` started a second recovery completion path while the original fetch was still active. The browser could enter the outer failure path despite the backend successfully completing and caching the run.

## Resolution

- Remove the focus- and `pageshow`-triggered `Promise.race`.
- Await the original investigation request as the single normal completion path.
- Start request-ID recovery only when that fetch actually fails.
- Retain request-scoped live-step polling to prevent previous-run steps from appearing.
