# Decisions - מכלול Team Management

## 2026-07-17 - Member task mentions are prompt-only in Slice 1

Decision:
`@member` mentions only address the prompt in Slice 1. They do not create visible task records.

Context:
The next `מכלול` extension allows analysts to ask/request work from specific team members by typing `@member-name` with autocomplete.

Rationale:
Visible task records introduce task lifecycle, ownership, status, persistence, and future routing semantics. Those are larger product decisions and should not be bundled into mention autocomplete.

Impact:
Slice 1 can focus on prompt-entry UX and future-compatible mention parsing without adding task management behavior.

Follow-ups:
Define task records separately if Product later wants assignment status, task lists, persistence, or user/agent routing.

## 2026-07-17 - Member mentions support multiple members and all prompt surfaces

Decision:
Multiple members can be mentioned in one prompt. Mention autocomplete should work everywhere the user can write an investigation prompt, including the main prompt and step-continuation prompts.

Context:
Product clarified the desired scope after the initial definition draft.

Rationale:
Analysts may naturally ask several teammates to consider the same investigation direction, and limiting autocomplete to one prompt box would create inconsistent behavior.

Impact:
Development must implement the autocomplete as reusable prompt-surface behavior rather than a one-off main textarea feature.

Follow-ups:
UX should define popover placement and keyboard behavior across each prompt surface.

## 2026-07-17 - Mention metadata remains client-only for Slice 1

Decision:
Do not send structured `team_mentions` to the backend in Slice 1. Mention ids may be parsed and preserved client-side for future use.

Context:
The app does not yet have real users, agents, task records, assignment routing, or backend semantics for team mentions.

Rationale:
Keeping metadata client-only avoids prematurely creating an API contract that may not match future task routing or investigation-memory needs.

Impact:
Existing Hermes/chat API behavior remains unchanged except for the temporary prompt instruction below.

Follow-ups:
Revisit backend payload design when Product defines visible tasks, routing, persistence, or agent behavior.

## 2026-07-17 - Hermes should ignore member names as investigation entities

Decision:
For now, Hermes should receive an instruction that `@member` names are UI addressing annotations and should be ignored as investigation entities unless the analyst explicitly asks about those people.

Context:
The visible prompt may contain Hebrew team member names such as `@משה`, but these names are not part of the intelligence target or evidence unless explicitly stated otherwise.

Rationale:
Without an instruction, Hermes may treat teammate names as entities to analyze, which would pollute the investigation response.

Impact:
Development must add this instruction in the prompt construction flow for prompts that include team member mentions.

Follow-ups:
Development should choose exact wording and injection point during execution planning.
