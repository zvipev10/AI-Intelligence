# Execution plan: I360 application migration

## Plan status

Draft — ready for human architecture/product review before coding.

## Goal

Convert the application's non-Workstream, non-playback data access and investigation functions to operate over authorized I360 data, preserving the current frontend and application behavior.

## Prerequisite review gate

| Artifact | Status |
|---|---|
| Product brief | Ready for planning; user supplied scope |
| Developer review | Ready with live-validation gates |
| UX review | Ready; degraded-state copy needs acceptance |
| QA review | Ready; cases need live field samples |
| Architecture/security | Required before credentials or writes |

## Implementation principles

- The browser continues to call the application server.
- I360 credentials never enter browser code.
- Domain tools consume normalized records through one provider interface.
- Every I360 response propagates warnings, capability limitations, and coverage metadata.
- Local and I360 providers coexist behind configuration until cutover.
- No slice modifies or depends on Workstream or playback.

## Slice 0 — Authenticated discovery and contract fixture

**Goal:** Turn public documentation assumptions into verified environment facts.

**Changes:** Add a read-only probe/diagnostic command and redacted contract fixtures. Verify authentication, base URL, health dependencies, item/entity schemas, search modes, geo, embeddings, media delivery, warnings, paging, and permission behavior with ordinary users.

**Exit criteria:** Approved field/capability matrix; representative IDs; no secrets in fixtures or logs; blockers classified as platform, data, or application work.

**Risk/reviewer:** High; architecture/security and platform owner. Stop after slice.

## Slice 1 — Provider boundary and canonical mapping

**Goal:** Decouple investigation behavior from local storage.

**Changes:** Define typed provider operations for search, semantic search, get, aggregate, context, entity/place resolution, and media. Implement the local provider by moving existing access behind the interface. Define canonical ID, time, source, reliability, certainty, location, entity, text, media, warning, and coverage fields. Add configuration and fail-closed startup validation.

**Exit criteria:** Current local behavior passes through the provider; mapping contract is documented and tested.

**Risk/reviewer:** Medium; development/architecture. Stop after slice.

## Slice 2 — Read-only I360 provider

**Goal:** Supply canonical evidence from I360.

**Changes:** Implement authenticated client transport, timeout/retry policy, pagination, warning handling, items search/get/aggregate/context, entity/place lookup, media URL/stream handling, and capability discovery. Normalize responses through Slice 1 mappings.

**Exit criteria:** Contract tests pass; live samples cover text, semantic, geo, entity, original text, transcript/OCR, and media; denied records remain inaccessible.

**Risk/reviewer:** High; architecture/security, development, QA. Stop after slice.

## Slice 3 — Core MCP evidence tools

**Goal:** Move foundational tools to the provider.

**Changes:** Convert `search_events`, `semantic_search_events`, `get_objects`, `resolve_location`, `resolve_entity`, and `aggregate_events`. Preserve current output schemas and add explicit provider warnings and coverage. Use bounded application-side aggregation only where I360 semantics do not match.

**Exit criteria:** Tool contract tests and differential cases pass; incomplete search is never reported as exhaustive.

**Risk/reviewer:** Medium; development/QA/product. Stop after slice.

## Slice 4 — Investigation reasoning tools

**Goal:** Run the current analytical logic over I360 candidates.

**Changes:** Convert event-reference resolution, actor history, identifier and semantic-clue tracing, related-event ranking, location-claim comparison, hypothesis challenge, linkage explanation, and sequence building. Keep deterministic scoring and evidence-bound LLM prompts. Ensure every citation resolves through the provider.

**Exit criteria:** Representative investigation scenarios produce grounded chains, alternatives, gaps, and resolvable citations in both locales.

**Risk/reviewer:** High; product analyst, development, QA. Stop after slice.

## Slice 5 — Application API and frontend integration

**Goal:** Make existing screens use I360-backed data without a redesign.

**Changes:** Route layers, layer rows, object detail, map/timeline records, and investigation query results through provider-backed services. Add authentication, unavailable/partial/denied states, capability-aware controls, and observability. Keep catalog layer IDs and selection contracts stable where possible.

**Exit criteria:** Search-to-map/list/timeline-to-object-view flow passes; media and bilingual behavior pass; UI distinguishes no matches from incomplete retrieval.

**Risk/reviewer:** High; UX/product/security/QA. Stop after slice.

## Slice 6 — Investigation state and saved artifacts

**Goal:** Preserve investigation continuity with I360 evidence references.

**Changes:** Finalize storage choice for investigation metadata, memory, saved questions, and saved layers. If moved to I360, create reviewed entity types, actors, soft-deletion and concurrency behavior; otherwise formalize the temporary current-store boundary. Validate stale or denied evidence references.

**Exit criteria:** Two users pass own/shared/denied scenarios; save/reopen and conflict tests pass; rollback path is proven.

**Risk/reviewer:** High; architecture/security/product. Stop after slice.

## Slice 7 — Target candidates

**Goal:** Preserve target search, creation, update, duplicate detection, and evidence attachment over I360 evidence.

**Changes:** Keep `TargetBank` behind a repository first, then implement the approved persistence choice. Map evidence IDs to I360 items, define target ownership and visibility, preserve provenance and duplicate rules, and handle removal/update conflicts.

**Exit criteria:** Existing target tests plus multi-user, stale-reference, duplicate, and concurrent-update cases pass.

**Risk/reviewer:** High; product, architecture/security, QA. Stop after slice.

## Slice 8 — Cutover and fallback

**Goal:** Make I360 the default provider safely.

**Changes:** Run acceptance and representative-volume tests; compare result quality and coverage; document operations; switch configuration by environment; retain a time-bounded rollback mechanism; remove local data dependencies only in a separately reviewed cleanup.

**Exit criteria:** Acceptance criteria pass, known gaps are accepted, operational owner and rollback are documented, and no migration acceptance depends on Workstream or playback.

**Risk/reviewer:** High; product, operations, security, QA. Stop before production switch.

## Likely affected areas

- `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`
- new provider/client/mapping modules under `llm_investigation_orchestrator_serbia_poc/mcp_server/`
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- configuration examples and deployment documentation
- provider, MCP, API, security, UI, and target tests

## Stop conditions

- Required evidence is not ingested or lacks stable identifiers.
- Access rules allow a user to retrieve denied records by any path.
- Search warnings or caps cannot be surfaced reliably.
- Mutable I360 records lack an accepted concurrency strategy.
- Required original text, locations, entity links, or media cannot be recovered.
- A slice requires Workstream or playback changes; re-scope separately.

## Rollback

Keep provider selection configuration and the local implementation until I360 cutover is accepted. Writes must not be dual-written without a reviewed reconciliation design. Roll back by restoring the previous provider configuration; schema cleanup or data deletion requires a separate plan.
