# Handoff Summary

Raw event, target, location, and location-metadata rows now include a bilingual, keyboard-accessible map pin action. The action switches to the map, centers at the selected object's coordinates, and opens an object-specific popup. Memory-restored raw layers refresh after the runtime location catalog loads, so valid row actions are no longer left disabled.

Selection is a visible toggle: the pin changes state, exposes `aria-pressed`, and highlights the selected row. Selecting it again removes the row highlight and popup.

Automated validation: JavaScript syntax check and 41 focused regression tests passed.

Deployed validation: the 170-row Locations layer exposed 170 enabled map actions. Browser smoke confirmed one selected row, one pressed action, and one popup after selection, then zero of each after unselection.

Branch: `codex/raw-record-map-jump`

Implementation commits: `732ed0a` plus the shared-selection follow-up on this branch.

Deployment assets: `app.js?v=154`, `styles.css?v=135`

Rollback: `/opt/serbia-poc-ui.backup-map-selection-20260811T154856Z`
