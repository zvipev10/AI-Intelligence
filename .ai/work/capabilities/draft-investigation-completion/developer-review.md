# Developer Review

## Review status

Draft — pending human checkpoint

## Reviewer / input source

AI-prepared from the user request and current `main` implementation.

## Feasibility

High. The current app already has draft creation, an in-document workspace, local/remote investigation registration, fake welcome actions, member data, and separate layer/result memory-save functions.

## Likely affected files/services

- `index.html`: draft header action and creation modal.
- `styles.css`: compact modal, participant chips, draft header state.
- `app.js`: explicit draft flag, modal lifecycle, conversion, pending save continuation, localization.
- UI contract tests and canonical deployment manifest.
- Existing `/api/investigations` only; no new backend endpoint.

## Recommended approach

Store explicit `is_draft` on local investigation records instead of inferring from a translated name. Preserve the draft ID during conversion, register the renamed record, clear `is_draft`, and render normal controls. Hold at most one pending memory action `{kind, payload, button}` and consume it once after successful creation.

## Technical risks

- Existing registry serialization/hydration must preserve the draft flag locally without treating older records as drafts.
- Remote registration may fail; the modal must remain open with an error and must not run the pending save.
- Button state must be restored on cancel/failure.

## Data/API considerations

No API schema change is required if draft status remains a UI lifecycle property and creation reuses the active ID with the entered final name.

## Test strategy

- Contract tests for new markup and explicit draft state.
- Unit/contract assertions for each modal trigger and single-use continuation.
- Existing full suite plus browser geometry and interaction checks.

## Proposed execution slices

1. Draft-mode header and modal conversion.
2. Layer/result memory-save interception and continuation.
3. Full regression, browser verification, and deployment artifacts.

## Blocking questions before execution planning

Approve the two choices in the capability brief.
