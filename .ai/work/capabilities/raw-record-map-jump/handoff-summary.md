# Handoff Summary

Raw event rows now include a bilingual, keyboard-accessible map pin action. The action switches to the map, centers at the record's canonical/event coordinates, and opens a popup for the exact selected record. The popup shows record ID, time, entity, location, and summary. Rows without coordinates expose a disabled action; sorting and filtering ignore the action column.

Automated validation: JavaScript syntax check and 40 focused regression tests passed.

Deployed validation: UAV video layer loaded with 3,745 rows; `REC-V2-006948` opened as an exact-record popup on the active map.

Branch: `codex/raw-record-map-jump`

Implementation commit: `732ed0a`

Deployment assets: `app.js?v=153`, `styles.css?v=134`

Rollback: `/opt/serbia-poc-ui.backup-raw-map-jump-20260811T153527Z`
