# Capability Brief

## Capability
Chat sticky-bottom scrolling (`chat-sticky-scroll`)

## Goal
Show new chat content automatically while the reader remains near the bottom, preserve the reader's position after an explicit upward scroll, and always follow a newly submitted user message.

## Accepted Behavior
- New user messages always scroll the conversation to the bottom.
- Assistant messages and live progress follow the bottom only when the conversation was within 96 pixels of it immediately before the update.
- Readers positioned farther from the bottom remain at their current reading position.
- Bulk live-step rerenders use one pre-update scroll decision.

## Non-goals
- A “new messages” badge.
- Persisting scroll position across reloads or investigation changes.
- Changing message rendering or chat history.

## Acceptance Criteria
- User submission forces the newest message into view.
- Incoming assistant content follows when near the bottom.
- Incoming assistant content does not pull the reader down after they scroll upward.
- Live-step list replacement does not accidentally re-enable following.
