# Capability Decisions

### 2026-07-26 — Let Moshe interpret artifact intent in general chat

Decision:
All indication-artifact interaction occurs through the existing general chat. Users address Moshe naturally; his instructions and bounded tools interpret intent and resolve `REC-...` evidence references plus an optional `TGT-...` assessment subject. No predefined phrases, saved expressions, dedicated composer, command buttons, or layer-selection UI are required.

Context:
The earlier manual-ID proposal still assumed a phrase-driven interaction and explicit UI actions. Product requires the collaboration to behave as a conversation with Moshe.

Rationale:
Natural-language interpretation is the agent's functional contribution, while staged proposals, reference resolvers, revision checks, and explicit later-turn confirmation keep persistence controlled.

Alternatives considered:
- Deterministic parsing of predefined chat commands.
- Manual chat mode with action buttons.
- Temporary record selection in the layer.

Impact:
Agent integration moves into the second MVP implementation slice immediately after the artifact API. `REC-...` identifies evidence; `TGT-...` optionally identifies an existing target under reassessment and is not evidence.

Follow-ups:
Define Moshe tool schemas, staged proposal semantics, instruction/evaluation cases, and ambiguous-confirmation behavior in the execution plan.

### 2026-07-26 — Use manual REC identifiers for indication entry

Decision:
For the MVP, users may supply one or more `REC-...` identifiers naturally in chat. Moshe resolves them against the workstream's explicitly attached event layer and previews the resolved records before persistence.

Context:
A temporary selection mode in the existing layer view introduced unnecessary UX and implementation scope for the first artifact slice.

Rationale:
Manual identifiers preserve the chat-first flow and prove persistence, validation, revision, and confirmation semantics without changing layer interactions.

Alternatives considered:
- Temporary multi-select mode in the existing layer view.
- Per-record `הוסף למעקב` actions.
- Agent-selected records.

Impact:
The MVP supports event-record indications only. Generic layer-item selection and non-event identifiers are deferred.

Follow-ups:
Reconsider layer-based selection after the manual artifact workflow is validated.

### 2026-07-24 — Make indications a pre-assessment artifact

Decision:
The first shared workstream artifact will group one or more indications into a lead for assessment toward possible target creation.

Context:
The existing target workflow can create a target candidate from fused evidence, but the collaborative workstream needs an earlier durable object for promising, incomplete, or contradictory signals.

Rationale:
Persisting a lead prevents useful patterns from remaining only in chat while keeping uncertainty explicit and avoiding premature target creation.

Alternatives considered:
- Create an evolving target assessment directly.
- Let the workstream create a target candidate from selected indications.
- Store indications only as chat messages.

Impact:
The flow becomes `raw records → indications → target assessment lead → assessment → target candidate`. Promotion is explicit, and the new artifact cannot mutate the target bank.

Follow-ups:
Approve terminology, multiplicity, indication-source requirements, and authority to send a lead to assessment.

Product resolution:
The internal type remains `target_assessment_lead`, but the UX exposes no formal artifact name. The MVP allows one active artifact per workstream, requires stable source references for all indications, treats free text as annotation only, and permits only the user to send the indications to assessment.

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
