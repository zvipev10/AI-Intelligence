# [Implementation] Slice 1 Correction - Remove Selector Section

## Purpose
Apply Product/UX feedback from Slice 1.

GitHub issue: #10

## Required action
Remove the visible selector wrapper/header/count and keep only a compact search/autocomplete line.

## Owner role
Development.

## Inputs
- `checkpoint-001.md`
- `developer-review.md`
- `ux-review.md`
- `status.md`

## Expected output
- Corrected UI implementation.
- `checkpoint-002.md` summarizing files changed, checks run, and Product/UX review request.

## Blocking
Slice 2 cannot start until this correction is implemented and reviewed.

## Completion criteria
- [ ] No visible "Data layers" section.
- [ ] No visible "Layer selection" section.
- [ ] No visible available-layer count block.
- [ ] Compact search/autocomplete remains available.
- [ ] API-backed layer opening still works.
- [ ] `checkpoint-002.md` created.

## Related artifacts
- `status.md`
- `ux-review.md`

## Parent capability
#3 / `000-parent-capability.md`
