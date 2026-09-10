# Developer Review

## Status
Approved under the user's delegated authority on 2026-09-10.

## Recommendation
Implement a dependency-free client adapter over the existing MapLibre marker flow. Build typed symbol descriptors from visible event/entity layers, use a curated mapping registry, and render compliant visual primitives with HTML/CSS. Preserve raw record IDs for viewer resolution. Avoid a new API until the demo requires persisted assessments.

## Risks and controls
- Records mention actors without proving presence: classify explicit movement/activity/presence language; otherwise omit presence.
- Duplicate reports: group organization presences by entity and location; label record-derived UAV objects as observations rather than unique assets.
- Confidence semantics: keep assessment state and source evaluation separate; do not infer a formal two-axis code when inputs are insufficient.
- Performance: reuse location aggregation and cap DOM work to visible layers.

## Test strategy
Contract tests for mappings, descriptor construction, grouping, confidence labels, viewer links, localization, and unchanged single-object marker behavior; JavaScript syntax and focused regression suite.

