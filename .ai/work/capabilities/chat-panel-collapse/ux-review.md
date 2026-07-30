# UX Review

## Capability
Minimize and restore the chat panel

## Review status
Approved by explicit user delegation (“Go on”).

## User flow
The analyst presses a compact button at the top of the divider. The chat collapses and the same button reverses direction to restore it.

## UI states
- Expanded: right-pointing chevron, tooltip `מזער שיחה`.
- Collapsed: left-pointing chevron, tooltip `הצג שיחה`.
- Mobile: control absent because panels are stacked.

## Accessibility notes
Use a native button with synchronized `title`, `aria-label`, `aria-expanded`, and `aria-controls`.

## UX edge cases
Keep the restore control visible, preserve prior width, and prevent the click from beginning a divider drag.

## Review recommendation
Approved for the focused implementation slice.
