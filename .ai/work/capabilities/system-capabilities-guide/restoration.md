# Restore the capabilities guide — 2026-09-22

The user requested the same restoration as the investigation journey page. Public and backend URLs returned 404; the file was absent from production and main but present on origin/codex/system-capabilities-guide.

Restore that exact approved source, include it in the deployment FILES list, publish, and atomically upload only this static file. No new behavior, dependencies, restart, data or configuration changes. Source equality, internal anchor targets and deployment inclusion passed. Restored with atomic replacement. Public GET returns HTTP 200 and is byte-identical to the approved source. SHA256: 1f7deb08933f0b648f742d2ae19c0d32599ccadaafd4d9e6fd18991a97980ee3. Browser is not connected, so visual revalidation is unavailable. Documentation scope: this restoration record; no architecture updates needed.
