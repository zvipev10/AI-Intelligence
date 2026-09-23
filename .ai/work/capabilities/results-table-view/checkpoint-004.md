# Checkpoint 004 — English basemap labels

User requests English city/place names. Replace baked-in native-language OSM raster tiles with CARTO Voyager vector style; override name-based symbol labels on style load to prefer name_en at every zoom, then name:en/name:latin/name fallback. Retain attribution from provider TileJSON, existing scenario center/bounds and investigation overlays. No API key, dependency or dataset change. Provider sources checked: https://github.com/CartoDB/basemap-styles and public style JSON. Raster service is being retired, so use the provider-recommended vector style.

Validation plan: JS syntax, mocked map initialization checks for zoom-independent English labels, unchanged house numbers/scenario bounds, public style/source/glyph/tile availability and static VM deployment. Missing English names retain available source name. Browser rendering not manually verified.
