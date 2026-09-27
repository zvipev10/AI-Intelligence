# Capability Brief

## Capability name

Annotated investigation memory

## Capability slug

`investigation-memory-annotations`

## Parent issue

Draft local issue body: `issues/parent-capability.md` (remote issue not created).

## Current status

Draft — pending product, UX, developer, and QA review. See `status.md`.

## User problem

An analyst can currently save a chat result or a layer to investigation memory, but cannot explain why it matters. They also cannot retain one specific table/viewer object or a hand-drawn geographic area as a reusable investigation-memory item.

## Business goal

Let analysts capture an explicit, analyst-authored rationale alongside the exact evidence, result, or area that should remain in investigation context.

## Target users

Assessment officers and the SIGINT/VISINT specialists working inside saved investigations.

## Proposed behavior

1. Every existing **Save to memory** action for a chat result or layer opens one shared, optional-comment dialog before saving.
2. A table row and an open object viewer expose **Save to memory**. They save one immutable object reference/snapshot with the same optional comment.
3. A completed drawn polygon is selectable on the map. Selecting it opens a small action surface with **Save to memory**, which opens the same comment dialog.
4. Saved comments are persisted with their memory item and included in the bounded context provided to the investigation agent.

## MVP scope

- Saved investigations only; no welcome-page or draft persistence.
- Optional plain-text comments, normalized and length-bounded server-side.
- Additive `memory.artifacts` entries for object and polygon saves; preserve existing `chat_summaries` and `layers` data unchanged.
- Record enough immutable object identity/provenance and polygon geometry to show the saved item later, without inferring new evidence or target/assessment status.
- Support bilingual labels, keyboard operation, error states, and already-saved feedback.

## Non-goals

- Editing/deleting saved comments or memory items.
- Server-side authorization changes.
- Converting a polygon into a search filter, target, evidence object, or assessment.
- Changing underlying source records or agent-generated conclusions.
- Saving unfinished polygons.

## Acceptance criteria

- [ ] Saving a layer or chat result allows an optional comment; both item and comment persist atomically.
- [ ] A single table row can be saved with an optional comment.
- [ ] The same single object can be saved from its viewer with an optional comment.
- [ ] A completed polygon is selectable and can be saved with an optional comment.
- [ ] Saved object/polygon entries retain stable identity/provenance or geometry, saved time, and analyst comment.
- [ ] Existing saved chat/layer items restore without migration failure.
- [ ] Comments are included in bounded investigation-agent memory context.
- [ ] The flows are unavailable while no saved investigation is active; failures do not mark an item as saved.
- [ ] Hebrew and English labels/directionality are correct.

## Edge cases

- Empty comment means save without a comment.
- Comment over the approved bound is rejected visibly without discarding the source item.
- A record/object no longer available in the active dataset remains context-only, not silently remapped.
- Polygon selection must not interfere with active drawing, map markers, or map navigation.
- Duplicate saves are treated consistently by item type and do not make a false success claim.

## Technical constraints

- Preserve `schema_version: 1` compatibility and existing atomic investigation-memory writes.
- Browser and server validate bounded text/geometry; do not trust client payloads.
- The current restore path understands layers only; artifacts need an explicit non-destructive presentation contract.
- The UI release must include `app.js`, `index.html`, `demo_bootstrap.js`, and `polygon_draw.js` only if each changes, with cache versions advanced as applicable.

## UX notes

Use one reusable dialog titled **Add to memory**. It identifies what will be saved, makes the comment optional, provides Save/Cancel, and returns focus to the original trigger. The polygon selection action is small and map-local; comment entry stays in the shared dialog.

## QA notes

Add server validation/persistence tests, client source/behavior regression tests, and manual bilingual desktop/mobile checks for each entry point, cancellation, timeout, duplicate, unavailable-object, and map-drawing interaction.

## Risks

- New persisted payload shapes could cause agent-context growth or restore regressions.
- Map click handling can conflict with drawing and existing result markers.
- Object types have different stable identifiers; a generic capture contract must fail closed when one is absent.

## Open questions

- Should a saved comment be shown to the analyst in a dedicated memory browser in this MVP, or only carried forward to the agent/context? Proposed: persist it now; defer a memory browser unless the existing UI has a suitable surface.
- Should duplicate object/polygon saves be blocked or allowed as separate analyst annotations? Proposed: allow separate entries because comments may represent distinct analytic rationale.

## Missing inputs

Product confirmation of the proposed MVP and the two open questions above.

## Required reviewers

- Product owner
- Developer
- UX
- QA

## Required child issues

- [ ] Product review
- [ ] Developer review
- [ ] UX review
- [ ] QA review
- [ ] Execution planning

## Proposed execution checkpoints

1. Approve item/comment persistence contract and reusable dialog flow.
2. Implement and test comments for existing chat/layer saves.
3. Implement and test table/viewer object saves.
4. Implement and test polygon selection/save.
5. Run bilingual regression, deploy, and complete handoff.

