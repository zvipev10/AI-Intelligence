# Capability Brief

## Capability name

Compact upper-section controls

## Capability slug

`header-simplification`

## Parent issue

Not created; draft body is in `issues/parent-capability.md`.

## Current status

Draft pending human UX/product confirmation. See `status.md`.

## User problem

The upper section uses too much space and gives persistent prominence to secondary system details.

## Business goal

Make the investigation workspace feel simpler and leave more visual attention for the active investigation.

## Target users

Analysts using the investigation workspace in Hebrew or English.

## Proposed behavior

- Render the language selector as a compact two-position control with `E` and `ע` printed directly on the control.
- Replace the verbose Hermes and database/data status rows with compact status indicators.
- Reveal the full service name, current state, and useful detail through a tooltip/popover on hover and keyboard focus.
- Keep critical failure states visually distinguishable without requiring the tooltip.

## MVP scope

- Header-only markup, styling, and status-update behavior.
- Existing loading, connected/ready, local/demo, and failed states.
- Accessible names and keyboard focus behavior for every compact control.

## Non-goals

- Changing Hermes, MCP, database, or dataset connectivity.
- Redesigning the investigation selector or team controls.
- Implementing new translation infrastructure.

## Acceptance criteria

- The language control displays only `E` and `ע` as its visible labels and clearly indicates the selected language.
- Hermes and database/data status each occupy one compact indicator in the default header view.
- Each status exposes a descriptive service name and current detail on hover and keyboard focus.
- Ready, loading/unknown, and error states remain distinguishable by more than color alone.
- Existing runtime status changes continue to update the visible state and accessible description.
- The controls remain usable at the existing responsive header breakpoint.

## Edge cases

- Runtime status request fails.
- Dataset loads while Hermes is unavailable or in local demo mode.
- A pointerless/touch device cannot hover.
- Long version or error text does not fit in a tooltip.
- RTL and LTR labels appear in the same compact group.

## Technical constraints

- Latest `main` has Hermes/MCP and dataset status rows in the primary Serbia POC.
- The language switch is in `llm_investigation_orchestrator_serbia_poc_english_wip_20260806_0718`; it currently prints `עברית` and `English` outside the track.
- No backend/API changes are expected.

## UX notes

Use a dot plus a small service glyph/initial or another non-color state cue. Tooltip content must also be available on focus; touch should have an equivalent tap interaction or accessible label.

## QA notes

Verify all status transitions, keyboard navigation, RTL layout, responsive layout, and pointerless access to details.

## Risks

- Over-compression could hide that the status refers to the loaded dataset.
- A hover-only implementation would be inaccessible.
- The bilingual WIP is a parallel app copy, so implementation and validation must target it explicitly.

## Open questions

1. Should status detail open on click/tap as well as hover/focus?

## Missing inputs

- Human approval of the prepared UX and developer review gate.

## Required reviewers

- Product/UX
- Development
- QA

## Required child issues

- [ ] UX/product review
- [ ] Developer review
- [ ] QA review
- [ ] Execution planning

## Proposed execution checkpoints

1. Approve the compact control anatomy, labels, and interactions.
2. Implement header markup/styles and status state binding.
3. Validate responsive, RTL/LTR, keyboard, touch, and failure states.

## Handoff to developer

Questions for developer:
- Confirm the accessible detail interaction and exact dataset/Hermes state mapping.

Expected developer output:
- feasibility notes
- affected files and status-state mapping
- accessible tooltip/popover approach
- test strategy and execution slices
