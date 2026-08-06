# Serbian Intelligence Synthetic Dataset V2.1

V2.1 preserves the V2 scenario, schema, record identifiers, source balance, and UAV observations while adding deterministic cross-source evidence chains for fusion evaluation.

## Runtime artifacts

- `north_kosovo_serbian_intelligence_v2_1_14800.csv`
- `north_kosovo_serbian_intelligence_v2_1_14800.jsonl`
- `serbia_kosovo_events_projection_v2_1.csv`
- `serbian_uav_observations_v2_1.jsonl`
- `serbia_kosovo_entities_v2_1.json`
- `serbia_kosovo_locations_v2_1.json`

## Evaluator-only artifacts

- `serbia_kosovo_evaluator_labels_v2_1.csv`
- `fusion_target_truth_v2_1.jsonl`

Evaluator truth must not be loaded by Moshe, MCP retrieval, or the application. Canonical coordinates remain area anchors and are not observation-level coordinates.

Regenerate with `generate_serbian_intelligence_v2_1.py` and validate with `validate_serbian_intelligence_v2_1.py --regenerate`.
