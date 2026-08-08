# Handoff Summary

## Current state
The locale-keyed MCP runtime, English semantic cache, target-bank isolation, Section 4 workstream isolation, and unified staged playback are deployed and verified.

## Published baseline
Commit `eb9168c` on `origin/codex/he-en-localization` contains the brief, developer review, QA review, execution plan, and status dashboard.

## Key finding
The screenshot was caused by partially translated `.en` assets, not by the English UI toggle. The old generator accepted mixed Hebrew/English output. The regenerated active v2.1 runtime contains 14,800 rows with zero Hebrew matches; the TikTok subset contains 1,101 clean rows.

## Next action
Run final bilingual acceptance review or proceed to the next localization slice.

## Checkpoint 010 local result
Playback now has one staged flow. The first visible window starts at the beginning of the v2.1 dataset and ends at the first scenario slice boundary, so initial state behaves like the previous historical/default view for the initial scenario window. Moshe reevaluation is skipped when the baseline is created and can run only after a later slice arrives and active workstreams exist. UI/data layer rows are filtered by the active `visible_timeframe`, open catalog layers reload after timeframe changes, and the UI no longer presents separate historical vs real-time modes while keeping timeframe display and the Next button.

## Checkpoint 010 production result
Deployed to `151.145.93.180`; backup retained at `/opt/serbia-poc-ui-backups/staged-playback-20260808T203509Z`. Production smoke temporarily activated the baseline visible timeframe, verified English TikTok layer rows were all within `2026-09-12T04:25:50.096250Z` to `2026-09-17T06:00:00Z`, verified playback status reports `mode: real_time` with the dataset-start first window, restored the previous inactive `active_visibility.json`, and confirmed the UI service remained active.

## Section 4 local result
Workstreams now persist under `workstreams/v2_1/he/` and `workstreams/v2_1/en/`. Legacy/shared workstream files are Hebrew-owned fallback data only. List, get, create, update, archive, artifacts, presentation, chat actions, and playback reevaluation pass locale through the server/UI path. English user-visible workstream and artifact fields reject Hebrew before persistence.

## Section 4 production result
Deployed to `151.145.93.180`; backup retained at `/opt/serbia-poc-ui-backups/workstream-locale-20260808T200045Z`. Production smoke created one English and one Hebrew workstream, verified physical files in the correct language roots, verified cross-locale IDs return not found, verified English Hebrew-text rejection, removed the smoke files, and confirmed both smoke investigation lists were empty afterward.

## MCP production result
After the VM reboot, the prebuilt English v2.1 hybrid cache and final server were deployed. English health, exact, location, entity, aggregation, intent, and semantic payloads contain zero Hebrew. The English semantic manifest and cache namespace are isolated, all services are active, and target databases remain empty and healthy. See `checkpoint-008.md`.

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
The locale-isolated target persistence and unified staged playback decisions are recorded in `docs/decisions.md`. `docs/architecture.md` does not exist; create it only as part of a broader accepted architecture documentation task. No product-context update is needed.

## Issue status
Parent/child GitHub issues have not been created. The parent capability remains open; Slice 1 remains active.
