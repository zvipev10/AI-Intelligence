# Checkpoint 003 — Deduplicated record viewer and simulated UAV stream

## Status and recommendation
Complete, merged, deployed, and smoke-validated.

## Delivered
- Removed the duplicated record narrative from the viewer header. The full event summary now appears once in the readable body card.
- Record headers now use a compact source identity; UAV records use the localized `UAV video observation` title.
- Replaced the disconnected UAV-media placeholder with an automatically playing canvas-based aerial stream simulation.
- The simulation includes moving objects, terrain, a road, reticle, scan lines, altitude, speed, and UTC telemetry.
- The feed is deterministic at mission level and is restarted for every UAV-record opening.
- The animation is cancelled when the viewer closes or before another UAV stream starts.
- The feed is visibly and textually marked as simulated and not authentic operational footage.

## Validation
- `node --check app.js`: passed.
- Viewer contract assertions and `git diff --check`: passed.
- Python tests remain unavailable on this local Windows host because no Python executable is installed.

## Files
`app.js`, `styles.css`, `index.html`, `test_object_viewer.py`, release provenance, and capability handoff artifacts.

## Publication and deployment
- Merged and pushed to remote `main` at `85c9538`.
- Release manifest: `deployment/SHA256SUMS-v183.txt`.
- Production target: `/opt/serbia-poc-ui` on `151.145.93.180`.
- Rollback backup: `/home/ubuntu/deploy-backups/uav-stream-85c9538`.
- Deployed asset hashes match v183.
- Public HTTP serves `app.js?v=180` and `styles.css?v=149`.
- Public asset inspection confirms the simulated-stream initializer and `SIMULATED ISR` disclosure.
- The obsolete event-summary title expression is absent from production.
- UI, general Hermes, and Moshe Hermes services are active; the status API reports V2.1 with 14,800 rows.
