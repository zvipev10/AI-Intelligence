# Checkpoint 005 — Satellite basemap implementation plan

User explicitly accepts Street/Satellite toggle with English labels and unchanged investigation overlays. Extend existing map presentation capability (#75 / PR #76).

Implementation: Esri World Imagery raster source with visible source credits; CARTO vector English labels retained above imagery. Toggle visibility of captured basemap layers only; never replace MapLibre style, data layers or markers. Default Street preserves current behavior; buttons allow Satellite. Satellite label contrast adjusted and restored on return. Source failures return to Street with visible status. This basemap is independent of synthetic, dated Satellite records.

Developer/UX/QA recommendation: small source/UI change; localized keyboard-accessible buttons, selected state, disabled until style loaded. Verify geometry/camera/overlay preservation in switching test, labels and attribution, live imagery CORS and public asset deployment. Provider metadata and Syria sample tile return 200; imagery credits: Esri, Vantor, Earthstar Geographics, GIS User Community. Imagery date/resolution varies; do not imply live capture or alignment with event dates. No new package or credential.

Execution: implement UI/source, test switch and failure behavior, deploy static assets, publish verification handoff. No independent human role approval is asserted; proceeding on user's implementation request.

Implementation checks passed: test_basemap_ui.cjs (toggle visibility, English labels, attribution, retained markers/custom route layer, restored contrast, source-specific failure fallback); existing Table and Syria media Node tests; JS syntax. Street remains default. Static release JS 207 / CSS 154 pending deployment.
