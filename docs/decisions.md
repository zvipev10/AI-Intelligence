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
