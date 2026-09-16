# Developer Review

Status: approved assumptions delegated by the user's end-to-end implementation instruction.

Use the existing atomic JSON-store, MCP tool registry, multiplexed Hermes profile, member-routing, typed result-layer, object-viewer, and MapLibre presentation patterns. Add a separate assessment store and do not extend Evidence or target schemas. Overlay geometries use GeoJSON-compatible validated coordinates and a bounded feature count. Optimistic revision checks prevent stale updates.

Risks: profile deployment drift, cross-agent authorization leakage, invalid geometry, oversized overlays, and conflating assessment graphics with ground truth. Mitigate with explicit tool allowlists, server validation, revision checks, capped features, provenance, and assessment-specific styling.
