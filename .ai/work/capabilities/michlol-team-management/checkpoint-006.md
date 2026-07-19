# Checkpoint 006 - Member Mentions VM Deployment

## Date

2026-07-17

## Request

Deploy the implemented `@member` autocomplete Slice 2 to the shared review VM.

## Deployment

Deployed to the shared VM on 2026-07-17.

- Host: `151.145.93.180`
- Active UI directory: `/opt/serbia-poc-ui`
- Service: `serbia-poc-ui.service`
- Public review URL: `http://151.145.93.180/`

## Files deployed

Only the three changed UI files were deployed, preserving the existing VM server configuration, assets, data, saved questions, investigation memory, and Hermes API config:

- `/opt/serbia-poc-ui/index.html`
- `/opt/serbia-poc-ui/app.js`
- `/opt/serbia-poc-ui/styles.css`

## Verification

- SSH connectivity succeeded with the existing VM key.
- `serbia-poc-ui.service` was active before deployment.
- Copied the three UI files through a timestamped `/tmp/serbia-poc-ui-slice2-*` staging directory.
- Installed the files into `/opt/serbia-poc-ui`.
- Restarted `serbia-poc-ui.service`; it reported `active`.
- VM-local `/api/status` returned:
  - `mode=hermes`
  - `configured=true`
  - `build=serbia-poc-1`
- VM-local index serves:
  - `styles.css?v=84`
  - `app.js?v=105`
- Public `http://151.145.93.180/` serves:
  - `styles.css?v=84`
  - `app.js?v=105`
- Public `http://151.145.93.180/app.js?v=105` contains:
  - `TEAM_MENTION_AGENT_INSTRUCTION`
  - `MICHLOL_MEMBERS`
  - `teamMentionMenu`
  - both prompt builders appending the Hermes ignore instruction.

## Not validated in this deployment step

- Full browser interaction against the public VM UI was not repeated after deployment.
- Live Hermes investigation run with `@member` mention was not executed.

Local pre-deploy browser smoke is documented in `checkpoint-005.md`.

## Review needed

Product/UX/QA should review Slice 2 on the VM:

1. Open `http://151.145.93.180/`.
2. Type `@` in the main prompt and confirm all five members appear.
3. Type `@איסוף` and confirm גדי appears.
4. Use Arrow Up/Down and Enter/Tab to insert a member.
5. Confirm no visible task record is created.
6. Confirm existing prompt submission, selected-layer context, step-continuation prompt, and header teammate menu behavior are not regressed.
