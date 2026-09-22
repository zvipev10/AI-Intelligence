# QA review

Status: Draft test plan; product tests not executed in this documentation task. Review #68.

## Blocking before implementation approval
Finalize manifest/state identity and migration/rollback semantics; agree user-visible switching and queuing; supply or assign Syria content requirements. Set measurable performance thresholds after a baseline. These are execution prerequisites, not blockers to publishing the proposal.

## Required tests by risk
1. Contract: missing/unknown scenario, unsupported schema, corrupt/missing assets, invalid map bounds, dangling entity/location references, wrong index/model version, unavailable tile resource, invalid feature/agent binding. Fail closed without fallback.
2. Kosovo regression: map/timeline/table, layer-name recovery and filters, saved layers/investigation memory, source search, specialists, playback, targets/evidence and both documentation pages/media.
3. Isolation: same dataset version, investigation ID and event ID in both scenarios; memories, routes, saved records, audit results, browser storage and background jobs stay separate. Dataset upgrades retain compatible historical state or explicitly require migration.
4. Switching: busy run drains; timeout leaves original active; explicit cancellation recorded accurately; two operators contend for one lock; stale browser/worker callbacks rejected; no overlap in resident scenario workers; crash at every activation phase; failed startup restores prior scenario or remains visibly unavailable.
5. Persistence: Kosovo -> Syria -> Kosovo retains exact intended records and agent memory, supports refresh/restart, and does not resurrect inactive queues/cron work or replay completed writes.
6. Resource admission: chat, general agent, each specialist, optional agent backend, memory updates and playback all use one bounded queue; queued jobs can cancel, overload is visible, no starvation/deadlock.
7. Capacity: startup, largest dataset/index query, semantic search, browser-record hydration and playback agent update; collect peak memory, swap rates, CPU, latency and process counts. Repeat switching to detect retained workers. No OOM/restart loops; latency/headroom limits agreed before live acceptance.
8. Release completeness: every profile-referenced map/media/page/data/index asset is present and checksummed. Stage checks must not preload the inactive dataset into an active process.

## Non-blocking recommendations
Start with a small synthetic Syria fixture to validate contracts before full ingestion. Use fixed expected IDs/counts in regression tests, while separately evaluating nondeterministic agent answers against evidence/behavior criteria. Automate switched-state tests without requiring simultaneous demo processes.

## Recommendation and ownership
Pause for design review before implementation. Next: product/developer/UX reviewers resolve #68; QA then formalizes executable acceptance cases. Parent #67 stays open. Historical suite failures must be reported and baselined; do not silently waive new regressions.
