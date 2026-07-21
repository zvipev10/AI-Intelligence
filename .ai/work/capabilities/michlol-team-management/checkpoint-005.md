# Checkpoint 005 - Member Task Mentions Autocomplete

## Date

2026-07-17

## Request

Implement the approved `@member` autocomplete slice for `מכלול` team members.

## What changed

- Added a shared frontend `MICHLOL_MEMBERS` catalog for the five predefined team members.
- Rendered the compact header `מכלול` strip from the shared catalog instead of duplicated static markup.
- Added reusable `@` mention autocomplete for investigation prompt-entry surfaces:
  - main investigation prompt;
  - step-continuation prompt.
- Supported multiple mentions in one prompt.
- Added compact member suggestions with avatar, name, and role.
- Added keyboard behavior:
  - Arrow Up / Arrow Down changes active suggestion;
  - Enter / Tab inserts;
  - Escape closes.
- Added pointer selection and outside-click closing.
- Added no-match behavior: the popover hides when no member matches.
- Kept mention metadata transient/client-side only.
- Added the approved always-on Hermes instruction so teammate names such as `@משה` are ignored as investigation entities unless explicitly requested.
- Preserved the existing `/api/investigate` request shape; no structured `team_mentions` payload is sent.
- Bumped cache keys:
  - `styles.css?v=84`
  - `app.js?v=105`

## Files changed

- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `.ai/work/capabilities/michlol-team-management/execution-plan.md`
- `.ai/work/capabilities/michlol-team-management/status.md`
- `.ai/work/capabilities/michlol-team-management/issues/050-member-task-mentions.md`

## Validation

- `git diff --check` passed.
- Shell `node --check` could not run because `node` is not available in this PowerShell environment.
- Node-backed runtime parse check passed for `app.js`.
- Local browser smoke on `http://127.0.0.1:5177/` passed:
  - `@` in the main prompt opened five member suggestions.
  - Arrow Down + Tab inserted `@טליה`.
  - The menu closed after insertion.
  - Filtering by role text `@איסוף` showed גדי.
  - No-match text hid the popover.
  - Header rendered all five member ids from the shared catalog.
  - `styles.css?v=84` and `app.js?v=105` loaded.
  - Main and step-continuation textareas both have autocomplete wiring.

## Not fully validated

- A live continuation request was not run because the local static smoke does not execute a real Hermes investigation flow.
- VM deployment was not performed in this checkpoint.

## Review needed

- Product/UX: review prompt-only mention behavior and compact picker interaction.
- QA: validate RTL typing, keyboard selection, filtering, no-match behavior, main prompt submission, step-continuation submission, selected-layer prompt context, and header/team menu regression.

## Rollback

Restore static header markup if needed, remove the mention autocomplete CSS/JS, remove the always-on Hermes instruction wrapper, and restore cache keys. No backend or data migration is involved.
