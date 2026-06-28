# AI Intelligence Project Handoff

Last updated: 2026-06-27

This is the primary handoff for continuing the AI Intelligence project in another assistant/chat. It reflects the current `main` branch workspace and the latest VM deployment state after the data normalization, source-layer UI refactor, and result-layer architecture work.

## One-Line Summary

The active project is the Serbia/North Kosovo intelligence-analysis POC: a Hebrew analyst UI backed by Hermes and MCP tools over a 10,000-record synthetic event corpus. The UI now treats all visualization outputs as layers: event-source layers, location-summary layers, and time-aggregation layers can be shown/hidden and rendered according to their own map/timeline/table capabilities.

## Repository And Current State

Repository:

- `https://github.com/zvipev10/AI-Intelligence`

Current branch:

- `main`
- Latest observed head: merge commit `849a829 Merge pull request #1 from zvipev10/app-v2-agent-steps-in-chat`

Important local workspace:

- Active repo path used by Codex: `C:\Users\user\Documents\AI Intelligence\.codex_ai_intelligence_repo`
- The parent folder `C:\Users\user\Documents\AI Intelligence` may contain other/older files; use `.codex_ai_intelligence_repo` for this project.

Current local working tree has intentional uncommitted work:

- UI changes in `llm_investigation_orchestrator_serbia_poc/index.html`
- UI changes in `llm_investigation_orchestrator_serbia_poc/app.js`
- UI changes in `llm_investigation_orchestrator_serbia_poc/styles.css`
- Gateway fixes in `llm_investigation_orchestrator_serbia_poc/server.py`
- MCP/source normalization updates in `llm_investigation_orchestrator_serbia_poc/mcp_server/*.py`
- Data normalization files under `llm_investigation_orchestrator_serbia_poc/data/`
- New normalizer: `llm_investigation_orchestrator_serbia_poc/data/normalize_sources.py`
- New report: `llm_investigation_orchestrator_serbia_poc/data/source_normalization_report.json`

Do not assume these changes are committed.

## Active POC

Serbia / North Kosovo POC:

- Directory: `llm_investigation_orchestrator_serbia_poc`
- Local UI: `http://127.0.0.1:8769/`
- VM UI: `https://151.145.93.180/`
- Purpose: scenario-portability demo over North Kosovo escalation data, with analyst questions, data-grounded MCP tools, agent-step visibility, and map/timeline/table result presentation.

Cargo POC still exists but is not the active focus:

- Directory: `llm_investigation_orchestrator_poc`
- Local UI: `http://127.0.0.1:8768/`

## Current VM Deployment

VM:

- Host: `151.145.93.180`
- User: `ubuntu`
- SSH key path used locally: `C:\Users\user\Downloads\oracle.key`
- Important: user explicitly said not to touch/modify the key file.

Active UI service:

- Service: `serbia-poc-ui.service`
- Actual served path: `/opt/serbia-poc-ui`
- This is important: an earlier deploy mistakenly copied to `/opt/serbia-poc/ui`, but the active service serves `/opt/serbia-poc-ui`.
- Current served versions verified through the public HTTPS endpoint:
  - `styles.css?v=35`
  - `app.js?v=47`

Active MCP/Hermes service:

- MCP path: `/opt/serbia-poc/mcp_server/server.py`
- Data path: `/opt/serbia-poc/data/serbia_kosovo_events_projection.csv`
- Hermes gateway service: `hermes-gateway.service`
- Hermes local API port on VM: `127.0.0.1:8642`

Useful VM checks:

```bash
sudo systemctl is-active serbia-poc-ui.service
sudo systemctl is-active hermes-gateway.service
curl -k -fsS https://151.145.93.180/ | grep -E 'styles.css\?v=|app.js\?v='
curl -fsS http://127.0.0.1:8769/api/status
curl -fsS http://127.0.0.1:8769/api/live-steps
grep -n 'rawEventsOverlay\|final-answer-show-btn\|buildLocationLayer' /opt/serbia-poc-ui/app.js /opt/serbia-poc-ui/index.html
```

## Deployment Notes

Use `/opt/serbia-poc-ui` for UI deploys.

When generating `/opt/serbia-poc-ui/.hermes-api.json`, write it as UTF-8 without BOM. The gateway now reads it with `utf-8-sig`, but no-BOM is still preferred.

Known fixed issue:

- A PowerShell-generated `.hermes-api.json` caused: `Unexpected UTF-8 BOM (decode using utf-8-sig)`.
- Fix implemented in `server.py`: `load_hermes_config()` reads config using `encoding="utf-8-sig"`.
- The deployed config was also rewritten without BOM.

Recommended UI deployment pattern:

1. Preserve the existing API key from `/opt/serbia-poc-ui/.hermes-api.json` or Hermes config.
2. Package `server.py`, `index.html`, `app.js`, `styles.css`, `help.html`, `README.md`, `vendor/`, and `data/`.
3. Copy to `/opt/serbia-poc-ui`.
4. Restart `serbia-poc-ui.service`.
5. Verify served versions through the public HTTPS endpoint, not only disk files.

## Current UI Architecture

The UI has been refactored from “views over current records” into a layer-based result model.

Core idea:

```text
tool/final result
  -> result layers
  -> map/timeline/table render each visible layer according to capability
```

Current layer types:

- `events`
  - One layer per `source_type`, e.g. `טלגרם`, `X`, `חדשות מקומיות`.
  - Capabilities: table, map, timeline.
- `locations`
  - Static location-summary layer, e.g. `ריכוזי מיקומים`.
  - Capabilities: table, map.
  - Not filter-derived from source tabs unless backing events exist in an event layer.
- `time_aggregation`
  - Static time aggregation layer, e.g. summary by date/hour.
  - Capabilities: table, timeline.

Important functions in `app.js`:

- `buildEventLayers(events)`
- `buildLocationLayer(locations)`
- `buildTimeAggregationLayer(items)`
- `setResultLayers(...)`
- `visibleLayers(capability)`
- `activeTableLayer()`
- `renderMap()`
- `renderTimeline()`
- `renderEvidence()`

Current UI behavior:

- The raw/results table is an overlay shared by map and timeline.
- Table tabs are layer tabs, not source-type-only tabs.
- Each layer tab has an eye toggle.
- Hiding a layer affects all visualizations where that layer participates.
- The overlay can be resized and minimized.
- Final assistant answers now have a `הצג` button.
- Clicking final `הצג` restores that answer’s result presentation and clears any open step-view banner.
- Tool steps still have `הצג` buttons that present the step’s specific result/layers.

Removed UI sections:

- Removed the former result summary header (`תמונת מצב`, `ממצאי חקירת הסוכן`, event count badge) from the top of the result panel.
- Removed the old separate `אירועים גולמיים` top-level view tab.
- Removed extra bottom query/layer labels that duplicated information.

## Data Normalization

The active data was normalized to remove confusing/non-real source categories.

Removed field:

- `source_category`

Removed source/source-like labels from active data:

- `דיסאינפורמציה/מידע מטעה`
- `רעש לא קשור`
- `דיווח אזרחי`
- `דיווח חירום`

Approved visible `source_type` values:

- `פייסבוק`
- `חדשות מקומיות`
- `X`
- `בלוג פוליטי`
- `טלגרם`
- `הודעת דובר`
- `טיקטוק`
- `ערוץ חדשות בינלאומי`
- `שמועה מקומית`
- `קבוצת וואטסאפ`

Active source counts after normalization:

```text
1307 חדשות מקומיות
1280 טלגרם
1074 טיקטוק
1017 שמועה מקומית
 970 X
 912 קבוצת וואטסאפ
 887 הודעת דובר
 875 בלוג פוליטי
 870 פייסבוק
 808 ערוץ חדשות בינלאומי
```

Normalized active files:

- `data/north_kosovo_attachment_inspect/north_kosovo_synthetic_dataset_he_10k_subset.csv`
- `data/north_kosovo_attachment_inspect/north_kosovo_synthetic_dataset_he_10k_subset.jsonl`
- `data/serbia_kosovo_events_projection.csv`
- `data/serbia_kosovo_evaluator_labels.csv`

Normalizer/report:

- `data/normalize_sources.py`
- `data/source_normalization_report.json`

Validation already performed:

- Active data row count preserved: `10000`.
- Core fields preserved: `timestamp`, `location_id`, `event_id`, `text`.
- No active-data matches for removed labels or `source_category`.

Historical backup/test/recorded files may still contain old terms. Do not treat those as active runtime data.

## Model Prompt And MCP Schema Updates

The model/gateway prompt and MCP schema were updated so source examples match the normalized data.

Updated:

- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`

Removed stale examples such as:

- SIGINT
- financial alerts
- sensors
- port/customs records

Current guidance uses visible channels such as:

- `טלגרם`
- `טיקטוק`
- `X`
- `פייסבוק`
- `חדשות מקומיות`
- `הודעת דובר`
- `קבוצת וואטסאפ`
- `שמועה מקומית`
- `בלוג פוליטי`
- `ערוץ חדשות בינלאומי`

## MCP Tools

Current Serbia MCP tools:

```text
classify_question_intent
plan_next_investigation_step
search_events
get_events
resolve_location
resolve_event_reference
find_actor_history
aggregate_events
explain_linkage
build_event_sequence
resolve_entity
trace_identifier
trace_semantic_clues
find_related_events
compare_location_claims
challenge_hypothesis
```

Tool outputs can include:

- `events` / `event_ids`
- `locations` / `location_ids`
- `map_locations`
- `aggregate_groups`
- `route`
- `ordered_event_ids`
- `recommended_next_seeds`
- `new_clues_to_trace`
- `conflict_groups`
- `alternative_events`
- `gaps`
- `bridges`
- entity resolver matches

Visualization architecture now treats displayable outputs as layers.

First-class display-layer candidates:

- events
- locations
- time aggregations

Potential future layer types:

- routes/sequences
- conflict groups
- entity/actor presence
- link/bridge relationships
- semantic clue clusters

## Entities

There is no `entity_id` column in the active DB/data files.

Active data fields:

- Projection CSV has `entity_or_actor`.
- Raw dataset has `actor_mentioned` and `observed_actor`.
- There are 16 unique actor names in the current data.

There is a small synthetic resolver registry in MCP code:

- `ENT-KFOR`
- `ENT-EULEX`
- `ENT-KOSOVO-POLICE`
- `ENT-SERBIAN-ACTORS`

These are code-level aliases, not first-class DB rows.

## Data Policy

Visible runtime data:

- `serbia_kosovo_events_projection.csv`
- `serbia_kosovo_locations.json`

Evaluation-only hidden labels:

- `serbia_kosovo_evaluator_labels.csv`

Do not expose evaluator labels to the orchestrator, MCP runtime, UI, or prompt. They include ground truth and misleading labels that would contaminate the intelligence-analysis scenario.

## Current Result Presentation Behavior

Current behavior:

- Tool-step `הצג` presents the selected step’s results.
- Final-answer `הצג` presents/restores the final answer’s result layers.
- Answer arrival still applies the final result presentation automatically in most paths, but a recent observed issue showed an answer could return without a new visible presentation. The final `הצג` button was added first; next design decision is how forceful/automatic final-answer presentation should be.

Open design question:

- When a final answer arrives, should the result panel always switch to the final answer’s layers, or should it preserve the current step/layer view until the user clicks final `הצג`?

Suggested next behavior:

- Do not silently override an explicitly selected tool-step view.
- If no step view is active, final answer should update result layers automatically.
- Always provide final `הצג` as a reliable manual restore.

## Near-Term RAG Plan

The team discussed adding a small RAG capability in the near future. This should be a focused retrieval-layer improvement, not a large architecture rewrite.

Goal:

- Improve semantic recall over the 10,000 event records and later over tool outputs/layer objects.
- Let the retrieval layer find records based on real corpus similarity rather than only general model reasoning or keyword matching.
- Keep deterministic filtering, IDs, and auditability.

Recommended near-term implementation:

1. Add a lightweight local semantic index over active event text.
   - Index fields: `event_id`, `event_summary`, `entity_or_actor`, `location_name`, `source_type`, `timestamp_utc`.
   - Store metadata needed for filters: time, location, source type, actor, reliability/certainty.
   - Keep `REC-*` IDs as the canonical join key.

2. Use hybrid retrieval, not vector-only retrieval.
   - Existing keyword/filter tools stay.
   - Add semantic candidate retrieval.
   - Fuse/rerank candidates deterministically where possible.

3. Expose through MCP as a bounded tool, not raw vector DB access.
   - Candidate tool name: `semantic_search_events` or `retrieve_event_context`.
   - Input: query/clues, optional time/location/source filters, limit.
   - Output: `event_ids`, `events`, scores, matched terms/semantic rationale.
   - UI can render returned events as normal event layers.

4. Keep RAG evidence auditable.
   - Every result must map back to `REC-*`.
   - Do not return anonymous chunks with no record ID.
   - Final answers must cite event IDs when evidence is used.

5. Start small.
   - Do not introduce Elastic/OpenSearch unless the project grows beyond the current POC.
   - For this corpus size, a local file-based or lightweight vector index is enough.
   - The implementation can be regenerated from CSV during deploy/startup.

Possible stack options:

- Local embeddings using a small multilingual embedding model if available in the deployment environment.
- SQLite + vector extension, FAISS/HNSW, or a simple persisted embedding matrix for POC scale.
- If model/runtime constraints make local embeddings hard, defer embedding generation and first implement lexical+semantic clue expansion using existing fields.

RAG integration with layers:

- RAG returns event IDs and events.
- The UI creates normal event layers by `source_type`.
- Later, RAG can return a separate “semantic cluster” layer if we want to visualize retrieved themes.

Do not do yet:

- Do not expose raw vector queries to the model.
- Do not make RAG replace MCP tools.
- Do not make RAG decide truth.
- Do not use hidden evaluator labels for retrieval.

## Validation Commands

From repo root:

```powershell
cd llm_investigation_orchestrator_serbia_poc
node --check app.js
& "C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m py_compile server.py mcp_server/server.py mcp_server/benchmark_tools.py mcp_server/regression_quality.py
git diff --check
```

MCP smoke test:

```powershell
$env:PYTHONIOENCODING='utf-8'
& "C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" mcp_server\smoke_client.py
```

Data validation:

```powershell
Select-String -Path `
  data\north_kosovo_attachment_inspect\north_kosovo_synthetic_dataset_he_10k_subset.csv,`
  data\north_kosovo_attachment_inspect\north_kosovo_synthetic_dataset_he_10k_subset.jsonl,`
  data\serbia_kosovo_events_projection.csv,`
  data\serbia_kosovo_evaluator_labels.csv `
  -Pattern 'source_category|דיסאינפורמציה/מידע מטעה|רעש לא קשור|דיווח אזרחי|דיווח חירום' -SimpleMatch
```

Expected: no matches in active data files.

## Known Risks / Watch Items

1. Layer architecture is new.
   - Test map/timeline/table after each result path: live answer, recorded answer, tool-step `הצג`, final-answer `הצג`.

2. Static location layers are intentionally not source-filtered.
   - They are peer layers, not derived event filters.
   - Eye toggle hides/shows the whole location layer.

3. VM deploy path confusion.
   - Use `/opt/serbia-poc-ui`, not `/opt/serbia-poc/ui`.

4. Config BOM.
   - Write `.hermes-api.json` without BOM.
   - `server.py` now tolerates BOM via `utf-8-sig`.

5. Historical files still contain old source labels.
   - Active data is clean; historical test/recorded files may not be.

6. Entity IDs are not in DB.
   - Treat entities as future layer candidates only after adding first-class entity data.

## Suggested First Message To A New Assistant

```text
Read PROJECT_HANDOFF.md first. Continue work on the Serbia/North Kosovo POC in llm_investigation_orchestrator_serbia_poc. The current branch is main. The UI is deployed from /opt/serbia-poc-ui on VM 151.145.93.180 and currently serves styles.css?v=35 and app.js?v=47. Do not touch C:\Users\user\Downloads\oracle.key. The UI now uses a layer architecture; preserve that model when adding new filters or visualizations.
```

## File Review Order

For UI/layer work:

1. `llm_investigation_orchestrator_serbia_poc/index.html`
2. `llm_investigation_orchestrator_serbia_poc/styles.css`
3. `llm_investigation_orchestrator_serbia_poc/app.js`
4. `llm_investigation_orchestrator_serbia_poc/server.py`

For agent/tool behavior:

1. `llm_investigation_orchestrator_serbia_poc/server.py`
2. `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`
3. `llm_investigation_orchestrator_serbia_poc/mcp_server/smoke_client.py`
4. `llm_investigation_orchestrator_serbia_poc/mcp_server/regression_quality.py`

For data normalization:

1. `llm_investigation_orchestrator_serbia_poc/data/normalize_sources.py`
2. `llm_investigation_orchestrator_serbia_poc/data/source_normalization_report.json`
3. Active CSV/JSONL files under `llm_investigation_orchestrator_serbia_poc/data/`

## Final Sanity Checklist Before Future Handoff

- Run `git status --short --branch`.
- Verify served VM asset versions through the public HTTPS endpoint, not just disk.
- Verify `serbia-poc-ui.service` is active.
- Verify `/api/live-steps` returns JSON.
- If MCP changed, run smoke test before deploy.
- If data changed, run active-data forbidden-label search.
- Do not expose evaluator labels.
- Do not touch the SSH key file.
