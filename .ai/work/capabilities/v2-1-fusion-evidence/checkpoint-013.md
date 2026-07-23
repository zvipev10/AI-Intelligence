# Checkpoint 013 — Stable evidence-group reconciliation

Date: 2026-07-23

## Problem

`attach_target_evidence` compared literal generated `source_group` labels. Adding evidence could renumber ordinal `visible-report:001`, `002`, and similar labels without changing their memberships, causing valid attachments to be rejected as immutable-group changes.

The latest production failure attempted to attach `REC-V2-006452`, `REC-V2-007655`, and `REC-V2-004558` to `TGT-70C964B0ECC0`. All three records belong to `uav-mission:UAV-MSN-021`; the operation failed only because two existing visible-report labels swapped ordinals.

## Fix

- Compare the partition relationships among existing records rather than literal recomputed labels.
- Preserve every existing stored group ID when membership remains equivalent.
- Reject a real merge of two existing groups or a real split of one existing group.
- Assign genuinely new visible-report groups a stable membership-derived hash rather than another ordinal ID.
- Keep stable UAV-mission and observation group IDs when they do not conflict.

## Validation

- 29 target-bank, fusion, and MCP-boundary tests passed on the VM.
- Tests cover harmless ordinal swaps, true merge rejection, stable new visible-report IDs, and the exact six-record production failure against a temporary database.
- The exact regression now attaches all three UAV records, preserves the three existing stored group IDs, and results in six evidence records without touching production data.

## Deployment guard

Back up the target database and MCP server before deployment. Restart Moshe’s gateway after installing the constrained MCP server. Do not automatically retry the previously failed write; the user can ask Moshe to retry after deployment.
