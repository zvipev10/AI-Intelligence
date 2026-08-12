# Developer Review

## Status

Ready for planning — product decisions approved by the user.

## Feasibility and approach

Implement the welcome page as a sibling top-level view in the existing document. Keep the production initialization path intact so health, registry, memory, layers, and MapLibre continue loading. Hide the workspace and workspace-only header controls while welcome is active; reveal them in place after the real ribbon is activated and call `state.map.resize()`.

## Affected files

- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- UI regression tests under `llm_investigation_orchestrator_serbia_poc/`

## Existing patterns

Reuse `currentLocale`, `activeLocaleText`, `applyLocaleUi`, `currentMembers`, the investigation registry, system-status state, and existing avatar assets.

## Risks and mitigations

- Hidden map sizing: resize after reveal.
- Nested actions: use a focusable card container plus separate real buttons; stop propagation for actions.
- Localization drift: route all dynamic welcome copy through `activeLocaleText` and rerender on locale change.
- Mock persistence confusion: label demo dialogs and actions explicitly.

## Test strategy

Add contract tests for required DOM/hooks and use browser verification for initial state, bilingual switching, card entry, return navigation, modal actions, and responsive presentation.

## Recommended slices

1. Welcome shell, real ribbon, view switching, and return path.
2. Demo actions and similar investigations.
3. Responsive/accessibility polish and regression validation.
