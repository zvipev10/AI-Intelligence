# UX Review

## Review status

Draft — pending human approval

## User flow

1. Analyst starts a draft from the welcome composer and enters the regular workspace.
2. Header shows one `Create investigation` button instead of normal investigation/team controls.
3. Direct click or first memory-save attempt opens the same modal.
4. Analyst enters a required name and may select fake participants.
5. Create closes the modal, restores normal controls, and resumes a pending save when applicable.

## UI states

- Default draft: create button.
- Modal idle: name, optional participant chips, demo disclosure, cancel/create.
- Invalid: inline required/duplicate-name error.
- Submitting: disable controls and show progress.
- Failure: retain fields, show inline error.

## Accessibility notes

Use a labelled modal dialog, initial focus on the name input, Escape/backdrop cancel, focus restoration, keyboard-toggleable participant chips, and an `aria-live` error region.

## UX edge cases

Cancel from a save-triggered modal must not save or show a false failure. A later save may reopen it. Locale changes should update modal copy without losing entered data.

## Product questions

- Recommended: optional selectable fake member chips with explicit “demo only; no invitations are sent” copy.
- Recommended: reject duplicate names inline rather than merging with an existing investigation.

## Review recommendation

Approve the recommended choices, then continue to execution planning.
