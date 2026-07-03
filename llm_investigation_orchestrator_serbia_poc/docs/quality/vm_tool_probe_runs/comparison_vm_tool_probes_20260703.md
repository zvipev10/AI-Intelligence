# VM Tool Probe Comparison - 2026-07-03

Artifact: `tool_probes_20260703T175042Z.json`

Completed: 13/13 probes. Runtime failures: 0.

| ID | Tool | Status | Time | Key result |
|---|---|---:|---:|---|
| `tp_01_semantic_zvecan_shooting_paraphrase` | `semantic_search_events` | pass | 396.041ms | returned 223 via lexical_tfidf |
| `tp_02_semantic_kfor_role` | `semantic_search_events` | pass | 78.684ms | returned 256 via lexical_tfidf |
| `tp_03_semantic_geographic_deception` | `semantic_search_events` | pass | 784.559ms | returned 1469 via lexical_tfidf |
| `tp_04_compare_location_claims` | `compare_location_claims` | pass | 1516.507ms | 168 conflict groups from 2150 candidate events |
| `tp_05_aggregate_municipality_hotspots` | `aggregate_events` | pass | 290.605ms | municipality: 10000 events, 10 groups |
| `tp_06_aggregate_location_first_last` | `aggregate_events` | pass | 229.665ms | location: 10000 events, 20 groups |
| `tp_07_search_force_movement_keywords` | `search_events` | warning | 1204.168ms | 2000/2401 returned; truncated=True. Search found more than 2000 records; output is truncated and requires narrowing/aggregation. |
| `tp_08_resolve_core_locations` | `resolve_location` | gap | 1.044ms | location_ids=[]. Known functional gap: broad combined location phrase does not resolve to municipality/location IDs. |
| `tp_09a_resolve_kfor` | `resolve_entity` | pass | 55.146ms | entity_ids=['ENT-KFOR'] |
| `tp_09b_resolve_kosovo_police` | `resolve_entity` | pass | 4.375ms | entity_ids=['ENT-KOSOVO-POLICE', 'ENT-KOSOVO-SPECIAL-POLICE'] |
| `tp_10_classify_semantic_investigation` | `classify_question_intent` | pass | 0.245ms | investigation / investigation / view=timeline |
| `tp_11_classify_structured_aggregation` | `classify_question_intent` | pass | 1.389ms | timeline_retrieval / retrieval / view=timeline |
| `tp_12_plan_next_frontier` | `plan_next_investigation_step` | invalid_probe | 0.262ms | continue -> expand_pending_recommended_seeds. Probe uses placeholder IDs; runner works but this probe should be replaced with real seed IDs. |

## Findings

- The VM-local direct MCP tool layer is healthy: all 13 probes executed without runtime failure.
- `semantic_search_events` returns useful volumes for all three semantic probes: 223, 256, and 1469 records.
- `compare_location_claims` is working: 2150 candidate events and 168 conflict groups.
- `aggregate_events` works for municipality aggregation and first/last location timeline support.
- `search_events` still truncates broad force-movement retrieval at 2000 out of 2401 records. This is expected under the current coverage policy and should be handled by narrowing or aggregation.
- `resolve_location` still does not resolve one broad combined query containing “צפון קוסובו, צפון מיטרוביצה, זבצ׳אן, זובין פוטוק ולפוסאביץ׳”. This is a functional gap in the resolver, not a runtime failure.
- `tp_12_plan_next_frontier` is not a valid quality probe yet because it uses placeholder event IDs.
