# [Correction] Slice 3 mobile filter panel visibility

## Purpose
Change the Slice 3 filter panel correction request so the filter section opens as a floating window above the results tabs, on top of the active map or timeline.

GitHub issue: #17

## Product request
Product changed the request after reviewing the mobile issue. The filter section should not be fixed by stacking it inside the results overlay. Instead, Development should make the filter section open as a floating window above the results tabs, on top of the map or timeline surface.

## Problem
On phone-width viewports, tapping the layer-tab filter button opens the filter panel in the DOM, but the panel is pushed below the visible bottom of the raw results overlay. Users may not see that anything happened.

Updated Product direction:
- The filter section should be detached from the raw results table layout.
- It should open as a floating window over the active visual surface: map when map is active, timeline when timeline is active.
- It should appear above the results tab/table area so opening filters is immediately visible.

## Owner role
Development.

## Inputs
- `mobile-audit-2026-07-08/report.md`
- `mobile-audit-2026-07-08/02-iphone-390x844-filter-open.png`
- `mobile-audit-2026-07-08/02-android-360x800-filter-open.png`
- `checkpoint-009.md`
- `checkpoint-010.md`

## Expected output
Development fix, checkpoint summary, and VM/mobile validation evidence for the floating filter window. Implemented in `checkpoint-011.md`.

## Blocking
Blocks Slice 4 until Product/UX/Development review `checkpoint-011.md`, unless Product explicitly waives review.

## Development update
Implemented in `checkpoint-011.md`:
- `#layerFilterPanel` is detached from the raw results table layout and rendered as a sibling of `#rawEventsOverlay` under `.view-stack`.
- The filter section opens as an absolute floating window above the results tabs/table.
- The floating window stays over the active map or timeline surface.
- Mobile map and timeline validation passed at phone widths.
- Deployed to the VM with `app.js?v=83` and `styles.css?v=65`.

## Acceptance criteria
- [x] Opening the filter button shows a floating filter window above the results tabs/table, on top of the active map or timeline surface.
- [x] The filter window is detached from the raw results table layout.
- [x] On 360px wide phone viewport, opening the filter window makes it visible immediately without relying on the user scrolling the raw results overlay.
- [x] On 390px wide phone viewport, opening the filter window makes it visible immediately without relying on the user scrolling the raw results overlay.
- [x] On tablet and desktop widths, the floating window remains readable and does not obscure the layer selector, map controls, timeline header, results tab actions, or window controls in a confusing way.
- [x] The filter window has a clear close/dismiss action.
- [x] The table remains usable and horizontally scrollable.
- [x] Filter, visibility, and close actions remain visually distinct and do not overlap.
- [x] Existing tablet behavior remains acceptable at 768x1024.
- [x] Existing transparency/readability treatment remains acceptable.
- [x] No browser console errors or warnings during the tested flow.
- [ ] Product/UX/Development approve corrected Slice 3 behavior.

## Suggested validation
- Test local or deployed build at 360x800, 390x844, and 768x1024.
- Test both map and timeline views when possible.
- Flow: load app, open `טלגרם`, tap the active layer filter button, verify the floating filter window appears above the results tabs on top of the active visual surface, and verify table usability remains intact.

## Parent capability
#3 / `000-parent-capability.md`

## Related issues
- #13 / `090-slice-3-filter-panel.md`
