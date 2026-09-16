# Execution Plan — Talia Enemy Assessments

## Gate
The user explicitly approved end-to-end implementation of steps 1–5 and requested additive capability only. Product, technical, UX, and QA assumptions are recorded in this workspace.

## Slice 1 — Contract, persistence, tools
Create the validated assessment artifact/store, revision model, and constrained MCP tools. Add tests for happy paths, invalid references/geometry, stale revisions, and target isolation.

## Slice 2 — Hermes profile and routing
Provision Talia through the existing multiplexed gateway pattern, add a narrow allowlist, and route selected/mentioned Talia while preserving investigation context.

## Slice 3 — UX and assessment overlays
Normalize assessment result layers, add viewer support and controlled point/area/route/confidence-envelope rendering with evidence navigation and standard result controls.

## Slice 4 — Integration and release
Run focused and broad regression tests, execute a real dataset assessment, verify target-bank immutability, deploy with rollback backups, smoke-test production, and publish the handoff.

## Stop conditions
Pause before any required modification to existing Evidence semantics, target eligibility/persistence, General/Moshe authorization, or workstream/playback behavior. Additive adapters and result kinds are permitted.
