# Catalog recovery handoff — 2026-09-16

## Delivered
Authoritative live catalog matching recovers unambiguous Hebrew naming mistakes, returns choices for ambiguous names, and fails closed if the catalog is unavailable. Canonical actions preserve explicit location/entity/event/time filters through the gateway, HTTP loading, saved layers and refresh. Browser success is reported after loading; failures remain visible. Tool status is pending_ui, not opened. Frontend asset 185. No new dependencies.

## Changed files
UI server.py, app.js, index.html; mcp_server/catalog_layers.py and server.py; both deployment file lists; catalog Python/Node tests and evidence UI version assertion; recovery plan/checkpoints/status.

## Checks and risks
185 Python tests: 180 passed, five historical asset/manifest assertions fail identically on origin/main. See checkpoint-003.md. All 14 catalog-focused tests pass, including real HTTP scope checks. Node tests verify scope identity, refresh/save restore, and success/failure notices. node --check and git diff --check pass.
Conservative matching asks for clarification when multiple candidates are close. Geography must be supplied as explicit canonical location IDs from the conversation; the resolver does not invent geographic scope. Actual agent/browser production verification remains pending.

## Publishing and next step
PR #58 targets main at the user's request. Parent #56 and child #57 remain open for deployment acceptance. No VM deployment occurred before the user redirected work to the merge. Deploy only affected source files with backups; do not run the destructive full deployment helper for this hotfix. Shared module must be present under both UI and MCP mcp_server directories before restart.

## Suggested documentation
Keep recovery behavior and release evidence in this capability workspace. No architecture or product-context rewrite is needed. Add live verification and rollback location here after release.
