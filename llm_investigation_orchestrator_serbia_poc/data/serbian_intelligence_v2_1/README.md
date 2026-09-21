# Serbian Intelligence Synthetic Dataset V2.1

V2.1 preserves the V2 scenario, record identifiers, source balance, and UAV observations while adding deterministic cross-source evidence chains for fusion evaluation and 24 synthetic cellular-call records.

## Cellular Calls source

- Hebrew source label: `שיחות סלולר`; English label: `Cellular Calls`.
- Nine linked calls reuse one synthetic Side A number and IMEI: three calls in each of `LOC-V2-013`, `LOC-V2-009`, and `LOC-V2-010`.
- Every Side B uses a different synthetic identity and a different existing canonical location elsewhere in Kosovo.
- Every call has a locally generated simulated WAV recording and a bilingual synthetic transcript.
- All communication identifiers and audio are synthetic demonstration data; no real PII or voices are included.

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
