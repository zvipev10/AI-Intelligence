# Corrective Checkpoint 005 — UAV location-hydration redraw

## Problem
Restored UAV layers could load before the runtime V2.1 location catalogue. The
map skipped symbols without coordinates, and the later location hydration only
redrew the evidence table. A manual layer visibility toggle made the symbols
appear.

## Change
- Redraw all result views after runtime locations are loaded.
- Advance the script cache key to `app.js?v=175`.
- Add a regression contract that prevents an evidence-only redraw in the
  location-hydration block.

## Acceptance
- `OBS-UAV-V2-00246` remains present in the deployed UAV layer API.
- A restored UAV layer renders supported MIL-STD observation markers without a
  manual visibility toggle.
- Existing focused and application regression tests pass.

## Publication
- Implementation commit on remote `main`: `2e05abf`
- Production assets: `app.js?v=175`, `styles.css?v=145`
- Production backup: `/home/ubuntu/deploy-backups/uav-map-redraw-2e05abf`
- Manifest: `deployment/SHA256SUMS-v178.txt`
- Public API: v2.1, 14,800 rows; the exact observation is present.
- Cold-load browser acceptance: 1,487 military markers and 501 hostile markers
  rendered from the restored UAV layer without a manual visibility toggle.
