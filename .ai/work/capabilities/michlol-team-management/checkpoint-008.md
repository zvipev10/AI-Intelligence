# Checkpoint 008 - Mobile Mention Visual QA

## Date

2026-07-17

## Request

Investigate visual bugs in the latest `@member` mention feature on mobile.

## Evidence captured

Screenshots were captured at a 390 x 844 mobile viewport.

- `audit-mobile-mention-20260717/01-mobile-initial.png`
- `audit-mobile-mention-20260717/02-mobile-at-menu.png`
- `audit-mobile-mention-20260717/03-mobile-selected-mention.png`
- `audit-mobile-mention-20260717/04-local-fixed-mobile-at-menu.png`
- `audit-mobile-mention-20260717/05-local-fixed-mobile-selected-mention.png`
- `audit-mobile-mention-20260717/06-public-deployed-mobile-at-menu.png`
- `audit-mobile-mention-20260717/07-public-deployed-mobile-selected-mention.png`

## Findings

- The `@member` suggestion menu opened below the prompt on mobile, which made it float down over the following map/results area.
- The mention-highlight wrapper and textarea had different heights because the textarea remained an inline-level control inside the wrapper.
- The selected mention was technically blue, but the wrapper mismatch made the mobile prompt look less stable than the original textarea.

## Implementation

- Mobile `@member` menu placement now prefers opening above the prompt when there is room.
- The mention source textarea is now `display: block`, keeping the textarea, wrapper, and highlight layer aligned.
- Mobile menu max height is slightly reduced to fit better above the prompt.
- Bumped review cache keys:
  - `styles.css?v=86`
  - `app.js?v=107`

## Validation

- `git diff --check`
- Mobile browser QA on local patched files at 390 x 844.
- Verified local patched metrics:
  - textarea height: `58`
  - wrapper height: `58`
  - highlight layer height: `58`
  - selected mention value: `@טליה `
  - selected mention token color: `rgb(138, 180, 248)`

## Deployment

Deployed to the shared VM on 2026-07-17.

- Host: `151.145.93.180`
- Active UI directory: `/opt/serbia-poc-ui`
- Service: `serbia-poc-ui.service`
- Public review URL: `http://151.145.93.180/`

## Deployment verification

- Copied only `index.html`, `app.js`, and `styles.css` through a timestamped `/tmp/serbia-poc-ui-mobile-mentions-*` staging directory.
- Restarted `serbia-poc-ui.service`; it reported `active`.
- VM-local `/api/status` returned `mode=hermes`, `configured=true`, and `build=serbia-poc-1`.
- VM-local and public index both serve:
  - `styles.css?v=86`
  - `app.js?v=107`
- Public `styles.css?v=86` contains the textarea alignment fix and mobile menu max-height rule.
- Public `app.js?v=107` contains the mobile `preferAbove` menu placement logic.
- Public mobile browser smoke at 390 x 844 verified:
  - textarea height: `58`
  - wrapper height: `58`
  - highlight layer height: `58`
  - selected mention value: `@טליה `
  - selected mention token color: `rgb(138, 180, 248)`

## Review needed

Product/UX/QA should confirm on mobile:

1. Typing `@` opens the suggestion menu above the prompt.
2. The menu no longer covers the map/results area.
3. Selecting a member keeps the inserted mention blue.
4. The prompt field does not jump or gain extra height from the mention highlight layer.
