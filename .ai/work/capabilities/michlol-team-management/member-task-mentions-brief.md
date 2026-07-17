# Capability Addendum - Member Task Mentions

## Capability extension

Allow the analyst to direct a question or requested task to specific `מכלול` members by typing `@` and choosing a member from autocomplete.

## Status

Product clarifications accepted / Pending UX and Development review.

## User story

As an analyst working inside an investigation, I want to type `@` followed by a team member name and choose the member from autocomplete, so that I can explicitly ask a task from a specific person in the `מכלול`.

## Product intent

This extends the existing static `מכלול` team foundation. It does not introduce real users, authentication, permissions, notifications, or autonomous agents in the first slice.

The first implementation should make the analyst's intent explicit in the prompt/task text and keep the selected member identity available in a structured way for future routing.

## MVP behavior

- Autocomplete is available in the main investigation prompt textarea.
- Autocomplete is also available in other prompt-entry surfaces, including step-continuation prompts.
- Typing `@` opens a compact member picker.
- Continuing to type filters all predefined `מכלול` members by display name and role label.
- Selecting a member inserts a mention token, for example `@משה`, into the textarea and returns focus to the prompt.
- Multiple mentioned members are supported in one prompt.
- The picker uses the same member picture/name treatment as the header list where practical.
- The selected mentions may be parsed into client-side structured metadata using stable member ids.
- In MVP, submitting the prompt still follows the existing Hermes/chat flow; no real assignment, notification, member-specific routing, backend task creation, or backend `team_mentions` payload is performed.
- Hermes receives a temporary instruction that `@member` names are UI addressing annotations and should be ignored as investigation entities unless the user explicitly asks about those people.

## Future behavior

- Route a task to a real human user or an agent when those capabilities exist.
- Persist task assignment/status per investigation.
- Show assigned tasks in a dedicated investigation/team work area.
- Support agent-specific execution semantics when `member_type=agent` is introduced.

## Non-goals for the first slice

- Creating a task management board.
- Creating visible task records.
- Sending notifications.
- User login, authorization, or identity management.
- Real-time collaboration.
- Agent execution or automatic task routing.
- Assigning tasks from layer rows, map items, timeline items, or result cards.
- Sending structured team mention data to the backend.

## UX considerations

- The autocomplete should feel like part of the prompt composer, not a separate modal.
- Keyboard operation should support Arrow Up/Down, Enter/Tab to choose, and Escape to close.
- Mouse/touch selection should work without submitting the prompt.
- The popover must not cover the send button or prompt action buttons in small layouts.
- Empty/no-match state should be quiet and compact.
- All five predefined members should be searchable even when only three are visible in the compact header strip.

## Development considerations

- The static member catalog should move from duplicated header markup into a small JS data source before autocomplete implementation, so the header and mention picker use the same ids, names, roles, and avatar paths.
- Mention parsing should store stable ids separately from display text. Display names may change and future duplicate names are possible.
- Prompt submission can include `team_mentions` metadata only after the API contract is reviewed. If no backend contract is approved for Slice 1, keep metadata client-side and preserve existing prompt behavior.
- The mention token should remain readable in plain text if copied or saved.

## QA considerations

- Hebrew RTL typing around `@` mention tokens.
- Keyboard and mouse selection.
- Filtering by partial Hebrew name and role text.
- Multiple mentions in one prompt, if supported by implementation scope.
- Unknown `@text` should not break prompt submission.
- Existing prompt submit, selected-layer prompt context, prompt options menu, and investigation memory save behavior should not regress.

## Product decisions

- `@member` mentions only address the prompt; they do not create visible task records.
- Multiple mentioned members are supported in one prompt.
- Mention autocomplete should work everywhere the user can write an investigation prompt, including the main prompt and step-continuation prompts.
- Mention metadata remains client-only in Slice 1. Do not send structured `team_mentions` to the backend yet.
- Add a Hermes instruction for now: mentioned team member names should be ignored as investigation entities and treated only as UI addressing annotations.

## Open questions

No blocking Product questions remain for Slice 1 definition.

UX/development details still to close before implementation:

1. Exact autocomplete popover placement and collision behavior for each prompt surface.
2. Whether client-side mention metadata should be stored in JS state only during editing/submission, or also retained with the rendered chat message locally.
3. Exact Hermes instruction wording and where it should be injected in the existing prompt construction flow.

## Recommendation

Implement Slice 1 as prompt-surface mention autocomplete plus stable client-side mention parsing. Do not create real task records, send backend mention metadata, or route work until Product defines task lifecycle, ownership, status, and future user/agent behavior.
