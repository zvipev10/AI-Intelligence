# Checkpoint 010 — Persistent attack-target catalog layer

Date: 2026-07-21

## Approved behavior

- Persisted Moshe attack-target candidates are advertised as the regular catalog layer `attack-targets:all`.
- Opening the layer uses the shared table/map target renderer and the canonical dataset location coordinates.
- Target rows include their persisted raw-data record references.
- If this catalog layer is open when Moshe returns target data, it refreshes from SQLite and becomes the single canonical target layer in the UI.

## Architecture and security

- SQLite remains private to the backend/MCP subsystem.
- The UI server invokes a fixed-purpose reader with `shell=False`; the reader opens SQLite with `mode=ro`.
- The reader exposes a fixed, parameterized, bounded projection of at most 500 targets. It accepts neither arbitrary SQL nor browser-provided database paths.
- Missing or unavailable target persistence does not break the rest of the layer catalog; it yields an empty target layer.

## Validation

- `node --check app.js`: passed on the deployment VM.
- `python3 -m unittest test_member_ui_regression.py test_target_catalog_api.py`: 11 tests passed.
- `python3 -m unittest test_target_catalog_reader.py`: 1 test passed.
- Read-only integration against the production database found 3 targets and 14 raw evidence references.

## Deployment guard

Back up the existing target database before installing or restarting. Deployment must not replace, initialize, or clear the database.

## Deployment result

- Deployed to the VM UI service on 2026-07-21 and restarted `serbia-poc-ui` successfully.
- Production API advertises `attack-targets:all` with 3 rows and returns 14 raw-data references.
- The original database and protected pre-deployment backup are both 36,864 bytes with mode `0600`.
- UI restart count is 0; available memory after deployment is 226 MB with 423 MB swap in use.
- General-agent and Moshe gateway health endpoints both returned `status: ok` (their processes are not represented by the attempted systemd unit names).
