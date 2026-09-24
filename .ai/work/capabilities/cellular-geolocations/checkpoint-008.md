# Polygon drawing control

Added polygon_draw.js and a small translucent bottom-right map button. Uses existing MapLibre GeoJSON, no dependency. Minimum three distinct vertices; first-point click closes the polygon. Escape/button cancels the draft while preserving finished shapes. Completed shapes remain page-local only; no network, filters or agent actions. Control repositions above the result table and attribution; map markers do not intercept drawing clicks.

Checks: geometry/cancellation/navigation tests and existing results harness passed; browser verified drawing, closure, street/satellite compatibility. Fixed asynchronous source update handling found during cancellation QA.

Deployed 424ce052 successfully. Live assets match local files; service healthy with 443 records and maintenance disabled. Backup: /opt/demo-runtime/backups/syria-polygon-424ce052. Browser cancellation rechecked after the source update fix. Added regression coverage for cancellation while tiles load. Draft PR85 updated, not merged; refresh application to load app220/styles158.
