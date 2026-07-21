# Execution Plan - מכלול Team Management

## Prerequisite review gate

| Review | Status | Artifact |
|---|---|---|
| Product | Approved | `product-review.md` |
| Development | Approved | `developer-review.md` |
| UX | Approved | `ux-review.md` |
| QA | Approved | `qa-review.md` |

## Implementation approach

Implement Slice 1 as a static read-only UI capability:

- Generate and commit five local PNG avatar assets.
- Add a compact `מכלול` list beside the active investigation combo.
- Keep member identity model future-compatible through stable ids and `member_type=user` in markup attributes.
- Avoid backend, auth, persistence, or agent behavior.

Implement the approved `@member` autocomplete extension as a separate Slice 2:

- Move the predefined `מכלול` member catalog into a shared frontend data structure.
- Render the existing compact header strip from that shared catalog.
- Add reusable `@` autocomplete behavior to every investigation prompt-entry surface, currently the main prompt and step-continuation prompt.
- Support multiple mentions in one prompt.
- Keep selected mention metadata transient/client-side only.
- Do not send structured `team_mentions` to the backend.
- Add the approved always-on Hermes instruction so teammate mentions are ignored as investigation entities for now.

## Files affected

- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/assets/michlol/*.png`
- `.ai/work/capabilities/michlol-team-management/checkpoint-001.md`
- `.ai/work/capabilities/michlol-team-management/checkpoint-005.md`
- `.ai/work/capabilities/michlol-team-management/status.md`

## Slice 1

Static team list and generated avatars.

Expected changes:

- Header renders `מכלול` member strip near the investigation combo.
- Five predefined users are visible.
- Each member has a generated picture.
- Avatar fallback initials exist.
- Existing investigation combo behavior remains unchanged.

Risk level: low to medium, mostly header layout.

Reviewer role after slice: Product/UX/QA.

## Deferred slices

- Slice 2: `@member` autocomplete for prompt-only team addressing.
- Later slice: per-investigation team selection/persistence, only if Product requests it.
- Later slice: real users or agent participants, only after identity/agent semantics are defined.

## Slice 2

Prompt-only `@member` autocomplete.

Expected changes:

- Shared member catalog powers both the header strip and autocomplete suggestions.
- Main prompt and step-continuation prompt open a compact picker when typing `@`.
- Picker filters all five predefined members by name and role.
- Arrow Up/Down moves selection, Enter or Tab inserts, Escape closes.
- Picker hides when no members match.
- Selected member inserts readable text such as `@משה`.
- Multiple mentions in the same prompt work independently.
- Hermes receives a general instruction to ignore teammate mentions as investigation entities.
- Existing `/api/investigate` payload shape remains unchanged.

Risk level: medium, because this touches prompt keyboard handling and prompt construction.

Reviewer role after slice: Product/UX/QA.

QA focus:

- RTL Hebrew typing around `@`.
- Keyboard and pointer selection.
- Filtering by display name and role.
- No-match behavior.
- Main prompt submit behavior.
- Step-continuation prompt submit behavior.
- Selected-layer prompt context regression.
- Existing compact header and teammate expander regression.

## Rollback

Slice 1 rollback: remove the `michlol-team` markup, CSS rules, and local avatar assets. No data migration is involved.

Slice 2 rollback: remove the mention menu markup/CSS/JS, restore static header markup if needed, and remove the Hermes ignore instruction from prompt construction. No backend migration is involved.
