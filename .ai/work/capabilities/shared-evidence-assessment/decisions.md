# Capability Decisions

### 2026-07-24 — Use chat as the Phase 1 workstream interaction surface

Decision:
Create workstreams from the existing plus menu through a distinct `מעקב` composer mode. Require one explicit layer, treat the user's message as the objective, preview the derived title and responsibility in an agent-style message, and persist only after confirmation. Keep the active indicator minimal; pressing it returns status and actions to chat.

Context:
The existing chat already supports follow-up messages and layer attachments. A separate workstream form or management panel would duplicate those mechanics without demonstrating the intended collaborative-workspace direction.

Rationale:
The new behavior is durable shared work with explicit ownership and lifecycle, while chat remains the familiar surface for context, decisions, and actions.

Impact:
Phase 1 messages are deterministic and user-triggered. There is no automatic monitoring, LLM-generated status, drawer, or workstream management screen.

Follow-ups:
Review the implemented checkpoint with Product, UX, and QA before merge. Define automated agent updates only in a later slice.

### 2026-07-24 — Keep Phase 1 independent from Investigation Memory items

Decision:
Phase 1 associates a workstream with an investigation by `investigation_id` and may record a generic starting-source reference. It does not select, import, or reference individual Investigation Memory items.

Context:
Investigation Memory item selection introduces context browsing, stable item-reference semantics, missing/superseded handling, and coupling between two capabilities. None is required to prove durable workstream persistence.

Rationale:
Phase 1 should answer one question: can the product persist and reopen a unit of shared human-agent work independently from chat?

Alternatives considered:
- Select memory items during workstream creation.
- Copy the full current Investigation Memory into the workstream.
- Treat all investigation memory as implicit workstream context.

Impact:
Memory integration moves to a later context-assembly slice before automatic agent reevaluation.

Follow-ups:
Define explicit memory selection and promotion semantics after the artifact model exists.

### 2026-07-24 — Separate planning and Phase 1 implementation pull requests

Decision:
Merge planning PR #24 before branching Phase 1 implementation. Track implementation in issue #30 and a separate pull request.

Context:
PR #24 is the only open pull request and contains only capability artifacts.

Rationale:
Keeping approved planning separate from product code makes review order and rollback clear.

Alternatives considered:
- Add implementation commits to PR #24.
- Stack implementation directly on the planning branch.

Impact:
The implementation branch must start from `main` after PR #24 merges.

Follow-ups:
Create the Phase 1 implementation branch and PR after merge.
