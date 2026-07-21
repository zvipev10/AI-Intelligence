# Checkpoint Summary

## Checkpoint

004 - Slice 4 routing core and Hermes profile constraint

## Checkpoint status

Deployed for user testing; pending routing/security acceptance

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

- Real target-identification evaluation and Slice 5 attack-target presentation.
- Sustained concurrent-load acceptance; initial smoke load is recorded below.

## Recommendation

Pause for routing/security review. If approved, proceed to Slice 5 shared attack-target presentation.

## Validation results

- 20 routing, session, shared-result, member-UI, and profile-isolation tests pass on Linux.
- JavaScript syntax and Python compilation pass on the VM.
- Profile tests prove the separate port/audit path, Serbia-only MCP selection, exact approved tool allowlist, and absence of evaluator contract markers.
- Current VM capacity: 954 MB RAM, approximately 460 MB available at inspection, 2 GB swap; existing gateway current memory approximately 171 MB with a historical peak around 591 MB.

## Deployment and smoke verification

Deployment date: 2026-07-19

- Backup: `/opt/serbia-poc-ui-backups/slice4-20260719T-routing`.
- General gateway remains healthy on `127.0.0.1:8642`.
- Moshe gateway is enabled and healthy on `127.0.0.1:8643`.
- UI service is healthy on port `8769`, V2.1 reports 14,800 rows, and member UI assets remain installed.
- Target bank initialized empty with directory `0700`, database `0600`, and counts `targets=0`, `evidence=0`.
- Deployed Moshe profile exposes one Serbia MCP server with 24 selected tools.
- Ordinary smoke request returned `responding_agent=general`.
- First `@משה` smoke request returned `responding_agent=moshe` and a Moshe mission/session ID.
- Consecutive `@משה` smoke request reused the same mission/session ID.
- The next message without `@משה` returned `responding_agent=general` with no mission ID.
- Moshe gateway after smoke load: approximately 186 MB current RAM, 196 MB peak, 9 MB current/peak swap, zero service restarts after corrected activation.
- Whole VM after smoke load: 954 MB total RAM, approximately 214 MB available, 2 GB swap with approximately 489 MB used.

Deployment corrections:

- Hermes profile creation does not allow `--clone` with `--no-skills`; cloned configuration was subsequently restricted by the provisioner.
- The persistent unit must set profile-scoped `HERMES_HOME` without `-p`, and `API_SERVER_PORT=8643` because the API adapter reads the port from the environment.
- Cloned Telegram/WhatsApp and other messaging variables are removed; only the API-server platform remains.
- Temporary deployment/validation directories, including copied configuration, were removed after verification.
- User testing exposed OpenAI's 64-character `prompt_cache_key` limit because the initial mission ID embedded the full conversation ID. Mission/session IDs now use a fixed 35-character `moshe-<conversation-hash>-<nonce>` format. A 500-character conversation-ID boundary test and a deployed real Moshe request both pass without the previous HTTP 400 error.
