# Execution Plan — Common Evidence Foundation

## Plan status
Approved by explicit user instruction to implement and deploy stages 1–3.

## Slice 1 — Evidence model and projection
Create a SQLite-backed evidence repository and deterministic projection for UAV/public records. Validate canonical identifiers, status, confidence, claim fields, and provenance.

## Slice 2 — Neutral fusion
Create neutral preparation/persistence tools by reusing current source grouping, relationship scoring, quantity reconciliation, and evidence snapshots. Refactor target preparation to delegate neutral work without changing target authorization.

## Slice 3 — Presentation and deployment
Add `evidence` to requested-result materialization, response normalization, UI layers, map/table rendering, and object viewer. Test the Ibar Bridge scenario, regression-test existing targets, deploy, and smoke-test production.

## Risks and controls
- Data explosion: observations are projected on demand; only validated fused objects persist.
- False fusion: require one subject, location, object class, temporal coherence, provenance, and explicit source grouping.
- UI duplication: evidence layers open only on demand and raw source records remain separately accessible.
- Target regression: retain existing target eligibility and persistence boundary tests.

## Rollback
Remove the evidence tool registration and layer kind; the existing raw and target stores remain independent.

