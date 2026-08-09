# Checkpoint 002 — Deployment regression and rollback

## Status

Regression confirmed and deployment rolled back on 2026-08-09.

## Incident

The feature was deployed with `remote_deploy_workstream_slice2.py`. That legacy script uploads six
complete UI files plus the MCP server and Moshe profile from its local checkout. The checkout was
based on the older `capability/moshe-indication-chat` line, so deployment replaced newer production
functionality rather than applying only the intended instruction changes.

## Evidence

All six managed UI files differed from the automatic pre-deployment backup:

- `server.py`
- `app.js`
- `index.html`
- `styles.css`
- `agent_result_pipeline.py`
- `workstream_artifacts.py`

The deployed MCP server also lacked newer bilingual/classification logic present in the backup.

## Recovery

Restored the exact files from:

`/opt/serbia-poc-ui-backups/workstream-slice2-20260809T112716Z`

Restored:

- all six UI files;
- `/opt/serbia-poc/mcp_server/server.py`;
- Moshe's installed `SOUL.md`;
- Moshe's installed `config.yaml`.

The restored files were verified byte-for-byte with `cmp`. Python compilation passed before service
restart.

## Post-rollback validation

- `serbia-poc-ui.service`: active
- `hermes-moshe-gateway.service`: active
- `GET /api/status`: 200, locale-aware v2.1 response, 14,800 rows
- Public root request: 200 in service logs

## Current product state

The regression is removed. The workstream-creation simplification is no longer deployed because its
instruction changes were rolled back together with the unsafe bundle.

## Required correction

Rebase the change onto the current production source and create a narrow deployment path that:

1. verifies pre-deployment hashes or expected source text;
2. changes only the current UI server instruction, current MCP tool description, and current Moshe
   profile;
3. creates a separate rollback backup for those exact files;
4. rejects any unexpected production/source drift;
5. runs regression checks for current bilingual, classification, header, result-presentation, and
   workstream behavior before and after deployment.

## Recommendation

Pause redeployment until the narrow current-baseline patch and regression plan are reviewed.
