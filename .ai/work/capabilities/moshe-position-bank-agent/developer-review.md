# Developer/Architecture Review — Draft

## Status

Draft recommendations pending human review. Not approved for execution planning.

## Feasibility

The current application already provides raw-event loading, MCP investigation tools, layer catalog/rows endpoints, investigation memory, and a static Moshe team profile. It does not yet provide a durable cross-investigation knowledge-artifact store, source-family lineage, artifact lifecycle, or a specialized agent identity/tool allowlist.

## Recommended architecture

Use a deterministic-first pipeline:

1. normalization and source-lineage enrichment;
2. spatial/temporal candidate generation;
3. hard independence and compatibility rules;
4. scored fusion with explicit uncertainty;
5. LLM explanation and contradiction review only after deterministic gating;
6. human acceptance;
7. append-only artifact/revision persistence;
8. read-only bank tools for expert answering.

The LLM should not decide source independence or invent coordinates. Those are validated fields and deterministic calculations.

## Persistence options

### Option A — Versioned JSON artifacts

Fastest POC path and consistent with current filesystem persistence. Easy to inspect and deploy, but weak for concurrency, indexing, transactional updates, and audit integrity.

### Option B — SQLite bank (recommended MVP)

One versioned SQLite database with artifacts, revisions, evidence links, review actions, and audit records. It supports atomic writes, indexed queries, referential checks, and a later migration path without introducing a service dependency.

### Option C — External database/service

Appropriate for multi-user production, but beyond the current POC and would trigger broader identity, permissions, deployment, and operations work.

## Proposed logical components

- `source_lineage`: derives/validates independent source families.
- `position_candidate_builder`: spatial-temporal blocking and object compatibility.
- `position_fusion`: calculates fused geometry, uncertainty, count range, confidence factors, and contradictions.
- `position_bank_repository`: artifacts, revisions, evidence, review actions, audit.
- `moshe_agent_policy`: role prompt, tool allowlist, citation and refusal rules.
- MCP tools for draft creation and bank retrieval.
- UI catalog layer and review workflow.

## Existing-tool assessment

The existing Serbia MCP server already provides useful read-only building blocks:

- `resolve_location`: resolves named areas to canonical location ids and map metadata.
- `search_events`: retrieves raw records by location, time, entity, source type, reliability, and keywords.
- `aggregate_events(group_by=location)`: identifies geographic concentrations and first/last observations.
- `semantic_search_events`: retrieves semantically similar records and supports location/time/source filters.
- `find_related_events`: expands from seed records using location, distance, time, entity, identifier, and semantic signals.
- `explain_linkage`: explains pairwise linkage dimensions.
- `compare_location_claims`: detects conflicting geographic claims; useful as a contradiction check, not as a fusion engine.

These tools can support a manually orchestrated investigation, but they cannot yet guarantee target creation because they do not provide source-family independence, arbitrary geometry/radius search over raw coordinates, deterministic cluster formation, same-object validation, duplicate-bank search, or artifact writes.

## Proposed geographic-first mission process

1. Parse explicit mission scope: area/geometry, time range, optional object/entity constraints.
2. Search `attack targets` first for nearby compatible draft or approved artifacts.
3. Resolve the area and retrieve all raw records within it and the mission time range.
4. Form geographic candidate clusters using observation coordinates and uncertainty, not only shared `location_id`.
5. Split each geographic cluster by time window and mobility class.
6. Within each cluster, normalize object class/entity/count and run semantic linkage across record text.
7. Build a linkage graph; require one coherent component describing the same compatible object.
8. Collapse derivative records into source families and require at least two independent families.
9. Check contradictions, calculate fused geometry/uncertainty, and preserve uncertain count as a range.
10. Re-run duplicate-bank matching against the fused result.
11. If a compatible artifact exists, propose new evidence/revision instead of a new target.
12. Otherwise create a draft, never an approved target; return an auditable mission report.

The recommended implementation is one composite deterministic MCP operation, for example `build_attack_target_candidate`, rather than relying on an LLM to correctly repeat dozens of low-level calls. It may internally reuse the existing search and linkage functions and return intermediate evidence for inspection.

## Hermes agent creation and invocation plan

The current application invokes Hermes through `POST /v1/runs` with per-run `input`, `instructions`, conversation history, and `session_id`; the repository does not currently define a separate named Moshe agent. Plan the new agent as follows:

1. Add a versioned Moshe agent profile containing identity, mission contract, system instructions, output schema, refusal boundary, and tool allowlist.
2. Register a dedicated Hermes toolset that combines existing read tools with attack-target-bank tools. Enforce write permissions in the bank MCP server, not only in the prompt.
3. Add an application endpoint such as `POST /api/agents/moshe/missions` accepting an explicit mission scope.
4. The endpoint loads the Moshe profile and creates a Hermes run with a unique `moshe-mission-*` session id. Mission state is separate from ordinary investigation chat.
5. Poll `/v1/runs/{run_id}` and stream `/v1/runs/{run_id}/events` using the existing Hermes session pattern.
6. Persist mission status, tool trace, proposed artifact id, duplicate decision, and final report.
7. Invoke it from an explicit UI action on Moshe (for example “Assign mission”), never from page load or a schedule.
8. If the installed Hermes version supports native named agent profiles/toolsets, map the profile there; otherwise retain the same semantics in the application-level runner while still creating an isolated Hermes run. Confirm the native configuration schema during developer review before implementation.

Proposed bank tools:

- `search_attack_targets_near` (read-only, drafts and approved)
- `get_attack_target` (read-only, evidence and revisions)
- `build_attack_target_candidate` (read-only/draft payload generation)
- `create_attack_target_draft` (write, Moshe mission only)
- `append_attack_target_evidence` (write, draft/revision workflow)
- `approve_attack_target` / `reject_attack_target` (human-authorized; unavailable to Moshe)

## Recommended execution slices after approval

1. Data contract and offline gold-set validator; no agent writes.
2. Read-only position-bank repository and layer projection.
3. Deterministic candidate/fusion engine producing drafts in a sandbox.
4. Human review lifecycle and audited acceptance.
5. Moshe specialized agent with read-all-raw/read-bank/create-draft tools.
6. Bank expert Q&A, staleness/contradiction handling, performance and security validation.

Each slice changes data or behavior and requires a checkpoint before the next slice.

## Technical questions

- How will source-family lineage be generated for the existing V2 corpus?
- Which geometry library, if any, is acceptable without creating deployment friction?
- Should confidence be an explainable rule score, a calibrated probability, or only an ordinal label in MVP?
- How are mobile-object freshness and track continuity represented?
- Should accepted bank artifacts be global and investigation links many-to-many?
