# Handoff Summary — Chat panel collapse

## Outcome
Desktop analysts can minimize the chat from a compact divider control and restore it from the same location.

## Behavior
- Conversation state and prior width are preserved.
- Results and map receive the released space.
- MapLibre resizes after the transition.
- Divider dragging is unchanged while expanded and disabled while collapsed.
- Mobile layout remains unchanged.

## Validation
70 focused tests passed and visual QA passed at 2000 × 1200.

## Risks
No known release-blocking risks. Native keyboard semantics are present; a manual screen-reader check remains optional follow-up polish.

## Publishing
Code and artifacts are intended for the active shared branch.
