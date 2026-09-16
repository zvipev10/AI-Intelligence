# Catalog recovery handoff — 2026-09-16

## Delivered
Authoritative live catalog matching recovers unambiguous Hebrew naming mistakes, returns choices for ambiguous names, and fails closed if the catalog is unavailable. Canonical actions preserve explicit location/entity/event/time filters through the gateway, HTTP loading, saved layers and refresh. Browser success is reported after loading; failures remain visible. Tool status is pending_ui, not opened. Frontend asset 185. No new dependencies.

## Changed files
UI server.py, app.js, index.html; mcp_server/catalog_layers.py and server.py; both deployment file lists; catalog Python/Node tests and evidence UI version assertion; recovery plan/checkpoints/status.

## Checks and risks
185 Python tests: 180 passed, five historical asset/manifest assertions fail identically on origin/main. See checkpoint-003.md. All 14 catalog-focused tests pass, including real HTTP scope checks. Node tests verify scope identity, refresh/save restore, and success/failure notices. node --check and git diff --check pass.
Conservative matching asks for clarification when multiple candidates are close. Geography must be supplied as explicit canonical location IDs from the conversation; the resolver does not invent geographic scope. Production service, catalog endpoint, asset-version, and source-hash verification passed. Actual agent/browser interaction verification remains pending because no browser surface was available after deployment.

## Publishing and next step
PR #58 is merged into `main` as `e634682`. The targeted VM deployment is complete; rollback files are under `/home/ubuntu/deploy-backups/catalog-reconcile-e634682`. The shared module is installed under both UI and MCP `mcp_server` directories. Parent #56 and child #57 remain open for interactive acceptance.

## Suggested documentation
Keep recovery behavior and release evidence in this capability workspace. No architecture or product-context rewrite is needed. Add live verification and rollback location here after release.
