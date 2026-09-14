# i360 frontend feasibility assessment

Date: 2026-09-14. Application baseline: `9fea4819821ac2cbb0605f9f424eea202a19ab80` (`main`). Public HL API contract: `195`.

## Recommendation

**A custom frontend on i360 is feasible. A frontend-only change that replaces all our current application services with i360 is not established by the documentation.**

Use i360 for authorized retrieval, entity persistence, media reads, and available search/aggregation services. Retain our application-specific orchestration and presentation contracts behind an adapter initially. Treat replacing Hermes with Agentic Flows Studio as a separate migration with its own acceptance tests.

Review recommendation: **pause for architecture/product review before implementation**, then perform a bounded integration proof. This assessment approves no model changes, deployment, ingestion, or product rewrite.

## Coverage and confidence

- Read the eight public kit pages: start, quickstart, walkthrough (all five stages), architecture, runtime, design time, deployment, and use cases, including expandable capability descriptions.
- Read the seven public Studio documentation pages: start, quickstart, walkthrough, design, runtime, deployment, and use cases. Did not execute a flow or treat the designer as evidence of an integration working.
- Retrieved the live `/map` JSON and `/openapi.json`; reviewed the operation inventory, all capability groups and explicit gaps, and the detailed contracts relevant to this application's data, media, search, permissions, and concurrency needs.
- Downloaded the kit and agent-skill archives for inspection only. Reviewed their onboarding, constraints, extension and skeleton architecture, status, attachment workaround, and relevant field reports. Did not install or run downloaded code. Archived observations are historical evidence, not live test results.
- Inspected the broader platform map's 197-node catalog and selected relevant node bodies (agenticfw, intelliagent memory, relations, operational entities, and link analysis). This was an inventory review plus focused reading, **not a line-by-line review of every internal service document**. The map itself labels every node draft and says none has live-estate verification.
- Full text of the authenticated documentation corpus could not be read: `GET /api/v1/meta/docs` and the browser guide reader return `401 missing_token`. Its index advertises 21 guides and 11 reference topics. The downloaded skill carries only a subset. Consequently, this is not an exhaustive authenticated documentation review.
- No credentials, customer records, writes, model calls, capability probes requiring authentication, performance measurements, or production tests were used.
- Local sources reviewed: `docs/architecture.md`, the canonical package README/deployment notes, `index.html`, `app.js`, `server.py`, `scenario_playback.py`, and `workstream_artifacts.py`. `docs/product-context.md` does not exist; source and current architecture contracts supplied the context.

## What the current frontend actually depends on

The canonical frontend is `llm_investigation_orchestrator_serbia_poc/app.js` with `index.html`, styles, and MapLibre. It calls our server for investigations, memory, saved questions, layer catalogs/rows, workstream presentations and archival, playback status/advancement, agent runs and live steps. Startup also loads localized dataset assets.

This is more than a record browser. The server routes General/Moshe through Hermes, maintains investigation context, normalizes evidence and presentation objects, and triggers background reevaluations. Persistence includes JSON files and locale-separated state, with target persistence described as SQLite in the architecture notes. Playback has a global visibility window, revision-scoped jobs, and deduplication rules. Workstream artifacts require `expected_revision`, maintain revision history, and validate actors and action transitions.

## Feature comparison

| Current need | i360 support documented | Work needed / limitation |
|---|---|---|
| Custom workspace, chat, map, list, timeline, panels | Kit produces an owned React/TypeScript frontend and FastAPI backend; custom code can survive regeneration | Rebuild or port the interaction code. Generated CRUD screens are a starting point, not feature parity. Keep MapLibre and application presentation logic where useful. |
| Raw evidence search | Item search offers text, semantic, visual-description, time, geographic shapes, sources, and field filters | Map our canonical event fields and IDs to real ingested items. Read capability flags and warnings. Separate item records from writable entity instances. |
| Map filtering and clustering | Bounding box, polygon, radius and place search; geographic aggregation | Clustering and place lookup depend on deployed services. No exposed basemap/tile API or MIL-STD renderer was found. Preserve our symbols, provenance, and map-selection behavior. |
| Timeline and counts | Time/category/geo aggregation | Time bucket size is platform-chosen. Semantic totals are capped ranked pools, not full counts; semantic aggregation does not support time/geo. Exact analytics parity requires validation or custom computation. |
| Record/object viewer | Item detail, related context, entity detail, media bytes, Range seeking, optional signed URLs | Preserve text fallbacks and source identity. Original text/transcripts/OCR require item detail; a null search text is not proof of no content. Signed URLs require installation configuration. |
| Investigations, saved layers/questions, chats, memory, workstreams | Writable entity types, instance CRUD, actor assignments and links | Design app-owned types or verify safe reuse. Existing built-in INVESTIGATION is not automatically equivalent to our investigation object. Persist UI/job metadata explicitly. |
| Per-user seen indicators | Item `was_read` exists | It is shared item state, not per-user read state. Our per-user workstream seen state needs separate storage. |
| Evidence links and revisions | Link creation, annotations, record fields | No dedicated link-instance deletion operation. Model removable evidence associations as app-owned relation records or another reviewed representation. Keep provenance, revision history and validation. |
| General/Moshe orchestration and UI actions | HL API provides inference and search; Studio describes governed tools, agents, subflows, human gates and audit/replay | No confirmed drop-in mapping to our sessions, tools, memory, background reevaluation, or `catalog_layer_actions`. Keep Hermes initially; verify Studio separately. |
| Staged playback / Next / reset | Time-filtered retrieval supplies a useful primitive | No equivalent scenario-playback API. Preserve the global run, advancing visibility, revision claims, no-future-data rules and independent memory-update behavior in our application. |
| Hebrew/English | Unicode text, original/English text buckets, multilingual place lookup | Locale-isolated mutable state and fail-closed language behavior remain our responsibility. Model/search quality in both languages is untested. |
| Live UI refresh | SSE watches named items/entities/mentions | No new-record discovery, replay or webhook. Reconnect and periodic reads/list polling remain necessary. |
| Files and new source data | Reads existing media; platform has separate ingestion pipelines | No first-class upload/ingested-item creation through HL API. Migration/import needs a platform-operated pipeline. Real live UAV delivery is not established by stored-video Range support; our current viewer is a simulation. |

## Confirmed exposed-API gaps

These are gaps in the published high-level application interface, not claims that the entire i360 installation lacks the underlying infrastructure.

1. **Ingested items and media uploads:** no item-ingestion or normal attachment-upload operation. Ordinary entity CRUD is not ingestion and does not populate the same indexed intelligence-item/media pipeline. The kit ships a temporary base64-in-TEXT chunk workaround; its own authors describe migration debt and request a real upload API. Do not use that as the default evidence/media architecture.
2. **Relationship removal and bulk record writes:** link instances can be created but have no dedicated removal operation. Entity records have no batch-write endpoint (schema batches are different). This matters for changing evidence membership and importing saved state.
3. **Reliable event consumption:** record SSE is best-effort and only watches known IDs. Events can be silently lost, contain identity/time rather than the new record content, and cannot be replayed. No webhook exists. It cannot be our sole trigger or correctness mechanism.
4. **Permission-profile administration:** the capability map says type grants are applied as a side effect of creating types; full profile management is not exposed. Record actor lists can be replaced through PATCH, but membership/roles and existing-type grants require an agreed administrative path.
5. **Inference controls:** the map identifies missing per-caller usage limits. Chat streaming/JSON output do not supply our agent lifecycle or domain workflows. `ChatMessage.content` is still a string in contract 195; historical vision workarounds via `extra_body` are not a stable multimodal-message contract. Similar-image query input is distinct from storing an uploaded file.
6. **Operational assurance:** the map lists readiness/liveness as placeholder probes that do not prove catalog/EMS reachability. General architecture claims about availability and quotas are not sufficient operational evidence for this facade.

## Blocking questions before a full rewrite

1. **Actual data and installation capabilities.** Are our source records already ingested? Which IDs, coordinates, event/ingestion times, original language, entity associations, and media survive? Are text/image embeddings, geo clustering, signed media, models and notifications active for the target users? An inaccessible feature flag is unknown, not false.
2. **Access-control consistency.** The contract explicitly states that entity search applies type permission plus actor visibility, while GET-by-ID is gated by type permission alone. Prove our required investigation isolation through search, direct fetch, linked records, media, agent tools and saved artifacts with ordinary users. Do not assume the permission slogan implies identical enforcement on every path.
3. **Concurrent updates.** PATCH is documented as read/merge/replace. No `If-Match`, ETag, `expected_revision`, transaction or record-write idempotency contract was found in the exposed operations. Our existing conflict/revision behavior needs a server-enforced solution; an application revision field alone does not prevent two writers from winning simultaneously. Ask for guarantees and test races before choosing storage.
4. **Durable jobs and agent context.** A stateless generated backend does not replace our process locks, background threads, persisted claims, and retry state. Decide where durable job state/coordination lives. Studio is a candidate, not a proven replacement. Its public pages describe MCP tools and durable runs, while the draft platform node says real MCP transport is deferred and persistent memory is unconfirmed. These claims need reconciliation by the platform team.
5. **Evidence semantics and graph completeness.** `/items/context` can return empty relations after lookup failure, without warnings; co-occurrence is not a confirmed formal relationship. Preserve explicit evidence membership and distinguish unknown links from absent links. No general graph-traversal/analysis API equivalent was found on HL API.
6. **Exact frontend/data contract.** Preserve canonical layer IDs, row/object references, multi-location observations, confidence versus affiliation, evidence provenance, map/table selections, saved filters, localized state and playback time policy. A capability named "entities" or "geo" does not guarantee those semantics.

## Documentation inconsistencies to resolve

- Kit use-cases says no change notifications; contract 195 exposes limited record SSE. Use the detailed contract with deployment verification.
- Architecture says model quotas are inherited; the capability map identifies missing per-caller limits.
- Architecture advertises rich multimodal composition. The map marks text-plus-image as refused, while the current contract supports specific combinations (visual-description search with filters and image input for ask-all). Distinguish each operation and verify the precise combination required.
- Entity-search operation prose says sort order is unverified, while its `SearchRequest.sort` schema describes measured sorting and section-qualified field names. Test paging/order; do not choose whichever sentence is more convenient.
- Kit README/skeleton status and later field reports differ about live validation. Later reports show simple apps tested, not our product validated.
- Studio pages describe governed tools and durable execution; the broader draft map has older/unverified MCP and memory claims. Neither is evidence that our current toolchain can be replaced unchanged.

## Proposed architecture and migration order

```text
Custom frontend (map, timeline, chat, workstreams, evidence viewer)
    -> Application API (identity forwarding, domain contracts, coordination)
        -> i360 HL API (items, entities, media, queries, supported inference)
        -> Existing Hermes / General / Moshe orchestration initially
```

1. **Read-only proof:** authenticate an ordinary user; connect one existing evidence layer and object/media viewer; map IDs/text/time/locations; exercise map filters and both locales. Do not create new types yet.
2. **Persistent workflow proof:** after a reviewed model and dry run, save/reopen one investigation and one workstream with evidence membership, user isolation, revision conflicts and soft-deletion behavior.
3. **Agent parity proof:** keep existing routing, replace only data tools through the adapter, and prove citations, layer-opening actions, saved memory and scoped results.
4. **Playback/reliability proof:** enforce the same visibility policy in both frontend queries and tools; test concurrent Next requests, dropped SSE, reconnects, expired tokens and duplicate reevaluation prevention.
5. **Frontend migration:** replace screen by screen only after the corresponding workflow passes. Evaluate Studio and moving persistence separately rather than coupling three migrations.

This sequence is a recommendation, not an approved execution plan. Avoid a schedule estimate until data access and the first two proofs settle the largest uncertainties.

## Validation required

- Ordinary-user and two-user isolation: own/shared/denied records, GET versus search, media access, actor removal, expired session and saved-result reopening.
- Known source samples: canonical IDs, Hebrew/original text, transcript/OCR fallback, multi-location evidence, unknown relations, no future-slice evidence.
- Search/analytics: exact filter predicates, stable paging and sort, semantic-count labels, missing embeddings, unsupported geo, and empty-result warnings.
- Persistence: save/reopen, long memory/history payloads, simultaneous revisions, partial writes, removed evidence membership, deleted records still fetchable by ID.
- Agent parity: bounded scope, citation resolution, layer actions, independent General memory update, Moshe reevaluation deduplication, cancellation/retry behavior.
- Operational checks: actual dependency reachability, stream loss, model outage, media expiration/Range seek and representative latency/volume.

## Sources

All retrieved 2026-09-14. Links identify the public source; authenticated guide references remain unread unless carried in the downloaded skill.

- [Kit index](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/kit), [quickstart](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/kit/quickstart), [walkthrough](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/kit/demo)
- [Architecture](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/architecture), [runtime](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/kit/runtime), [design time](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/kit/devtime), [deployment](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/kit/deployment), [use cases](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/kit/use-cases)
- [Capability map](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map), [OpenAPI contract](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/openapi.json), [authenticated docs](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/api/v1/meta/docs)
- [Kit archive](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/kit.zip): `docs/EXTENDING.md`, `skeleton/README.md`, `STATE.md`, `patterns/attachments/README.md`, August 21 field reports and August 22 upload request. [Agent skill archive](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/skill.zip): reference index, getting started and reuse/create guides.
- [Studio](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/studio), [quickstart](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/studio/quickstart), [walkthrough](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/studio/walkthrough), [design](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/studio/design), [runtime](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/studio/runtime), [deployment](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/studio/deployment), [use cases](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/studio/use-cases)
- [Broader platform map](https://platform-hl-api.intel360.lambda.projects.e-bitbox.com/map/platform/) (draft corpus build 2026-09-10; selected AI, memory, relations and operational-entity nodes).

## Handoff and context maintenance

- Completed: documentation/source feasibility assessment. No product files changed or i360 mutations performed.
- Assumption: "rewrite our frontend" means preserve current user-visible workflows while using i360 as the data platform; removing capabilities requires a separate product decision.
- Remaining risk: authenticated behavior and production suitability are unverified; several public documents conflict.
- Next owner/action: product/architecture choose the bounded proof and the platform team supplies authenticated guide access, ordinary-user test access and answers to the blocking questions.
- Suggested durable documentation updates, after acceptance: record chosen integration boundary in `docs/architecture.md`, accepted migration choices in `docs/decisions.md`, and create the missing product-context document if the rewrite begins.
- Issue/PR status: assessment only; no implementation capability or child tasks opened. Open a parent capability and scoped validation tasks after the direction is accepted. Publish this report on a review branch with a draft PR where available.
