# Corrective Checkpoint 007 — MapLibre marker positioning

MIL-STD marker elements were styled with `position: relative`, overriding
MapLibre's required absolute positioning. The marker descriptors, hostile
affiliation, filter result, and DOM elements were correct, but the resulting
symbols were translated from normal document flow and rendered outside the map.

The marker rule now preserves absolute positioning. The exact production flow
for `OBS-UAV-V2-00246` must show one hostile red marker inside the map before
and after the row-level Show on map action. Release assets are
`app.js?v=176`, `styles.css?v=147`, and `deployment/SHA256SUMS-v180.txt`.

## Publication and production acceptance

- Implementation commit on remote `main`: `ed5614c`.
- Production target: `/opt/serbia-poc-ui` on `151.145.93.180`.
- Rollback backup: `/home/ubuntu/deploy-backups/milstd-marker-position-ed5614c`.
- Deployed `index.html` and `styles.css` hashes match `SHA256SUMS-v180.txt`.
- `serbia-poc-ui` is active and the public page serves `styles.css?v=147`.
- Exact browser acceptance for `OBS-UAV-V2-00246`: one filtered result; the
  hostile marker computes to red and `position: absolute`; its bounding box is
  inside the map before focus and remains inside after Show on map; one popup
  opens and the row action is pressed.
