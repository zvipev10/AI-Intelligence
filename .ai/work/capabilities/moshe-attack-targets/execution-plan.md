# Execution Plan

## Status and prerequisite gate

Status: Executed through Slice 7. All approved Slice 6 thresholds pass; production verification is complete and final capability acceptance is pending.

## Slice 1 - Shared agent invocation and result pipeline

- Extract the current General-agent normalization and presentation contracts into shared backend modules.
- Support agent identity, Hermes session ID, optional mission-run ID, and typed layer results without agent-specific UI paths.
- Preserve all existing General-agent behavior and tests.
- Stop for checkpoint review because this changes shared interfaces and architecture.

## Slice 2 - SQLite target bank and constrained tools

- Implement the `targets` and `target_evidence` schema for candidate-only, final-state storage.
- Store canonical `location_id` and `entity_id` references without copying coordinates or entity data.
- Add parameterized create/update/read tools, backup, and admin-only reset; expose no raw SQL, filesystem, delete, or status-transition tools to Moshe.
- Enforce the approved ownership, `0700` directory, `0600` database, transaction, and latest-five-backup policy.
- Stop for schema, migration, permission, backup, and recovery review.

## Slice 3 - Fusion and source-independence tools

- Reuse existing investigation tools and add deterministic source-group normalization, independence checks, evidence snapshot construction, quantity reconciliation, and duplicate-candidate lookup.
- Enforce at least two independent source groups; collapse reposts and records from the same UAV mission.
- Save medium/high-confidence candidates only; report low-confidence findings without persistence.
- Stop for fusion-contract and evaluator-isolation review.

## Slice 4 - Moshe profile, routing, and session continuity

- Add an on-demand Hermes Moshe profile with the approved restricted tool allowlist.
- Route only messages containing exact `@משה` to Moshe.
- Continue the same Moshe mission and Hermes session across consecutive `@משה` messages; close it on the first message without the mention.
- Let Moshe request missing information directly; each user reply intended for Moshe must again contain `@משה`.
- Stop for routing, context-boundary, permission, and prompt review.

## Slice 5 - Shared attack-target presentation

- Add the shared `attack_targets` layer kind and return it through the common result contract.
- Render attributed Moshe responses and candidate targets in the existing map/table pipeline, including evidence and approved loading, clarification, empty, error, permission, RTL, mobile, and accessibility states.
- Do not add a Moshe-specific rendering path or timeline.
- Stop for UX and General-agent regression review.

## Slice 6 - Full V2.1 evaluation

- Run all 300 positive chains and 100 hard negatives with evaluator truth physically and logically excluded from runtime, deployment, configuration, imports, and persisted target data.
- Use a separate post-run evaluator.
- Proposed release thresholds: chain recall at least 90%; evidence precision at least 90%; evidence recall at least 90%; hard-negative rejection at least 95%; false-merge rate at most 5%; duplicate-target rate at most 2%; deterministic source-independence tests 100%; evaluator-truth leakage zero; no accepted General-agent regressions.
- Record failures by category and repeat the complete deterministic suite after fixes.
- Stop for QA acceptance.

## Slice 7 - Production deployment, verification, and handoff

- Back up the target bank, deploy shared modules, MCP tools, Moshe profile, and UI changes through the existing deployment path.
- Verify permissions, routing/session behavior, direct Moshe presentation, persistence, backup/reset recovery, UI states, service health, and VM memory/swap under representative workloads.
- Keep the prior release deployable and document rollback.
- Publish checkpoints and final handoff only after production verification.

## Expected implementation areas

- `server.py` and shared backend result/agent modules extracted from it.
- `app.js`, `styles.css`, and `index.html` for the shared layer renderer and attribution.
- `mcp_server/server.py` and focused target-bank/fusion modules.
- Hermes profile/configuration and deployment allowlists/scripts.
- Unit, integration, routing, persistence, UI, security, regression, and evaluator tests.

## Rollback

- Disable exact-mention routing and remove the Moshe profile from the active configuration.
- Restore the prior shared application/MCP deployment.
- Restore the SQLite file from the pre-deployment backup when persistence rollback is required.
- Do not alter the V2.1 dataset or evaluator truth during rollback.

## Completion rule

Each slice requires passing checks and its named checkpoint before the next slice. Slice 1 authorization requires Product and QA approval of this plan, including the proposed thresholds.
