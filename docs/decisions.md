# Decision Log

Use this file for durable product and technical decisions.

## Format

### YYYY-MM-DD — Decision title

Decision:
[What was decided]

Context:
[Why this came up]

Rationale:
[Why this option was chosen]

Alternatives considered:
[Short list]

Impact:
[Product/technical impact]

Follow-ups:
[Any needed actions]

### 2026-07-18 - Preserve V2 and add evaluator-grounded V2.1 fusion evidence

Decision:
Keep V1 and deployed V2 immutable. Create V2.1 from V2 with intentional cross-source shared-object evidence chains and evaluator-only truth labels.

Context:
V2 public and UAV records were sampled independently. They were aligned to the same scenario but could not reliably prove that two sources described the same physical object, which made Moshe fusion evaluation depend on accidental correlations.

Rationale:
A small version increment preserves reproducibility and rollback while providing measurable positive and negative cases. Evaluator truth remains outside raw and runtime projection data so the investigating agent cannot use it.

Alternatives considered:
Overwrite V2; infer truth from accidental V2 correlations; create an entirely unrelated dataset.

Impact:
V2.1 contains 300 positive cross-source chains and 100 hard negatives at the existing 14,800-record scale. Runtime selection is optional; production remains on V2 until separately released.

Follow-ups:
Use V2.1 to implement and evaluate Moshe, the global `attack targets` layer, duplicate detection, source-independence rules, and human approval.

### 2026-07-28 — Define playback scenarios as scoped timeframe stages

Decision:
Represent a reusable historical playback scenario as identity/version metadata,
one data scope, and an ordered list of stages with inclusive `from` and
exclusive `to` timestamps. Keep record IDs, targets, assignments, agent state,
and transition history outside the scenario artifact.

Context:
The initial playback design placed responsibilities, released references, and
other runtime concerns in the manifest. Product proposed that a list of
time-bounded stages was sufficient and explicitly approved the simplified
design.

Rationale:
Time windows describe when scenario information becomes visible without
coupling the platform contract to a particular record sequence. Runtime and
collaboration state evolve independently and belong in persistent run and
workstream models.

Alternatives considered:
- Embed record IDs in each stage.
- Put assignments and decisions in the scenario manifest.
- Encode a domain-specific target assessment sequence.

Impact:
Manifests are strict and reject unsupported fields. Playback visibility is
cumulative, stages may contain gaps but cannot overlap, and any historical
fixture can change its records without changing platform code.

Follow-ups:
Implement retrieval visibility enforcement before exposing playback controls,
then add UI and automatic agent reevaluation in separately approved slices.
