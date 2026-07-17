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
- The MVP data is static/predefined, not managed by authentication or user administration.
- The model should leave room for future member types, especially `agent`.

## MVP scope

- Define a predefined team member catalog.
- Present team members in the investigation UI.
- Use each member picture and name.
- Keep the UI read-only for the first slice unless Product explicitly asks for assignment/editing behavior.
- Preserve compatibility with future real users and future agent participants.

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
- The MVP uses a predefined member list.
- Every predefined member has a name and picture.
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
- If generated or placeholder pictures are used, licensing and consistency should be explicit.
- The feature should remain independent from the investigation-memory storage model until Product defines what, if anything, should be persisted per investigation.

## UX notes

- `מכלול` should feel like a workspace/team affordance, not a marketing panel.
- Use compact presentation compatible with the current investigation UI.
- Avatar/name treatment should support scanability and future status/role metadata.
- Avoid creating a separate landing page or modal-heavy flow for the MVP.

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

1. Where should `מכלול` appear in the UI: header, side panel, investigation selector area, or a dedicated workspace panel?
2. Should members be global predefined users, or should each investigation have a selected subset?
3. Does MVP require choosing/assigning members to an investigation, or only displaying the predefined team?
4. What predefined users should ship in the first version: names, pictures, and count?
5. Should the initial model include roles such as lead analyst, OSINT, GEOINT, reviewer, or commander?
6. Should future agents appear visually different from human users from day one?
7. Should the capability persist selected team state server-side per investigation, or stay static/read-only for the first slice?

## Missing inputs

- Initial predefined user list.
- Picture source/asset direction for each predefined user.
- Desired UI placement.
- Whether MVP is read-only or includes selecting team members per investigation.
- Any required role labels or team hierarchy.

## Required reviewers

- Product: define exact `מכלול` semantics, MVP behavior, and predefined users.
- UX: define placement, compact member presentation, avatar fallback, mobile behavior.
- Development: review data shape, asset strategy, and integration point.
- QA: validate edge cases and regression surface.
- Architecture/Security: light review if the MVP stores team state or anticipates real users/agents.

## Required child issues

- [ ] Product review
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
