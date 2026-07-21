# [QA Review] Moshe Fusion, Routing, Persistence, and Regression Plan

## Purpose

Approve test coverage for Moshe fusion quality, evaluator isolation, routing/session continuity, SQLite safety, presentation, and General-agent regressions.

## Required action

Carry the approved QA strategy into execution planning and define exact metric thresholds before full evaluation.

## Owner role

QA

## Inputs

- `qa-review.md`
- Chapters 1 and 2
- Architecture/security review
- V2.1 truth and hard-negative artifacts in isolated test scope

## Expected output

Approved QA planning baseline and test gates for every execution slice.

## Blocking

QA planning no longer blocks execution planning. Exact quantitative thresholds block the full-evaluation slice if not defined earlier.

## Completion criteria

- [x] Positive and hard-negative evaluation scope approved.
- [x] Routing/session tests approved.
- [x] Persistence and transaction tests approved.
- [x] Evaluator-isolation negative tests approved.
- [x] General-agent and presentation regression coverage approved.
- [x] Production memory/swap observation included.
- [ ] Exact quantitative quality thresholds to be set in execution planning.

## Related artifacts

- `.ai/work/capabilities/moshe-attack-targets/qa-review.md`

## Parent capability

Moshe Attack Targets MVP; remote parent issue pending.
