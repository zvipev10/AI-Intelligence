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

## Files affected

- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/assets/michlol/*.png`
- `.ai/work/capabilities/michlol-team-management/checkpoint-001.md`
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

- Slice 2: per-investigation team selection/persistence, only if Product requests it.
- Slice 3: real users or agent participants, only after identity/agent semantics are defined.

## Rollback

Remove the `michlol-team` markup, CSS rules, and local avatar assets. No data migration is involved.
