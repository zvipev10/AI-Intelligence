# Checkpoint 007 - Blue Mention Token Follow-up

## Date

2026-07-17

## Request

Apply Product/UX feedback that after selecting an `@name`, the inserted mention should be visually blue rather than regular white prompt text.

## Implementation

- Added a synchronized mention-highlight layer for prompt textareas.
- Recognized `@member` tokens are rendered with the existing blue accent color.
- Unknown `@text` remains regular prompt text.
- The underlying textarea value remains unchanged, so prompt submission, autocomplete filtering, client-only mention metadata, and Hermes behavior are unchanged.
- Applied the same behavior to the main prompt and step-continuation prompt surfaces.
- Bumped review cache keys:
  - `styles.css?v=85`
  - `app.js?v=106`

## Validation

- `git diff --check`
- JavaScript parse check for `llm_investigation_orchestrator_serbia_poc/app.js` was completed before artifact-only follow-up edits; standalone `node` is not available in the PowerShell shell.

## Deployment

Deployed to the shared VM on 2026-07-17.

- Host: `151.145.93.180`
- Active UI directory: `/opt/serbia-poc-ui`
- Service: `serbia-poc-ui.service`
- Public review URL: `http://151.145.93.180/`

## Deployment verification

- Copied only `index.html`, `app.js`, and `styles.css` through a timestamped `/tmp/serbia-poc-ui-mention-blue-*` staging directory.
- Restarted `serbia-poc-ui.service`; it reported `active`.
- VM-local `/api/status` returned `mode=hermes`, `configured=true`, and `build=serbia-poc-1`.
- VM-local and public index both serve:
  - `styles.css?v=85`
  - `app.js?v=106`
- Public `styles.css?v=85` contains `.mention-highlight-token`.
- Public `app.js?v=106` contains `enableMentionHighlight` and `syncMentionHighlight`.

## Review needed

Product/UX/QA should confirm:

1. Selecting a predefined `@member` inserts the mention and shows it in blue.
2. Normal text remains regular prompt text.
3. Unknown `@text` does not become blue.
4. Main prompt and step-continuation prompt behavior are not regressed.
