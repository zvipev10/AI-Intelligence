# Corrective Checkpoint 007 — MapLibre marker positioning

MIL-STD marker elements were styled with `position: relative`, overriding
MapLibre's required absolute positioning. The marker descriptors, hostile
affiliation, filter result, and DOM elements were correct, but the resulting
symbols were translated from normal document flow and rendered outside the map.

The marker rule now preserves absolute positioning. The exact production flow
for `OBS-UAV-V2-00246` must show one hostile red marker inside the map before
and after the row-level Show on map action. Release assets are
`app.js?v=176`, `styles.css?v=147`, and `deployment/SHA256SUMS-v180.txt`.
