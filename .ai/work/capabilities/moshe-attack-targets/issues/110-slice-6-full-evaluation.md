# [Slice 6] Full V2.1 Evaluation

## Purpose

Evaluate all 300 positive chains and 100 hard negatives with an isolated post-run evaluator.

## Completion criteria

- [ ] All approved quantitative thresholds pass.
- [ ] Evaluator-truth leakage is zero.
- [ ] General-agent regression results are accepted.
- [ ] QA checkpoint approved.

## Depends on

`100-slice-5-target-presentation.md`

## Current result

The first complete evaluation failed the quality gates. Baseline and diagnosis are recorded in `checkpoint-006.md` and `evaluation-006.json`.

## Recovery plan

`slice-006-quality-recovery-plan.md`

Implementation remains checkpointed into bounded retrieval, evidence-pair scoring, ambiguity control, and a frozen full rerun.
