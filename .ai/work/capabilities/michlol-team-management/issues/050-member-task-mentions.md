# [Child] Member Task Mentions with @ Autocomplete

## Parent

`000-parent-capability.md`

## Status

Deployed / Pending Product, UX, and QA review

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
- Add a general temporary Hermes instruction so mentioned team member names are ignored as investigation entities and treated only as UI addressing annotations. The instruction is always included for now.

## Acceptance criteria draft

- [x] Typing `@` in the main prompt opens member autocomplete.
- [x] The autocomplete includes all five predefined members.
- [x] Typing after `@` filters by member display name and role label.
- [x] Choosing a suggestion inserts a readable mention token into the prompt.
- [x] A recognized selected mention is visually highlighted in blue.
- [x] Multiple member mentions can appear in the same prompt.
- [x] Mention autocomplete works in step-continuation prompt surfaces as well as the main prompt.
- [x] Keyboard and pointer selection are supported.
- [x] Unknown `@text` does not block normal prompt submission.
- [ ] Existing prompt submission, layer-context prompt selection, and prompt options behavior are not regressed.
- [x] The implementation keeps stable ids available client-side separately from display text.
- [x] No visible task record is created by using `@member`.
- [x] No structured `team_mentions` payload is sent to the backend.
- [x] Hermes is generally instructed to ignore `@member` names as investigation entities unless the user explicitly asks about those people.

## Product decisions

- Mentions only address the prompt; they do not create task records.
- Multiple mentions are supported.
- Autocomplete is required everywhere the user writes an investigation prompt.
- Metadata is client-only for Slice 1.
- Hermes should receive a general/always-on instruction to ignore the member names as investigation entities for now.

## Approved implementation details

- Popover appears near the caret/input area.
- Popover is constrained and scrollable when space is tight.
- Keyboard behavior: Arrow Up/Down moves selection, Enter or Tab selects, Escape closes.
- No-match state hides the popover.
- Client-side mention metadata is transient during editing/submission and is not attached to rendered local chat messages.
- Hermes ignore instruction is included generally for all prompts, not only when recognized teammate mentions exist.

## Open questions

No blocking questions remain.

## Review needed

- Product: no blocking Product action after the latest clarifications.
- UX: complete for planning based on approved implementation details.
- Development: complete for planning based on approved client-only scope and always-on Hermes instruction.
- QA: validate RTL, keyboard, filtering, no-match behavior, prompt-regression coverage, selected-layer prompt context, and step-continuation submission.

## Implementation checkpoint

`../checkpoint-005.md`

## Deployment checkpoint

`../checkpoint-006.md`

## UX follow-up checkpoint

`../checkpoint-007.md`
