# Checkpoint Summary

## Checkpoint

004 - Slice 4 routing core and Hermes profile constraint

## Checkpoint status

Partial implementation; architecture decision required

## Completed

- Added an exact current-message `@משה` matcher; history is not inspected.
- Added a thread-safe registry keyed by conversation/investigation ID.
- Consecutive `@משה` messages reuse one mission and bound Hermes session.
- A message without `@משה` closes and clears the Moshe mission/session.
- A later mention creates a new mission.
- Stale session binding and cross-conversation leakage are rejected.

## Validation

- Five routing/session tests pass on the Linux VM.
- Python compilation passes.
- Read-only VM inspection confirmed Hermes 0.14 native named profiles and CLI session resume.
- Read-only source inspection confirmed the installed `/v1/runs` handler accepts session/history/instructions but no named profile or per-run tool allowlist.

## Decision required

Recommended for the MVP: invoke the native Moshe profile on demand through `hermes -p moshe chat -Q`, capture the returned session ID, and use `--resume` for consecutive mentions. This honors the no-second-gateway decision and provides profile-level MCP/tool isolation. The tradeoff is no live structured progress stream for Moshe; the final result still uses the shared normalization and presentation pipeline.

Alternative: modify the installed Hermes gateway API to resolve a named profile per run. This keeps structured streaming but introduces an upstream patch, concurrent-profile security work, deployment coupling, and upgrade risk.

The previously rejected alternative is a second permanent gateway for Moshe.

## Not completed

- Moshe profile provisioning and restricted MCP configuration.
- Backend invocation/resume integration.
- Clarification and restricted-tool integration tests.
- Production deployment.

## Recommendation

Approve the on-demand native-profile CLI transport for the MVP, then complete Slice 4.
