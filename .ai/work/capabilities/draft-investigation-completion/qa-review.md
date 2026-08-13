# QA Review

## Review status

Draft — pending product/UX checkpoint

## Acceptance criteria review

The proposed criteria cover direct creation, both save triggers, continuation, cancellation, localization, and normal-investigation regression.

## Happy path tests

- Welcome prompt opens draft workspace with only the create action.
- Direct creation with name and fake participants restores normal controls.
- Layer save and result/message save each open the modal and resume once.

## Edge and negative tests

- Empty, whitespace-only, and duplicate names.
- Cancel/backdrop/Escape from each trigger.
- Registration failure and repeated submit.
- Repeated save clicks while modal is open.
- Normal investigation save bypasses the modal.
- Hebrew/English and RTL/LTR.

## Regression areas

Welcome ribbons, existing investigation switching, team member selection, prompt execution, memory button states, and production source manifests.

## Automation suggestions

Extend `test_welcome_page.py`, investigation registry/UI tests, and memory UI contract tests; add a headless Edge interaction smoke for modal focus and pending-save continuation.

## QA recommendation

Continue after product/UX approves the two explicit choices.
