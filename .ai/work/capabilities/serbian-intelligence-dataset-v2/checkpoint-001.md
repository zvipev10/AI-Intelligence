# Checkpoint 001 - Dataset V2 Generated

## Date

2026-07-17

## Scope

Generated a separate Serbian-intelligence-perspective V2 corpus without modifying or activating V1.

## Outputs

- 14,800 raw CSV/JSONL records.
- 14,800 canonical runtime projection rows.
- 10,300 replacement post-EVT-011 escalation records.
- 3,800 structured synthetic UAV-video exploitation observations.
- 950 public-source Serbian-side records (6.4189%).
- V2 entities, locations, evaluator labels, README, and generation report.

## Scenario boundaries

- EVT-001 through EVT-011 form the perspective-adjusted buildup.
- EVT-012 through EVT-025 implement the approved rapid escalation, limited Serbian control, NATO/Kosovo containment, and frozen standoff without sustained battle.
- Serbian-side records use public sources only.
- UAV observations focus on opposing, international, civilian, or ambiguous activity and never provide friendly-force internal telemetry.
- All movements and operational events are fictional.
- No actual image/video assets are included.

## Validation

- Generator Python AST parse passed.
- Two consecutive generations produced identical output hashes.
- V1 source/entity/location hashes remained unchanged.
- Raw rows: 14,800.
- Projection rows: 14,800.
- UAV observation rows: 3,800.
- Unique record IDs: passed.
- Canonical projection columns: passed.
- Entity and location referential integrity: passed.
- Friendly-side share <=10%: passed.
- Friendly records public-only: passed.
- `git diff --check`: passed.
- Generated timeline: 2026-09-12 through 2026-09-17.

Full evidence is stored in `data/serbian_intelligence_v2/generation_report_v2.json`.

## Review findings

### Blocking issues

None for dataset generation.

### Non-blocking comments

- Human Product/QA sampling should review narrative variety, Hebrew phrasing, movement continuity, and force-balance plausibility.
- Runtime activation requires a separate checkpoint because it changes the active product behavior and index inputs.

### Recommendation

Pause for Product/QA review of the generated V2 corpus before application activation.

## Publishing status

Pending commit and push on `codex/serbian-intelligence-dataset-v2`.
