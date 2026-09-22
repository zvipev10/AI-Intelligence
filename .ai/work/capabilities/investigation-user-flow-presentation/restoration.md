# Restore the published user-flow page — 2026-09-22

User requested fixing the 404 at http://151.145.93.180/investigation-user-flow.html.
The VM and homepage are healthy. The page is missing from /opt/serbia-poc-ui and main, but exists on origin/codex/system-capabilities-guide at f8d8f1e and in VM backups.

Plan: restore the exact approved HTML from that branch; add it to remote_deploy_ui.py FILES so future deployments include it; commit and publish; deploy only this static file with atomic replacement; verify HTTP 200, source hash and page navigation. No restart or dataset/config replacement required.

Review: content unchanged; no new dependencies, interface or architecture. Main application remains intact. No assumptions about which earlier deployment removed the file. Rollback removes only the restored page if it did not previously exist, or restores its pre-update backup.

Status: restored on the VM; public GET returns 200 and is byte-identical to approved source. Anchor checks and deployment-list inclusion passed. No service restart or other production file changes.

Deployed SHA256: f65fd06a2ca5491ce6a47dbc15985b5f468e8f38a5a7da8899deac4169f1640b.
Published in PR #64. Browser visual recheck unavailable because no browser is connected; prior presentation acceptance is preserved by source equality. No new visual changes. The restoration record is the suggested documentation update; no architecture updates needed.
