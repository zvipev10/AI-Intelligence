# Polygon drawing control

Added polygon_draw.js and a small translucent bottom-right map button. Uses existing MapLibre GeoJSON, no dependency. Minimum three distinct vertices; first-point click closes the polygon. Escape/button cancels the draft while preserving finished shapes. Completed shapes remain page-local only; no network, filters or agent actions. Control repositions above the result table and attribution; map markers do not intercept drawing clicks.

Checks: geometry/cancellation/navigation tests and existing results harness passed; browser verified drawing, closure, street/satellite compatibility. Fixed asynchronous source update handling found during cancellation QA.
