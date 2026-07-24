# Handoff Summary

## 2026-07-24 — Structured evidence-reference layers

Checkpoint 014 is deployed. General and Moshe now return separate `requested_result_layers` and `evidence_reference_layers` through the shared `present_requested_results` contract. The answer renders `מזהי ראיות` as independently controlled map/timeline layer links; no result or evidence layer is shown automatically. Eighty-six automated regressions pass, both live agent smokes produced structured evidence, and all VM services are healthy. Rollback backup: `/home/ubuntu/deploy-backups/evidence-reference-layers-20260724T140000Z`.

## Current state

All implementation slices are deployed. Slice 6 quality gates pass, and Slice 7 production verification is technically complete. Final Product/QA capability acceptance remains.

## Latest implementation

- Shared `attack_targets` result layer in `agent_result_pipeline.py`.
- Audit-backed target extraction and canonical presentation enrichment in `server.py`.
- Shared typed-layer consumption, refresh/deduplication, map/table/evidence presentation in `app.js` and `styles.css`.
- Focused backend and UI regression coverage.
- UI follow-up adds a live Moshe-originated roster message, punctuation-safe and persistent mention highlighting, and raw record IDs in target map popups.
- Checkpoint 007 labels Moshe responses as `משה - קצין מטרות` based on `responding_agent`, including explicit mentions without roster selection.

## Validation

53 focused Linux tests pass, along with JavaScript syntax, Python compilation, the complete 400-case evaluation, production routing/session checks, isolated restore, permissions, evaluator isolation, and `git diff --check`.

## Deployment state

UI follow-up commit `cf3e325` is deployed. General remains on port 8642, Moshe on port 8643, and UI on port 8769. Code rollback backup: `/opt/serbia-poc-ui-backups/ui-fixes-20260720T175638Z`.

Production smoke checks passed for service health, served assets, raw-reference search results, and a Moshe-attributed live member-opening response. The target bank was not cleared: SQLite integrity is `ok`, and the existing 3 targets and 14 evidence links remained unchanged. Pre-deployment database backup: `/opt/serbia-poc/backups/attack_targets/attack_targets-pre-ui-20260720T175618Z.db`.

Checkpoint 007 deployed the exact `משה - קצין מטרות` answer label. Rollback backup: `/opt/serbia-poc-ui-backups/moshe-title-20260720T200414Z`. Eight focused Linux tests and JavaScript syntax passed; the served asset, V2.1 14,800-row status, UI service health, and unchanged SQLite counts were verified.

Checkpoint 008 deployed bounded corroboration discovery and evidence-pair ranking inside `prepare_target_candidate`. Rollback backups: `/opt/serbia-poc-backups/moshe-quality-20260721T034228Z` and `/opt/serbia-poc/backups/attack_targets/attack_targets-pre-quality-20260721T034228Z.db`. A read-only preparation smoke test passed; all services are active, runtime evaluator artifacts remain absent, and SQLite remains unchanged.

The in-app browser blocked further access to the VM raw-IP URL under its URL policy, so final visual interaction verification is assigned to the user.

## Next action

Product/QA accepts `checkpoint-009-slice-7-release.md` and the recorded residual risks. Then mark the parent capability complete.

## Open decisions

No implementation decision remains. Acceptance must explicitly include the 1.27% residual false-merge rate, seven-class alias scope, and constrained-VM memory/swap risk.
