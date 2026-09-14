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
- Whether I360 LLM replaces any current inference path in a later capability.
