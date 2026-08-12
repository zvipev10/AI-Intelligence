# Capability Brief

## Capability name

Investigation welcome page

## Capability slug

`welcome-page`

## Parent issue

Not created remotely. Draft: `issues/parent-capability.md`.

## Current status

Draft — pending product, UX, development, and QA review. See `status.md`.

## User problem

The application opens directly inside one investigation and does not give users an overview of their investigations, collaborators, or related investigations they could join.

## Business goal

Provide an investigation-oriented entry point that helps users understand system health, resume existing work, manage participants, and discover similar investigations.

## Target users

Analysts and investigation participants using the Serbia/North Kosovo intelligence workspace.

## Proposed behavior

- The initial application view is a Hebrew RTL welcome page.
- Its header shows the existing app name, system health, and an `E / ע` language control.
- There is no "New investigation" action in this first implementation.
- "My investigations" presents large, clickable ribbons.
- The existing real investigation is represented using its current investigation record and existing Michlol team members.
- Attention state, pending invitations/requests, recent activity, progress, and next milestone appear inside each investigation ribbon rather than in separate page sections.
- An invite/add-participant action is available within each owned investigation ribbon and must not activate the ribbon behind it.
- Clicking the existing investigation ribbon replaces the welcome view with the existing investigation workspace on the same page, without opening a new page or tab.
- A separate "Similar investigations" section displays mocked investigation ribbons and mocked metadata.
- Mock similar-investigation participation actions are visibly distinct and do not imply that production data was changed.

## MVP scope

- Welcome/workspace view switching in the existing static frontend.
- One real "My investigations" ribbon based on the current active investigation and existing team.
- Mock metadata where the current application has no backing model: attention, invitations, activity, progress, milestones, and recommendations.
- Mock similar-investigation ribbons with join/request-to-join controls.
- Responsive RTL layout and keyboard-accessible ribbon activation.
- Preserve the existing investigation workspace behavior after entry.

## Non-goals

- Creating investigations.
- Persisting invitations, participant changes, or join requests to a backend.
- Implementing recommendation logic.
- Adding a new route or opening investigations in a new page.
- Replacing the existing investigation registry or team model.
- Building the English translation in this slice unless separately approved; the language control may be presentation-only for the mock.

## Acceptance criteria

- [ ] On initial load, the welcome view is shown instead of the investigation workspace.
- [ ] The header contains the current app name, health status, and `E / ע`; it contains no new-investigation action.
- [ ] The real investigation appears under "My investigations" and uses the current investigation name and existing Michlol members.
- [ ] Attention, invitation/request state, recent activity, progress, and next milestone are contained within the real investigation ribbon.
- [ ] The real ribbon exposes an invite/add-participant control.
- [ ] Activating the real ribbon by pointer or keyboard opens the existing workspace in the same document.
- [ ] Activating an action within a ribbon does not also open the investigation.
- [ ] Similar mocked investigations appear in a visually separate section with join or request-to-join controls.
- [ ] Mock actions clearly communicate their non-persistent/demo state.
- [ ] The existing map, conversation, team, investigation memory, and health initialization continue to work after entering the workspace.
- [ ] The layout remains usable at desktop and narrow viewport widths and preserves RTL reading order.

## Edge cases

- Investigation registry data is absent or corrupt.
- Health checks are still loading or fail while the welcome view is visible.
- Member avatar fails to load.
- Long investigation names, many participants, or zero participants.
- Users activate a nested participant action with keyboard input.
- Browser refresh after the user has entered an investigation.

## Technical constraints

- The relevant frontend is vanilla HTML/CSS/JavaScript in `llm_investigation_orchestrator_serbia_poc/`.
- The existing workspace initializes map and investigation state on page load; hiding it must not break size calculation or MapLibre rendering.
- Existing local-storage investigation records are the only current client-side source for real investigation identity.
- Existing team members are defined in `app.js`; there is no persistent participant-management API.
- Unrelated working-tree changes must remain untouched.

## UX notes

- Treat the entire ribbon as the primary navigation target while keeping nested controls independently operable.
- Visually distinguish "My investigations" from "Similar investigations" and real state from demo-only actions.
- Show health status in plain language, not only by color.
- Preserve strong focus states and semantic button behavior.
- Decide whether the welcome page can be revisited from the workspace before implementation.

## QA notes

- Verify initial view, same-page entry, nested-action event handling, RTL layout, keyboard behavior, and existing workspace regression.
- Test the health loading/success/failure states on the welcome view.
- Test with empty and malformed local storage.
- Verify map rendering after entering a workspace that was initially hidden.

## Risks

- Initializing MapLibre inside a hidden workspace may produce an incorrectly sized map unless it is resized when revealed.
- A clickable container with nested buttons can create invalid or confusing interaction semantics if implemented as nested buttons.
- Mock actions may be mistaken for persistent behavior without explicit copy.
- The existing header contains investigation creation/switching controls; the desired workspace-header behavior after entry is not yet specified.

## Open questions

1. After entering an investigation, how does the user return to the welcome page: app name, back control, browser history, or no return control in MVP?
2. Should the existing investigation switcher and its `+` creation control remain visible inside the investigation workspace?
3. Should invite/add participant open a demo modal, show a disabled/coming-soon state, or reuse an existing team-management interaction?
4. Should `E / ע` switch the full UI now or be a non-functional first-step control?
5. Should refreshing the page always return to welcome or remember that the user entered the investigation?

## Missing inputs

- Approved welcome-page wireframe or visual direction.
- Approved behavior for the five open questions above.
- Confirmation of which mock investigation titles/content are appropriate.

## Required reviewers

- Product: scope, action behavior, and navigation decisions.
- UX: ribbon hierarchy, nested actions, responsive RTL behavior, and return path.
- Development: initialization strategy and safe same-page view switching.
- QA: regression and accessibility test plan.

## Required child issues

- [ ] Product review
- [ ] Developer review
- [ ] UX review
- [ ] QA review
- [ ] Execution planning

## Proposed execution checkpoints

1. Welcome-page shell and safe view switching.
2. Real investigation ribbon and participant interaction.
3. Similar mocked investigations, responsive/accessibility polish, and regression QA.

## Handoff to developer

Questions for developer:

- Can the current map and workspace initialize while visually hidden, or should workspace initialization be deferred until ribbon activation?
- Which existing functions must run before the welcome ribbon can use the real investigation registry and health state?
- What is the smallest safe change that preserves current workspace behavior?

Expected developer output:

- feasibility notes
- likely affected files/services
- implementation options
- recommended approach
- technical risks
- test strategy
- proposed execution slices
