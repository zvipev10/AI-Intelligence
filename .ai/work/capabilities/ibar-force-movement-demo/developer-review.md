# Developer review

Status: Ready for planning by explicit user delegation.

The safest implementation is to extend the deterministic V2.1 generator while leaving immutable V2 inputs untouched. The scenario will add nine derived raw records: three UAV observations and six public corroborations. Existing projection and evaluator-label artifacts must receive matching rows, and the UAV observation artifact must receive the three UAV records.

Neutral fusion remains unchanged because it intentionally creates location-scoped object-presence evidence. Talia will compare the three fused objects and decide whether the pattern supports force movement.

Risks:

- Legacy artifact filenames contain `14800`; consumers must use file contents rather than infer count from the name.
- A model may still decline movement; validation must include an actual Talia run.
- The movement wording must avoid implying exact convoy continuity.

Test strategy:

- Deterministic regeneration twice.
- Dataset cardinality, referential-integrity, and scenario-field assertions.
- Evidence-catalog assertions for the three scenario locations.
- Existing evidence and assessment unit tests.
- Deployed natural-language Talia run.
