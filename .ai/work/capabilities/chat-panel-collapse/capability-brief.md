# Capability Brief

## Capability name
Minimize and restore the chat panel

## Capability slug
chat-panel-collapse

## Parent issue
Local issue draft: `issues/parent-capability.md`

## Current status
Pending implementation approval. See `status.md`.

## User problem
The chat panel permanently consumes a large part of the desktop workspace, even when the analyst wants to focus on the map or results table.

## Business goal
Let analysts temporarily maximize the intelligence visualization area without losing the current conversation.

## Target users
Desktop analysts working with the chat and map/results workspace.

## Proposed behavior
- Add a compact, standard minimize button at the top of the divider between chat and results.
- Pressing it collapses the entire chat panel and expands the result panel.
- The divider retains a compact restore control in the same location.
- Restoring returns the chat to its previous width and preserves conversation state.
- The control uses the existing Material Symbols icon set and visual tokens.
- The control is not shown on the stacked mobile layout.

## MVP scope
- Desktop collapse and restore.
- Accessible label, title, pressed state, and keyboard activation through a native button.
- Safe interaction with the existing draggable divider.
- Map resize after each transition.

## Non-goals
- Collapsing only the message history while retaining the composer.
- Persisting the collapsed state across page refresh.
- Changing the mobile stacked layout.
- Changing the map/chat default proportions.

## Acceptance criteria
- [ ] A minimize control appears at the upper end of the chat/results divider.
- [ ] One press hides the chat and gives its space to results.
- [ ] The control remains visible and restores the chat in one press.
- [ ] The restored chat uses its prior width.
- [ ] Existing divider dragging still works when expanded.
- [ ] The map is resized after collapse and restore.
- [ ] The button has clear Hebrew tooltip and accessible labels for both states.
- [ ] The control is hidden at the existing mobile breakpoint.

## Edge cases
- Collapse after manually resizing the panels.
- Window resize while collapsed.
- Rapid repeated presses.
- Switching map/timeline or showing a result table while collapsed.

## Technical constraints
- Preserve the existing CSS grid and `--chat-width` / `--result-width` sizing model.
- Do not discard or recreate the chat DOM.
- Do not introduce a new dependency.

## UX notes
- Use a small circular divider control with an existing chevron/panel icon.
- Keep it visually subordinate to primary actions.
- Direction must communicate the resulting movement in the RTL desktop layout.

## QA notes
- Verify expanded, collapsed, and restored screenshots at the production desktop viewport.
- Verify keyboard focus and activation.
- Verify divider drag regression and mobile breakpoint behavior.

## Risks
- A zero-width grid track could hide the restore control if the divider is collapsed with it.
- Divider pointer handling could accidentally start a resize when the button is pressed.
- MapLibre requires an explicit resize after the grid transition.

## Open questions
None. The screenshot and request define the control location and intended outcome.

## Missing inputs
Human approval to pass the repository's UX/development gate before implementation.

## Required reviewers
- Product/UX: confirm the stated collapse/restore behavior.
- Development: confirm the grid-track approach.
- QA: confirm the regression checklist.

## Required child issues
- [x] Product definition
- [ ] Developer review
- [ ] UX review
- [ ] QA review
- [ ] Execution planning

## Proposed execution checkpoints
1. Implement divider button and collapse state.
2. Add automated regression coverage.
3. Verify both visual states and deploy.

## Handoff to developer
Questions for developer:
- Confirm that the divider remains its own grid track while the chat track becomes zero width.

Expected developer output:
- feasibility notes
- affected files
- implementation approach
- test strategy
