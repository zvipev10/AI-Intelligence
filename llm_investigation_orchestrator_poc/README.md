# LLM Investigation Orchestrator POC

This is an isolated second prototype. It copies the required dataset and map runtime so changes cannot affect the cross-reference POC.

Run locally:

```powershell
$env:PYTHONPATH=(Resolve-Path '..\.tools\python')
python server.py 8768
```

Then open `http://127.0.0.1:8768/`.

The local server serves the static Hebrew interface and forwards investigation runs through an SSH channel to the protected Hermes API on the OCI VM. The browser never receives the SSH key or Hermes API key.

The ignored `.hermes-api.json` file contains the local connection settings created by `mcp_server/remote_enable_api.py`. The Hermes API listens only on the VM loopback address at `127.0.0.1:8642` and the `api_server` platform is limited to the `mcp-intelligence-events-poc` toolset.

## Hermes MCP deployment

The read-only MCP server lives in `mcp_server/server.py` and is deployed on the Hermes OCI VM at:

```text
/opt/intelligence-poc/mcp_server/server.py
/opt/intelligence-poc/data/events_he_large.csv
/opt/intelligence-poc/data/events_he_expanded_5000.csv
```

The original `events_he_large.csv` baseline is retained. The expanded dataset is `events_he_expanded_5000.csv`; deployment selects it through the Hermes MCP environment variable `INTELLIGENCE_POC_DATA`.

Hermes registers it as `intelligence-events-poc` using stdio transport. It exposes fifteen read-only tools:

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
challenge_hypothesis
```

`classify_question_intent` is a deterministic routing tool. The orchestrator calls it first to decide whether the analyst asked for retrieval, geographic aggregation, timeline retrieval, or a deeper investigation.

`plan_next_investigation_step` is a lightweight process-control checkpoint. It does not replace the model's analytical choice; it tells the orchestrator whether required seeds, semantic clues, unclassified candidate events, or adjacent linkage checks remain open before challenge or final summary is allowed. In deeper investigations the model passes a candidate ledger that classifies discovered events as main chain, support, alternative, rejected, gap, or background.

`find_related_events` can optionally filter candidate expansion by `source_types`, so an investigation can ask for only telephone metadata, signal intercepts, financial alerts, movement sensors, or other evidence families while keeping the same linkage scoring.
`trace_identifier` can be scoped by time, location, and source type. `trace_semantic_clues` follows operational clue terms when a chain shifts from a formal identifier to descriptive language such as cargo, warehouse, route, or vehicle phrasing. `aggregate_events` supports `top_n` and returns map-ready location metadata. `explain_linkage` checks the evidence bridge between two event IDs before the agent presents a transition as part of a chain.

The production Hermes configuration was backed up before registration. The gateway remains responsible for the MCP subprocess lifecycle.

## Real agent flow

1. The UI posts the Hebrew investigation question to `/api/investigate`.
2. The local gateway opens an SSH `direct-tcpip` channel to the VM loopback API.
3. Hermes uses the configured ChatGPT OAuth model and the intelligence MCP tools.
4. The answer cites event IDs, which the UI links back to the map, timeline, and raw-event table.
5. Hermes tool lifecycle events populate the agent activity panel.

## Benchmark plan

Before increasing dataset size, measure the current baseline with the MCP benchmark harness:

```powershell
$env:PYTHONIOENCODING='utf-8'
python mcp_server/benchmark_tools.py --rounds 5
```

The benchmark covers every MCP tool in a broad scenario:

- reference/location resolution
- broad and filtered search
- event retrieval
- actor history with alias expansion
- aggregation by location/source/actor
- deterministic linkage explanation between event pairs
- chronological sequence building
- entity resolution
- identifier tracing, including negated matches
- related-event expansion, including source-type-filtered expansion
- hypothesis challenge with alternatives and gaps

Record these metrics before each dataset-size experiment:

- per-tool mean, p50, p95, and max latency
- total benchmark time
- full agent run time for representative analyst questions
- UI responsiveness while live steps update

Suggested scaling sequence:

1. Baseline: original 2,044 events.
2. Medium: 5,000-event expanded dataset.
3. Large: about 10,000 events.
4. Stress: about 25,000 events.

The medium dataset keeps the hidden suspicious chain stable, adds 60 complete benign logistics chains, and fills the rest with benign/noise records so the experiment tests signal-to-noise and latency separately from scenario correctness.
