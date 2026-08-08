# Checkpoint Summary

## Checkpoint
002 — English projection remediation

## Checkpoint status
Complete. The active v2.1 English runtime dataset and its v2 compatibility projection pass the no-Hebrew gate.

## Slice goal
Replace the partial phrase projection with deterministic English generation for runtime event, location, and entity assets, then reject any generated asset containing Hebrew characters.

## Root cause
`generate_english_projection.py` translated a small set of exact labels and sentence fragments. It did not translate all generated narrative templates, entity names, location metadata, UAV fields, or v2.1 fusion language. Mixed-language `.en` files were still accepted because the generator had no output validation.

## What changed
- Expanded deterministic translations for v2/v2.1 runtime labels, entities, locations, event scenarios, public-source narratives, UAV observations, and fusion narratives.
- Translated all structured projection columns used by the result table, including actor-facing entity data, object class, movement, direction, and confidence fields.
- Limited generation to the supported v2/v2.1 projection families; legacy v1 and recorded playback assets are outside this slice.
- Added a hard Unicode Hebrew scan that fails generation and reports affected files and line counts.
- Regenerated six `.en` assets for v2 and v2.1.

## Validation evidence
- Generator: `Projected dataset: v2`, `Projected dataset: v2.1`, `Validated clean English output: 6 files`.
- v2: 14,800 event rows; zero Hebrew matches across events, locations, and entities.
- v2.1: 14,800 event rows; zero Hebrew matches across events, locations, and entities.
- Runtime `server.load_ui_events("en")`: 14,800 rows; zero Hebrew matches.
- Runtime TikTok subset: 1,101 rows; zero Hebrew matches.

## Known validation limitation
`data/validate_serbian_intelligence_v2_1.py` cannot complete against the current baseline because `serbian_uav_observations_v2_1.jsonl` contains pre-existing malformed JSON at line 1, column 829. This file was not modified by this slice.

## Files changed
- `generate_english_projection.py`
- v2 English events, locations, and entities projections
- v2.1 English events, locations, and entities projections
- capability status, checkpoint, and handoff artifacts

## Risks and follow-up
- Legacy v1 and recorded-run English assets still require a separate localization slice if they remain user-accessible.
- MCP locale-keyed state and semantic-cache isolation remain pending.
- Production deployment and mobile visual verification remain pending.

## Continue / pause recommendation
Pause for product/QA review of the generated English runtime rows, then continue with the MCP locale boundary and deployment.
