# Serbia/Kosovo Investigation Orchestrator POC

This is a separate POC derived from the current investigation orchestrator. It keeps the same UI, gateway, MCP tool contract, event schema, and investigation logic, but replaces the scenario configuration and default data with a Serbia/North Kosovo corpus.

The purpose of this copy is to validate that the orchestration pattern is scenario-portable: the agent should investigate claims, locations, actors, media reports, disinformation signals, contradictions, and escalation patterns without depending on cargo-specific entities or routes.

## Local Run

```powershell
$env:PYTHONIOENCODING='utf-8'
python server.py 8769
```

Then open `http://127.0.0.1:8769/`.

The local UI serves static assets and forwards investigation runs through the same Hermes gateway pattern used by the original POC. A separate Hermes deployment/configuration is still required before this POC can run end-to-end against a remote agent.

## Hermes API Configuration

The UI gateway always reads its runtime Hermes connection settings from:

```text
.hermes-api.json
```

The real `.hermes-api.json` file is intentionally not committed because it contains the Hermes API key and, for local development, the VM SSH key path. Use the committed examples as templates:

```text
.hermes-api.local.example.json
.hermes-api.vm.example.json
```

For local development on the Codex/Windows machine, copy `.hermes-api.local.example.json` to `.hermes-api.json` and fill in the VM address, SSH key path, and API key. In this mode the same `server.py` uses SSH/Paramiko to reach the Hermes API listening on the VM loopback address.

For deployment on the Hermes VM, copy `.hermes-api.vm.example.json` to `/opt/serbia-poc-ui/.hermes-api.json` and fill in the API key. In this mode the same `server.py` uses `"transport": "direct"` and talks to Hermes locally at `127.0.0.1:8642`, without SSH.

The public bind address is also runtime configuration, not a separate code fork. Locally the server defaults to `127.0.0.1`. On the VM, the systemd service should set:

```text
POC_UI_HOST=0.0.0.0
```

So the intended split is:

```text
same server.py
different .hermes-api.json
different POC_UI_HOST value
```

## Data Projection

The source dataset is retained unchanged under `data/north_kosovo_attachment_inspect/`.

The runtime MCP reads:

```text
data/serbia_kosovo_events_projection.csv
data/serbia_kosovo_locations.json
```

The projection maps the Serbia/Kosovo source fields into the existing canonical event schema:

```text
event_id,timestamp_utc,source_type,source_reliability,entity_or_actor,location_id,event_summary
```

The runtime file is intentionally clean. It exposes only the canonical fields above. `event_summary` contains only the original raw text, and `source_reliability` is neutralized to avoid leaking truth labels.

Evaluation-only labels are stored separately in:

```text
data/serbia_kosovo_evaluator_labels.csv
```

That file contains scenario IDs, clusters, ground-truth status, misleading-type labels, rumor/disinformation flags, and original reliability labels. It is not used by the MCP server or UI.

## MCP Tools

The MCP server remains read-only and exposes the same fifteen tools:

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

The tool algorithms and DB structure were not changed for this copy. Scenario-specific configuration was replaced with Serbia/Kosovo locations, actors, identifier patterns, and semantic clues. Hidden scenario labels are deliberately kept out of the agent-visible runtime.

## Verification

Run a local MCP smoke test:

```powershell
$env:PYTHONIOENCODING='utf-8'
python mcp_server/smoke_client.py
```

Run the tool benchmark:

```powershell
$env:PYTHONIOENCODING='utf-8'
python mcp_server/benchmark_tools.py --rounds 3
```

The benchmark covers the full tool surface against Serbia/Kosovo questions: intent classification, location/event resolution, broad search, filtered search, actor history, aggregations, linkage explanation, sequence building, entity resolution, identifier tracing, semantic tracing, related-event expansion, and hypothesis challenge.
