# Execution Plan

## Prerequisite review gate

- Product direction: approved by user on 2026-07-18.
- Developer review: approved for execution in `developer-review.md`.
- QA review: approved for execution in `qa-review.md`.
- UX review: not required; this capability does not change UI behavior.

## Slice 1 - Generator and truth contract

- Add a V2.1 generator that reads V2 as immutable input.
- Select deterministic UAV truth anchors.
- Bind compatible public records and generate varied confirmation language.
- Produce evaluator-only truth IDs, roles, and hard-negative labels.

## Slice 2 - Generation and validation

- Generate V2.1 artifacts.
- Add a repeatable validator.
- Check counts, independence, alignment, non-leakage, integrity, determinism, and V1/V2 immutability.

## Slice 3 - Compatibility and handoff

- Smoke-load the V2.1 projection with current runtime code.
- Record limitations and readiness for Moshe.
- Do not deploy or switch production without a separate decision.

## Rollback

Delete the V2.1 directory and generator. V1, V2, and production remain unchanged.
