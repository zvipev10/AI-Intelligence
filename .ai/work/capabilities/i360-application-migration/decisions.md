# Decisions: I360 application migration

## 2026-09-14 — Preserve the application contract through a provider adapter

Decision: Keep the frontend, application API, Hermes routing, and investigation logic as the initial product boundary. Add an I360-backed provider beneath them.

Rationale: I360 supplies core data operations, while the application contains domain-specific reasoning and presentation behavior that has no direct platform equivalent.

Impact: Migration can proceed by capability with a local fallback and measurable parity checks.

## 2026-09-14 — Exclude Workstream and playback

Decision: Workstream and scenario playback are excluded from the migration implementation plan and acceptance criteria.

Rationale: The user removed Workstream from current scope and previously identified playback as demo-only.

Impact: No Workstream or playback UI, API, tool, artifact, persistence, or reevaluation work belongs in these implementation slices.

## Pending decisions

- I360 authentication and token-exchange model.
- Canonical field and identifier mapping.
- Whether investigation state and target candidates move to I360 in the first release or remain behind current repositories temporarily.
- Which I360 model/configuration meets the Part 2 quality, latency, and cost acceptance thresholds.

## 2026-09-14 — Split data application and agent migration

Decision: Deliver the migration in two parts. Part 1 contains all non-chat application capabilities and is independently releasable. Part 2 adds an application-owned agent controller using I360 `llm/chat` and the Part 1 domain services.

Rationale: Data access and analyst workflows provide value without unverified agent-runtime behavior. The split isolates inference and orchestration risk and permits separate rollback of the data provider and agent provider.

Impact: Part 1 must operate without Hermes. Part 2 cannot bypass Part 1 authorization or canonical data contracts.

## 2026-09-14 — Use a dedicated evidence-search control in Part 1

Decision: Do not repurpose the chat composer as the Part 1 search field. Add a dedicated I360 search control that materializes results as a normal application layer.

Rationale: The current composer represents an investigation question and implies an agent-generated answer. A direct search has different modes, filters, result semantics, warnings, and completion behavior. Creating a result layer reuses the application's established map, timeline, table, object-view, filtering, and saving interactions.

Impact: Part 1 can disable chat without losing data discovery. Part 2 restores the composer with its original conversational meaning and may use selected Part 1 layers as agent context.
