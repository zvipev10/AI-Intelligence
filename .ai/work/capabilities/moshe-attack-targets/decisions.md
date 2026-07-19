# Moshe Attack Targets Decisions

## 2026-07-19 - Minimal final-state SQLite target bank

Decision:
Use SQLite with `targets` and `target_evidence` for an end-state V2.1 MVP. Implement only `candidate`; defer approval/rejection, revisions, movement, staleness, revocation, and concurrency workflows.

Context:
Moshe will initially run manually against the final state of a fixed synthetic dataset. The MVP goal is to validate fusion quality, not operational target lifecycle management.

Rationale:
SQLite provides safe writes and queries while the reduced schema avoids implementing operational complexity before fusion value is demonstrated.

Impact:
Moshe creates summarized candidates with evidence snapshots. Human approval/rejection is outside the MVP. Targets reference canonical locations and entities by ID and appear through the existing layer conventions.

Follow-ups:
Developer, QA, UX, and architecture/security reviews remain required before execution planning.

## 2026-07-19 - Explicit Moshe routing and shared presentation architecture

Decision:
Route only current messages containing `@משה` to Moshe. Consecutive mentions reuse one Hermes Moshe mission/session; a non-mention closes the mission and routes to General. Moshe owns clarification, fusion, candidate writes, explanation, and presentation. General and Moshe use one refactored backend/result/layer/frontend pipeline.

Context:
The current application already has result normalization and shared map/table/timeline presentation, but parts are coupled to the existing request handler and general-agent labels. A separate Moshe renderer would duplicate that infrastructure.

Rationale:
Agent identity and permissions should vary while transport, normalization, layer construction, and rendering remain shared. Hermes v0.14.0 provides native profiles and session resumption for Moshe context continuity.

Impact:
Moshe implementation includes a prerequisite shared-backend refactor, generic agent attribution, a common result envelope, and an `attack_targets` layer kind. There is no direct mission form, sticky routing, or human approval phase in the MVP.

Follow-ups:
Development must review the expanded refactor scope before execution planning. QA must cover regressions for General-agent results and existing layer presentation.

## 2026-07-19 - Moshe runtime security boundary

Decision:
Keep SQLite private to the Serbia MCP service, expose only constrained candidate tools to Moshe, physically and logically isolate evaluator truth, prohibit target deletion in the MVP, and require transactional backups before target-bank deployments.

Context:
Moshe introduces persistent agent writes and is evaluated against a hidden V2.1 answer key.

Rationale:
The agent must see realistic evidence but never the evaluator answer key or unrestricted storage access. The single-service VM permits a simple OS-level ownership model.

Impact:
The database uses a protected production path, target writes flow only through MCP transactions, backups are retained, and evaluation/reset operations stay administrative and separate from Moshe.

Follow-ups:
QA must turn these boundaries into automated negative and deployment tests.
