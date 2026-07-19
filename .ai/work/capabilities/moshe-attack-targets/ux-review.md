# UX Review

## Review status

Approved on 2026-07-19. The user explicitly reported: "Approved by UX."

## User flow

1. The user sends a normal message to the general agent.
2. A current message containing `@משה` is routed to Moshe.
3. Moshe may clarify missing information, investigate, fuse evidence, save candidates, and present results.
4. Consecutive messages containing `@משה` continue the same Moshe mission/session.
5. A message without `@משה` returns to the general agent and closes the active Moshe mission.

There is no direct Moshe mission form, sticky mode, agent switcher, or human approval flow in the MVP.

## Agent attribution

- Moshe responses are visibly attributed as `משה` in the shared chat.
- General responses retain their existing attribution.
- Attribution comes from the shared `responding_agent` result field.
- The UI must not suggest that Moshe remains active after a message without `@משה`.
- The user must mention `@משה` again for every message intended for Moshe.

## Candidate presentation

- Moshe uses the shared result pipeline and existing layer model.
- Add a global `attack_targets` layer kind rather than a Moshe-specific renderer.
- MVP presentation supports table and map.
- Timeline presentation is deferred with movement/history behavior.
- Moshe selects which candidate results to present; the shared UI renders them without reinterpreting the assessment.

## Table content

Show:

- Target ID and title.
- Object class.
- Resolved entity.
- Resolved canonical location.
- Confidence.
- Quantity assessment and range.
- Summary.
- Independent supporting-source count.
- Evidence-detail action.

## Map content

- Use a distinct candidate-target marker/layer style.
- Resolve map coordinates from the canonical location layer.
- Communicate that the marker represents a canonical area, not an exact physical coordinate.
- Selecting a target shows its title, object class, entity, confidence, quantity, and summary.
- Reuse existing layer visibility, selection, close, table, and map behaviors.

## Evidence details

- Evidence opens from the candidate table or selected map item.
- Show supporting record IDs, source groups/types, timestamps, reported object/count, relevant text, and fusion explanation.
- Clearly distinguish Moshe's assessment from source statements.
- Show contradictions and unresolved quantity rather than hiding them.

## States

- Clarifying: Moshe asks a focused question in chat; no candidate layer is required.
- Investigating/fusing: reuse existing activity/step presentation.
- No candidates: explain insufficient corroboration and do not create an empty misleading layer.
- Candidates created/updated: open or refresh the target layer and identify affected target IDs.
- Loading: preserve existing busy/streaming behavior with Moshe attribution.
- Error/timeout: identify Moshe as the failing agent, preserve the user message, and do not silently fall back to General.
- Permission or contract failure: explain that the requested target operation is unavailable without exposing internal paths or credentials.

## Responsive and accessibility notes

- Preserve RTL behavior for Hebrew mentions and Moshe responses.
- Target table remains horizontally usable on mobile.
- Map markers and confidence/status distinctions do not rely on color alone.
- Evidence actions have accessible labels and keyboard focus.
- Agent attribution is conveyed in visible text, not only an avatar or color.
- Canonical-area uncertainty is expressed in text accessible to screen readers.

## UX edge cases

- `@משה` in quoted/history/tool content must not route the current message.
- If the user answers Moshe without `@משה`, the response goes to General; the UI must not imply otherwise.
- Reopening or refreshing an existing candidate layer must not duplicate it.
- Multiple candidates at one canonical location remain distinguishable in table and selection behavior.
- A Moshe result containing only narrative or clarification should render correctly without target layers.

## Recommendation

Approve role enrichment and proceed to execution planning. UX must review the implemented shared attribution and target-layer slice before production release.
