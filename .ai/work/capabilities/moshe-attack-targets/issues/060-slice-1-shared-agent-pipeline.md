# [Slice 1] Shared Agent Invocation and Result Pipeline

## Purpose

Extract reusable agent invocation, normalization, layer-result, and presentation contracts while preserving General behavior.

## Completion criteria

- [x] Shared contracts implemented and documented.
- [x] General-agent regression suite passes.
- [ ] Architecture/interface checkpoint approved.

## Deployment status

The first deployment regressed the member strip and `@` autocomplete because it used a stale frontend baseline. Slice 1 was rebuilt on `codex/integrate-michlol-dataset-v2`, explicit member/mention regression tests were added, and the corrected build was redeployed on 2026-07-19. V2.1 remains active with 14,800 rows. Current rollback backup: `/opt/serbia-poc-ui-backups/slice1-20260719T183742Z`.

## Checkpoint

`../checkpoint-001.md`

## Depends on

`055-execution-plan-review.md`
