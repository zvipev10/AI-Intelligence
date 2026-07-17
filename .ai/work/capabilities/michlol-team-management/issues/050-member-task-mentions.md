# [Child] Member Task Mentions with @ Autocomplete

## Parent

`000-parent-capability.md`

## Status

Product clarified / Pending UX and Development review

## Request

Start defining the ability for the analyst to ask/request specific tasks from `מכלול` team members by typing `@member-name` with autocomplete.

## Proposed MVP

- Add `@` autocomplete in every investigation prompt-entry surface, including the main prompt composer and step-continuation prompts.
- Source autocomplete from the predefined five `מכלול` members.
- Show member picture, display name, and role label in the suggestion list.
- Insert a readable mention token into the prompt.
- Support multiple mentioned members in one prompt.
- Preserve stable member id metadata client-side for future routing.
- Keep existing Hermes/chat submission behavior unchanged.
- Do not create visible task records.
- Do not send structured `team_mentions` to the backend in Slice 1.
- Add a temporary Hermes instruction so mentioned team member names are ignored as investigation entities and treated only as UI addressing annotations.

## Acceptance criteria draft

- [ ] Typing `@` in the main prompt opens member autocomplete.
- [ ] The autocomplete includes all five predefined members.
- [ ] Typing after `@` filters by member display name and role label.
- [ ] Choosing a suggestion inserts a readable mention token into the prompt.
- [ ] Multiple member mentions can appear in the same prompt.
- [ ] Mention autocomplete works in step-continuation prompt surfaces as well as the main prompt.
- [ ] Keyboard and pointer selection are supported.
- [ ] Unknown `@text` does not block normal prompt submission.
- [ ] Existing prompt submission, layer-context prompt selection, and prompt options behavior are not regressed.
- [ ] The implementation keeps stable ids available client-side separately from display text.
- [ ] No visible task record is created by using `@member`.
- [ ] No structured `team_mentions` payload is sent to the backend.
- [ ] Hermes is instructed to ignore `@member` names as investigation entities unless the user explicitly asks about those people.

## Product decisions

- Mentions only address the prompt; they do not create task records.
- Multiple mentions are supported.
- Autocomplete is required everywhere the user writes an investigation prompt.
- Metadata is client-only for Slice 1.
- Hermes should receive an instruction to ignore the member names as investigation entities for now.

## Open questions

- UX placement/collision behavior for the autocomplete popover on each prompt surface.
- Development placement for the temporary Hermes instruction in the prompt construction flow.
- Whether selected mention metadata should remain transient or be attached to the local rendered chat message.

## Review needed

- Product: no blocking Product action after the latest clarifications.
- UX: confirm composer autocomplete behavior, keyboard rules, popover placement, and empty state.
- Development: confirm data source refactor and whether any API payload change is included.
- QA: confirm RTL, keyboard, filtering, and prompt-regression coverage.
