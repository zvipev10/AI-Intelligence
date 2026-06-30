# AI Intelligence Project Handoff

Last updated: 2026-06-29

This is the primary handoff for continuing the AI Intelligence project in another assistant/chat. It reflects the current `main` branch workspace and the latest VM deployment state after the data normalization, additive result-layer UI refactor, recorded-run refresh, map marker popup work, and Phase 2 query builder planning.

## One-Line Summary

The active project is the Serbia/North Kosovo intelligence-analysis POC: a Hebrew analyst UI backed by Hermes and MCP tools over a 10,000-record synthetic event corpus. The UI now treats all visualization outputs as additive layers: event-source layers, location-summary layers, group-aggregation layers, and time-aggregation layers can be shown/hidden/closed and rendered according to their own map/timeline/table capabilities.

## Repository And Current State

Repository:

- `https://github.com/zvipev10/AI-Intelligence`

Current branch:

- `main`
- Latest observed head should be checked with `git log -1 --oneline`; the repo is expected to be clean and aligned with `origin/main` after each handoff.

Important local workspace:

- Active repo path used by Codex: `C:\Users\user\Documents\AI Intelligence\.codex_ai_intelligence_repo`
- The parent folder `C:\Users\user\Documents\AI Intelligence` may contain other/older files; use `.codex_ai_intelligence_repo` for this project.

Current local working tree expectation:

- `main` should be clean and aligned with `origin/main`.
- This handoff was updated from a fresh GitHub clone, not from the older local working copy.
- Latest observed pre-handoff GitHub head before this handoff update: `9a3b5c6 Use standard visibility icons`.
- Do not continue from stale local files if `git fetch origin main` shows remote commits ahead.

**Important sync lesson (2026-06-29):** A stale local workspace and stale VM deployment briefly reintroduced old behavior: rectangular map markers and automatic final-answer presentation. GitHub already had the correct point-marker/manual-show behavior, but the VM was still serving older `styles.css?v=36` and `app.js?v=48`. Before every deploy, fetch GitHub, verify `git status --short --branch`, and deploy from the current committed `main`, not from stale uncommitted local files.

**Latest UI completion note (2026-06-29):** Map markers are colored points with popups; final-answer results are not presented automatically and are shown only via the final `הצג תוצאות` button. Result layers are shown in a flush transparent tabbed overlay attached to the map/timeline borders. Each layer appears as a real tab with a standard `×` close control, and the whole overlay uses standard window controls: `−` minimize, `□` restore/maximize, and `×` close/clear. Step presentation controls moved into each step card: a text button toggles between `הצג תוצאות` and `הסתר תוצאות`, and `הצג שאילתה` opens the query modal. Current deployed asset versions are `styles.css?v=52` and `app.js?v=68`.

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
- Current served versions verified on the VM after the latest UI deploy (as of 2026-06-29):
  - `styles.css?v=52`
  - `app.js?v=68`
- These versions include colored point markers, manual final-answer presentation via `הצג תוצאות`, additive layer tabs, table resize/minimize, close/clear result-window behavior, query edit modal controls, `הצג תוצאות` / `הסתר תוצאות` controls styled identically to `הצג שאילתה` without the old square icon-button class, real tabbed result layers, standard tab/window close controls, and shared standard table visibility icons.

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

1. Run `git fetch origin main` and confirm local `main` is aligned with `origin/main`.
2. Preserve the existing API key from `/opt/serbia-poc-ui/.hermes-api.json` or Hermes config.
3. Package committed files only: `server.py`, `index.html`, `app.js`, `styles.css`, `help.html`, `README.md`, `vendor/`, `data/`, `recorded_runs/`, and `mcp_server/` when needed.
4. Copy to `/opt/serbia-poc-ui`.
5. Restart `serbia-poc-ui.service`.
6. Verify served versions through the public HTTPS endpoint, not only disk files.
7. Never deploy from a stale local working tree with uncommitted old UI files.

## Recorded Demo Runs

Recorded demo runs are served by the UI backend from:

```text
llm_investigation_orchestrator_serbia_poc/recorded_runs/
```

Each recording is a JSON file with this shape:

```json
{
  "id": "q2_movement",
  "question": "analyst question shown in the replay modal",
  "title": "short title shown in the replay modal",
  "recorded_at_utc": "2026-06-28T12:56:18Z",
  "elapsed_ms": 171554,
  "source": "live_hermes_run_main_rerun_YYYYMMDD",
  "result": {
    "run_id": "run_...",
    "answer": "...",
    "event_ids": [],
    "answer_event_ids": [],
    "recommended_view": "map",
    "view_reason": "...",
    "investigation_steps": [],
    "events": [],
    "usage": {}
  }
}
```

The UI exposes recordings through:

```text
GET /api/recorded-questions
GET /api/recorded-run?id=<recording-id>
```

The browser replays the saved `investigation_steps` at `replay_delay_ms` from `/api/recorded-questions` currently 2000 ms per step, then renders the saved final answer and result layers. Follow-up questions after a recording are sent as real live questions; the replayed user/assistant messages are added to chat history before the next live request.

Create or refresh a recording from a real local run:

```powershell
cd llm_investigation_orchestrator_serbia_poc
$env:PYTHONPATH=(Resolve-Path ..\.tools\python).Path
$env:PYTHONIOENCODING='utf-8'
& "C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" server.py 8769
```

In another PowerShell window:

```powershell
$question = "האם ניתן לזהות דפוס של תנועת כוחות או הגברת נוכחות בזמן ובמרחב?"
$body = @{
  prompt = $question
  history = @()
  investigation_id = "recording-q2-$(Get-Date -Format yyyyMMddHHmmss)"
} | ConvertTo-Json -Depth 20
$started = Get-Date
$result = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8769/api/investigate" -ContentType "application/json; charset=utf-8" -Body $body
$elapsed = [int]((Get-Date) - $started).TotalMilliseconds
$recording = [ordered]@{
  id = "q2_movement"
  question = $question
  title = "תנועת כוחות והגברת נוכחות"
  recorded_at_utc = (Get-Date).ToUniversalTime().ToString("o")
  elapsed_ms = $elapsed
  source = "live_hermes_run_main_rerun_$(Get-Date -Format yyyyMMdd)"
  result = $result
}
$recording | ConvertTo-Json -Depth 100 | Set-Content -Encoding utf8 "recorded_runs\q2_movement.json"
```

After saving a recording, verify it locally:

```powershell
Invoke-RestMethod "http://127.0.0.1:8769/api/recorded-questions"
Invoke-RestMethod "http://127.0.0.1:8769/api/recorded-run?id=q2_movement"
```

Then open `http://127.0.0.1:8769/`, press the `+` recorded-questions button, and replay the refreshed question. Check that:

- The question appears in the modal.
- Steps replay at roughly two seconds per step.
- Final answer, event IDs, map/timeline/table layers, and per-step `הצג` all work.
- The saved result does not contain failed/partial runs.

Deploy recordings with the UI. Include the whole `recorded_runs/` directory in the package copied to `/opt/serbia-poc-ui/recorded_runs`. No Hermes/MCP restart is required for recording-only changes; restart `serbia-poc-ui.service` because recordings are served by the UI backend.

Recommended VM recording verification:

```bash
curl -k -fsS https://151.145.93.180/api/recorded-questions
curl -k -fsS "https://151.145.93.180/api/recorded-run?id=q2_movement" | head -c 500
```

Do not generate demo recordings from synthetic fallback data or manually shortened answers. The recording must come from a real `/api/investigate` Hermes run so it preserves the actual answer, step explanations, tool outputs, result layers, and usage/performance metadata.

## Current UI Architecture

The UI has been refactored from “views over current records” into an additive layer-based result model.

Core idea:

```text
tool/final result
  -> result layers
  -> map/timeline/table render each visible layer according to capability
```

Layer identity model:

- Every displayed layer has a `sourceId` and a `dataId`.
- `sourceId` identifies where the layer came from: a specific final assistant answer or a specific investigation step.
- `dataId` identifies the visual data inside that source, for example event-source layer, location-summary layer, date aggregation, or generic aggregation.
- The concrete layer key is built from `sourceId + dataId`.
- Pressing `הצג` is additive: it adds related layers without replacing currently displayed layers.
- Pressing the same `הצג` again re-shows/focuses existing layers instead of duplicating them.
- If a layer was closed with `x`, pressing the same `הצג` recreates it.
- Layer colors are assigned automatically from a palette and released when the layer is closed.

Current layer types:

- `events`
  - One layer per `source_type`, e.g. `טלגרם`, `X`, `חדשות מקומיות`.
  - Capabilities: table, map, timeline.
- `locations`
  - Location-summary layer, e.g. `ריכוזי מיקומים`.
  - Capabilities: table, map.
  - Not filter-derived from source tabs unless backing events exist in an event layer.
- `time_aggregation`
  - Time aggregation layer, e.g. summary by date/hour.
  - Capabilities: table, timeline.
- `group_aggregation`
  - Generic aggregation layer, e.g. grouping by actor/source/category when it is not a map or timeline group.
  - Capabilities: table.

Important functions in `app.js`:

- `buildEventLayers(events)`
- `buildLocationLayer(locations)`
- `buildTimeAggregationLayer(items)`
- `buildGroupAggregationLayer(items)`
- `buildResultLayers(...)`
- `addResultLayers(...)`
- `finalSourceId(result)`
- `stepSourceId(resultOrBase, stepNumber)`
- `visibleLayers(capability)`
- `activeTableLayer()`
- `renderMap()`
- `renderTimeline()`
- `renderEvidence()`

Current UI behavior:

- The raw/results table is a transparent overlay shared by map and timeline, flush with the map/timeline borders.
- Table tabs are real layer tabs, not source-type-only pills.
- Each layer tab has a standard eye/eye-off toggle.
- Each layer tab has a standard `×` close control.
- Each layer tab displays the layer color.
- Hiding a layer affects all visualizations where that layer participates.
- Closing a layer removes it from the current workspace and releases its color.
- The overlay can be resized, minimized with `−`, restored/maximized with `□`, and closed/cleared with `×`.
- Final assistant answers have a `הצג תוצאות` button styled like the step action pills.
- Clicking final `הצג תוצאות` adds or focuses that answer’s result layers without automatically overriding the current visual state on answer arrival.
- Tool steps use `הצג תוצאות` / `הסתר תוצאות` for step result layers and `הצג שאילתה` for query/tool details.
- Map locations are shown as colored point markers, not always-open rectangles.
- Clicking a map point opens a MapLibre popup with the location name, item count, and contributing layer labels.

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

- Tool-step `הצג` presents the selected step's results/layers.
- Final-answer `הצג תוצאות` presents/restores the final answer's result layers.
- Final answer arrival does **not** automatically replace the current map/timeline/table presentation. This is intentional: the analyst decides when to present the final answer's layers.
- `applyHermesResult(..., { restoreOnly: true })` is the path used by final `הצג תוצאות` to build/show final-answer layers.
- Normal final-answer arrival only finalizes the chat answer and keeps visualization state under user control.

Design decision:

- Preserve the current step/layer view until the user clicks final `הצג תוצאות`.
- Do not silently override an explicitly selected tool-step view.
- Keep final `הצג תוצאות` as the reliable manual restore/presentation action.

## Phase 2: Query Builder — Editable Query Form

**Status:** Step 1 UI foundation and query edit modal controls exist in current `main`. Future work should continue from the committed GitHub state, not from older local snapshots.

**Objective:** Transform the query display from read-only JSON (`<pre>` modal) to an editable form component with smart "Run New Query" button visibility.

**Key Changes in Step 1:**

1. Remove result data from query object: `event_ids`, `map_locations`, `aggregate_groups` no longer appear in `queryReadoutForLayer()` payload.
2. Replace modal `<pre>` element with form-based modal containing:
   - Tool name (read-only display)
   - Layer selector (editable dropdown: map, timeline)
   - Arguments editor (editable textarea with JSON)
   - "תריץ שליפה חדשה" button (hidden until user edits)
3. Add state tracking: `state.queryEdited` boolean, change detection on form inputs.
4. Add form styling to match existing UI palette.
5. Stub handler `handleQueryFormSubmit()` for Phase 2a.

**Files affected:**
- `app.js` (query cleanup, query form state/functions, modal controls, step-card visibility behavior, layer presentation behavior; current deployed version `v=68`)
- `index.html` (query modal/result controls; current deployed script version `v=68`)
- `styles.css` (query form, layer tabs, point markers, result-window controls, standard eye/eye-off visibility icons and step-result text toggle styling; current deployed version `v=52`)

**Rationale:**
- Query ≠ Results: Query payload should contain only request parameters, not response data.
- Form-based UI: Editable fields are more intuitive than JSON text.
- Smart visibility: Run button appears only after edits, preventing accidental re-runs of unchanged queries.
- Foundation for Phase 2: Prepares UI for spatial query type selector, temporal range picker, and filter dropdowns.

**Full plan:** Continue from this handoff and the committed code in `main`; do not rely on older private scratch files from another Windows user profile.

**Next phase after Step 1:**
- Phase 2a: Implement `handleQueryFormSubmit()` to call agent with edited query and create new layer.
- Phase 2b: Add spatial query type selector + draw tools (proximity, polygon, corridor).
- Phase 2c: Add temporal range picker.
- Phase 2d: Add filter dropdowns (source, certainty, labels).

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

3. VM deploy path and stale-code confusion.
   - Use `/opt/serbia-poc-ui`, not `/opt/serbia-poc/ui`.
   - Verify public served asset versions after deploy.
   - If the UI shows rectangles instead of colored points, the VM is serving stale CSS/JS.
   - If final answers auto-present results, the VM/local code is stale; current `main` requires manual final `הצג`.

4. Config BOM.
   - Write `.hermes-api.json` without BOM.
   - `server.py` now tolerates BOM via `utf-8-sig`.

5. Historical files still contain old source labels.
   - Active data is clean; historical test/recorded files may not be.

6. Entity IDs are not in DB.
   - Treat entities as future layer candidates only after adding first-class entity data.

## Suggested First Message To A New Assistant

```text
Read PROJECT_HANDOFF.md first. Continue work on the Serbia/North Kosovo POC in llm_investigation_orchestrator_serbia_poc. The current branch is main and should be clean/aligned with origin/main. The UI is deployed from /opt/serbia-poc-ui on VM 151.145.93.180 and currently serves styles.css?v=52 and app.js?v=68. Do not touch C:\Users\user\Downloads\oracle.key.

Current behavior: colored map point markers with popups; final answers do not auto-present visualization layers; final `הצג תוצאות` presents/restores final-answer layers manually. The result table is a flush transparent tabbed overlay with real layer tabs, standard eye/eye-off toggles, per-tab `×` close, resize, `−` minimize, `□` restore/maximize, and window `×` close/clear. Final and step result actions use the same non-overlapping pill styling as `הצג שאילתה`; step cards toggle `הצג תוצאות` / `הסתר תוצאות`, and `הצג שאילתה` opens query details. Query edit modal controls exist but query re-execution is still future work.

The UI uses an additive source/data layer architecture; preserve that model when adding new filters or visualizations. Before deploying, fetch GitHub and verify the VM is not serving stale assets.
```

## File Review Order

For UI/layer work:

Preserve the additive layer model:

- Keep visualization state decoupled from chat state.
- Use `sourceId` for final-answer/step origin and `dataId` for the layer data identity.
- `הצג` should add/focus related layers, not replace unrelated visible layers.
- Layer colors are workspace-level visual identities and should not be tied to chat order.

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
