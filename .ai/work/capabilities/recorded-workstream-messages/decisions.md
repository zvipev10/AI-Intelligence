# Decisions

### 2026-08-11 — Match existing recording save and replay behavior

Decision:
Allow duplicate workstream recordings. Both supported workstream messages expose
the existing-style save interaction, and their replay badge/action behavior
matches existing saved-recording replay without new conventions.

Context:
Product clarified that the capability must include real user-triggered saving,
not only replay support, and explicitly selected existing replay behavior.

Rationale:
Consistency reduces UX and implementation complexity and preserves the user's
current mental model for Recordings.

Impact:
No duplicate suppression or workstream-specific Recorded badge is introduced.
Replay remains read-only while following existing recording control states.

Follow-ups:
Implement a typed structured snapshot and verify replay emits no mutation calls.
