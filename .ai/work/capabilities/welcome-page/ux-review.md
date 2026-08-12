# UX Review

## Status

Ready for planning — product decisions approved by the user.

## Flow

Refresh opens the welcome page. Users review their investigation ribbon, invoke participant actions without navigation, or activate the ribbon to enter the workspace in the same document. Activating the app name returns to welcome. Similar-investigation actions show a demo-only confirmation.

## Interaction rules

- The ribbon is keyboard focusable and activates on Enter/Space.
- Nested buttons stop ribbon activation.
- Status is conveyed by text and icon/color.
- Real and similar sections are visually distinct.
- The existing language switch updates page direction and every welcome string immediately.

## Responsive behavior

Desktop uses wide ribbons with metadata columns. Narrow layouts stack content and keep actions at least 44px tall. RTL/LTR order follows the active document direction.

## Accessibility

Use section headings, meaningful `aria-label` values, visible focus rings, progress semantics, dialog labeling, and no nested interactive elements.

## Approved copy behavior

Mock actions explicitly include “Demo”/“הדגמה” in the resulting dialog so users do not infer persistence.
