# QA Review

## Capability
Minimize and restore the chat panel

## Review status
Approved by explicit user delegation (“Go on”).

## Acceptance criteria review
The criteria are observable through DOM state, computed layout, accessible attributes, and browser interaction.

## Happy path tests
- Collapse hides the chat and expands results.
- Restore returns the chat and prior layout.
- The button label and icon change with state.

## Edge cases
- Divider drag remains available only while expanded.
- Map receives resize after each transition.
- Mobile breakpoint hides the divider and control.

## Regression areas
Desktop grid proportions, MapLibre rendering, results table overlay, chat composer, and divider resizing.

## QA recommendation
Proceed with automated regression checks and desktop browser verification.
