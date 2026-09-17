# Checkpoint 003 — assessment spatial graphics correction

## Finding

Assessment `ASM-DA2072FD0ACCCFDF` combined reports with mutually inconsistent movement directions at one canonical location, but represented the conclusion as a large rectangular `assessed_area`. The renderer then gave that polygon a relatively opaque fill. The resulting graphic looked like a territorial MIL-STD symbol even though it was neither MIL-STD nor supported as a bounded area by the cited evidence.

## Correction

- Talia must choose overlay types by analytical meaning and may not invent a route from textual directions at one location.
- Conflicting movement directions produce at most a compact assessed point, or no overlay when location is also unsupported.
- Every overlay requires at least one supporting `EVD-*` reference.
- Assessed areas now use a faint amber fill and dashed boundary.
- Confidence envelopes use a distinct faint purple fill and dotted boundary.
- Coherent route axes use a blue line and destination arrowhead.
- Assessment graphics remain separate from Evidence MIL-STD symbology.

## Validation

- Assessment-store unit suite: 5 tests passed, including rejection of an unsupported overlay.
- `app.js` syntax check: passed.
- Full local Talia profile suite is blocked in the bundled Windows Python because PyYAML is absent; production Python includes it.

## Deployment

Deployed to the Serbia demo VM from commit `2a3c3f5`. Rollback files are stored at `/home/ubuntu/deploy-backups/talia-spatial-2a3c3f5`. Both `serbia-poc-ui.service` and `hermes-gateway.service` were active after restart; the live page serves `app.js?v=189` and `styles.css?v=151`.

The affected saved result `ASM-DA2072FD0ACCCFDF` was revised from revision 1 to revision 2. Its unsupported rectangular area is replaced by a low-confidence assessed point at the shared canonical location, explicitly noting that contradictory directions do not support a movement axis. Revision 1 remains in immutable assessment history.
