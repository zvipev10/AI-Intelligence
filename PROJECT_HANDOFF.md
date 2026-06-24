# AI Intelligence Project Handoff For Claude

Last updated: 2026-06-24

This file is the primary handoff document for continuing the project in another assistant/chat. It captures the current repository state, deployed state, architecture, important files, known risks, and the exact context needed to avoid rediscovering old decisions.

## One-Line Summary

The project contains two intelligence-analysis POCs. The active work is the Serbia/North Kosovo POC: a Hebrew analyst UI backed by a Hermes orchestrator model and MCP tools over a 10,000-record synthetic event corpus, with map/timeline/evidence visualizations, recorded demo replays, and agent-step explainability embedded inside the chat answer.

## Repository And Git State

GitHub repository:

- https://github.com/zvipev10/AI-Intelligence

Current active branch:

- `app-v2-agent-steps-in-chat`
- Branch URL: https://github.com/zvipev10/AI-Intelligence/tree/app-v2-agent-steps-in-chat
- PR creation URL: https://github.com/zvipev10/AI-Intelligence/pull/new/app-v2-agent-steps-in-chat

Main branch at time of handoff:

- `main` / `origin/main`: `39110d1 Require model evidence IDs for retrieval answers`

Active branch head at time of handoff:

- `e8de1f5 Keep mobile evidence scroller RTL`

Recent v2 branch commits, newest first:

```text
e8de1f5 Keep mobile evidence scroller RTL
9b8cd94 Refresh fifth demo recording
74d596a Broaden mobile evidence overflow media query
2e18302 Force mobile evidence table overflow
0eb99c9 Restore mobile evidence horizontal scroll
10c4683 Use card layout for mobile evidence view
9bdbd33 Fix mobile evidence table overflow
6634253 Embed agent research steps in chat
```

Important dirty working-tree note:

- `llm_investigation_orchestrator_serbia_poc/recorded_runs/q2_movement.json` is modified locally and was deliberately not committed in the latest work.
- Do not include it in unrelated commits unless the user explicitly asks to refresh question 2 recording.

## Active POCs

Cargo / previous POC:

- Directory: `llm_investigation_orchestrator_poc`
- Local UI: `http://127.0.0.1:8768/`
- Purpose: original cargo/cross-inference scenario, including the hidden object `OF-4482`.

Serbia / North Kosovo POC:

- Directory: `llm_investigation_orchestrator_serbia_poc`
- Local UI: `http://127.0.0.1:8769/`
- VM UI: `http://151.145.93.180:8769/`
- Purpose: scenario-portability demo without cargo-specific concepts, based on 10,000 raw North Kosovo escalation records.

## Current Deployed State On Hermes VM

VM:

- Host: `151.145.93.180`
- User: `ubuntu`
- SSH key normally used locally: `C:\Users\e054922\Downloads\oracle.key`

Current Serbia UI deployment:

- Path: `/opt/serbia-poc-ui`
- Service: `serbia-poc-ui.service`
- Verified active on 2026-06-24.
- `index.html` currently serves:
  - `styles.css?v=27`
  - `app.js?v=35`

Current Serbia MCP/Hermes deployment:

- MCP path: `/opt/serbia-poc/mcp_server/server.py`
- Hermes gateway service: `hermes-gateway.service`
- Verified active on 2026-06-24.
- Hermes local API port on VM: `127.0.0.1:8642`

Useful VM checks:

```bash
systemctl is-active serbia-poc-ui.service
systemctl is-active hermes-gateway.service
grep -n 'styles.css?v=\|app.js?v=' /opt/serbia-poc-ui/index.html
grep -n 'research-steps-toggle\|orientation: portrait\|direction: rtl' /opt/serbia-poc-ui/styles.css | head -10
```

Deploy UI files manually from local Windows workspace:

```powershell
scp -o ConnectTimeout=8 -i "C:\Users\e054922\Downloads\oracle.key" -o StrictHostKeyChecking=no llm_investigation_orchestrator_serbia_poc/index.html ubuntu@151.145.93.180:/tmp/index.html
scp -o ConnectTimeout=8 -i "C:\Users\e054922\Downloads\oracle.key" -o StrictHostKeyChecking=no llm_investigation_orchestrator_serbia_poc/app.js ubuntu@151.145.93.180:/tmp/app.js
scp -o ConnectTimeout=8 -i "C:\Users\e054922\Downloads\oracle.key" -o StrictHostKeyChecking=no llm_investigation_orchestrator_serbia_poc/styles.css ubuntu@151.145.93.180:/tmp/styles.css
ssh -o ConnectTimeout=8 -i "C:\Users\e054922\Downloads\oracle.key" -o StrictHostKeyChecking=no ubuntu@151.145.93.180 "cp /tmp/index.html /opt/serbia-poc-ui/index.html && cp /tmp/app.js /opt/serbia-poc-ui/app.js && cp /tmp/styles.css /opt/serbia-poc-ui/styles.css && sudo systemctl restart serbia-poc-ui.service && systemctl is-active serbia-poc-ui.service"
```

Deploy a refreshed recorded run, example q5:

```powershell
scp -o ConnectTimeout=8 -i "C:\Users\e054922\Downloads\oracle.key" -o StrictHostKeyChecking=no llm_investigation_orchestrator_serbia_poc/recorded_runs/q5_assessment.json ubuntu@151.145.93.180:/tmp/q5_assessment.json
ssh -o ConnectTimeout=8 -i "C:\Users\e054922\Downloads\oracle.key" -o StrictHostKeyChecking=no ubuntu@151.145.93.180 "cp /tmp/q5_assessment.json /opt/serbia-poc-ui/recorded_runs/q5_assessment.json && sudo systemctl restart serbia-poc-ui.service"
```

## Architecture

High-level flow:

```text
Hebrew analyst question
  -> browser UI
  -> local/VM Python gateway server.py
  -> Hermes API
  -> main orchestrator model
  -> MCP tools in mcp_server/server.py
  -> CSV/JSON event data
  -> tool audit records
  -> final model answer
  -> UI chat + embedded research process + map/timeline/evidence view
```

Runtime configuration split:

- Same `server.py` is used locally and on the VM.
- Local Windows development uses `.hermes-api.json` with SSH transport to VM.
- VM deployment uses `.hermes-api.json` with direct transport to local Hermes API.

Committed config templates:

- `llm_investigation_orchestrator_serbia_poc/.hermes-api.local.example.json`
- `llm_investigation_orchestrator_serbia_poc/.hermes-api.vm.example.json`

The real `.hermes-api.json` is intentionally uncommitted because it contains secrets and local key paths.

## Key Files

Serbia UI and gateway:

- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/help.html`

Serbia MCP:

- `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/smoke_client.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/regression_quality.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/benchmark_tools.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/remote_deploy_serbia.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/remote_deploy_ui.py`

Serbia data:

- `llm_investigation_orchestrator_serbia_poc/data/serbia_kosovo_events_projection.csv`
- `llm_investigation_orchestrator_serbia_poc/data/serbia_kosovo_locations.json`
- `llm_investigation_orchestrator_serbia_poc/data/serbia_kosovo_evaluator_labels.csv`

Recorded demo runs:

- `llm_investigation_orchestrator_serbia_poc/recorded_runs/real_hotspots_20260621.json`
- `llm_investigation_orchestrator_serbia_poc/recorded_runs/q2_movement.json`
- `llm_investigation_orchestrator_serbia_poc/recorded_runs/q3_stabilizer.json`
- `llm_investigation_orchestrator_serbia_poc/recorded_runs/q4_violence_noise.json`
- `llm_investigation_orchestrator_serbia_poc/recorded_runs/q5_assessment.json`

Performance logs:

- `llm_investigation_orchestrator_serbia_poc/performance_logs/`
- `llm_investigation_orchestrator_poc/performance_logs/`

Cargo POC files:

- `llm_investigation_orchestrator_poc/server.py`
- `llm_investigation_orchestrator_poc/app.js`
- `llm_investigation_orchestrator_poc/styles.css`
- `llm_investigation_orchestrator_poc/index.html`
- `llm_investigation_orchestrator_poc/help.html`
- `llm_investigation_orchestrator_poc/mcp_server/server.py`

Original direct-model benchmark POC:

- `llm_cross_reference_benchmark/`
- `llm_cross_reference_benchmark_he/`

## Version 2.0 UI Changes

Implemented on branch `app-v2-agent-steps-in-chat`.

What changed:

- Removed the right-side `הקשר החקירה` section from the Serbia UI.
- Removed frontend `investigation_state` construction and sending.
- Moved agent work explanations into the chat answer itself.
- While the agent is running, steps appear live/open inside the active `סוכן חקירה` message.
- When the final answer arrives, steps collapse under `תהליך המחקר` at the top of that same answer, similar to the existing collapsible event IDs.
- The result/map/timeline/evidence panel remains separate.
- Mobile evidence table was kept as a horizontally scrollable table, not cards.
- Current mobile table scroller:
  - `styles.css?v=27`
  - `overflow-x: scroll`
  - table fixed width in portrait
  - both scroller and table set to `direction: rtl`

Important UI implementation points:

- Active assistant message state lives in `app.js`:
  - `activeAssistantMessage`
  - `activeActivityList`
  - `activeActivityEmpty`
- Relevant functions:
  - `startAssistantResearchMessage`
  - `ensureAssistantResearchMessage`
  - `setActiveResearchMessage`
  - `finalizeAssistantMessage`
  - `renderActivitySteps`
  - `applyHermesResult`
  - `replayRecordedResult`

## Serbia MCP Tools

The MCP server exposes these tools:

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

Special tools:

- `classify_question_intent`: first-step intent classifier. Uses MCP sampling when available and falls back to deterministic classification.
- `plan_next_investigation_step`: bounded process-control tool that suggests concrete next steps; it does not replace the orchestrator model's analytical brain.
- `compare_location_claims`: compares visible location-report conflicts using visible reliability/certainty fields only. It does not know hidden truth labels.

Hybrid LLM/sampling tools:

- `classify_question_intent`
- `resolve_event_reference`
- `trace_semantic_clues`
- `find_related_events`
- `compare_location_claims`
- `challenge_hypothesis`

Design rule:

- Deterministic retrieval remains the source of event candidates.
- LLM sampling may classify, rerank, summarize, or suggest bounded follow-up clues.
- LLM sampling must not silently invent event IDs outside deterministic candidate sets.

## Data Policy

Visible runtime data:

- `serbia_kosovo_events_projection.csv`
- `serbia_kosovo_locations.json`

Evaluation-only hidden labels:

- `serbia_kosovo_evaluator_labels.csv`

Important: do not expose evaluator labels to the orchestrator, MCP runtime, UI, or prompt. They contain scenario IDs, ground truth, misleading labels, and other information that would unfairly help the model.

The visible DB projection intentionally contains only what an analyst could see:

- canonical event IDs
- timestamps
- source type/reliability/certainty as visible fields
- actor/entity
- location
- raw event summary

## Recorded Demo Questions

The demo uses five recorded questions available through the `+` button in the UI.

Current compact questions:

1. `איפה נמצאים מוקדי החיכוך העיקריים בצפון קוסובו, ומה המוקדים המדויקים בתוך כל אזור?`
2. `האם ניתן לזהות דפוס של תנועת כוחות או הגברת נוכחות בזמן ובמרחב?`
3. `מה הגורם הבינלאומי המרכזי עושה בפועל: מייצב את השטח, מציב חיץ, או מגביל את חופש הפעולה?`
4. `האם הדיווחים על ירי ופיצוצים נראים כמו אירועים אמיתיים או כמו רעש מידע?`
5. `על בסיס כל מה שמצאת, האם מדובר באכיפה נקודתית או בדפוס הסלמה רחב יותר בצפון קוסובו?`

Latest q5 recording:

- File: `llm_investigation_orchestrator_serbia_poc/recorded_runs/q5_assessment.json`
- Created: 2026-06-23
- Source: `live_hermes_run_local_rerun_v2`
- Live run ID: `run_c071179942ba4a1d85cf991a6403a0dc`
- Runtime: about 56.4 seconds
- Steps: 4
- Event/location IDs: 30
- Recommended view: `evidence`
- Deployed to VM and verified through `/api/recorded-run?id=q5_assessment`

Note on q2:

- Local `q2_movement.json` has uncommitted modifications. Treat it as pending/user-generated unless explicitly asked to commit or revert.

## Running Locally

From repo root:

```powershell
cd llm_investigation_orchestrator_serbia_poc
$env:PYTHONIOENCODING='utf-8'
python server.py 8769
```

Open:

```text
http://127.0.0.1:8769/
```

If using the Codex bundled Python:

```powershell
& "C:\Users\e054922\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "llm_investigation_orchestrator_serbia_poc\server.py" 8769
```

Current local status endpoint was verified as:

```json
{"mode": "hermes", "configured": true, "build": "serbia-poc-1"}
```

## Verification Commands

Syntax check for UI JS:

```powershell
& "C:\Users\e054922\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" --check llm_investigation_orchestrator_serbia_poc/app.js
```

MCP smoke test:

```powershell
$env:PYTHONIOENCODING='utf-8'
python llm_investigation_orchestrator_serbia_poc/mcp_server/smoke_client.py
```

Regression quality gate:

```powershell
$env:PYTHONIOENCODING='utf-8'
python llm_investigation_orchestrator_serbia_poc/mcp_server/regression_quality.py
```

Regression compare against a baseline:

```powershell
$env:PYTHONIOENCODING='utf-8'
python llm_investigation_orchestrator_serbia_poc/mcp_server/regression_quality.py --compare llm_investigation_orchestrator_serbia_poc/test_runs/regression_quality_20260620T192453Z.json
```

Benchmark all tools:

```powershell
$env:PYTHONIOENCODING='utf-8'
python llm_investigation_orchestrator_serbia_poc/mcp_server/benchmark_tools.py --rounds 3
```

## Performance Reality

The slow part is not the DB tools. It is usually model orchestration and final synthesis.

Observed pattern from prior logs:

- Tool execution can be milliseconds to a few seconds.
- End-to-end runs can be 50-200+ seconds.
- Large investigation prompts and final answer synthesis dominate latency.

For demos:

- Prefer recorded questions via the `+` button.
- Recorded replay uses real model answers captured from prior runs.
- Steps replay progressively, so the UI feels interactive without waiting for a live Hermes run.

## Current Known Issues / Watch Items

1. Mobile evidence scroller
   - Current state: horizontal scroll works and is set RTL.
   - Recent user feedback: scroller was perfect but looked LTR; fixed by setting `.table-wrap` direction to RTL.
   - If user still dislikes behavior, next likely fix is JS-assisted scroll/drag rather than pure CSS.

2. Dirty q2 recording
   - `recorded_runs/q2_movement.json` is modified locally.
   - Do not accidentally commit it.

3. Model may choose `evidence` instead of `timeline`
   - If timeline is desired, ask explicitly: `תציג כרצף זמן`, `סדר לפי זמן`, or `ציר זמן`.

4. Broad live runs are slow
   - Use recorded demo for presentations.
   - If real live demo is required, choose narrower questions.

5. Hidden/evaluator fields
   - Do not put `serbia_kosovo_evaluator_labels.csv` into runtime prompts/tools.

6. Git branch discipline
   - Active UI 2.0 changes are on `app-v2-agent-steps-in-chat`.
   - Main does not yet include these v2 changes.

## Cargo POC Context

Cargo POC goal:

- Demonstrate that a model can discover hidden cross-inference behavior in diverse simulated operational data.

Important cargo hidden behavior:

- Target object was `OF-4482`.
- Earlier problem: the second POC often found only a partial chain or stopped after it had enough evidence, without returning all supporting records.
- Tools/instructions were expanded with semantic clue tracing, bounded seed expansion, larger coverage defaults, and `plan_next_investigation_step`.

Do not overfit Serbia instructions back into cargo, and do not reintroduce cargo-specific words into Serbia prompts/tools.

## Serbia Demo Story

The demo narrative:

- A Serbian intelligence officer receives 10,000 raw records about several days of escalation in North Kosovo.
- The analyst is not asking for a news summary, but for structured intelligence sensemaking:
  - local enforcement or broader northern operation?
  - is the international force stabilizing or constraining Serbian freedom of action?
  - is there significant force movement over time and space?
  - are shooting/explosion/border/roadblock reports reliable or information noise?
  - do point events connect into an evolving scenario requiring a decision?

The value of the POC:

- Natural-language analyst questions.
- Agentic tool orchestration.
- Data-grounded evidence retrieval.
- Model-generated reasoning bridges for each step.
- Visual recommendation: map, timeline, or raw evidence.
- Recorded replay for demo speed.

## Suggested First Message To Claude

Use this in a new Claude chat:

```text
Read PROJECT_HANDOFF.md first. Continue work on the Serbia/North Kosovo POC in llm_investigation_orchestrator_serbia_poc. The active branch is app-v2-agent-steps-in-chat. Do not commit the existing dirty q2_movement.json unless explicitly asked. Current VM UI is http://151.145.93.180:8769/ and local UI is http://127.0.0.1:8769/.
```

## File Review Order For Claude

For UI work:

1. `llm_investigation_orchestrator_serbia_poc/index.html`
2. `llm_investigation_orchestrator_serbia_poc/styles.css`
3. `llm_investigation_orchestrator_serbia_poc/app.js`
4. `llm_investigation_orchestrator_serbia_poc/server.py`

For agent/tool behavior:

1. `llm_investigation_orchestrator_serbia_poc/server.py`
2. `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`
3. `llm_investigation_orchestrator_serbia_poc/mcp_server/smoke_client.py`
4. `llm_investigation_orchestrator_serbia_poc/mcp_server/regression_quality.py`

For demo/recorded replay:

1. `llm_investigation_orchestrator_serbia_poc/recorded_runs/`
2. `llm_investigation_orchestrator_serbia_poc/server.py`
3. `llm_investigation_orchestrator_serbia_poc/app.js`

## Final Sanity Checklist Before Any Future Handoff

- Run `git status --short --branch`.
- Check which branch is active.
- Do not commit unrelated dirty recorded-run files.
- Verify VM `styles.css?v=` and `app.js?v=` after UI deploy.
- Verify `serbia-poc-ui.service` after VM deploy.
- If MCP changed, run smoke/regression before deploy.
- If recorded run changed, verify `/api/recorded-run?id=<id>` on the VM.
