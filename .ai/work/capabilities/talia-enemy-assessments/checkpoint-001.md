# Checkpoint 001 — Talia capability foundation

Implemented additively on `codex/talia-enemy-assessments`:

- Revisioned SQLite `ASM-*` assessment artifacts with evidence-reference and geometry validation.
- Create, update, get, search, attach-evidence, and supersede MCP tools.
- Talia multiplex profile and exact `@טליה` / `@Talia` routing with a target/workstream-free allowlist.
- Standard on-demand result-layer handling for `kind=assessments`.
- Assessment table/viewer and controlled point, area, route, and confidence-envelope map graphics.
- Separate navigation from assessments to their supporting Evidence objects.

Validation:

- Assessment storage/tool/routing tests pass.
- Python compilation and JavaScript syntax checks pass.
- A real projected Evidence object (`EVD-REC-V2-006594`) created and reopened a medium-confidence polygon assessment (`ASM-0ADCCB54E93CF32B`) in an isolated test store.
- Existing target-writing APIs are absent from Talia's tool allowlist.

Existing behavior changed only where required: Talia's English UI role label is corrected from “Terrain Officer” to “Enemy Assessment Officer”, and static asset versions are bumped for cache invalidation. No Evidence semantics, target eligibility, raw-layer presentation, General/Moshe authorization, or workstream/playback logic changed.
