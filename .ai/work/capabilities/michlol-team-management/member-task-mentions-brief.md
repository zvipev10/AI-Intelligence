# Capability Addendum - Member Task Mentions

## Capability extension

Allow the analyst to direct a question or requested task to specific `מכלול` members by typing `@` and choosing a member from autocomplete.

## Status

Draft / Pending Product, UX, and Development review.

## User story

As an analyst working inside an investigation, I want to type `@` followed by a team member name and choose the member from autocomplete, so that I can explicitly ask a task from a specific person in the `מכלול`.

## Product intent

This extends the existing static `מכלול` team foundation. It does not introduce real users, authentication, permissions, notifications, or autonomous agents in the first slice.

The first implementation should make the analyst's intent explicit in the prompt/task text and keep the selected member identity available in a structured way for future routing.

## MVP behavior proposal

- Autocomplete is available in the main investigation prompt textarea.
- Typing `@` opens a compact member picker.
- Continuing to type filters all predefined `מכלול` members by display name and role label.
- Selecting a member inserts a mention token, for example `@משה`, into the textarea and returns focus to the prompt.
- The picker uses the same member picture/name treatment as the header list where practical.
- The selected mention is parsed into structured metadata using the stable member id.
- In MVP, submitting the prompt still follows the existing Hermes/chat flow; no real assignment, notification, or member-specific routing is performed.

## Future behavior

- Route a task to a real human user or an agent when those capabilities exist.
- Persist task assignment/status per investigation.
- Show assigned tasks in a dedicated investigation/team work area.
- Support agent-specific execution semantics when `member_type=agent` is introduced.

## Non-goals for the first slice

- Creating a task management board.
- Sending notifications.
- User login, authorization, or identity management.
- Real-time collaboration.
- Agent execution or automatic task routing.
- Assigning tasks from layer rows, map items, timeline items, or result cards.

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

## Open questions

1. Should the first slice support multiple mentioned members in one prompt, or only one?
2. Should mention autocomplete be limited to the main prompt textarea, or also available in step-continuation prompts?
3. Should submitted prompts send structured `team_mentions` to the backend immediately, or should Slice 1 remain client/UI only until task routing is defined?
4. When a member is mentioned, should Hermes receive any instruction beyond the literal prompt text?
5. Should a mention create a visible task record now, or is the MVP only explicit prompt addressing?

## Recommendation

Implement Slice 1 as prompt-composer mention autocomplete plus stable mention parsing. Do not create real task records or route work until Product defines task lifecycle, ownership, status, and future user/agent behavior.
