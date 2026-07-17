# Serbian Intelligence Dataset V2

This directory contains a separate synthetic scenario corpus generated from Serbian military intelligence collection perspective. It does not replace or modify any V1 file.

All operations, movements, observations, and territorial changes are fictional. Public formation names are scenario references and do not assert real participation. UAV records are structured synthetic video-exploitation outputs; no image or video media is included.

## Contents

- `north_kosovo_serbian_intelligence_v2_14800.csv`: full raw corpus with collection provenance and optional UAV fields.
- `north_kosovo_serbian_intelligence_v2_14800.jsonl`: JSONL equivalent of the raw corpus.
- `serbia_kosovo_events_projection_v2.csv`: clean canonical nine-field runtime projection.
- `serbia_kosovo_evaluator_labels_v2.csv`: hidden scenario/evaluation labels; do not expose to the agent, UI, retrieval index, or prompt.
- `serbia_kosovo_entities_v2.json`: V1 entities plus V2 public formation references.
- `serbia_kosovo_locations_v2.json`: V1 locations plus coarse V2 scenario areas.
- `serbian_uav_observations_v2.jsonl`: structured synthetic UAV-video exploitation observations linked to raw records.
- `generation_report_v2.json`: counts, hashes, distributions, and automated validation results.

## Generation

From the repository root:

```powershell
python llm_investigation_orchestrator_serbia_poc/data/generate_serbian_intelligence_v2.py
```

Generation is deterministic with seed `20260717`. Re-running the generator rewrites only this V2 directory.

## Current integration status

The application and MCP server still use V1. Activating V2 is a separate reviewed change.
