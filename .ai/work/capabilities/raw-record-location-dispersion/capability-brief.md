# Capability Brief

## Capability
Deterministic raw-record location dispersion

## Status
Approved for implementation by the user on 2026-09-10 under the existing end-to-end delegation.

## Problem
Raw records sharing a canonical `location_id` currently overlap on the map. The recently merged MIL-STD renderer compensates with artificial marker offsets, but the record objects themselves do not have distinct coordinates.

## Approved behavior
- Add deterministic record-level `latitude` and `longitude` to application raw-record rows.
- Preserve canonical `location_id`, location metadata, filtering, aggregation, and reasoning.
- Disperse records only within a small radius of the canonical point.
- Use the record coordinates for individual map placement, including MIL-STD UAV observations.
- Keep organization presences grouped at their canonical location.
- Label record positions as approximate in map and detail presentation.
- Do not introduce additional per-record provenance fields; this demo uses a documented dataset-wide deterministic placement policy.

## Acceptance criteria
1. The same record receives the same coordinates on every load and in both locales.
2. Coordinates remain within the configured radius of the canonical location.
3. Raw-record and UAV observation symbols use record coordinates without render-time radial displacement.
4. Organization presence symbols retain canonical coordinates and grouping.
5. Clicking one record opens the existing raw-record viewer.
6. The map and viewer call record-level positions approximate.
7. Missing canonical coordinates fall back safely without invented placement.
8. Existing MIL-STD, viewer, playback, localization, and production contracts pass.

## Non-goals
Changing canonical locations, adding measured sensor coordinates, road-network snapping, editing source claims, or using dispersed coordinates for analytical distance calculations.

