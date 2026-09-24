# Map polygon drawing

User scope: a small transparent bottom-right map icon, click vertices and click the first vertex to close a polygon, with no subsequent action. Implement an isolated MapLibre drawing helper using local GeoJSON only. Minimum three distinct vertices; preview the next segment, preserve completed polygons in the current page, allow Escape/button cancellation. Keep controls above the result-table overlay and attribution. No API calls, filters, persistence or agent actions.

Checks: drawing/closure/cancel geometry, marker interference, map navigation after completion, basemap switching and live browser verification. Deploy existing UI release with rollback.
