# [Child] Member Task Mentions with @ Autocomplete

## Parent

`000-parent-capability.md`

## Status

Draft / Pending review

## Request

Start defining the ability for the analyst to ask/request specific tasks from `מכלול` team members by typing `@member-name` with autocomplete.

## Proposed MVP

- Add `@` autocomplete in the main investigation prompt composer.
- Source autocomplete from the predefined five `מכלול` members.
- Show member picture, display name, and role label in the suggestion list.
- Insert a readable mention token into the prompt.
- Preserve stable member id metadata for future routing.
- Keep existing Hermes/chat submission behavior unchanged unless a backend API contract is explicitly approved.

## Acceptance criteria draft

- [ ] Typing `@` in the main prompt opens member autocomplete.
- [ ] The autocomplete includes all five predefined members.
- [ ] Typing after `@` filters by member display name and role label.
- [ ] Choosing a suggestion inserts a readable mention token into the prompt.
- [ ] Keyboard and pointer selection are supported.
- [ ] Unknown `@text` does not block normal prompt submission.
- [ ] Existing prompt submission, layer-context prompt selection, and prompt options behavior are not regressed.
- [ ] The implementation keeps stable ids available separately from display text.

## Open questions

- Multiple mentions in one prompt: yes/no for first slice?
- Main prompt only, or also step-continuation prompt?
- Client-only metadata first, or send `team_mentions` to backend immediately?
- Should Hermes receive a structured instruction for mentioned members, or only the visible prompt text?
- Should a mention create a task record now, or only address the prompt?

## Review needed

- Product: confirm MVP semantics and whether a visible task record is required.
- UX: confirm composer autocomplete behavior, keyboard rules, popover placement, and empty state.
- Development: confirm data source refactor and whether any API payload change is included.
- QA: confirm RTL, keyboard, filtering, and prompt-regression coverage.
