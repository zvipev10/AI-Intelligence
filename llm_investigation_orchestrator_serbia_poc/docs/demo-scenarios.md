# Single active demo scenarios

One application URL serves one active scenario. Shared application code and agent roles live on the same branch. Profiles select geography, datasets and feature availability; country-specific application forks are unnecessary.

## Installed scenarios

| Scenario | Dataset | Initial content |
|---|---|---|
| `kosovo` | `v2.1` | Existing 14,833 events and preserved application/agent state |
| `syria` | `network-v1` | 208 records: 4 CCTV/Satellite, 4 ADINT, 200 IPDR; 20 layer definitions |

Syria has no synthetic operational facts, locations, entities, targets or evidence. Kosovo example investigations and prompts are hidden there. Add real demo content as a new dataset/profile version rather than overwriting the published empty package.

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
- Private baseline backup: `/opt/demo-runtime/backups/20260922T195952Z/`.

Memories, sessions, investigations, catalogs, targets, playback and browser storage are scenario scoped. Provider credentials are deliberately not scenario data: the latest active role's credential store is carried into the next scenario at the stopped transition, preventing stale copied OAuth refresh tokens. Gateway API credentials retain their role-specific bindings. Secrets and private backups never belong in Git.

One application agent execution slot covers interactive, specialist, OpenAI and background application calls. The queue is bounded at eight, prioritizes foreground requests and ages background requests after 30 seconds. This limit does not claim to regulate unrelated messaging integrations. Tool calls are serial within demo profiles.

## Installation and future releases

`provision_demo.py` is a **one-time migration**, run with application/gateway writers stopped and a private backup taken. It refuses to overwrite existing migrated state. Use the Hermes venv's existing PyYAML/python-dotenv dependencies. Install `deployment/demo.conf` as the UI systemd drop-in and `deployment/demo-recover.service` as an enabled system service. Do not rerun provisioning to deploy a feature.

Update shared runtime source in both `/opt/serbia-poc-ui` and `/opt/serbia-poc` as applicable. Both roots need `demo_runtime.py`, `demo_profiles/` and the selected immutable datasets; both UI and gateway must receive the compatible MCP server. Retain guide pages, five demo videos and posters. Never overwrite `/opt/demo-runtime/state` or agent homes as part of a source deployment. Produce the installed release manifest from the exact committed source and verify its file hashes before activation. Do not use the old country-specific MCP configuration installer after provisioning: it would restore legacy profile bindings.

Every shared-code release should test both profiles sequentially, plus Kosovo → Syria → Kosovo and fault-injected readiness rollback. Pin the application commit, Hermes commit, profile/dataset versions and checksums in the release manifest; preserve state-schema compatibility independently of Git rollback.

## Interrupted switch recovery

On boot, `demo-recover.service` runs before UI/gateway/dashboard, restores the previous selection with a new generation, and retains maintenance until verified. Inspect `control/transition.json`; then run `activate_demo.py <previous-scenario>` to complete health verification and reopen admission. Interrupted mutation jobs require an explicit retry; they are not automatically replayed.

For a whole-release rollback, stop all three services, restore the private source/config backup and the latest compatible state snapshot, remove the scenario UI drop-in only when returning to the legacy runtime, reload systemd and verify the original endpoint. Do not restore an old state snapshot over newer analyst work without choosing that recovery point explicitly.

## Verification limits

The 1 GB VM remains constrained. Use one scenario and one application agent execution slot; future feature workloads need separate capacity validation. Automated API, tool, state and asset checks supplement browser acceptance. An empty Syria dataset cannot validate future Syria narratives or expected analytical answers.

## Offline semantic search cache

The 1 GB VM must not build a semantic index during an analyst request. Scenario MCP processes require a prebuilt compatible cache; a missing/stale cache returns an explicit operational error. Empty Syria searches return zero without an index. The existing hybrid search backend is unchanged.

On a development machine with sufficient RAM and the exact release dataset bytes:

```sh
python build_demo_index.py kosovo --output /trusted/build/kosovo-index --engine python
```

The deployed MCP uses Python without NumPy, so use the `python` engine. Install both generated `semantic_event_index_hybrid_embedding.pkl` and `.json` under `/opt/demo-runtime/state/kosovo/v2.1/semantic_index/` before activation. Verify the transferred SHA-256 against the build output. These are private derived release artifacts, not Git source. Only accept trusted caches: pickle files can execute code. The operator verifies the cache hash and raw dataset signatures before stopping services. Dataset/index-format/engine changes require a rebuilt cache and a real semantic-search smoke check. Build-time Python must support the runtime's pickle format.

Cold index construction during qualification timed out and caused heavy swapping. The offline cache avoids that construction cost; it does not eliminate the VM's overall RAM limit.

## Syria convoy dataset update

Syria profile version 2 selects immutable `convoy-v1`. Two fictional sites at (35.000, 38.500) and (35.045, 38.500) are about 5.004 km apart. Each site has three CCTV records (five-second H.264 clips) and three Satellite records (three timestamped images each), all linked to `ENT-SYR-CONVOY`. Every asset is visibly synthetic. `build_syria_convoy_demo.py` is an offline fixture generator requiring Pillow/imageio-ffmpeg; these dependencies are not needed on the VM.

The initial `empty-v1` state remains preserved. The upgrade copied only Syria state while UI/dashboard/gateway were stopped, changed the new state metadata to convoy-v1, installed its prebuilt index, and verified release/profile/MCP readiness. Backup: `/opt/demo-runtime/backups/syria-convoy-dd6b362`. Reverting a dataset upgrade requires restoring the matching profile/source manifest as well as selecting the retained state; merely editing active.env is insufficient. Browser storage is version-scoped, so empty-v1 browser state remains in its old namespace.

### Paired visits revision (convoy-v2)

Profile 3 consolidates both sources to one record per location: two CCTV plus two Satellite records. Satellite records contain three repeat visits on September 20, 21 and 22, 2026. For each visit the convoy appears at Site 1 at 08:00 UTC and Site 2 at 08:15 UTC, consistent with northward movement over 5 km. Shared visit IDs and reciprocal record/image/timestamp fields connect each pair. Each record viewer shows only its own site's three captures. Shared visit IDs and counterpart references correlate visits across records without displaying the other site's images. The two CCTV clips correspond to September 22. Return journeys and travel between captures are not shown; all observations remain synthetic.

The stopped-state upgrade preserves convoy-v1. Runtime release `0ba309bee374f6fea8b76c2f71edc7c977c42314`; source backup `/opt/demo-runtime/backups/syria-convoy-v2-0ba309b`. The current generator emits convoy-v2. Existing v1 media/data are retained as immutable historical artifacts, not active catalog records.

## Syria ADINT/IPDR fixture

Profile 5 selects network-v1. ADINT has four observations at Site 1 and three points 500m north/east/west. IPDR has 200 sessions without asserted GPS coordinates. One session shares Site 1 ADINT's IP and contains its observation timestamp; IMEI appears only in IPDR. Existing keyword search accepts IP/IMEI/advertising IDs; record details expose those identifiers and session boundaries. A session match is a synthetic fixture relation, not a pre-established connection to the convoy.

Build with `python build_syria_network_demo.py` (standard library only), then build the scenario search cache offline. Existing CCTV/Satellite fields and Kosovo datasets/profile are unchanged. Runtime c7c331911d76d575a92b9aba434ede0434a4d818; backup `/opt/demo-runtime/backups/syria-network-c7c3319`. Prior Syria packages/state remain preserved. Version upgrades copy current Syria state only while all demo writers are stopped.
