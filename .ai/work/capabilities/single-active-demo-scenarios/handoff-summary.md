# Implementation handoff

User-authorized steps 1–6 are implemented and deployed. One shared codebase selects Kosovo or Syria through validated profiles; exactly one scenario runs at a time. Kosovo is active at completion. Syria has the same 16 catalog layers with zero records and a countrywide Syria map. No Syria narrative or future features were invented.

## Source and deployment

- PR #69 / branch `codex/single-active-demo-plan`; not merged into main.
- Runtime commit `34860bcef4aca0a2eeb7ba7f9c1a1cce879b79ef`; Hermes `00bbfc690060d1323ddb2f065297c7425cb71c26`.
- Public endpoint: http://151.145.93.180 . Existing investigation and capabilities guides/media remain available.
- Exact installed manifest: `/opt/demo-runtime/releases/34860bcef4aca0a2eeb7ba7f9c1a1cce879b79ef/release-manifest.json`.
- Private recovery backup: `/opt/demo-runtime/backups/20260922T195952Z/`; migration proof reconciles 2,869 files.
- Runtime source lives in `/opt/serbia-poc-ui` and `/opt/serbia-poc`; state and role homes remain under `/opt/demo-runtime`, outside releases.

## Operator action

From `/opt/serbia-poc-ui`, run `/home/ubuntu/.hermes/hermes-agent/venv/bin/python activate_demo.py syria` or `... activate_demo.py kosovo`. This preserves prior scenario state, briefly stops the UI/dashboard/shared gateway, and checks readiness. The user accepted the resulting brief WhatsApp interruption. Reload existing browser tabs after switching. A failed target rolls back with a new activation generation; a drain timeout leaves the existing runtime intact. Boot recovery retains maintenance until the operator verifies health.

Read `llm_investigation_orchestrator_serbia_poc/docs/demo-scenarios.md` before deploying, restoring, or changing datasets. Do not rerun one-time provisioning or the legacy country-specific MCP installer. Build semantic caches offline with `build_demo_index.py`, verify the trusted cache/hash metadata, and install before activation. Missing/stale caches never trigger live VM rebuilds.

## Changed areas and verification

Profiles/empty dataset; shared runtime state selection; API and browser generation checks; single bounded agent admission; role-specific Hermes homes/session/audit state; migration and activation/recovery tooling; profile-driven map and empty catalog; deployment/runbook/tests. Detailed evidence: [checkpoint-003.md](checkpoint-003.md).

233 application tests: 225 passed, same 8 baseline failures. MCP: 72 passed, 2 skipped. 13 scenario tests passed. JavaScript syntax and catalog action harness passed. Live checks cover both datasets/agents, empty-layer action, stale-generation rejection, lock contention, failed-readiness rollback, state-preserving round trip, tile access and 12 guide/media assets. No browser visual acceptance is claimed.

## Next role and durable context

Review/merge PR #69, then conduct user browser acceptance. Implementation child #70 closes on merge; parent #67 remains open until acceptance. Subsequent features use short shared-code branches and test both profiles sequentially. Suggested durable doc updates: add the one-active-demo policy to `docs/decisions.md`, link the operator/state contract from `docs/architecture.md`, and list Kosovo plus empty Syria in `docs/product-context.md`. The implemented contract is already published in the focused runbook; no unrelated documentation rewrite is needed.
