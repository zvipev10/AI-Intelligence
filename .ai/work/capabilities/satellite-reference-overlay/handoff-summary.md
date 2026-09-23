# Handoff summary

The basemap selector is compact, and Satellite mode now composes three existing map resources: Esri raster imagery, CARTO vector transportation/boundary references, and CARTO labels. Street mode restores the native CARTO presentation. No dependency, API, dataset, or analytical-layer change was introduced.

Satellite is the default initial basemap. Street remains selectable and is still the automatic fallback when the imagery source fails.

## Deployment

- Deployed to `/opt/serbia-poc-ui` on `151.145.93.180` on 2026-09-23.
- `serbia-poc-ui.service` is active and `/api/status` responds successfully.
- Public assets expose `styles.css?v=155`, `demo_bootstrap.js?v=209`, and `app.js?v=208`.
- Public asset checks confirmed the compact selector and satellite reference-layer logic.
- Rollback archive: `/home/ubuntu/deploy-backups/basemap-overlay-predeploy-20260923.tar.gz`.
- Source branch: `codex/map-style-toggle-overlay`.
- Main is unchanged because the GitHub PR CLI is unavailable in this workspace; the published branch is ready for GitHub review/merge.
