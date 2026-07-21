# Checkpoint 002 - VM UI Deployment Fix

## Date

2026-07-17

## Request

The VM did not appear to show the `מכלול` member-selection feature after the integration branch was published.

## Finding

The VM backend was already running the dataset-v2 runtime:

- `build`: `serbia-poc-v2`
- `dataset_version`: `v2`
- `dataset_rows`: `14800`

The VM UI was stale. Public `index.html` was still serving the older cache keys:

- `styles.css?v=83`
- `app.js?v=105`

That old UI bundle did not include the latest `מכלול` member-selection behavior.

## Action Taken

Deployed only the integrated UI files from `codex/integrate-michlol-dataset-v2` to `/opt/serbia-poc-ui/` on the VM, preserving the already-running dataset-v2 backend and data:

- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/styles.css`

Restarted `serbia-poc-ui.service` after copying the files.

## Verification

Public VM now serves the integrated UI cache keys:

- `styles.css?v=88`
- `app.js?v=109`

Public `app.js?v=109` contains the expected feature markers:

- `MICHLOL_MEMBER_WELCOME`
- `selectConversationMember`

Public `styles.css?v=88` contains the expected styling markers:

- `.michlol-member.active`
- `.member-welcome-message`

Browser smoke validation on `http://151.145.93.180/` confirmed:

- 5 `מכלול` member buttons render.
- Selecting `טליה` marks `talia-tama-officer` active.
- The prompt placeholder changes to `כתוב אל טליה...`.
- A member welcome message is added to the chat area.

## Notes

If an existing browser tab still shows the old behavior, hard refresh the page to clear the stale cached UI bundle.
