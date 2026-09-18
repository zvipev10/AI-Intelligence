# Execution plan

## Prerequisite gate

- Capability brief: ready
- Developer review: ready through explicit user delegation
- QA review: ready through explicit user delegation

## Slice 1 — derived raw scenario

Extend `generate_serbian_intelligence_v2_1.py` with deterministic movement-scenario rows and matching projection, label, and UAV artifacts. Update the validator for the derived row counts and scenario invariants.

## Slice 2 — evidence regeneration and verification

Regenerate V2.1 and the evidence catalog. Assert that each route point produces fused KSF convoy evidence and retains source provenance.

## Slice 3 — deployment validation

Deploy the derived dataset and evidence catalog, restart affected services, clear only test assessments if needed, run the natural Talia request, and verify the assessment and map overlay.

## Rollback

Restore the previous V2.1 generated artifacts and evidence catalog. Immutable V2 artifacts are never changed.
