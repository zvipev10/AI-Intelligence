# Developer Review

## Status

Ready for planning based on the user's explicit implementation direction.

## Recommended approach

- Extend saved-question JSON with backward-compatible `recording_type` and a
  structured `workstream_message` payload.
- Keep the existing endpoints, allowing either the legacy `question/result`
  shape or the new typed workstream shape.
- Extract shared structured renderers for creation-confirmation and detail cards.
- Add the existing save-control states to both live card render paths.
- Replay through the structured renderer; never persist or trust raw HTML.

## Affected files

`server.py`, `app.js`, and focused saved-question/workstream UI tests.

## Risks

Backward compatibility, stored-content sanitization, accidentally retaining live
mutation actions during replay, and localized production drift.

## Proposed slices

1. Typed persistence/API validation and tests.
2. Shared renderer, save controls, and read-only replay.
3. Full regression and localized deployment adaptation.
