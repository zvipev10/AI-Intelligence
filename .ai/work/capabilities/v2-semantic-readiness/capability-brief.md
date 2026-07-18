# Capability Brief — V2 Semantic Readiness

## Goal

Complete the semantic adaptation of the synthetic Serbian-intelligence V2 corpus before Moshe agent implementation.

## Authorized scope

- Expand semantic concepts for UAV objects, military movement/formations, force concentration, affiliations, same-object terminology, and count language.
- Preserve normalized UAV observation fields in the V2 runtime projection.
- Index the structured fields directly and return them with semantic results.
- Add deterministic regression tests and V2 semantic probes.
- Rebuild/validate the V2 semantic index.

## Non-goals

- Moshe agent or attack-target-bank implementation.
- Live or real-world data ingestion.
- Changes to immutable V1 artifacts.
- External embedding-model integration.
- UI behavior changes.

## Acceptance criteria

- V2 projection includes normalized UAV object/count/movement/confidence fields.
- All 3,800 UAV projection rows retain object class and estimated count.
- Semantic document text explicitly includes structured fields.
- V2 concept aliases cover the user-requested families in Hebrew, Serbian/English terminology where relevant.
- Synonym queries retrieve compatible V2 object records.
- Count queries use the structured count signal.
- Index cache remains version-isolated and invalidates after projection change.
- V1 source hashes remain unchanged.
- Regression and performance results are recorded.

## Product approval

Execution explicitly requested by the user on 2026-07-18.
