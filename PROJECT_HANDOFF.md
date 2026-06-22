# Project Handoff

Last updated: 2026-06-20

## Active POCs

There are two related local POCs in this workspace:

- Cargo / previous POC: `llm_investigation_orchestrator_poc`
- Serbia / North Kosovo POC: `llm_investigation_orchestrator_serbia_poc`

Local UI ports used in the project:

- Cargo POC UI: `http://127.0.0.1:8768/`
- Serbia POC UI: `http://127.0.0.1:8769/`

Both POCs use the same broad architecture:

1. Analyst asks a Hebrew question in the UI.
2. Local gateway sends the question, history and investigation state to Hermes.
3. Hermes runs the main orchestrator model.
4. The model calls MCP tools.
5. MCP tools query local/remote CSV-backed event data and return structured results.
6. The model summarizes the investigation.
7. The UI shows chat answer, map/timeline/evidence view and step explanations.
8. Tool calls are also written to an audit log so the UI can show what the agent actually did.

## Important Components

Main Serbia files:

- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/help.html`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`
- `llm_investigation_orchestrator_serbia_poc/data/serbia_kosovo_events_projection.csv`
- `llm_investigation_orchestrator_serbia_poc/data/serbia_kosovo_locations.json`

Main Cargo files:

- `llm_investigation_orchestrator_poc/server.py`
- `llm_investigation_orchestrator_poc/app.js`
- `llm_investigation_orchestrator_poc/styles.css`
- `llm_investigation_orchestrator_poc/index.html`
- `llm_investigation_orchestrator_poc/help.html`
- `llm_investigation_orchestrator_poc/mcp_server/server.py`

Special MCP tools to remember:

- `classify_question_intent`: first-step tool that classifies the analyst question as simple lookup, aggregation, timeline, or investigation. It returns mode, tool budget and recommended view hint.
- `plan_next_investigation_step`: investigation-control tool. It does not replace the model brain; it gives bounded next-step guidance so the model does not jump too early to a conclusion.
- `compare_location_claims`: Serbia tool for comparing location-related reports using visible reliability/certainty fields, useful for detecting suspicious location dispersion or information noise.

## Recent Implemented Changes

Serbia POC:

- Added/used `municipality` aggregation support in `aggregate_events`.
- Updated UI/server mapping so aggregate results by `location` or `municipality` can be shown on the map when coordinates exist.
- Added general model instructions for geographic questions:
  - For geo hotspot questions, use both municipality/area aggregation and precise location aggregation when useful.
  - For violence/shooting/explosion questions, separate confirmed events from information noise, old videos, rumor, civilian explanations and weak reports.
- Added certainty/reliability exposure in the visible Serbia DB projection.
- Added `compare_location_claims` to help compare conflicting location reports.
- Updated help page in Hebrew with:
  - richer Serbia story;
  - military/security-ish source types such as force-movement observations, SIGINT/communications indications, drone/helicopter reports, alerts, police activity and emergency sources;
  - architecture diagram;
  - MCP tools section;
  - separate descriptions of `classify_question_intent` and `plan_next_investigation_step`.
- Removed these help sections per user request:
  - `הנחיות ופרומפטים חשובים`
  - `הקשר בין המטרה לפתרון`
  - `מה רואים במסך`
  - `אמינות ופירוש`

Both POCs:

- Dark mode and Google/Noto-style fonts were already applied earlier.
- Resizable UI panels exist.
- Last UI tweak: aligned analyst input textarea and `שלח` button font size with chat message size:
  - normal: `13px`
  - medium screens: `12px`
  - bumped CSS cache version to `styles.css?v=19` in both `index.html` files.

Serbia classifier fix after latest UI run:

- The UI question `תמיין לפי זמן את האירועים המרכזיים כדי לקבל תמונה` did not choose timeline because `classify_question_intent` recognized `לפי` as retrieval but did not recognize `תמיין לפי זמן` / `לפי זמן` as timeline intent.
- Fixed `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py` timeline terms to include `לפי זמן`, `מיין לפי זמן`, `תמיין לפי זמן`, `מיון לפי זמן`, `סדר לפי זמן`, etc.
- Fixed `llm_investigation_orchestrator_serbia_poc/server.py` fallback view detection to include `לפי זמן`, `מיין`, `תמיין`, `כרונולוג`.
- Local classifier now returns `intent: timeline_retrieval` and `recommended_view_hint: timeline` for that exact question.
- Deployed updated Serbia MCP to Hermes successfully; config backup: `/home/ubuntu/.hermes/config.yaml.before-serbia-poc-1781980166`.

Follow-up change: make `classify_question_intent` truly LLM-based via MCP sampling:

- User asked to implement option 1: change Hermes configuration and tool code so the MCP tool itself uses an LLM through MCP sampling.
- Updated `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`:
  - On initialize, the MCP server records whether the client supports `sampling`.
  - `classify_question_intent` now calls `sampling/createMessage` when sampling is available.
  - The sampling prompt returns JSON only with `intent`, `recommended_mode`, `recommended_view_hint`, `confidence`, and `reason`.
  - The tool normalizes that model result into the stable contract: `recommended_mode`, `tool_budget`, `allowed_tool_families`, `blocked_tool_families`, and `recommended_view_hint`.
  - `classification_source` is now `mcp_sampling` when sampling succeeds, `deterministic_fallback` when sampling is unavailable/fails, and `model_override` only for legacy hidden compatibility.
- Updated `llm_investigation_orchestrator_serbia_poc/server.py`:
  - The main prompt now tells the orchestrator to call `classify_question_intent` first and not send manual `model_intent` fields.
- Updated `llm_investigation_orchestrator_serbia_poc/mcp_server/remote_deploy_serbia.py`:
  - Serbia MCP config now sets `sampling: { enabled: true }`.
- Updated `llm_investigation_orchestrator_serbia_poc/mcp_server/smoke_client.py`:
  - Local smoke client now mocks `sampling/createMessage` and asserts `classification_source == "mcp_sampling"`.
- Updated Serbia help page to describe MCP sampling inside `classify_question_intent`.
- Local smoke test passed with mocked MCP sampling.
- Deployed updated Serbia MCP to Hermes successfully; config backup: `/home/ubuntu/.hermes/config.yaml.before-serbia-poc-1781981612`.
- Remote verification shows the MCP config has `sampling: { enabled: true }` and the smoke test returns `classification_source: mcp_sampling`.
- Full end-to-end UI/API run currently fails because Hermes provider auth on the VM is missing: `No Codex credentials stored. Run hermes auth to authenticate. Run hermes model to re-authenticate.`

After user completed Hermes auth on the VM:

- Verified Hermes gateway is active and Serbia MCP still has `sampling: { enabled: true }`.
- Ran end-to-end local UI/API test with:
  - `תמיין לפי זמן את האירועים המרכזיים כדי לקבל תמונה`
- Result:
  - `recommended_view: timeline`
  - `view_reason: הסדר כרונולוגי ברור`
  - performance log: `llm_investigation_orchestrator_serbia_poc/performance_logs/20260620T190519Z-run_bb7928d5f6804f30909a6805225c7b4d.json`
  - remote MCP audit confirms `classification_source: mcp_sampling`.
- Note: The model returned a reasonable clarification because the query had no subject/event anchor; this is expected. The visualization choice and MCP sampling path worked.

Preparation before converting more tools to LLM/hybrid tools:

- Careful backup was created before tool-conversion work:
  - `backups/serbia-poc-before-llm-tools-20260620-221618.zip`
  - Verified to contain the Serbia MCP server, UI gateway, help page, visible event projection and evaluator labels.
- Added regression quality gate:
  - `llm_investigation_orchestrator_serbia_poc/mcp_server/regression_quality.py`
- The gate covers the first three quality layers agreed with the user:
  1. MCP/tool contract tests for all 16 tools.
  2. Full structured-output snapshots for baseline comparison.
  3. Oracle-label quality metrics from `data/serbia_kosovo_evaluator_labels.csv`.
- Current baseline run:
  - `llm_investigation_orchestrator_serbia_poc/test_runs/regression_quality_20260620T192453Z.json`
  - Result: 16 tools covered, 28 calls, 0 failures.
- Compare-mode verification run:
  - `llm_investigation_orchestrator_serbia_poc/test_runs/regression_quality_20260620T192505Z.json`
  - Compared against the baseline and all event-returning calls had event Jaccard 1.0.
- Run command with bundled Python:
  - `& "C:\Users\e054922\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "llm_investigation_orchestrator_serbia_poc\mcp_server\regression_quality.py"`
- Compare after a tool change:
  - `& "C:\Users\e054922\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "llm_investigation_orchestrator_serbia_poc\mcp_server\regression_quality.py" --compare "llm_investigation_orchestrator_serbia_poc\test_runs\regression_quality_20260620T192453Z.json"`
- Existing `smoke_client.py` remains the focused check for MCP sampling and still verifies `classification_source == "mcp_sampling"`. The broader regression harness records classification source but accepts deterministic fallback in local mode, because the live Hermes sampling path was already verified separately.

Hybrid MCP tool conversion implemented after the backup:

- Updated `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py` with a shared `sample_json_task` helper for bounded MCP sampling inside tools.
- Converted selected tools to hybrid behavior while preserving deterministic retrieval:
  - `resolve_event_reference`: sampling turns a vague event reference into bounded visible search phrases; DB matching remains deterministic and no hidden labels are used.
  - `trace_semantic_clues`: sampling suggests follow-up clues, but they are not silently merged into the current retrieval. This avoids broadening the result set without an explicit next step.
  - `find_related_events`: deterministic scoring still finds candidates; sampling can rerank only the deterministic top candidates and cannot introduce outside event IDs.
  - `compare_location_claims`: deterministic grouping still finds conflict groups; sampling adds a cautious textual assessment only.
  - `challenge_hypothesis`: deterministic profiling still finds evidence/alternatives/gaps; sampling adds competing hypotheses and disproof tests based only on returned evidence.
- Updated MCP tool descriptions so the orchestrator sees these hybrid constraints.
- Updated `smoke_client.py` with task-aware sampling mocks and assertions for new `llm_*` fields.
- Updated `help.html` to explain hybrid MCP-sampling tools in Hebrew.
- Final local validation:
  - `py_compile` passed for server, smoke client and regression harness.
  - `smoke_client.py` passed and confirmed sampling sources for classification, semantic clue expansion, related rerank, geographic assessment and hypothesis challenge.
  - Regression compare run: `llm_investigation_orchestrator_serbia_poc/test_runs/regression_quality_20260620T194033Z.json`
  - Result: 16 tools, 28 calls, 0 failures.
  - Event stability: all event-returning calls kept Jaccard 1.0 except `resolve_event_reference`, which intentionally changed from 0 results to 20 candidates for vague natural-language references.
  - Resolver label check looked reasonable: tactical/Zvecan candidates were all military-related with average relevance about 3.5; false border-crossing candidates were disinformation-heavy.

## Demo Questions For Serbia POC

Current compact demo questions:

1. `איפה נמצאים מוקדי החיכוך העיקריים בצפון קוסובו, ומה המוקדים המדויקים בתוך כל אזור?`
2. `האם ניתן לזהות דפוס של תנועת כוחות או הגברת נוכחות בזמן ובמרחב?`
3. `מה הגורם הבינלאומי המרכזי עושה בפועל: מייצב את השטח, מציב חיץ, או מגביל את חופש הפעולה?`
4. `האם הדיווחים על ירי ופיצוצים נראים כמו אירועים אמיתיים או כמו רעש מידע?`
5. `על בסיס כל מה שמצאת, האם מדובר באכיפה נקודתית או בדפוס הסלמה רחב יותר בצפון קוסובו?`

Additional tactical demo question tested:

`מה באמת קרה באירוע הטקטי ליד זבצ׳אן?`

Observed result:

- The answer was analytically useful: it concluded that the pattern around Zvecan looked more like security vehicle movement, temporary blockages and rumor/noise than verified combat or confirmed shooting.
- Evidence IDs included:
  - `REC-046497`
  - `REC-007201`
  - `REC-063208`
  - `REC-039571`
  - `REC-035775`
  - `REC-050682`
  - `REC-013084`
  - `REC-038800`
  - `REC-028612`
  - `REC-016386`
- But the model recommended `evidence`, not `timeline`.
- Better demo phrasing if timeline is desired:
  - `מה באמת קרה באירוע הטקטי ליד זבצ׳אן? תציג את ההתרחשות כרצף זמן ותבדיל בין אירועים מאומתים, דיווחי ירי לא מאומתים ורעש מידע.`

## Performance Notes

The bottleneck is mostly model orchestration/summarization, not DB query execution.

Example Serbia run for the Zvecan tactical question:

- Performance log: `llm_investigation_orchestrator_serbia_poc/performance_logs/20260620T164622Z-run_7884fb0e30084a0fb62132347585f954.json`
- Total server wait: about 209 seconds.
- Tool calls: 33.
- Tool execution total: about 7.3 seconds.
- Slowest tool: `find_related_events`, about 2.6 seconds.
- Model orchestration gap: about 200 seconds.

Earlier Cargo POC performance work:

- Response-time logs were removed from the UI and written to per-run files under each POC's `performance_logs` directory.
- Polling was optimized to avoid a new SSH connection per status request.

## Known Behavioral Issues / Watch Items

- The model sometimes chooses `evidence` for questions that are demo-friendly as `timeline`, because it interprets the user intent as source validation rather than chronological reconstruction.
- For timeline demos, use natural but explicit wording like `תציג כרצף זמן`.
- Broad investigation questions can trigger many tool calls and slow model reasoning.
- Tool execution is usually fast; end-to-end latency is dominated by model orchestration and final synthesis.
- In very large corpora, unrestricted recursive expansion is risky. The current approach uses bounded tools and model-guided expansion rather than a huge all-paths graph search.

## Cargo POC Context

Cargo POC goal:

- Show that an LLM/agent can discover hidden cross-inference behavior in diverse simulated operational data.
- First POC used a direct model over a simulated DB.
- Second POC uses an agentic orchestration model with tools and visual presentation choices: map, timeline, raw/evidence.

Important hidden cargo behavior previously discussed:

- Target object was `OF-4482`.
- Earlier challenge: second POC often found only partial chain or chose enough evidence without returning all supporting events.
- Tools/instructions were expanded with semantic clue tracing, bounded seed expansion, larger limits, and `plan_next_investigation_step`.
- Be careful not to overfit cargo-specific language in shared instructions.

## Serbia POC Context

Serbia POC goal:

- Open a clean new POC based on the current architecture but without cargo-specific dependencies.
- No DB structure or core logic change was desired; the visible DB projection should not reveal hidden scenario labels or fields that unintentionally help the model.
- The demo narrative: a Serbian intelligence officer analyzes 10,000 raw records about several days of escalation in North Kosovo.
- Intelligence questions:
  - Is Kosovo doing local enforcement or a broader northern operation?
  - Is the international force stabilizing the area or limiting Serbian freedom of action?
  - Is there significant force movement over time and space?
  - Are shooting, roadblock, border-crossing and explosion reports reliable or disinformation/noise?
  - Do point events connect into an evolving scenario that requires decision?

## Deployment Notes

Serbia Hermes deployment was set up earlier and the local UI gateway was restarted on port `8769`.

Known status from earlier:

- Serbia local gateway status returned:
  - `{"mode":"hermes","configured":true,"build":"serbia-poc-1"}`
- Serbia MCP deployment had 16 tools and included `compare_location_claims`.
- Hermes config backup created earlier:
  - `/home/ubuntu/.hermes/config.yaml.before-serbia-poc-1781971559`

Remote deploy or SSH actions require approval/escalation because network access is restricted.

## How To Continue In A New Chat

Suggested first instruction in the new chat:

`Read PROJECT_HANDOFF.md and continue working on the Serbia POC. The local app is in llm_investigation_orchestrator_serbia_poc and should run on port 8769.`

If the next task is UI-only, inspect:

- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/index.html`

If the next task is agent behavior, inspect:

- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`

If the next task is performance, inspect:

- `llm_investigation_orchestrator_serbia_poc/performance_logs`
- `llm_investigation_orchestrator_poc/performance_logs`
