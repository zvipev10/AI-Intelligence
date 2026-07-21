# [Child] Header Member Conversation Selection

## Parent

`000-parent-capability.md`

## Status

Deployed / Pending Product, UX, and QA review

## Request

Allow the analyst to select a `מכלול` member from the upper section so the conversation continues in that member context instead of the generic conversation mode.

## MVP behavior

- Header member chips are clickable.
- Selecting a member visually marks that member as active.
- Selecting a member appends a hardcoded welcome message from that member.
- Selecting the same member again does not append duplicate welcome messages.
- Switching members appends the newly selected member's welcome message.
- Prompt UI reflects the selected member context.
- Existing Hermes/backend execution remains unchanged until real member agents are implemented.

## Non-goals

- Real member agents.
- Backend routing.
- Persistence of selected member mode.
- Task records or notifications.

## Acceptance criteria

- [x] Visible header members can be selected by click.
- [x] Selected member has a clear active state.
- [x] Selected member has `aria-pressed=true`.
- [x] Selecting a member appends a hardcoded welcome message.
- [x] Re-clicking the selected member does not duplicate the welcome message.
- [x] Switching members appends the new member's welcome message.
- [x] Existing prompt submission behavior remains routed through the current Hermes flow.
- [ ] Product/UX/QA review on the deployed VM.

## Checkpoint

`../checkpoint-010.md`
