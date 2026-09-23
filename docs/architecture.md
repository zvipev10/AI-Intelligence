# Architecture Notes

This document records durable architecture behavior that future implementation work should preserve.

## Shared runtime and scenario isolation

One canonical application package serves Kosovo and Syria; no country-specific code forks or simultaneous demo deployments. `demo_runtime.py` loads validated `demo_profiles/<scenario>.json` and binds dataset/store paths before MCP stores are imported. Profiles carry geography, localized file references, checksums, catalog sources and dataset identity. The current Syria profile is version 6 / `network-v1`; Kosovo is version 1 / `v2.1`.

| Boundary | Ownership / location |
|---|---|
| Immutable data and media | Versioned packages referenced by scenario profile; source tree remains shared |
| Application persistence | `/opt/demo-runtime/state/<scenario>/<dataset>/`: investigations, targets, evidence, assessments, playback, caches and audit |
| Browser persistence | `<scenario>:<dataset>:` storage prefix installed by `demo_bootstrap.js` before application startup |
| Agent homes | `/opt/demo-runtime/hermes-homes/<scenario>/<role>/`, selected through `demo-general`, `demo-moshe`, `demo-talia` aliases |
| Role audit | `<scenario>/<dataset>/audit/<role>.jsonl`; per-run records under `audit/runs/` |
| Active identity | `scenario_id`, `dataset_version`, `activation_generation`; control files and `active.env` select one runtime |
| Locale | Existing Hebrew/English data/store/cache isolation inside the selected scenario; omitted locale retains compatibility behavior |

Agent homes are scenario/role scoped, while application data and audits are also dataset scoped. Do not describe an unchanged role home as a fresh dataset-specific agent memory. Provider credentials may be carried between corresponding roles at a stopped scenario transition to avoid stale OAuth tokens; this is distinct from copying conversations or learned scenario memory.

`activate_demo.py` verifies installed release/profile/state/cache compatibility, locks activation, enters maintenance, drains work, then stops UI, dashboard and gateway. The dashboard owns MCP workers too. Selection updates aliases, environment, gateway tool registry and **each role's audit path**. Readiness checks UI/gateway/catalog and actual role identity/counts before committing current identity and reopening admission. Stale tabs receive HTTP 409 and must reload. Failed readiness restores the prior selection with a fresh generation; boot recovery preserves maintenance until verification.

The installed Hermes root registry must contain tool definitions bound to the active scenario even though roles use named homes. Updating profile files alone is insufficient. The audit-path update prevents an old dataset directory receiving tool results while the UI reads the new directory.

A shared reentrant execution gate serializes application agent work, with a queue of eight, cancellation for queued requests and foreground priority with aging. It includes interactive, specialist, optional OpenAI and application background jobs, but does not regulate unrelated messaging integrations. On the constrained VM, semantic indexes are built offline and checksummed; missing/stale caches fail explicitly rather than building during requests. Inactive scenario packages/state remain on disk without a second resident runtime.

Operational commands and release/rollback rules are in the [scenario runbook](../llm_investigation_orchestrator_serbia_poc/docs/demo-scenarios.md).

## Result presentation and raw source fields

`map`, `timeline` and `table` are valid agent presentation choices for requested results, supporting evidence references and catalog actions. English/Hebrew instructions choose spatial, chronological or record/identifier presentation accordingly. Legacy view `evidence` aliases to Table; evidence object kinds are unchanged.

The standalone Table tab reuses the same raw-results table DOM, selected layer, filters, sorting and record viewer as the Map/Timeline overlay. Table mode changes layout rather than cloning the component. Geometry-free records retain their IDs and open-record actions; map capability is derived from available locations for raw catalog/materialized/saved rows. IPDR's source-specific table and viewer expose native IP/IMEI and session fields, not inferred actor/location; identifiers remain strings.

`present_requested_results` materializes selected canonical rows and their recommended view. `agent_result_pipeline.py` preserves the structured presentation through audit parsing. Whole/filtered catalog actions and saved-memory actions use their own contracts; the browser reports actual loading success/failure. Presentation never implies a target or assessment mutation.

## Basemap composition

The MapLibre client keeps basemap references separate from analytical presentation.

- Satellite is the initial default; Street mode uses the native CARTO Voyager vector style.
- Name-based labels prefer English at every zoom, falling back to available names where English is missing.
- Basemap imagery is geographic context, independent of timestamped synthetic Satellite source records; retain provider attribution.
- Satellite mode places Esri World Imagery below selected CARTO `transportation` and `boundary` line layers and CARTO symbol/label layers.
- Satellite-specific paint is presentation-only and must be restored from the captured CARTO layer definitions when Street mode is selected.
- Application-created operational layers, result routes, markers, and MIL-STD symbols are not part of `state.basemapLayers` and must not be hidden or restyled by basemap switching.
- Satellite-source failure must fail visibly and restore Street mode.
- Scenario profiles own the initial camera. The Syria `network-v1` profile uses Damascus `[36.2765, 33.5138]` at zoom `11`; data presentation remains free to fit the camera to result geometry.

## Locale-isolated runtime state

Hebrew and English remain separate runtime contexts within the selected scenario. The v2.1 paths below describe the Kosovo implementation; resolve scenario roots through `DemoRuntime`, rather than hard-coding Kosovo paths for Syria.

- Immutable runtime data is selected by locale and dataset version.
- MCP runtime bundles are locale-specific and fail closed if English assets are missing or invalid.
- Semantic caches are isolated by locale, dataset version, and source checksum identity.
- Mutable target persistence uses separate Hebrew and English SQLite databases.
- Mutable workstream persistence uses separate Hebrew and English roots:
  - `workstreams/v2_1/he/`
  - `workstreams/v2_1/en/`
- Legacy untagged/shared workstream records are treated as Hebrew-owned fallback data.
- English persisted presentation/evidence/workstream fields reject Hebrew characters before write.

Hebrew remains the compatibility default for omitted locale values. New English flows must pass explicit locale and must not fall back to Hebrew data.

## Unified staged playback

Playback uses one staged flow. The previous user-facing distinction between historical mode and real-time mode has been removed.

Runtime contract:

- `/api/playback` reports `mode: "real_time"` for the unified staged flow.
- `/api/playback/mode` accepts older `mode: "historical"` payloads as compatibility input, but routes them to staged playback.
- The first baseline window starts at the dataset beginning and ends at the first scenario slice boundary.
- The current Brnjak v2.1 first visible window is:
  - from `2026-09-12T04:25:50.096250Z`
  - to `2026-09-17T06:00:00Z`
- Pressing Next advances the cumulative `visible_timeframe`.
- Moshe reevaluation is skipped when the baseline is created.
- Moshe reevaluation can run only after a later slice arrives and active workstreams exist.
- A separate general-agent memory update can run after a later slice when the
  selected investigation has non-empty saved memory.
- General memory updates are revision-scoped background jobs and receive only
  saved investigation memory plus playback timeframe context; they do not
  receive workstreams, Moshe assessments, or target-bank state.
- General memory-update lifecycle and output are exposed through the playback
  status payload and rendered only in chat.

Visibility contract:

- UI data-layer queries must filter rows by the active playback `visible_timeframe`.
- MCP/data queries must respect `active_visibility.json` when active.
- The active playback run and visibility policy are global for the deployed UI/MCP process.
- Investigation selection changes request and UI context only; it does not select or create a separate playback run.
- `/api/playback`, `/api/playback/mode`, and `/api/playback/next` resolve the same active global run across investigations.
- Production smoke or diagnostics that alter `active_visibility.json` must restore the previous policy before completion.

UX contract:

- The UI shows staged playback as one control state.
- The timeframe remains visible.
- The Next button remains available while there is a next slice.
- The UI must not reintroduce a historical-vs-real-time mode selector without a new product/architecture decision.

MIL-STD presentation contract:

- The canonical entity layer adds location-level `presence_claim`,
  `presence_evidence_count`, `assessment_status`, `confidence`,
  `latest_timestamp_utc`, and bounded `evidence_record_ids` fields.
- The client maps the approved 12 organization IDs and four UAV object classes
  through a versioned `MIL_STD_*` registry.
- Organization presences and normalized evidence observations/fusions are
  presentation descriptors; raw event layers use neutral location markers and
  raw records remain the provenance source and storage unit.
- Affiliation is independent from confidence. Reported claims use a separate
  uncertainty indicator and label; the affiliation frame retains its meaning.
- UAV entity association does not establish ownership, so initial UAV symbols
  use unknown affiliation.
- This demo profile does not perform persistent object correlation or claim
  external conformance certification.

Evidence contract:

- A raw `REC-*` record remains immutable provenance. It can be projected on
  demand into a normalized `reported` or `observed` `EVD-*` object without
  creating a second stored copy of every raw record.
- Neutral fusion creates a stable `EVD-FUSED-*` identity from its sorted source
  records and preserves both supporting and contradicting evidence links.
- Fused evidence may be persisted only after deterministic validation: one
  canonical subject, location, and structured object class, plus at least two
  independent supporting source groups and the existing temporal/confidence
  fusion checks.
- Evidence and raw layers remain demand-driven. Evidence uses the existing
  map, table, timeline, and object-viewer presentation paths; it does not imply
  target status or an enemy assessment.
- Target preparation delegates its neutral correlation work to the evidence
  fusion path, then applies Moshe's separate target-authorization boundary.
- For the fixed v2.1 demo dataset, UI deployment builds a versioned evidence
  catalog artifact for Hebrew and English. The layer catalog advertises it as
  `evidence:all`; presentation remains demand-driven and requires no live
  semantic search or fusion. The Hebrew catalog is also the read seed of the
  MCP evidence repository, while SQLite is its writable overlay, so Talia and
  the UI resolve the same deterministic fused evidence IDs.
- All raw rows are processed, but the catalog does not duplicate every
  unstructured public report as a symbol. It contains UAV observations, exact
  structured public extractions, and validated fused evidence; other reports
  remain accessible through their raw source layers.
- Evidence preparation preserves structured object classes and resolves a
  missing class through the same semantic concept vocabulary used by semantic
  event retrieval. Deployment-time fusion applies this normalization and
  groups records by canonical location, entity, normalized object class, and
  an eight-hour rolling window. Fused rows still require the existing source
  grouping and persistence checks.
- The layer manifest supplies catalog counts without loading the roughly 4 MB
  row artifact. Rows are loaded only when the evidence layer is opened and are
  filtered by the active playback timeframe.
- Evidence map rendering coalesces equivalent location/symbol/affiliation
  descriptors and renders at most 400 evidence symbols at once. This bound
  affects only the map; the full catalog remains available in table, timeline,
  viewer, and provenance paths.

Agent-to-UI catalog action contract:

- Named catalog opening uses MCP `open_catalog_layers`; the live resolver returns canonical IDs for exact/unique close matches, requests clarification for ambiguity and fails closed when the catalog is unavailable.
- The gateway extracts the latest successful action and validates it against `list_ui_layers(locale)`.
- The result exposes `catalog_layer_actions` and `catalog_layer_action_errors`.
- The browser awaits `openCatalogLayer`, activates the layer, selects a supported view, and redraws.
- Supported location/entity/event/time constraints travel in `open_catalog_layers.filters`, preserving scope through loading, saved reconstruction and refresh. Other predicates use retrieval plus explicit result IDs/`present_requested_results`; saved layers remain `present_saved_memory_layers`.
