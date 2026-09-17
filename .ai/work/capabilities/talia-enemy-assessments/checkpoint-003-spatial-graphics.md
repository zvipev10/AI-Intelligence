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
