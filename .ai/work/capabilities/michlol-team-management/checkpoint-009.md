# Checkpoint 009 - Mobile Mention Popup and Caret Alignment Fix

## Date

2026-07-17

## Request

Fix two remaining mobile visual bugs from Product/Developer review:

1. When filtering leaves only one `@member` suggestion, the autocomplete popup is not in the right place.
2. After selecting a member and continuing to type, the caret is not aligned with the visible text.

## Evidence

User-provided screenshots showed:

- A one-result `@טליה` suggestion popup overlapping the prompt field.
- A selected `@טליה` mention followed by Hebrew text where the native caret did not align with the rendered highlighted text.

Additional local verification screenshots:

- `audit-mobile-mention-20260717/10-local-field-outside-one-result.png`
- `audit-mobile-mention-20260717/11-local-field-outside-selected-text.png`
- `audit-mobile-mention-20260717/12-public-field-outside-one-result.png`
- `audit-mobile-mention-20260717/13-public-selected-text-caret-alignment.png`

## Root cause

- The popup was positioned from the textarea rectangle, not from the active mention/caret context, and the mobile fallback still allowed it to overlap the prompt field.
- The visible blue mention was rendered in a separate highlight layer with a heavier font weight than the transparent textarea text. The browser placed the native caret using textarea text metrics, while the visible text used different metrics.

## Implementation

- Added caret measurement for textarea prompts using a temporary mirror element.
- The autocomplete popup now uses caret position for horizontal alignment.
- On mobile, popup vertical placement is kept outside the prompt field and prefers the space above the prompt when available.
- The blue mention token now inherits the same font weight as the textarea text, preserving text/caret alignment.
- Bumped review cache keys:
  - `styles.css?v=87`
  - `app.js?v=108`

## Validation

- `git diff --check`
- Local mobile browser QA at 390 x 844.
- Verified local patched metrics:
  - one-result popup does not overlap the prompt field
  - selected mention value: `@טליה מה נשמע`
  - selected mention token color: `rgb(138, 180, 248)`
  - selected mention token font weight: `400`
  - textarea font weight: `400`

## Deployment

Deployed to the shared VM on 2026-07-17.

- Host: `151.145.93.180`
- Active UI directory: `/opt/serbia-poc-ui`
- Service: `serbia-poc-ui.service`
- Public review URL: `http://151.145.93.180/`

## Deployment verification

- Copied only `index.html`, `app.js`, and `styles.css` through a timestamped `/tmp/serbia-poc-ui-mobile-caret-*` staging directory.
- Restarted `serbia-poc-ui.service`; it reported `active`.
- VM-local `/api/status` returned `mode=hermes`, `configured=true`, and `build=serbia-poc-1`.
- VM-local and public index both serve:
  - `styles.css?v=87`
  - `app.js?v=108`
- Public `styles.css?v=87` contains `.mention-highlight-token { color: var(--blue); font-weight: inherit; }`.
- Public `app.js?v=108` contains `textareaCaretViewportRect`.
- Public mobile browser smoke at 390 x 844 verified:
  - one-result popup does not overlap the prompt field
  - selected mention value: `@טליה מה נשמע`
  - selected mention token color: `rgb(138, 180, 248)`
  - selected mention token font weight: `400`
  - textarea font weight: `400`

## Review needed

Product/UX/QA should confirm on mobile:

1. Typing `@טליה` shows a single suggestion outside the prompt field.
2. The single-result popup is horizontally aligned with the active mention area.
3. Selecting `@טליה` and typing Hebrew text keeps the caret aligned with the visible text.
4. The mention stays blue and prompt submission behavior is unchanged.
