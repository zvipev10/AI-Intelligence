# Checkpoint 003 — deployed implementation and qualification

Date: 2026-09-23. Scope: authorized steps 1–6; no future feature work. Parent #67, implementation #70, PR #69. User accepted brief shared-gateway integration interruption. Countrywide Syria and Kosovo active at completion are retained assumptions.

## Implemented result

One shared source release and one active scenario. Checksummed Kosovo v2.1 and empty Syria empty-v1 profiles choose data, map and source catalog. Syria has zero events/locations/entities and 16 catalog layers, including the same 12 raw sources and four derived catalogs. No fabricated records, learned Kosovo memory or sample investigations appear in Syria. Profile/dataset identity namespaces server state, browser storage, role homes, sessions, indexes and audit logs.

A reentrant execution slot covers interactive agents, specialists, optional OpenAI and background application work. Queue capacity eight, foreground priority with background aging, queued cancellation and no automatic replay. API requests are counted during drain. Maintenance blocks new mutations; activation generations reject stale tabs/workers. Browser bootstrap loads identity before storage and application code.

`activate_demo.py` locks, validates release/profile/cache/state compatibility, drains, stops UI/dashboard/gateway, selects persistent role homes and starts one runtime. Gateway, catalog and role MCP identity/count checks gate readiness. Failed readiness restores the previous selection with a new generation; failed drain retains current runtime; boot recovery keeps maintenance until operator verification. `provision_demo.py` is one-time, refuses overwrite, uses SQLite consistent copies/quick checks and preserves symlinks. Migration reconciled 2,869 files.

## Deployment and issues resolved

Runtime commit `34860bcef4aca0a2eeb7ba7f9c1a1cce879b79ef`; base main `d475d2e3722bebe4f335459f22648740467106d2`, fetched before work and rechecked after the interrupted session. Hermes commit `00bbfc690060d1323ddb2f065297c7425cb71c26`. Installed release manifest records normalized source hashes and profile versions under `/opt/demo-runtime/releases/<runtime-commit>/`. Private baseline source/config/SQLite/stopped-state backups remain at `/opt/demo-runtime/backups/20260922T195952Z/`. Original state directories are retained.

Installed Hermes requires root-registry tool definitions for named profiles; removing them prevented tool discovery. Keep all definitions bound to the active scenario. The dashboard owns additional MCP workers and now participates in stop/start. Profile tool lists explicitly include shared catalog opening and runtime status. Role API keys retain their overrides. Initial copied OAuth credentials became stale after token rotation; activation carries the current corresponding role's credential store at the stopped boundary, without copying learned memory. These findings supersede initial checkpoint-002 implementation details.

Cold semantic-index construction on the 954 MiB VM caused heavy swapping and an 84.92-second failed request. No OOM was found in the inspected kernel interval. The fix builds the same hybrid index offline, installs its trusted pickle plus checksum/dataset metadata, rejects missing/changed caches before activation and forbids scenario request-time builds. Cache SHA-256: `2a5f241f0008dcc48c3c0374d15a58945af13e2d02e899d885bce5268dbb6163`. No search backend or ranking change was introduced.

## Automated checks

- Scenario tests: 13 pass (profiles/checksums/empty data, isolation, generation guards, private/static path denial, admission/cancellation, rollback/drain/recovery, no live cache build, cache integrity).
- Full application suite: 233 total, 225 pass, 8 failures reproduced from the 220-test baseline. Failures remain stale asset/source/routing/welcome assertions in `test_chat_autoscroll`, `test_evidence_ui`, `test_mobile_run_recovery`, `test_moshe_profile`, `test_production_v162_contract`, `test_talia_profile`, and two `test_welcome_page` checks. They are not waived or reported green.
- MCP suite: 74 total, 72 pass, 2 skip. Run with package-correct server imports; naive cross-directory discovery has an import-name collision.
- JavaScript syntax and `test_catalog_recovery_ui.cjs` pass, including empty catalog success and explicit load-failure outcome. The harness intentionally prints a load-failure message while asserting the failure path.
- Python compilation and `git diff --check` pass.

## Live evidence

- Kosovo: 14,833 records; actual general-agent aggregate count correct. Syria: zero records, all 16 layer counts zero; actual general-agent aggregate count correct.
- Syria Moshe emits the correct `open` action for `location-metadata:all` and says the UI action is pending, without falsely claiming presentation. Talia read-only retrieval returns empty and does not create workstream/assessment records.
- Old generation rejected with HTTP 409. Concurrent activation lock rejects the second operator before mutation. Fault-injected Kosovo readiness failure restores Syria with a fresh generation and clears maintenance only after rollback health passes.
- Kosovo → Syria → Kosovo preserves all 14 checked saved-state files byte-for-byte. Active profile identity and MCP counts agree. Old scenario MCP workers exit with their owning services.
- Two public guide pages plus five videos and five posters: all 12 public assets match installed bytes. Syria OSM tile request returns a valid PNG (24,048 bytes).
- Baseline: 954 MiB RAM, 217 MiB available, 1,003 MiB swap used. Real lightweight agent runs: Kosovo count 35.4 s / minimum available 150,076 KiB; Syria count 32.16 s / 257,948 KiB; Moshe 44.08 s / 172,184 KiB; Talia 32.85 s.
- Final cached semantic query returns 200 records without a tool error: 60.2 s total, 23,838.578 ms tool time, minimum available 272,236 KiB, minimum free swap 1,099,428 KiB. This replaces the failed cold-build qualification, not the VM memory limitation.
- Private machine evidence: `control/migration-report.json`, `rollback-qualification.json`, `roundtrip-qualification.json`, `semantic-qualification.json`, and `http-qualification.json`.

## Acceptance limits and next action

No connected browser was available, so visual rendering, stale-tab interaction and video playback in a real browser remain human acceptance checks; HTTP and JavaScript harness checks are not claimed as browser QA. Optional OpenAI and playback/background admission were code/test verified, not live provider/load qualified. Empty Syria cannot validate future narrative answers. Existing unrelated messaging/services remain outside the application execution gate. The constrained VM still needs workload-specific qualification for future features; no resize was performed.

Source and artifacts are published on the PR branch, not main. Reviewer/product owner should review PR #69 and perform browser acceptance. #70 closes on merge; #67 stays open through acceptance. The operator runbook records switching, index build, deployment, credentials and restore contracts. Suggested shared documentation links are in handoff-summary.md.
