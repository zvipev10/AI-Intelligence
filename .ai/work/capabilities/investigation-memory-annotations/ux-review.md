# UX Review

## Capability

Annotated investigation memory

## Related issue

`issues/parent-capability.md`

## Review status

Draft — pending human UX approval.

## User flow

1. In a saved investigation, the analyst chooses **Save to memory** from a chat result, layer, table row, open object viewer, or selected completed polygon.
2. One compact dialog identifies the item and offers an optional **Comment** textarea, Save, and Cancel.
3. On success, the originating action changes to Saved and focus returns there. On cancel/failure, no saved state is implied.
4. The analyst opens **Memory** from a workspace button. This is a separate screen, not a Map/Timeline/Table view.
5. Memory shows simple grouped entries: Chat, Layers, Objects, and Areas. Each entry displays title/identity, saved time, comment when present, and a compact factual summary. It is read-only in MVP.

## UI states

- Empty: “No items saved to this investigation yet.”
- Loading: existing memory loading state, with no stale empty claim.
- Saving: dialog Save disabled with progress copy.
- Failure: inline dialog error; keep the comment for retry.
- Saved: trigger uses a clear saved state; duplicates remain available for objects/polygons because the analyst may add distinct comments.
- Unavailable source: render saved entry with its original identity/comment and a visible “Source unavailable” status.

## Accessibility notes

- Dialog has title, description, labelled textarea, Escape/Cancel, focus trap/return, and keyboard Save.
- Buttons expose localized labels and status through `aria-live` as appropriate.
- Polygon selection must have a keyboard-equivalent action if its map interaction cannot be reached from keyboard; recommended MVP: also list completed unsaved polygons in the Memory button/menu action, or provide a map-local labelled button after completion.

## UX edge cases

- Do not show the Memory button on welcome/draft context; show it only for a saved investigation.
- Do not let a polygon click begin selection while drawing is active.
- Object viewer save must be visible without hiding source fields or media.
- The Memory screen must preserve the previous map/timeline/table context on close.

## Review recommendation

Approve the dedicated Memory screen and shared dialog concept, pending a decision on keyboard access for completed polygons and exact Memory-button placement.

