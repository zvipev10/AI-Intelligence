# Capability Brief

## Capability name

מכלול - investigation team management

## Capability slug

michlol-team-management

## Parent issue

Local draft: `issues/000-parent-capability.md`

## Current status

See `status.md` for operational owner, blockers, and next action.

## User problem

An investigation is not always a solo analyst activity. The analyst needs a visible team context for the investigation: who is part of the working group, who can later contribute, and which people or agents belong to the investigation workflow.

## Business goal

Introduce the first foundation for team-based investigation work without coupling the MVP to authentication, authorization, real multi-user collaboration, or agent orchestration.

## Target users

- Primary analyst working inside an investigation.
- Future human collaborators assigned to the same investigation.
- Future AI agents that may participate as team members.

## Proposed behavior

The product introduces a concept called `מכלול`: a team/workgroup associated with investigation work.

For the MVP:

- The app exposes a predefined set of team members.
- Each team member has at least:
  - stable id
  - display name
  - picture/avatar
  - type, initially `user`
- The team members are visible in the investigation workspace using the existing UI language and density.
- The team list is displayed compactly near the investigation-name combo.
- The MVP data is static/predefined, not managed by authentication or user administration.
- The model should leave room for future member types, especially `agent`.

## MVP scope

- Define a predefined team member catalog.
- Present team members in the investigation UI.
- Use each member picture and name.
- Generate one picture/avatar asset for each predefined member.
- Display the predefined team as a compact read-only list near the investigation-name combo.
- Preserve compatibility with future real users and future agent participants.

## Predefined MVP members

| Stable id | Display name | Role label | Member type | Picture |
|---|---|---|---|---|
| `moshe-targets-officer` | משה | קצין מטרות | `user` | Generate picture |
| `talia-tama-officer` | טליה | קצינת תמא | `user` | Generate picture |
| `naama-field-officer` | נעמה | קצינת שטח | `user` | Generate picture |
| `gadi-collection-officer` | גדי | קצין איסוף | `user` | Generate picture |
| `yahli-processing-officer` | יהלי | קצין עיבוד | `user` | Generate picture |

Implementation note: Product provided each member as name plus role phrase. The table separates the first token as display name and keeps the rest as role label.

## Non-goals

- User authentication.
- Role-based access control.
- Real-time multi-user collaboration.
- Invitations, presence, online/offline status, notifications, or chat between team members.
- Agent execution, agent assignment, or agent autonomy.
- CRUD management for users.
- Persisted organization/team administration.

## Acceptance criteria

- A `מכלול` concept is visible and understandable in the investigation workspace.
- The MVP uses the five predefined members listed above.
- Every predefined member has a name and picture.
- The list is displayed compactly near the investigation-name combo.
- The implementation does not require login or real user accounts.
- The data model can later support real users and agents without replacing the concept.
- The feature does not interfere with chat, investigation memory, layer tabs, map, timeline, or table behavior.

## Edge cases

- Missing or broken picture asset should degrade to a stable initials/avatar fallback.
- Long names should not break the header/sidebar layout.
- The predefined list may be empty in development or test mode; the UI should handle empty state quietly.
- Future duplicate display names should remain distinguishable by stable id.
- RTL Hebrew layout should remain coherent when names contain English or mixed text.

## Technical constraints

- Current implementation should prefer a small static local data source unless developer review finds an existing stronger pattern.
- Avoid adding authentication or server-side identity dependencies in the MVP.
- If pictures are local assets, they should be committed and cacheable with the existing UI deploy flow.
- Generated pictures should be stored as local assets, committed with the feature, and cacheable with the existing UI deploy flow.
- Picture generation should use a consistent style across all five members.
- The feature should remain independent from the investigation-memory storage model until Product defines what, if anything, should be persisted per investigation.

## Extension under definition: member task mentions

The next requested extension is the ability to ask/request work from specific team members by typing `@member-name` with autocomplete in the investigation prompt.

Draft definition: `member-task-mentions-brief.md`.

Recommended first slice:

- Autocomplete from the same predefined member catalog in every prompt-entry surface.
- Insert a readable `@שם` mention token into the prompt.
- Support multiple member mentions in one prompt.
- Preserve stable member ids client-side separately from display text for future routing.
- Do not create visible task records.
- Do not send structured `team_mentions` to the backend in Slice 1.
- Add a general temporary Hermes instruction so `@member` names are ignored as investigation entities and treated only as UI addressing annotations.

## UX notes

- `מכלול` should feel like a workspace/team affordance, not a marketing panel.
- Use compact presentation compatible with the current investigation UI.
- Avatar/name treatment should support scanability and the provided role labels.
- Avoid creating a separate landing page or modal-heavy flow for the MVP.
- The compact list should sit near the existing investigation-name combo without disturbing the combo behavior.

## QA notes

- Validate the member list renders in desktop and mobile layouts.
- Validate broken picture fallback.
- Validate long Hebrew and mixed Hebrew/English names.
- Validate no regression to chat, layer opening, filters, map/timeline/table presentation, and investigation selector.

## Risks

- Product semantics of `מכלול` may be broader than "team members"; the name may imply operational roles, shifts, responsibilities, or task ownership.
- Starting with static users is simple, but the data shape must not block real user/agent integration later.
- Pictures can create asset-management and design consistency questions even before real identity exists.

## Open questions

No blocking product clarifications remain for the original read-only team-list MVP.

Product clarifications for the `@member` task mention extension are tracked in `member-task-mentions-brief.md`.

Non-blocking UX/development details to close before implementation:

1. Generated picture style: realistic headshots, illustrated avatars, or neutral operational portraits.
2. Exact compact layout near the investigation-name combo: inline row, stacked mini-list, or avatar strip with names/tooltips.
3. Whether future agents should have a reserved visual distinction in the initial data shape, even though no agent appears in the MVP.

## Missing inputs

- Exact generated-picture visual style.
- Final UX treatment for compact list layout beside the investigation-name combo.

## Required reviewers

- Product: approved initial MVP definition on 2026-07-17.
- UX: define placement, compact member presentation, avatar fallback, mobile behavior.
- Development: review data shape, asset strategy, and integration point.
- QA: validate edge cases and regression surface.
- Architecture/Security: light review if the MVP stores team state or anticipates real users/agents.

## Required child issues

- [x] Product review
- [ ] Developer review
- [ ] UX review
- [ ] QA review
- [ ] Execution planning

## Proposed execution checkpoints

1. Capability definition and product/UX/development review.
2. Slice 1: static team member data model and read-only UI placement.
3. Slice 2: optional per-investigation team selection/persistence, only if approved.
4. Slice 3: polish, responsive validation, avatar fallback, and QA handoff.

## Handoff to developer

Questions for developer:
- What is the simplest static data shape that can later evolve to real users and agents?
- Where can the UI be added with the lowest regression risk?
- Should member pictures live as local assets, generated placeholders, or external URLs?
- If Product wants per-investigation selection, should it use the existing investigation memory/storage path or a separate investigation metadata endpoint?

Expected developer output:
- feasibility notes
- likely affected files/services
- implementation options
- recommended approach
- technical risks
- test strategy
- proposed execution slices
