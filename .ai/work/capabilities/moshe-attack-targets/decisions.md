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

## 2026-07-19 - Deterministic visible-evidence fusion gate

Decision:
Build candidate source groups only from runtime-visible event fields. Collapse one UAV mission, matching observation IDs, and substantially matching visible reposts. Persist only medium/high-confidence assessments with at least two independent groups; low confidence is report-only.

Context:
Slice 2 stored source-group labels but did not determine whether they were independent. Moshe must not be able to bypass independence by supplying arbitrary labels.

Rationale:
The deterministic tool boundary keeps the MVP simple, auditable, and isolated from evaluator truth while leaving classification and the final explanation to Moshe.

Impact:
Creation rebuilds evidence snapshots, source groups, and quantity from canonical event records. Separate UAV missions may count independently; same-mission records never do. A visible-text repost threshold is an evaluation parameter, not hidden truth.

Follow-ups:
Measure false splits and false merges in the complete V2.1 evaluation before release.

## 2026-07-19 - Persistent isolated Moshe gateway

Decision:
Run Moshe as a persistent Hermes gateway on a dedicated named profile and local port. The application router sends only exact current-message `@משה` requests to it; General remains on its existing gateway.

Context:
The installed Hermes `/v1/runs` API cannot select a named profile or per-run tool allowlist. On-demand CLI invocation would lose the existing structured live-step stream.

Rationale:
A persistent profile preserves native sessions, restricted tools, structured run events, and the current intermediate-step UX without patching Hermes upstream.

Impact:
Moshe uses port `8643`, a separate audit file, a restricted Serbia-only MCP configuration, and its own systemd service. It remains idle until explicitly invoked. Deployment must enforce memory guards and validate both gateways because the VM has limited RAM.

Follow-ups:
Run representative dual-gateway load and rollback validation before production activation.

## 2026-07-20 - Single-tool target preparation with internal discovery

Decision:
Keep `prepare_target_candidate` as Moshe's single preparation interface. Starting from seed evidence, it performs bounded corroboration retrieval, evidence-pair ranking, competing-anchor disambiguation, and final preparation. Candidate creation independently revalidates the selected evidence before persistence.

Context:
The first complete Slice 6 evaluation showed that generic investigation retrieval left most true corroborating records undiscovered. The user requested that discovery and ranking remain part of preparation instead of adding another Moshe-facing tool.

Rationale:
One public tool keeps the MVP interaction simple while internal functions preserve testability and deterministic security boundaries.

Impact:
Preparation returns ranked public evidence, reasons, scores, alternatives, and ambiguity margins. Unclear results are report-only. SQLite schema, routing, presentation, and the write boundary do not change.

Follow-ups:
Deploy only after checkpoint 008 review, then run a read-only Moshe preparation smoke test.

## 2026-07-24 - Explicit structured evidence-reference layers

Decision:
Extend the shared `present_requested_results` tool with a separate `evidence_layers` channel. Present `מזהי ראיות` as independently controlled map/timeline layers selected explicitly by General or Moshe, while keeping requested results under `הצג תוצאות`.

Context:
Building the evidence section from identifiers in answer prose or from every tool result produced large, noisy, and frequently irrelevant output.

Rationale:
One final selection boundary can validate both user-requested data and materially relevant evidence without mixing them. Keeping two result arrays preserves the distinction throughout backend normalization and frontend state.

Impact:
New answers use structured evidence links, show up to 14 identifiers per layer without truncating underlying data, and never present evidence automatically. Old saved answers retain a read-only legacy block. The implementation is shared by General and Moshe and does not change SQLite.

Follow-ups:
Product visually accepts checkpoint 014. Table-only evidence references remain deferred.
