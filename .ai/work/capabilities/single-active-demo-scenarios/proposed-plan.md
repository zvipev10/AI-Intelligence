# Proposed delivery sequence

Historical planning proposal. The user subsequently authorized steps 1–6 (baseline through VM qualification), with empty Syria and the same layers. See execution-plan.md and checkpoint-003.md for the implemented contract; future features remain out of scope.

## Target organization
```text
shared application and common agent definitions
  demo-profiles/kosovo/<profile-version>/
  demo-profiles/syria/<profile-version>/
  datasets/<scenario-id>/<dataset-version>/
  release-manifests/<demo-release>.json
VM persistent state (outside application releases)
  state/<scenario-id>/<dataset-version>/...
  hermes-homes/<scenario-id>/<agent-role>/...
  activation/current.json
```
Paths are proposed, not existing contracts. One active endpoint/service set resolves configuration from the selected manifest. Multiple installed packages do not mean multiple resident runtimes. Do not copy the whole application into permanent regional branches.

## Phase 0 — Capture a reproducible Kosovo baseline
Owner: development/release; QA witnesses representative operations.
- Inventory the actual deployed source and reconcile drift with Git before tagging a known-good release. Do not assume current main is byte-identical to production.
- Record the app commit, Hermes/runtime version, common agent definitions, scenario prompt/config version, model/provider settings (references only, never credentials), dataset/schema version, map assets and derived-index/catalog checksums.
- Snapshot investigations, workstreams/artifacts, playback state, saved questions/layers, all agent memories/sessions and route bindings. Record an explicit restore procedure.
- Measure peak resident/cgroup memory, available memory, swap activity, CPU and response latency during startup, retrieval, semantic search and playback-triggered agent work.
- Inventory scheduled jobs and background services; do not disable unrelated VM services without a separate decision.
Done when: the current Kosovo demo can be reconstructed and its state restored, with an agreed baseline smoke script. Review checkpoint A: baseline and proposed contracts.

## Phase 1 — Introduce profiles without changing Kosovo behavior
Owner: development; product/architecture review before integration.
- Add a validated scenario manifest with stable scenario_id, profile version, immutable dataset reference/checksums, schema compatibility, map center/zoom/bounds/style/overlays, locale/time range, sample prompts and feature configuration.
- Add an agent section referencing versioned shared role definitions plus scenario overlays and exact tool/dataset bindings. Keep secrets external.
- Resolve the same manifest in UI server and MCP; expose non-secret active identity through runtime status. Fail activation on mismatch rather than silently falling back to Kosovo.
- Replace hardcoded dataset branches, map coordinates, region labels/examples and source/identifier assumptions. Inventory translation, semantic-index, playback and evidence-catalog generators as well as UI code.
- Migrate Kosovo into the profile first; keep existing paths/source layout where useful through a compatibility adapter. Do not rename the whole Serbia package during this step.
Done when: Kosovo still passes the agreed demonstration with configuration-driven geography and dataset selection.

## Phase 2 — Isolate state and bound agent execution
Owner: backend/agent development; QA state-isolation review.
- Namespace application storage, caches, recorded results, saved queries, investigation memory, target/evidence persistence and playback visibility by scenario and dataset identity. Add state_schema_version and migration compatibility checks.
- Separate Hermes home/profile state for each scenario and role; preserve it on disk. Start only active-scenario roles. Reuse role definitions, not learned memory or sessions. Verify installed Hermes profile/routing behavior before selecting the launcher implementation.
- Scope gateway route keys, Hermes and optional OpenAI session IDs by scenario, dataset, role and investigation as appropriate. Inventory every enabled agent backend so the optional OpenAI path cannot bypass isolation.
- Namespace browser storage. Bootstrap the active scenario before reading local state. Every work/mutation request carries scenario identity and a fresh activation generation; reject old tabs and stale callbacks after switching, even when switching back to the same scenario.
- Replace shared/truncated audit logs with per-run logs and scoped live-step tracking. Distinguish completed, failed, cancelled and queued work.
- Introduce one bounded agent execution queue across interactive chat, specialists, memory updates and playback. Interactive work has priority; background work cannot starve indefinitely. Queue visibility and cancellation are explicit. Serial tool execution/lazy loading are the initial memory-safe defaults where supported.
- Give existing Kosovo state an explicit one-time migration with checksums/count reconciliation and reversible backup. Do not merge same-version Syria/Kosovo directories or silently replay interrupted mutations.
Done when: isolation tests deliberately reuse the same investigation/record IDs across scenarios without collision, and all entry paths respect the execution slot.

## Phase 3 — Package Syria data and map
Owner: product/data; development provides validation.
- Specify geographic extent, time range, languages, sources, entities, narrative and expected answers with the user. Determine whether data is supplied or generated; do not invent operational facts.
- Validate dataset schema, identifiers, coordinates, timestamps, entity/location links and media references against the shared contract. Retain existing event IDs only inside a fully scenario-scoped envelope.
- Configure map view and verify actual tile/style/overlay coverage for Syria. A different map center alone is not evidence that all map resources cover the region.
- Build translations, evidence catalogs and semantic indexes off the constrained VM where practical. Publish checksummed, immutable artifacts with model/generator versions.
- Add deterministic smoke questions and expected record sets for map, timeline, raw layers and the enabled agents. Start with the current feature set; new features are separate work items.
Done when: a complete Syria package passes offline validation and is ready to activate. This phase can be authored off-VM while the single Kosovo runtime remains active.

## Phase 4 — Controlled activation and rollback
Owner: release/backend; architecture and UX review of transition behavior.
Proposed operator command: activate-demo <scenario-id> --release <manifest>. This is a design example, not an existing command or a UI feature.
1. Acquire an exclusive activation lock. Validate target paths, manifest compatibility/checksums, available disk and credentials by reference; stage files on disk without loading a second data/agent runtime.
2. Stop new requests and new scheduled/background work; show switching/maintenance status. Drain the current run within an agreed bounded timeout. On timeout, abort the switch and keep the current scenario; forced cancellation requires an explicit operator option and must not assume an external tool action was undone.
3. Persist state and in-flight status; invalidate old generations. Stop the old scenario's workers, timers and MCP processes. Confirm exit before loading the next scenario.
4. Select the target manifest and state roots; start the one runtime with the correct scenario/role profiles. Load only required data/indexes. No in-process mutation of global dataset variables.
5. Run health and scenario-identity checks across UI, gateway and tools, plus a read-only known query. Atomically mark the activation ready and reopen request admission. Browsers must refresh/bootstrap the new generation.
6. If startup/checks fail, stop the failed target and restore the prior compatible manifest/state. If rollback fails, remain in explicit maintenance mode; never claim a scenario is ready.
Persist switching phases so a host/process restart recovers to one verified scenario. Never resume an inactive scenario's cron jobs or queued writes automatically. A reset/clean-demo action is distinct from activation and must not delete preserved state by default.
Done when: repeated switches, concurrent switch attempts, restart mid-switch, stale requests, failed target startup and rollback all behave predictably with no overlap.

## Phase 5 — Deploy and qualify on the existing VM
Owner: release/QA.
- Extend deployment manifests to include scenario packages, maps, help/demo pages, videos/posters and all referenced assets; retain the guide-media regression check. Persistent state lives outside release directories.
- Use tagged app releases and explicit demo release manifests. Both demo profiles should be tested against each shared release. If an older release is pinned, switching must also validate state-schema compatibility; Git checkout alone is not rollback.
- Deploy/test Kosovo extraction first, then install Syria inactive, then execute Kosovo -> Syria -> Kosovo acceptance.
- Validate only active-scenario services are resident and only active jobs can run. Measure the largest planned workload, not just idle memory. Check repeated switching does not accumulate processes/caches.
- Establish resource/latency thresholds from baseline measurements before acceptance. If the VM cannot meet them, first reduce unnecessary resident workers/cache/index load and prepare indexes offline; consider resizing only as a separate decision, not a prerequisite invented here. Do not remove useful services blindly.
Done when: both scenarios pass their smoke scripts and round-trip restoration, with demonstrated rollback and measured resource headroom. Record the exact deployed manifest and backup locations.

## Phase 6 — Add the forthcoming features
Owner: product and feature teams after requirements are supplied.
For each feature, classify shared code versus scenario content versus optional feature setting; create its own capability/branch and review gates. Test shared changes against both profiles, even though runtime tests execute sequentially. Avoid feature branches named after countries or duplicated agent implementations. Keep Kosovo on a known-good demo manifest until the new release is qualified.

## Version policy
- main remains shared integration; short feature branches and reviewed PRs.
- Tag stable application releases; independently version dataset and profile packages. Never overwrite a published dataset in place.
- A demo release manifest binds app commit/tag, Hermes version, agent definition/overlay versions, provider/model configuration, dataset/schema version and derived-asset checksums. Model behavior is not guaranteed bit-for-bit reproducible merely by pinning a model name.
- Runtime state is backed up and migrated independently; credentials are excluded from Git and release artifacts.

## Gates and dependencies
0 -> 1 -> 2 -> 4 -> 5. Phase 3 needs the profile/schema contract from 1 and can be prepared off-VM before 4. Phase 5 requires both 3 and 4. New-feature planning can begin when requirements exist, but feature rollout must use the scenario contracts. Create slice child issues only after #68 resolves design assumptions; then promote this proposal to execution-plan.md. Every meaningful slice has tests, checkpoint, published artifacts and human review where behavior/interface/state changes.
