# Checkpoint Summary

## Checkpoint

002 - Slice 2 SQLite target bank and constrained tools

## Capability

Moshe Attack Targets MVP

## Related issue

`issues/070-slice-2-target-bank.md`

## Checkpoint status

Pending data/security review

## Handoff

Next role: Development and Architecture/Security

Required action: Review the candidate-only schema, MCP write boundary, backup/restore/reset behavior, and deployment configuration.

Expected output: Approve Slice 2 or request focused changes.

Do not proceed to: Slice 3 fusion/source-independence implementation.

Until: This checkpoint is approved.

## What changed since previous review

Slice 1 was approved by all required members and the user authorized Slice 2 development.

## Slice goal

Provide protected final-state SQLite persistence and constrained candidate tools without implementing fusion logic, Moshe routing, target presentation, or human lifecycle operations.

## What changed

- Added `target_bank.py` with transactional `targets` and `target_evidence` persistence.
- Enforced candidate-only status, medium/high confidence, approved quantity shapes, canonical references at the MCP boundary, unique evidence, and at least two source groups at creation.
- Added exact search/read/create/update/evidence-append MCP tools.
- Assigned `created_by=moshe` on the server; agents cannot supply creator, status, review fields, SQL, paths, deletion, backup, reset, or restore.
- Added administrator-only initialize/count/backup/reset/restore operations with explicit paths and confirmation flags.
- Backups use SQLite's backup operation, mode `0600`, and latest-five retention. Restore validates integrity, creates a safety backup, and verifies counts.
- Added production deployment configuration for protected target-bank and backup directories while leaving target tools out of the General-agent allowlist.
- Added a disposable Linux VM validation command; it cleans its temporary validation directory and does not deploy Slice 2.

## Files changed

- `llm_investigation_orchestrator_serbia_poc/mcp_server/target_bank.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/target_bank_admin.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/remote_deploy_serbia.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/remote_validate_target_bank.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/test_target_bank.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/test_target_tool_boundary.py`
- `.ai/work/capabilities/moshe-attack-targets/checkpoint-002.md`
- `.ai/work/capabilities/moshe-attack-targets/status.md`
- `.ai/work/capabilities/moshe-attack-targets/decisions.md`
- `.ai/work/capabilities/moshe-attack-targets/issues/070-slice-2-target-bank.md`

## Decisions made

- The storage layer enforces the minimum two-source-group invariant at creation; Slice 3 will determine whether groups are truly independent.
- Evidence is append-only through agent tools; existing evidence cannot be edited or deleted.
- General deployment configuration does not expose target write tools. Moshe's dedicated allowlist remains Slice 4 work.
- Slice 2 is not deployed or activated in production before checkpoint approval.

## Tests/checks run

- 10 target-bank tests pass locally; the POSIX permission test is skipped on Windows.
- 6 MCP boundary/integration tests pass locally.
- Existing 6 shared-agent pipeline tests and 4 member UI regression tests pass.
- Python compilation passes for the target bank, admin command, MCP server, validation script, and deployment script.
- Disposable Linux VM run: all 10 target-bank tests pass, including POSIX permissions.
- Linux permission verification: target directory `0700`, SQLite file `0600`.
- `git diff --check` passes.

## Not completed yet

- Source-group independence and fusion tools.
- Moshe profile, tool allowlist, routing, and sessions.
- Target layer presentation.
- Production target-bank deployment and initialization.
- Full V2.1 evaluation.

## Blockers

- Data/security checkpoint approval.
- Remote GitHub issues and draft PR remain unavailable through local `gh` tooling.

## Risks

- Source-group labels are agent/tool inputs until Slice 3 adds deterministic independence classification.
- The legacy full MCP deployment script still targets its existing V2 configuration; production Slice 2 deployment must use the current V2.1-safe release path.

## Open questions

None for the approved Slice 2 scope.

## Review requested from

Development and Architecture/Security.

## Continue / pause recommendation

Pause for data/security review.

## Next planned slice

Slice 3 - Fusion and source-independence tools.
