# Checkpoint Summary

## Checkpoint

004 - Slice 4 routing core and Hermes profile constraint

## Checkpoint status

Implemented; pending routing/security checkpoint approval

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

## Approved architecture

The user approved a persistent isolated Moshe gateway. General remains on port `8642`; Moshe uses its named profile on port `8643`. Both use the same structured `/v1/runs` contract, preserving live steps and final shared-result normalization.

The on-demand CLI approach and an upstream gateway patch were rejected because they respectively lose live structured events or create an upgrade/security burden.

## Additional implementation

- Added per-agent endpoint/audit configuration while keeping shared transport credentials.
- Added a restricted Moshe profile provisioner, identity prompt, and systemd unit.
- Restricted Moshe to the Serbia MCP and the approved investigation, fusion, duplicate, and candidate tools.
- Separated General and Moshe audit files so live progress cannot overwrite the other agent's steps.
- Routed live-step polling to the responding gateway while retaining the existing activity UI.
- Routed on the unmodified current user message, preventing `@משה` examples in enriched system instructions from triggering Moshe.
- Added a 400 MB memory-high guard and 600 MB hard service limit.

## Not completed

- Production deployment.
- Real-model clarification behavior and dual-gateway load validation, which belong to deployment/evaluation checkpoints.

## Recommendation

Pause for routing/security review. If approved, proceed to Slice 5 shared attack-target presentation.

## Validation results

- 20 routing, session, shared-result, member-UI, and profile-isolation tests pass on Linux.
- JavaScript syntax and Python compilation pass on the VM.
- Profile tests prove the separate port/audit path, Serbia-only MCP selection, exact approved tool allowlist, and absence of evaluator contract markers.
- Current VM capacity: 954 MB RAM, approximately 460 MB available at inspection, 2 GB swap; existing gateway current memory approximately 171 MB with a historical peak around 591 MB.
