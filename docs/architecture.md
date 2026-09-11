# Architecture Notes

This document records durable architecture behavior that future implementation work should preserve.

## Locale-isolated runtime state

The v2.1 intelligence workspace supports Hebrew and English as separate runtime contexts.

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
- Organization presences and UAV observations are presentation descriptors;
  raw records remain the provenance source and storage unit.
- Affiliation is independent from confidence. Reported claims use a separate
  uncertainty indicator and label; the affiliation frame retains its meaning.
- UAV entity association does not establish ownership, so initial UAV symbols
  use unknown affiliation.
- This demo profile does not perform persistent object correlation or claim
  external conformance certification.

Agent-to-UI catalog action contract:

- Direct unfiltered opening uses MCP `open_catalog_layers` with an exact ID from the injected localized catalog.
- The gateway extracts the latest successful action and validates it against `list_ui_layers(locale)`.
- The result exposes `catalog_layer_actions` and `catalog_layer_action_errors`.
- The browser awaits `openCatalogLayer`, activates the layer, selects a supported view, and redraws.
- Filtered requests remain search plus `present_requested_results`; saved layers remain `present_saved_memory_layers`.
