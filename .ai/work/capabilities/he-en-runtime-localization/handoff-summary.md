# Handoff Summary

## Current state
The locale-keyed MCP runtime is implemented and its initial code/assets are deployed, but production semantic acceptance is blocked by VM resource exhaustion. Target candidates remain locale-isolated; workstreams remain for the next slice.

## Published baseline
Commit `eb9168c` on `origin/codex/he-en-localization` contains the brief, developer review, QA review, execution plan, and status dashboard.

## Key finding
The screenshot was caused by partially translated `.en` assets, not by the English UI toggle. The old generator accepted mixed Hebrew/English output. The regenerated active v2.1 runtime contains 14,800 rows with zero Hebrew matches; the TikTok subset contains 1,101 clean rows.

## Next action
Recover the VM through the Oracle console, upload the prebuilt English v2.1 semantic cache, deploy the final fail-closed server revision, and finish checkpoint-008 production verification. Do not begin workstream isolation until Section 1 is accepted.

## Current production blocker
The first English hybrid semantic build exhausted the low-memory VM. Port 22 remains open but SSH banners time out. Exact/non-semantic deployment checks had passed before the build. See `checkpoint-008.md` for recovery commands, backup path, and remaining verification.

## Section 1 and 4 plan
`checkpoint-007.md` defines manifest-validated per-locale MCP runtime bundles, isolated semantic caches, fail-closed English asset loading, physically separate workstream roots, English nested-write guards, legacy Hebrew ownership, and complete automated/production acceptance criteria. No workstream migration or automatic translation is planned.

## Target-bank decision implemented
Two physical SQLite instances are selected by locale. No records were migrated: both started and finished empty. Future English presentation/evidence writes reject Hebrew characters, and MCP tools, UI reads, and administrative operations route explicitly by locale.

## Publishing status
Target-bank code is deployed; the checkpoint commit and branch push are the current publishing step. Draft PR creation remains unavailable because GitHub CLI is not installed.

## Deployment evidence
The previous VM assets are recoverable from `/opt/serbia-poc-ui/backups/he-en-data-20260808T162503Z`. After restart, the public API reported 14,800 English v2.1 rows and the complete 1,101-row TikTok payload contained zero Hebrew characters.

## Latest QA evidence
Both target banks passed production create/update tests, English Hebrew-text rejection, reset-to-empty, integrity, permissions, service-health, and locale-specific UI API checks. See `checkpoint-006.md`.

## Durable docs recommendation
The locale-isolated target persistence decision is recorded in `docs/decisions.md`. `docs/architecture.md` does not exist; create it only as part of a broader accepted architecture documentation task. No product-context update is needed.

## Issue status
Parent/child GitHub issues have not been created. The parent capability remains open; Slice 1 remains active.
