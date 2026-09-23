# Execution plan

Review gate: user explicitly requested implementation and deployment on 2026-09-23.

1. Restyle the current two-option basemap selector as a compact segmented pill.
2. Classify CARTO transportation and boundary line layers as satellite reference layers.
3. Move those layers above the imagery raster but below map labels.
4. Use muted amber roads and white borders in Satellite mode; restore original paint in Street mode.
5. Extend the existing basemap regression test and validate the public deployment.

Rollback: revert the release commit or restore the VM backup; no data or service interfaces change.
