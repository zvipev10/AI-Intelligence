# Restore the capabilities guide — 2026-09-22

The user requested the same restoration as the investigation journey page. Public and backend URLs returned 404; the file was absent from production and main but present on origin/codex/system-capabilities-guide.

Restore that exact approved source, include it in the deployment FILES list, publish, and atomically upload only this static file. No new behavior, dependencies, restart, data or configuration changes. Source equality, internal anchor targets and deployment inclusion passed. Public verification pending. Browser is not connected, so visual revalidation is unavailable. Documentation scope: this restoration record; no architecture updates needed.
