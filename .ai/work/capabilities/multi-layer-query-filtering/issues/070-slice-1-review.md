# [Review] Slice 1 Correction

## Purpose
Review the corrected selector and decide whether Slice 2 may start.

GitHub issue: #11

## Required action
Development implemented Product's UX comments from review of `checkpoint-002.md`; Product, UX, and Development should now review `checkpoint-003.md`.

## Owner role
Product, UX, and Development.

## Inputs
- `checkpoint-002.md`.
- Corrected UI.
- `status.md`

## Expected output
Review result for `checkpoint-003.md`: approval to continue to Slice 2 or requested changes.

## Blocking
Slice 2 remains blocked until this review is complete.

## Product review result
Product reviewed `checkpoint-002.md` and said the correction looks good, with these UX comments to implement:
- Make the new selector bar smaller, almost half the current width.
- Make the selector and all other map-top components transparent.
- Make the results table slightly transparent in the same visual direction.

## Development update
Implemented in `checkpoint-003.md`:
- Selector width reduced from 360px to 190px on desktop.
- Selector, autocomplete list, MapLibre top-left controls, raw overlay, and raw table use the same `rgba(15, 19, 27, .78)` translucent surface.
- Browser smoke confirmed selecting `טלגרם` still opens the raw table with 1,280 rows.

Follow-up correction implemented in `checkpoint-004.md`:
- Results overlay top chrome is compact again: 6px resize row plus 34px header row.
- Table body and cells are transparent instead of applying another translucent surface over the overlay.
- Sticky table headers use a lighter `rgba(15, 19, 27, .54)` background for readability without making the table look opaque.

## Completion criteria
- [x] Selector width reduced per Product comment.
- [x] Selector and map-top components made transparent/translucent.
- [x] Results table made slightly transparent while preserving readability.
- [ ] Product approves corrected selector and transparency treatment.
- [ ] UX approves corrected selector placement and transparency treatment.
- [x] Development confirms no API/catalog regression.
- [ ] `status.md` updated for Slice 2.

## Related artifacts
- `checkpoint-002.md`
- `checkpoint-003.md`
- `checkpoint-004.md`
- `status.md`

## Parent capability
#3 / `000-parent-capability.md`
