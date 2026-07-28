# Capability Decisions

### 2026-07-27 — Treat the selected teammate as the implicit chat addressee

Decision:
Selecting a teammate in the upper team bar addresses subsequent chat messages and continuation requests to that teammate without requiring the user to type `@name`. Pressing the selected teammate again clears the selection and returns to general chat. An explicit teammate mention in the typed message takes precedence. The visible user message remains unchanged.

Context:
Team selection previously changed only the prompt placeholder and response label. Backend routing still saw an unaddressed message and could fall back to the general agent, including after the user had selected Moshe.

Rationale:
The selected conversation participant is persistent interaction context and should carry the same routing meaning as repeatedly typing their mention.

Alternatives considered:
- Require an explicit mention on every message.
- Insert a visible mention into the composer.
- Keep selection as visual decoration only.

Impact:
Moshe selection routes to his dedicated profile. Other currently displayed teammates remain on the shared backend until they receive dedicated profiles, but their selected identity and role are transmitted as the conversation addressee.

Follow-ups:
Add dedicated routing profiles as other teammate agents become functional.

### 2026-07-26 — Make workstream creation a Moshe-owned conversation

Decision:
Expose `מעקב` only while Moshe is the selected conversation member. Keep the user in a dedicated Moshe chat mode while required information is incomplete. Once Moshe has a clear title, objective, and functional responsibility, the app persists the workstream from his structured handoff in that same turn without a separate preview or approval action.

Context:
The implemented Phase 1 flow still behaved as a deterministic local UI wizard, allowed assignment to any selected member, and required approve/cancel buttons. This contradicted the accepted chat-first direction.

Rationale:
Moshe contributes interpretation and clarification rather than merely labeling a client-generated record. Server-owned validation and persistence preserve the authority boundary without adding a redundant approval step.

Alternatives considered:
- Keep the local preview and confirmation controls.
- Allow every visible team member to own workstreams despite having no implemented agent contract.
- Create incomplete workstreams and request missing information afterward.

Impact:
The 2026-07-24 preview-and-confirm creation decision is superseded. Artifact promotion and archiving retain their existing protected-decision semantics.

Follow-ups:
Validate the real Moshe profile against complete and incomplete creation prompts in the demo environment.

### 2026-07-26 — Consolidate workstream status and selection in the upper bar

Decision:
The upper workstream control displays compact status and count and contains the selector when multiple workstreams exist. Selecting a workstream returns its detailed update and actions to chat. Reopening the same workstream replaces its earlier open-summary message instead of adding a duplicate.

Context:
The first implementation asked the user to choose among workstreams inside chat and could append repeated copies of the same open summary.

Rationale:
Status and navigation belong to persistent workspace chrome; content, explanation, and actions belong to the conversation.

Impact:
The indicator remains compact but is now a small upper-bar menu rather than a button that emits a selection prompt into chat.

Follow-ups:
Review status labels and long-title truncation during demo acceptance.

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

### 2026-07-26 — Resolve indication sources canonically instead of attaching a workstream layer

Decision:
Workstream creation no longer requires or attaches an event layer. Each confirmed `REC-...` indication is resolved by the app server against the canonical event dataset, and the server records its canonical source-layer reference.

Context:
The earlier Phase 1 flow required one layer as an evidence boundary. Once the MVP shifted to explicit record identifiers interpreted by Moshe, choosing a layer became redundant friction and prevented realistic multi-source leads.

Rationale:
The explicit record identifier plus server-side canonical resolution preserves existence checks and provenance without making the analyst locate or preselect a layer. It also permits one lead to contain indications from different source types.

Alternatives considered:
- Keep the mandatory workstream layer.
- Make layer attachment optional but restrict records when present.
- Store record IDs without canonical source provenance.

Impact:
The 2026-07-24 decision to require one explicit layer is superseded. `starting_source` and its source-layer action are removed from the MVP contract. Reopening a workstream in chat shows the active artifact.

Follow-ups:
Validate multi-source indications and canonical provenance in final MVP validation.

### 2026-07-28 — Make playback visibility a server-owned global boundary

Decision:
Publish the active scenario run's dataset, optional layers, cumulative
timeframe, and revision to an atomic policy file consumed directly by the
evidence server. Permit only one active run in the current demo deployment.

Context:
The agent can call many retrieval tools and cannot be trusted to consistently
forward a playback argument. Prompt-only filtering would allow future records
to reappear through semantic search, aggregation, related-event expansion,
object loading, presentation layers, or fusion.

Rationale:
A server-owned boundary applies regardless of the agent's chosen tool path.
One active run matches the current single-demo runtime and prevents ambiguous
global policy selection.

Alternatives considered:
- Add timeframe arguments to every agent tool call.
- Filter only the final response.
- Add session-scoped policy propagation in this slice.

Impact:
All relevant evidence paths use the same inclusive-start/exclusive-end window.
Entity and location summaries are derived from visible evidence. Stored target
candidates are hidden during playback because they lack stage-aware provenance.
Inactive playback preserves existing behavior.

Follow-ups:
Introduce session-scoped policy storage before supporting concurrent playback
users, and define target provenance before exposing stored targets in playback.

### 2026-07-28 — Reduce playback UX to one next-stage action

Decision:
Use one next-stage button in the existing workstream message. Its tooltip shows
the next configured timeframe. The first press starts the prepared scenario and
each later press releases one stage, then triggers Moshe once for that revision.

Context:
The broader playback-control plan introduced a picker, status panel, reset, and
completion controls that were unnecessary for the intended demonstration.

Rationale:
The single action keeps attention on the analytical change caused by newly
available evidence. Server-derived tooltip data preserves generic scenario
semantics without embedding fixture times in the UI.

Alternatives considered:
- Full playback panel and scenario picker.
- Client-side Moshe triggering after an advance.
- Show the current and future stage list.

Impact:
The server owns stage transition and Moshe-trigger idempotency. Moshe receives
both the newly released and cumulative windows. The final stage has no next
button. Deployment remains separately approved.

Follow-ups:
Validate the interaction and Moshe response on the VM after explicit deployment
approval.
