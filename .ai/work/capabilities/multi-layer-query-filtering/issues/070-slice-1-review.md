# [Review] Slice 1 Correction

## Purpose
Review the corrected selector and decide whether Slice 2 may start.

GitHub issue: #11

## Required action
Development implemented Product's UX comments from review of `checkpoint-002.md`; Product approved `checkpoint-005.md`; UX should now complete review before Slice 2 starts.

## Owner role
Product, UX, and Development.

## Inputs
- `checkpoint-005.md`.
- Corrected UI.
- `status.md`

## Expected output
UX review result for `checkpoint-005.md`: approval to continue to Slice 2 or requested changes.

## Blocking
Slice 2 remains blocked until this review is complete.

## Product approval
Product approved Slice 1 and the corrected `checkpoint-005.md` transparency treatment on 2026-07-08.

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

Second follow-up correction implemented in `checkpoint-005.md`:
- Shared transparent surfaces are lighter at `rgba(15, 19, 27, .58)`.
- Active tab and table headers now use `rgba(15, 19, 27, .24)` so they no longer read as black blocks.
- Table wrapper and cells remain fully transparent.
- Added subtle text shadow for readability on lighter translucent surfaces.

## Completion criteria
- [x] Selector width reduced per Product comment.
- [x] Selector and map-top components made transparent/translucent.
- [x] Results table made slightly transparent while preserving readability.
- [x] Product approves corrected selector and transparency treatment.
- [ ] UX approves corrected selector placement and transparency treatment.
- [x] Development confirms no API/catalog regression.
- [x] `status.md` updated after Product approval.
- [ ] `status.md` updated for Slice 2 after UX approval.

## Related artifacts
- `checkpoint-002.md`
- `checkpoint-003.md`
- `checkpoint-004.md`
- `checkpoint-005.md`
- `status.md`

## Parent capability
#3 / `000-parent-capability.md`
