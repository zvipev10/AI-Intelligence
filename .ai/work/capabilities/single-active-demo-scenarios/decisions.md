# Capability decisions

## 2026-09-22 — Only one active demo
Decision: the user explicitly requires one demo scenario at a time.
Context: Syria will add a dataset/map and future features, while preserving Kosovo. The existing VM has about 1 GB RAM and two CPUs; a prior read-only idle sample showed about 221 MB available and 1 GB swap occupied. Those observations are not a load-capacity guarantee.
Rationale: avoid duplicate resident agents/indexes and cross-scenario state while sharing development.
Impact: propose stop/start activation of one runtime, isolated saved state, a bounded shared execution queue and versioned demo packages. No second always-running deployment.
Alternatives excluded by user: simultaneously active Kosovo and Syria runtimes.
Follow-up: review proposed operator switching, downtime and state-preservation assumptions in #68. Implementation details remain recommendations, not approved decisions.

## 2026-09-23 — Accepted implementation and constrained VM behavior

The user authorized steps 1–6, empty Syria with the same layers, and brief interruption of the shared gateway integrations. Use countrywide Syria bounds; retain Kosovo as the active final scenario. Operator activation preserves state by default.

Stop UI, dashboard and gateway together: the dashboard owns separate MCP workers. Installed Hermes discovers profile toolsets through the root registry, so the root registry must retain definitions bound to the active scenario. This supersedes checkpoint-002's initial proposal to remove those definitions. Only active-scenario homes are selected; unrelated integrations remain configured.

Carry current role OAuth credentials across stopped transitions, because refresh tokens may rotate. Credentials are shared authorization, not learned scenario memory. Keep role-specific gateway API keys and keep all secrets outside Git. Scenario memories/sessions are never copied when switching.

Maintain one application execution slot and serial demo tools. Require prebuilt semantic indexes for scenario runtimes: cold construction on the 1 GB VM timed out and caused heavy swapping. Build the unchanged search backend offline; activation verifies cache/dataset hashes. This adds no dependency or second deployment. Future workloads still require capacity checks.

Publication: shared code/profile versions and runtime commit are pinned in the installed release manifest. Persistent state versions/backups remain independent of Git. No direct main push or merge is implied by VM deployment.
