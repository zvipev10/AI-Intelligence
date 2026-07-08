# Mobile Audit - Slice 3 VM Deployment

## Date
2026-07-08

## Scope
Review the deployed Slice 3 VM build at mobile and tablet viewport sizes.

Review URL:
`http://151.145.93.180/`

Build verified:
- `styles.css?v=64`
- `app.js?v=82`

## Flow Tested
1. Load deployed VM UI.
2. Search for `טלגרם` in the layer selector.
3. Open the Telegram layer.
4. Open the Slice 3 filter panel from the active layer tab.

## Screenshots
- `01-iphone-390x844-layer-open.png`
- `02-iphone-390x844-filter-open.png`
- `01-android-360x800-layer-open.png`
- `02-android-360x800-filter-open.png`
- `01-tablet-768x1024-layer-open.png`
- `02-tablet-768x1024-filter-open.png`

## Results By Viewport

### 390 x 844
General health: Needs fix before approving mobile Slice 3 behavior.

Findings:
- Telegram layer opens and the table renders 1,280 rows.
- Filter, visibility, and close actions are separate and do not overlap.
- The filter panel opens in DOM, but appears below the visible bottom of the overlay.
- The table remains horizontally scrollable.
- No browser console errors or warnings were captured.

### 360 x 800
General health: Needs fix before approving mobile Slice 3 behavior.

Findings:
- Telegram layer opens and the table renders 1,280 rows.
- Filter, visibility, and close actions are separate and do not overlap.
- The filter panel opens in DOM, but appears below the visible bottom of the overlay.
- The table remains horizontally scrollable.
- No browser console errors or warnings were captured.

### 768 x 1024
General health: Acceptable for Slice 3 review.

Findings:
- Telegram layer opens and the table renders 1,280 rows.
- Filter, visibility, and close actions are separate and do not overlap.
- The filter panel is visible beside the table.
- The panel shows the active layer name, raw field selector preview, empty draft and active states, and disabled placeholder controls.
- No browser console errors or warnings were captured.

## UX Risks
- On phone widths, tapping the filter button does not create a visible result in the current viewport. Users may think the button failed.
- The phone layout already requires scrolling from the chat area to the map/result area, so the filter panel should be extra obvious once opened.
- The raw overlay is very constrained on phone widths, making the filter panel/table stacking behavior fragile.

## Accessibility Risks
- On phone widths, the state change is not perceivable from the current viewport when the panel opens below the visible overlay area.
- The filter, visibility, and close targets are visually distinct, but their 18px rendered action boxes are smaller than common mobile touch target guidance.
- Screenshot review cannot confirm keyboard focus order or screen reader announcement quality.

## Recommendation
Request changes before mobile approval of Slice 3.

Minimum fix:
- On phone-width breakpoints, make the filter panel visible immediately when opened, preferably above the table inside the visible overlay area.
- Consider increasing the visible tap target area for the filter, visibility, and close controls without changing their visual meaning.

Tablet view can continue through review, but phone view should be corrected before Slice 4 behavior wiring.
