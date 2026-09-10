# Developer Review

## Status
Approved under delegated authority.

## Approach
Derive coordinates in `load_ui_events()` from a stable SHA-256 digest of `record_id`, canonical latitude/longitude, and a bounded radius. This avoids a large generated-data rewrite while ensuring every API-delivered raw record contains coordinates. Render ordinary event rows individually at those coordinates and let MIL-STD observations consume the same fields.

## Risks
- DOM marker volume: use individual placement for visible event layers and retain existing layer visibility controls.
- Geographic distortion: cap displacement and compensate longitude by latitude.
- Semantic confusion: show `Approximate position` in popups and the record viewer.

## Tests
Determinism, radius bounds, locale stability, missing-location fallback, coordinate preference, removal of MIL-STD radial offset, viewer labels, and existing regressions.

