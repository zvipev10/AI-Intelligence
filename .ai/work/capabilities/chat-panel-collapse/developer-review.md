# Developer Review

## Capability
Minimize and restore the chat panel

## Review status
Approved by explicit user delegation (“Go on”).

## Reviewer / input source
AI-prepared technical review, authorized by the user to continue implementation.

## Feasibility
The existing three-track CSS grid can collapse its chat track to zero while retaining a wider divider track for restoration. The chat DOM and its current state remain mounted.

## Likely affected files/services
- `index.html`
- `styles.css`
- `app.js`
- UI regression tests

## Existing patterns to follow
Use the existing Material Symbols font, CSS tokens, map resize hook, and divider pointer handling.

## Recommended approach
Add a native button inside the divider. Toggle a workspace class that overrides the grid tracks, preserve the current CSS width variables, suppress drag while collapsed, and resize MapLibre after the transition.

## Technical risks
- Button pointer events accidentally initiating divider drag.
- Restore control disappearing with the collapsed chat track.
- Map canvas retaining its old size.

## Test strategy
Static regression assertions plus browser verification of collapse, restore, focusable control, and mobile hiding.

## Required review gates before coding
Satisfied by the user’s explicit approval to continue.
