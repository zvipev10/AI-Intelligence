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
Development fix, checkpoint summary, and VM/mobile validation evidence for the floating filter window.

## Blocking
Blocks mobile approval of Slice 3 and should be resolved before Slice 4 behavior wiring unless Product explicitly waives phone-width mobile approval.

## Acceptance criteria
- [ ] Opening the filter button shows a floating filter window above the results tabs/table, on top of the active map or timeline surface.
- [ ] The filter window is detached from the raw results table layout.
- [ ] On 360px wide phone viewport, opening the filter window makes it visible immediately without relying on the user scrolling the raw results overlay.
- [ ] On 390px wide phone viewport, opening the filter window makes it visible immediately without relying on the user scrolling the raw results overlay.
- [ ] On tablet and desktop widths, the floating window remains readable and does not obscure the layer selector, map controls, timeline header, results tab actions, or window controls in a confusing way.
- [ ] The filter window has a clear close/dismiss action.
- [ ] The table remains usable and horizontally scrollable.
- [ ] Filter, visibility, and close actions remain visually distinct and do not overlap.
- [ ] Existing tablet behavior remains acceptable at 768x1024.
- [ ] Existing transparency/readability treatment remains acceptable.
- [ ] No browser console errors or warnings during the tested flow.

## Suggested validation
- Test local or deployed build at 360x800, 390x844, and 768x1024.
- Test both map and timeline views when possible.
- Flow: load app, open `טלגרם`, tap the active layer filter button, verify the floating filter window appears above the results tabs on top of the active visual surface, and verify table usability remains intact.

## Parent capability
#3 / `000-parent-capability.md`

## Related issues
- #13 / `090-slice-3-filter-panel.md`
