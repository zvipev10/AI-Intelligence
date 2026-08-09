# Checkpoint 001 — Evidence-first workstream creation deployment

## Result

Implemented, tested, deployed, and live-smoke validated on 2026-08-09.

## Changes

- Moshe resolves all supplied `TGT-*` and `REC-*` identifiers before asking for metadata.
- Target-seeded creation uses `get_target_candidate` for canonical context.
- Raw-record creation checks existing target membership and uses read-only candidate preparation for
  additional evidence context.
- Moshe infers title, objective, and responsibility and asks at most one focused blocking question.
- Workstream creation explicitly prohibits target-bank create/update operations.
- Persistent profile, runtime instruction, and MCP tool description are aligned.

## Validation

- `python -m unittest test_moshe_profile.py`: 8 passed.
- MCP `test_workstream_indication_tools.py` and `test_target_tool_boundary.py`: 21 passed.
- Python compilation passed for UI server, MCP server, and profile provisioner.
- `git diff --check` passed.
- Deployment verification passed for UI service, Moshe service, health endpoint, public UI contract,
  server contract, MCP tools, and installed Moshe tools.

## Live smoke

Prompt: `@משה צור מעקב אחר TGT-F2CA47CB9859`

Result: Moshe created `ws_20260809_112912_b5804737` in isolated investigation
`deploy-smoke-1786274915527` without a metadata question. It inferred:

- title: `מעקב היערכות KFOR בגישות הצפוניות לזבצ׳אן`
- an evidence-grounded monitoring objective
- Moshe's collection, corroboration, classification, and update responsibility

## Deployment

- Host: `151.145.93.180`
- Rollback backup: `/opt/serbia-poc-ui-backups/workstream-slice2-20260809T112716Z`
- UI and Moshe services: active
- Dataset: v2.1, 14,800 rows

## Risks

- Prompt behavior remains probabilistic; evaluation cases and contract assertions reduce drift but do
  not replace periodic live checks.
- Raw-record expansion can add latency depending on candidate preparation workload.
- The isolated smoke workstream remains persisted for auditability.

## Recommendation

Approve the deployment. Keep the parent capability open until the user validates one raw-record case
and confirms the inferred wording quality.
