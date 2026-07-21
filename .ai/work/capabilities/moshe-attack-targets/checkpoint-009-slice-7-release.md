# Checkpoint Summary

## Checkpoint

009 - Slice 7 production acceptance and release handoff

## Status

Production verification complete; ready for final Product/QA acceptance.

## Release scope

- Exact current-message `@משה` routing to the persistent Moshe profile.
- Consecutive-message Moshe mission continuity and General-message mission closure.
- Shared General/Moshe backend and presentation pipeline.
- SQLite candidate target bank with constrained MCP tools and protected backups.
- Target fusion preparation with bounded corroboration discovery, pair ranking, ambiguity handling, and independent creation-time validation.
- Shared attack-target map/table presentation with raw record references.

## Acceptance evidence

| Area | Production evidence | Result |
|---|---|---|
| General routing | Non-mention prompts returned `responding_agent=general` | Pass |
| Moshe routing | Exact `@משה` prompts returned `responding_agent=moshe` | Pass |
| Mission continuity | Two consecutive mentions reused one mission ID | Pass |
| Mission closure | A General message closed the mission; the next mention received a new mission ID | Pass |
| Non-writing behavior | Five acceptance prompts returned no target layers and did not change SQLite | Pass |
| Direct preparation | Read-only `prepare_target_candidate` selected and ranked three evidence records | Pass |
| Quality | All approved 300-positive/100-negative gates pass in checkpoint 008 | Pass |
| UI contracts | Served title, punctuation-safe mentions, agent opening, raw references, and shared target layer are present | Pass |
| Persistence | SQLite integrity `ok`; 3 existing targets and 14 evidence links preserved | Pass |
| Permissions | Target directory `0700`; database `0600`; root-owned backup `0600` | Pass |
| Restore | Backup restored to an isolated temporary database with integrity `ok` and matching counts | Pass |
| Evaluator isolation | Zero truth/evaluator files under both runtime trees | Pass |
| Services | UI, General, and Moshe active with zero failure restarts | Pass |
| Dataset | V2.1 active with 14,800 rows | Pass |

## Validation inventory

- 25 MCP fusion, target-bank, and security-boundary tests pass on Linux.
- 28 shared result, routing, member UI, and Moshe-profile tests pass on Linux.
- JavaScript syntax passes.
- Full isolated evaluation passes every approved gate.
- Production routing/session, read-only fusion, UI contract, permission, restore, isolation, and persistence checks pass.

## Rollback inventory

- UI Slice 5: `/opt/serbia-poc-ui-backups/slice5-20260719T202907Z`.
- UI follow-up: `/opt/serbia-poc-ui-backups/ui-fixes-20260720T175638Z`.
- Moshe title: `/opt/serbia-poc-ui-backups/moshe-title-20260720T200414Z`.
- Quality MCP code: `/opt/serbia-poc-backups/moshe-quality-20260721T034228Z`.
- Pre-quality SQLite: `/opt/serbia-poc/backups/attack_targets/attack_targets-pre-quality-20260721T034228Z.db`.

Code rollback restores `server.py` and `fusion_tools.py` from the quality backup and restarts both Hermes gateways. Database rollback is separate and should occur only when persistence recovery is required, after preserving the current database.

## Resource observation

Before the final live routing workload, available memory was approximately 305 MB. After five sequential General/Moshe requests and a ten-second settling period:

- available RAM: approximately 186 MB;
- swap used: approximately 331 MB of 2,047 MB;
- all services remained active;
- failure restart counts remained zero.

This passes stability for the representative acceptance workload but confirms the existing constrained-VM risk. Sustained Moshe workloads require resource monitoring; no application-level limits were approved for the MVP.

## Residual risks

- Evaluated false-merge rate is 1.27%, below the approved 5% ceiling but not zero.
- The visible alias taxonomy covers the seven V2.1 MVP target classes only.
- The VM has limited memory headroom under sequential dual-agent activity.
- Automated in-app browser verification is blocked by the raw-IP URL policy; the user remains the final visual acceptance owner.

## QA recommendation

Approve the Moshe Attack Targets MVP release with the recorded residual risks. Do not expand target classes or sustained workload expectations without a new capability review.

## Final action

Product/QA provides final capability acceptance. After acceptance, mark the parent capability complete; remote issue and draft-PR creation remain administrative follow-ups because they were never created during the local workflow.
