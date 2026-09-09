# Checkpoint 001 — Viewer implementation

## Status and recommendation
Complete, deployed, and smoke-validated. Delegated developer, UX, and QA review found no blocking issue.

## Delivered
- One accessible record/organization dialog shared by grid, eligible single-object map markers, and explicit assistant references.
- Record text and selected public metadata; organization identity, aliases, counts, locations, and sources.
- Allowlisted video/audio/image rendering when a URL is present, with no autoplay and an explicit unavailable-video state.
- Grouped or mixed map markers remain unchanged and do not open the viewer. Targets are excluded.
- Dialog close, backdrop, Escape, focus restoration, responsive layout, and media shutdown.

## Files
`app.js`, `index.html`, `styles.css`, focused viewer test, adjusted asset-version contracts, deployment manifest/readme.

## Validation
JavaScript syntax passed. 58 focused and regression tests passed, including viewer, workstream UI, welcome page, member UI, and canonical source manifest. Diff whitespace passed.

## Deployment and smoke validation
- Deployed the reviewed `app.js`, `index.html`, and `styles.css` to `/opt/serbia-poc-ui` on VM `151.145.93.180` on 2026-09-09.
- Rollback backup: `/home/ubuntu/deploy-backups/record-organization-viewer-20260909T232844Z`.
- UI, general gateway, and Moshe gateway services are active.
- Local VM status reports the configured V2.1 dataset with 14,800 rows.
- Local and public HTTP checks returned 200 and serve `app.js?v=171` and `styles.css?v=142`.

## Risks and remaining work
The repository currently has no playable media files; media playback is ready for rows that later carry a validated URL, while current UAV-like rows show the unavailable state. Automated and HTTP smoke validation passed; hands-on browser acceptance was not requested.
