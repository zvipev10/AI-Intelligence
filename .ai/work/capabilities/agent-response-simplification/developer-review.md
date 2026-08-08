# Developer Review — Collapsed research steps

## Review status

Approved by explicit user delegation on 2026-08-08.

## Feasibility

The existing `addActivity` renderer already groups each tool execution into one activity item. A native `details`/`summary` disclosure can preserve the current content and event handlers while changing only its default visibility.

## Affected files

- Bilingual WIP `app.js`
- Bilingual WIP `styles.css`
- Bilingual WIP `index.html` for cache versions
- Focused UI regression test

## Risks

- Nested action buttons must remain outside the summary click target.
- Dynamic/live and recorded steps must use the same renderer.
- Keyboard focus and expanded state must be visible.

## Recommendation

Use native `details`/`summary`; show only the step number and localized user-facing tool title in the summary. Preserve the existing metadata, rationale, input, result, and actions inside the expanded body.
