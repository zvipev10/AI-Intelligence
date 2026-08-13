# Capability Brief

## Capability name

Complete draft investigation creation

## Capability slug

`draft-investigation-completion`

## Parent issue

Local draft: `issues/parent-capability.md`

## Current status

Pending product/UX checkpoint. See `status.md`.

## User problem

A draft investigation can open the regular workspace, but the workspace presents normal investigation selection and participant controls before the draft has been converted into a named investigation. Saving a result or layer to investigation memory also assumes that conversion already happened.

## Business goal

Let analysts explore first and formalize the investigation only when they choose to create it or persist investigation memory.

## Target users

Analysts who begin from the welcome-page draft composer.

## Proposed behavior

- A draft opens the existing regular investigation workspace.
- While the active investigation is a draft, the header replaces the investigation selector and participant panel with one bilingual `Create investigation` button.
- The button opens a compact modal containing an investigation-name input and a fake participant invite/add interaction consistent with the welcome-page demo behavior.
- Clicking save-to-memory for either a message/result or a layer opens the same modal when the active investigation is still a draft.
- After successful creation, the draft becomes a normal investigation, normal header controls return, and a pending save action continues automatically.

## MVP scope

- Front-end draft detection and header mode.
- One reusable bilingual creation modal.
- Fake participant selection only; no invitations, messages, or membership persistence.
- Resume pending layer or result-memory saves after creation.
- Preserve the existing draft chat, results, layers, and investigation identifier during conversion.

## Non-goals

- Real participant invitation APIs or permissions.
- A new workspace, investigation data model, or draft persistence service.
- Changing normal investigation selection or welcome-page ribbons.

## Acceptance criteria

- [ ] Starting from the welcome composer opens the regular workspace in draft mode.
- [ ] Draft mode shows only `Create investigation` in place of the selector and participant panel.
- [ ] The creation button opens a small accessible modal with name and fake participant controls.
- [ ] Name is required; cancel leaves the draft unchanged.
- [ ] Creating converts the active draft without losing current workspace state.
- [ ] Message/result and layer save-to-memory actions open the same modal in draft mode.
- [ ] A save-triggered modal resumes exactly the initiating save once creation succeeds.
- [ ] Normal investigations keep existing header and save behavior.
- [ ] Hebrew/English and RTL/LTR behavior are covered.

## Edge cases

- Empty/whitespace-only or duplicate investigation names.
- Cancel after save-triggered opening.
- Repeated clicks while the modal or save is pending.
- Layer/result becomes stale before creation completes.
- Locale changes while the modal is open.

## Technical constraints

- Reuse the current in-document workspace and investigation registry.
- Preserve the active draft ID so existing chat/layer state and memory payload references remain coherent.
- Do not introduce a participant backend.

## UX notes

The participant interaction is explicitly demonstrative. The modal must say that no invitation is sent. Proposed selection is optional and uses the existing member avatars/names.

## QA notes

Contract tests should verify markup, draft-mode branching, pending-action continuation, and unchanged normal investigation behavior. Browser checks should cover desktop/mobile and both locales.

## Risks

- Ambiguous meaning of “fake like in welcome page”: the recommended interpretation is selectable fake member chips with explicit demo copy.
- Automatically resuming save after creation must not double-submit.

## Open questions

1. Should participants be selectable fake member chips (recommended), or should `Invite / add` only display the existing demo message?
2. Should a duplicate name select/merge with the existing investigation, or require a unique name (recommended)?

## Missing inputs

Human approval of the two recommended UX/product choices above.

## Required reviewers

Product/UX approval; developer and QA recommendations are prepared as drafts.

## Required child issues

- [ ] Product/UX checkpoint
- [ ] Implementation and automated tests
- [ ] Final QA and deployment decision

## Proposed execution checkpoints

1. Modal and draft-header state.
2. Save-to-memory interception and resume behavior.
3. Regression/visual QA and handoff.

## Handoff to developer

Implement only after the product/UX checkpoint approves participant behavior and duplicate-name handling.
