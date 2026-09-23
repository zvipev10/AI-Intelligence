# Syria convoy handoff

Deployed runtime `dd6b362a4fdcb06fe281b37f2fbfeb5669fd98eb`, Syria `convoy-v1`, profile 2. Source PR #72 is stacked on platform PR #69 and is not on main. Issue #71 closes on merge; parent #67 remains open through acceptance.

Delivered two additional Syria sources: CCTV (6 records/videos), Satellite (6 records, 18 timestamped images). At each of two fictional sites 5.004 km apart there are three records per source, all linked to one Convoy entity. All 24 media files include visible synthetic labels. Annotations are fixture data, not a claim of actual computer-vision processing. Map focuses the sites. Kosovo profile/data files have no diff.

Changed files: Syria profile and new immutable data/media; offline fixture generator; app record viewer for timestamped images; MCP media passthrough; populated-profile readiness; welcome/bootstrap asset versions; active-scenario media fence; deployment file list; tests and operator runbook.

Validation: 15 focused tests pass; image-sequence/video renderer harness passes; direct MCP confirms 12 enriched location/entity/media records; six MP4s decode; representative PNG visually inspected. Application suite: 235 tests, same eight baseline failures. MCP: 72 pass, 2 skip. JS syntax/Python compile/diff checks pass. Live public API confirms 12 records, two locations, one entity, 6 records in each new layer; all 24 public media responses match installed bytes. Evidence: `/opt/demo-runtime/control/syria-convoy-qualification.json`. No connected browser was available, so real-browser playback/layout acceptance remains pending.

State: stopped upgrade copied only Syria state to convoy-v1 and retained empty-v1. Source backup `/opt/demo-runtime/backups/syria-convoy-dd6b362`. Installed release manifest under `/opt/demo-runtime/releases/dd6b362a4fdcb06fe281b37f2fbfeb5669fd98eb/`. Existing role homes remain Syria-only. New version browser storage starts separately; old storage is preserved. Dataset rollback must restore matching source/profile/state, as explained in the runbook.

Assumptions: three images per satellite record, fixed 2026-09-22 demo times, fictional central-Syria sites. User explicitly approved synthetic media. Next role: user browser acceptance and PR reviewer; refresh http://151.145.93.180 and open CCTV/Satellite via the layer catalog. Suggested docs update completed in focused runbook; link that contract from architecture/product docs when consolidating the platform PR.
