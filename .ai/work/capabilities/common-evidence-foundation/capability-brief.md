# Common Evidence Foundation

## Status
Approved for implementation by the user's 2026-09-15 instruction.

## Problem
Raw records and target-specific fusion exist, but the platform has no neutral, persistent evidence object that both future assessment and current target workflows can consume.

## Scope
- Project existing UAV and public-source records into normalized evidence objects.
- Persist validated fused evidence with immutable raw-record provenance.
- Extract reusable fusion preparation from Moshe's target-specific flow.
- Add neutral evidence retrieval, fusion, persistence, and provenance tools.
- Add an on-demand `evidence` result layer and evidence-object viewer.
- Refactor target preparation to consume the neutral fusion preparation without changing target persistence rules.

## Non-goals
- Talia profile or enemy-assessment artifacts.
- Automatic projection/persistence of all 14,800 records.
- Advanced MIL-STD lines, polygons, or tactical graphics.
- Replacing current raw-record or target layers.

## Acceptance criteria
1. Existing records project deterministically as `reported` or `observed` evidence.
2. Valid coherent inputs can produce and persist `fused` evidence.
3. Every evidence object traces to immutable REC identifiers.
4. Duplicate and contradictory inputs remain explicit.
5. Moshe target preparation retains its existing eligibility behavior through the neutral fusion module.
6. `present_requested_results` accepts evidence IDs and the UI displays them on demand.
7. Ibar Bridge fixtures cover projection, fusion, provenance, and presentation.
8. Existing raw and target workflows regress cleanly.

