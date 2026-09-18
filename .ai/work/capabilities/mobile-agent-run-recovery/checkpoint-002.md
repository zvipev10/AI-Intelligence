# Checkpoint 002 — resume UX regression fixes

## Changes

- Removed the synthetic `connection_recovery` research activity.
- Added a 2.5-second grace period before visibility-triggered recovery.
- Changed live polling to append new step DOM nodes without rebuilding existing disclosures; full rebuilds retain the expanded-state fallback.
- Bumped `app.js` asset version to 192 and updated frontend contracts.

## Scope

Frontend only. No API, database, agent, or MCP changes.

## Validation

Focused and regression checks are recorded in the final handoff.
