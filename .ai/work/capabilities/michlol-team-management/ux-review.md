# UX Review - מכלול Team Management

## Review status

Approved for Slice 1 implementation.

## Reviewer/source of input

AI UX review based on Product-approved placement near the investigation-name combo and current header layout.

## Recommended UI

Place a compact `מכלול` strip directly below the investigation-name combo inside the existing center header area.

This keeps the team concept visually attached to the active investigation without adding a modal, side panel, or new navigation.

## Member presentation

- Show label `מכלול`.
- Show each member as a compact chip with:
  - circular avatar
  - first name
  - tooltip/title containing full name plus role
- Keep role labels out of the always-visible row to preserve compactness.
- Use generated portraits, but avoid rank symbols, national symbols, badges, or weapons.

## Empty and error states

- MVP is predefined and should not be empty in production.
- If an image fails, show the member initial inside the same avatar circle.

## Responsive behavior

- Desktop: one compact row under the combo.
- Tablet: allow chips to wrap within the switcher width.
- Mobile: stack below the combo and allow horizontal/line wrapping without overlapping header status.

## Accessibility

- The strip should be a list with an accessible label.
- Each member chip should expose the name and role through text/title/ARIA label.
- Images should be decorative if the surrounding member label provides the identity.

## UX risks

- Too much text near the combo can crowd the header, so visible copy should stay short.
- Future agents should eventually get a clear but subtle visual distinction; this is not needed for Slice 1 because all MVP members are humans.
