# Ibar force movement demo

## Goal

Add a deterministic synthetic raw-data sequence that supports a medium-confidence assessment of KSF force movement toward the Ibar Bridge without claiming exact convoy identity.

## Scope

- Add three time-ordered UAV observations at LOC-V2-013, LOC-V2-009, and LOC-V2-010.
- Add two independent public reports around each observation so deployment-time evidence creation can produce fused evidence at every point.
- Keep movement interpretation in Talia's assessment process; neutral fusion remains location-scoped object-presence fusion.
- Regenerate and validate V2.1 outputs and the evidence catalog.
- Deploy the dataset, evidence catalog, and MCP service, then verify a natural Talia request.

## Non-goals

- No `track_id` or claim that the exact same convoy was continuously tracked.
- No change to existing assessment overlay types.
- No change to raw V2 inputs; V2.1 remains the derived scenario dataset.

## Acceptance criteria

1. Three distinct locations contain compatible KSF convoy observations within a plausible operational interval.
2. Each location has independent corroboration and a cataloged fused evidence object.
3. Raw observations retain timestamps, movement status, direction, quantity, mission, and video segment provenance.
4. Talia can create a movement assessment and `route_axis` from a natural intelligence question while qualifying it as force-level inference.
5. Existing generator, evidence, and assessment tests remain green.

## Assumptions

- The user's instruction to proceed authorizes the product/data-model checkpoint for this focused synthetic demo addition.
- Force-pattern movement may be assessed without exact-object identity when time, geography, entity, object class, quantity, and direction are mutually consistent.
