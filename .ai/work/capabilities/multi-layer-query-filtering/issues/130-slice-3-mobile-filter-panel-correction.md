# [Correction] Slice 3 mobile filter panel visibility

## Purpose
Fix the phone-width Slice 3 mobile issue found during VM review.

GitHub issue: #17

## Product request
Product requests Development fix the phone-width Slice 3 mobile issue before Slice 4 behavior wiring, unless Product explicitly waives phone-width mobile approval.

## Problem
On phone-width viewports, tapping the layer-tab filter button opens the filter panel in the DOM, but the panel is pushed below the visible bottom of the raw results overlay. Users may not see that anything happened.

## Owner role
Development.

## Inputs
- `mobile-audit-2026-07-08/report.md`
- `mobile-audit-2026-07-08/02-iphone-390x844-filter-open.png`
- `mobile-audit-2026-07-08/02-android-360x800-filter-open.png`
- `checkpoint-009.md`
- `checkpoint-010.md`

## Expected output
Development fix, checkpoint summary, and VM/mobile validation evidence.

## Blocking
Blocks mobile approval of Slice 3 and should be resolved before Slice 4 behavior wiring unless Product explicitly waives phone-width mobile approval.

## Acceptance criteria
- [ ] On 360px wide phone viewport, opening the filter panel makes it visible immediately within the current raw overlay view.
- [ ] On 390px wide phone viewport, opening the filter panel makes it visible immediately within the current raw overlay view.
- [ ] The panel preferably stacks above the table inside the visible overlay area on phone breakpoints.
- [ ] The table remains usable and horizontally scrollable.
- [ ] Filter, visibility, and close actions remain visually distinct and do not overlap.
- [ ] Existing tablet behavior remains acceptable at 768x1024.
- [ ] Existing transparency/readability treatment remains acceptable.
- [ ] No browser console errors or warnings during the tested flow.

## Suggested validation
- Test local or deployed build at 360x800, 390x844, and 768x1024.
- Flow: load app, open `טלגרם`, tap the active layer filter button, verify panel visibility and table usability.

## Parent capability
#3 / `000-parent-capability.md`

## Related issues
- #13 / `090-slice-3-filter-panel.md`
