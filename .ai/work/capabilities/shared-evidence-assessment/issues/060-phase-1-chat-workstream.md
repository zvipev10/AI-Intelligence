# Issue 32 — Phase 1 chat-based workstream UX

## Goal

Expose the persistent workstream foundation through the existing chat without adding a separate management surface.

## Acceptance criteria

- `מעקב` is available from the plus menu.
- Tracking mode requires exactly one explicit layer.
- The objective comes from the user's message.
- Derived details are previewed in chat and require confirmation.
- Creation uses the workstream API.
- A minimal active indicator returns status and actions to chat.
- Multiple active workstreams are selected through a chat message.
- Archive requires explicit confirmation.
- Existing Investigation Memory and ordinary chat behavior do not regress.

## Status

Implemented and accepted on `capability/workstream-chat`; closes with PR #33.

## Related

- Parent capability: #25
- Persistence foundation: #30 / PR #31
- Checkpoint: `../checkpoint-002.md`
