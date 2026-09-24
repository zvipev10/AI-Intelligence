# Operations guide

Owns local setup, VM deployment, scenario activation, validation and recovery. Dataset narratives and expected fixture values are in [demo scenarios](demo-scenarios.md); service/state contracts are in [architecture](architecture.md).

## Release identity and deployment roots

Fetch remote `main` and inspect unrelated working changes before starting a release. Build from a reviewed commit. The installed `release-manifest.json` pins application/Hermes commits, profile/dataset versions, state schemas and normalized file hashes; `/opt/demo-runtime/control/deployed-release.json` locates the pinned release. Check `/api/status` for actual active identity, generation and profile. Historical asset-version numbers and backup paths are evidence, not a live release selector.

The UI root is `/opt/serbia-poc-ui` (`serbia-poc-ui.service`, port 8769); the MCP root is `/opt/serbia-poc`. The shared gateway uses port 8642 and `hermes-gateway.service`; `hermes-dashboard.service` uses port 9119. Public guide pages and their videos/posters are shared application assets. Release from the canonical package tree, update asset cache versions when applicable and verify the served asset content. Historical source-capture SHA256 manifests remain in the package deployment directory.

## Local development

From `llm_investigation_orchestrator_serbia_poc/`:

```sh
python server.py 8769
```

The default bind is `127.0.0.1`; VM service configuration uses `POC_UI_HOST=0.0.0.0`. Select `INTELLIGENCE_POC_SCENARIO` and an isolated state root for scenario-aware work; do not assume a legacy invocation selects the VM scenario. End-to-end runs also need matching gateway profile/tool bindings. Inspect `demo_runtime.py` and the checked-in profile rather than substituting country paths by hand.

Use `.hermes-api.local.example.json` or `.hermes-api.vm.example.json` as the template for private `.hermes-api.json`. Local access uses SSH/Paramiko; VM access uses its local gateway. Keep API keys, SSH credentials, runtime state and recordings outside Git.

## Switch on the VM

Run as `ubuntu`:

```sh
cd /opt/serbia-poc-ui
/home/ubuntu/.hermes/hermes-agent/venv/bin/python activate_demo.py syria
/home/ubuntu/.hermes/hermes-agent/venv/bin/python activate_demo.py kosovo
```

Optionally require an exact installed release:

```sh
/home/ubuntu/.hermes/hermes-agent/venv/bin/python activate_demo.py syria --release /opt/serbia-poc-ui/release-manifest.json
```

The operator checks release/profile checksums, takes an exclusive lock, pauses admission and drains application work (120 seconds by default). It then stops the UI, Hermes dashboard and gateway before selecting the next scenario. The dashboard must stop too: it retains its own MCP processes. Only the active scenario's tool bindings are registered when services restart. UI, gateway, catalog and each role's MCP identity/count checks must pass before admission reopens. Existing WhatsApp configuration remains; gateway restarts briefly interrupt it.

Failed readiness restores the previous scenario with a fresh activation generation. A drain timeout retains the current runtime. A rollback failure leaves maintenance enabled. Old browser tabs must reload; their writes are rejected with HTTP 409. Queued application requests can be cancelled; running external actions are drained, not assumed undone.

## State and credentials

- Application state: `/opt/demo-runtime/state/<scenario>/<dataset>/`.
- Agent homes: `/opt/demo-runtime/hermes-homes/<scenario>/<role>/`; stable `demo-general`, `demo-moshe`, `demo-talia` profile aliases select the active homes.
- Activation state: `/opt/demo-runtime/control/`; service environment: `/opt/demo-runtime/active.env`.
- Source releases: `/opt/demo-runtime/releases/<release>/release-manifest.json`.
- Migration proof: `control/migration-report.json`; original directories are retained.

Memories and sessions are isolated by scenario/role homes; application stores, catalogs, targets, playback and browser storage additionally use dataset namespaces. Locale separation is retained inside the selected scenario. Role homes are not automatically reset by a dataset-version change. Provider credentials are deliberately not scenario data: the latest active role's credential store is carried into the next scenario at the stopped transition, preventing stale copied OAuth refresh tokens. Gateway API credentials retain their role-specific bindings. Secrets and private backups never belong in Git. On every activation, `INTELLIGENCE_POC_AUDIT` must be refreshed to the selected dataset audit directory for each role. A stale audit path can cause tools to succeed while the UI receives no structured layer actions.

One application agent execution slot covers interactive, specialist, OpenAI and background application calls. The queue is bounded at eight, prioritizes foreground requests and ages background requests after 30 seconds. This limit does not claim to regulate unrelated messaging integrations. Tool calls are serial within demo profiles.

## Installation and future releases

`provision_demo.py` is a **one-time migration**, run with application/gateway writers stopped and a private backup taken. It refuses to overwrite existing migrated state. Use the Hermes venv's existing PyYAML/python-dotenv dependencies. Install `deployment/demo.conf` as the UI systemd drop-in and `deployment/demo-recover.service` as an enabled system service. Do not rerun provisioning to deploy a feature.

Update shared runtime source in both `/opt/serbia-poc-ui` and `/opt/serbia-poc` as applicable. Both roots need `demo_runtime.py`, `demo_profiles/` and the selected immutable datasets; both UI and gateway must receive the compatible MCP server. Retain guide pages, five demo videos and posters. Never overwrite `/opt/demo-runtime/state` or agent homes as part of a source deployment. Produce the installed release manifest from the exact committed source and verify its file hashes before activation. Do not use the old country-specific MCP configuration installer after provisioning: it would restore legacy profile bindings.

Every shared-code release should test both profiles sequentially, plus Kosovo → Syria → Kosovo and fault-injected readiness rollback. Pin the application commit, Hermes commit, profile/dataset versions and checksums in the release manifest; preserve state-schema compatibility independently of Git rollback.

## Interrupted switch recovery

On boot, `demo-recover.service` runs before UI/gateway/dashboard, restores the previous selection with a new generation, and retains maintenance until verified. Inspect `control/transition.json`; then run `activate_demo.py <previous-scenario>` to complete health verification and reopen admission. Interrupted mutation jobs require an explicit retry; they are not automatically replayed.

For a whole-release rollback, stop all three services, restore the private source/config backup and the latest compatible state snapshot, remove the scenario UI drop-in only when returning to the legacy runtime, reload systemd and verify the original endpoint. Do not restore an old state snapshot over newer analyst work without choosing that recovery point explicitly.

## Verification limits

The 1 GB VM remains constrained. Use one scenario and one application agent execution slot; future feature workloads need separate capacity validation. Automated API, tool, state and asset checks supplement browser acceptance. The current synthetic Syria fixture validates only its documented narrative and documented source/time boundaries; it does not validate future data, real-world identity conclusions or additional concurrent workloads.

## Offline semantic search cache

The 1 GB VM must not build a semantic index during an analyst request. Scenario MCP processes require a prebuilt compatible cache; a missing/stale cache returns an explicit operational error. The historical empty-v1 package can return zero without an index; current satellite-v1 is non-empty and requires a compatible prebuilt cache. The existing hybrid search backend is unchanged.

On a development machine with sufficient RAM and the exact release dataset bytes:

```sh
python build_demo_index.py kosovo --output /trusted/build/kosovo-index --engine python
python build_demo_index.py syria --output /trusted/build/syria-index --engine python
```

The deployed MCP uses Python without NumPy, so use the `python` engine. Install both generated `semantic_event_index_hybrid_embedding.pkl` and `.json` under the matching `/opt/demo-runtime/state/<scenario>/<dataset>/semantic_index/` before activation (currently Kosovo/v2.1 and Syria/satellite-v1). Verify the transferred SHA-256 against the build output. These are private derived release artifacts, not Git source. Only accept trusted caches: pickle files can execute code. The operator verifies the cache hash and raw dataset signatures before stopping services. Dataset/index-format/engine changes require a rebuilt cache and a real semantic-search smoke check. Build-time Python must support the runtime's pickle format.

Cold index construction during qualification timed out and caused heavy swapping. The offline cache avoids that construction cost; it does not eliminate the VM's overall RAM limit.

## Dataset upgrade procedure

1. Create a new immutable data package and compatible profile in the shared source release. Verify localized files, media URLs, checksums and schema compatibility. Keep previous packages.
2. Build the new scenario semantic cache offline from the exact dataset bytes. Stage source/profile/data in both UI and MCP roots as applicable, and stage media in the UI root.
3. Take a private backup; enter maintenance and drain work. Stop UI, Hermes dashboard and gateway before copying or migrating mutable state. Do not rerun one-time provisioning.
4. Preserve the previous state namespace. If carrying work forward, copy only the selected scenario's state into the new dataset namespace while writers are stopped, update `state.json`, and validate compatibility. Browser storage naturally uses a new namespace; do not import Kosovo browser state into Syria.
5. Install the matching index and source manifest, then use the activation operator to select the profile/dataset and refresh all role environments/audit paths. Verify catalog counts, active identity, actual role tools, media, and a representative search/presentation.
6. On rollback, restore the compatible profile/source manifest and select preserved state; editing `active.env` alone is insufficient. Do not overwrite newer analyst work with an old snapshot without explicitly choosing that recovery point.

Application versions, profile versions, immutable dataset versions and state-schema versions have different purposes. A source-only UI update does not recreate datasets or state. Server/gateway changes require controlled service restart; data/index changes require cache validation. Preserve guide pages, videos and posters during every release.

## Quick acceptance checks

- `/api/status`: expected scenario/dataset/generation, profile and initial map configuration; only one active runtime.
- Catalog and source rows: Syria 424 total, CCTV 2 / Satellite 2 / ADINT 120 / IPDR 300; original raw sources remain present with zero rows where applicable.
- Open IPDR: Table view, IP address/IMEI, no actor/location or map action; record links retain all identifiers.
- ADINT: verify all 120 native observations, 84 mapped points and 36 geometry-free rows. Check IP role and valid session intervals; two supplied IPDR records have reversed timestamps, preserved pending clarification.
- Open each Satellite record: one supplied image at its own Satellite site, no visit/pair metadata, explicit scenario timestamp basis; CCTV video and synthetic labels visible.
- Satellite/Street toggle: English-preferred names, reference roads/borders, unchanged analytical overlays; network failure gives visible Street fallback.
- After scenario/dataset activation, verify an actual catalog action reaches the UI, not merely that the agent mentions success. Check the selected dataset's role audit directory if actions disappear.
- Reload old tabs after activation. Returning to Kosovo restores its own working state, not Syria's.

Automated checks and live API/asset checks do not replace manual browser/media acceptance. Previously recorded full-suite baseline failures are documented in the capability handoffs; do not describe those suites as fully green.

## Developer checks and captured demonstrations

From the application package, use these checks as applicable to the changed subsystem:

```sh
python mcp_server/smoke_client.py
python mcp_server/benchmark_tools.py --rounds 3
python docs/quality/score_semantic_tool_integration.py --current-label working_tree
```

The semantic quality gold fixture is `docs/quality/semantic_tool_integration_gold_v2.json` under the package. Record actual results and baseline failures in the capability handoff; a historical report is not evidence for a new release.

Saved-question and recorded-run files belong to the selected runtime state directory, not the source deployment. Capture a complete successful live investigation response with its question, title, locale, identifiers, elapsed time and recording metadata; preserve all steps/results. Verify replay with the matching scenario/dataset/locale and confirm subsequent follow-ups call the live agent. Never replace mutable saved work during source deployment. See [architecture](architecture.md#saved-question-and-recording-interfaces) for API and storage contracts.
