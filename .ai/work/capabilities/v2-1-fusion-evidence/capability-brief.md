# V2.1 Cross-Source Fusion Evidence

## Goal

Create a V2.1 dataset that preserves the V2 schema, scenario, scale, and Serbian-intelligence perspective while adding intentional cross-source evidence chains suitable for evaluating Moshe's geographic and semantic fusion workflow.

## User decision

On 2026-07-18 the user approved proceeding with a V2.1 correction instead of overwriting deployed V2.

## Current problem

V2 public-source and UAV records are independently sampled from common event, actor, location, and time distributions. They are scenario-aligned but do not reliably describe the same physical object. Accidental correlations therefore dominate strict fusion evaluation.

## Scope

- Leave V1 and V2 files untouched.
- Produce approximately 14,800 V2.1 raw records with the existing runtime projection schema.
- Preserve 3,800 UAV observations and the current source balance.
- Add deterministic, intentional evidence chains joining UAV and public-source records.
- Use varied public terminology, uncertain counts, and multiple source platforms.
- Add evaluator-only truth identifiers and target truth artifacts; do not expose them in raw records or the runtime projection.
- Add negative/distractor evidence where practical.
- Validate reproducibility, source independence, scenario consistency, and V1/V2 immutability.

## Non-goals

- Implement Moshe or the attack-targets layer.
- Change the production dataset selection.
- Claim observation-level coordinates that the corpus does not contain.
- Alter V1 or deployed V2.

## Acceptance criteria

- V2.1 contains 14,800 unique raw records and 3,800 UAV records.
- At least 300 evaluator-known target objects have one UAV observation and two public-source confirmations from distinct platforms.
- Each chain agrees on event, actor, canonical location, and a bounded time window while varying terminology and count language.
- Evaluator truth is absent from raw and runtime projection files.
- At least 100 hard-negative records are labeled only in evaluator artifacts.
- Generation is deterministic and all V1/V2 hashes remain unchanged.
- A validation script proves the above conditions.

## Key assumption

Canonical locations support area-level fusion only. V2.1 truth identifies a shared scenario object within that area, not a precise sensor coordinate.
