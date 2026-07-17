# Checkpoint 010 - Header Member Conversation Selection

## Date

2026-07-17

## Request

Allow selecting a `מכלול` member by clicking a member in the upper section. After selection, the conversation should continue with that member rather than in the general mode. For now, add a hardcoded welcome message from the selected member until real member agents are implemented.

## Implementation

- Header members are now clickable buttons.
- Clicking a member sets `state.activeConversationMemberId`.
- The active member receives a selected visual state and `aria-pressed=true`.
- The prompt placeholder changes from the general investigation prompt to `כתוב אל <member>...`.
- A hardcoded local welcome message is appended from the selected member.
- Clicking the already active member does not append duplicate welcome messages.
- Switching to a different member appends that member's welcome message.
- While a member is selected, subsequent assistant/research message labels use the selected member label instead of the generic `סוכן חקירה` label.
- Cache keys were bumped:
  - `styles.css?v=88`
  - `app.js?v=109`

## Non-goals

- No real member agent routing yet.
- No backend API or persistence change.
- No task records, notifications, permissions, or user identity behavior.
- Existing Hermes prompt flow remains the execution path until member agents are implemented.

## Validation

- `git diff --check`
- Local browser smoke on patched files:
  - selecting `טליה` marks her active
  - `aria-pressed=true` on the selected member
  - prompt placeholder changes to `כתוב אל טליה...`
  - one welcome message is appended
  - re-clicking `טליה` does not add a duplicate welcome
  - switching to `משה` marks משה active and appends a second welcome

## Review needed

Product/UX/QA should confirm:

1. Clicking a visible header member clearly selects that member.
2. Clicking a hidden member from the `...` menu also selects that member.
3. The welcome message copy is acceptable as a temporary hardcoded message.
4. The selected-member mode is clear enough until real member agents exist.
5. Existing `@member` autocomplete and mobile mention behavior are not regressed.
