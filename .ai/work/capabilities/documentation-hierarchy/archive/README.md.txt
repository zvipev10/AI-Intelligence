# AI Intelligence

This repository contains one shared bilingual intelligence-analysis application with isolated Kosovo and Syria demo packages. Hermes General/Moshe/Talia roles serve one active scenario at a time. Kosovo retains its 14,833-record V2.1 dataset and saved work; the current Syria `network-v1` package contains 208 synthetic records.

Current capabilities include:

- General investigation with semantic and deterministic retrieval.
- Additive map, timeline, table, entity, location, evidence, target, and assessment layers.
- Raw-record viewing with simulated UAV video, CCTV movies and timestamped Satellite image sequences.
- Syria ADINT/IPDR correlation by IP and session time, returning IMEI from IPDR.
- A standalone Table tab for geometry-free records, with IP/IMEI-specific IPDR columns.
- A precomputed Evidence Layer plus on-demand evidence preparation and neutral fusion.
- Moshe (`@משה` / `@Moshe`) for evidence-backed target-candidate workflows.
- Talia (`@טליה`) for durable enemy assessments, supporting evidence, and assessment graphics.
- Investigation memory, saved questions, workstreams, and mobile agent-run recovery.
- Multiplexed Hermes routing through one gateway while retaining profile-specific tools, memory, and authorization boundaries.
- A compact Street/Satellite basemap switch; Satellite is the default and retains vector roads, administrative borders, and labels.

## Current deployment snapshot

As documented on 2026-09-23:

- UI `/opt/serbia-poc-ui`, service `serbia-poc-ui.service`, port `8769`; MCP `/opt/serbia-poc`.
- Shared gateway `hermes-gateway.service`; scenario transitions also stop `hermes-dashboard.service`.
- Active scenario: Syria profile 6, `network-v1`, 208 records and 20 catalog definitions. Kosovo `v2.1` remains installed and inactive.
- Initial Syria camera: Damascus `[36.2765, 33.5138]`, zoom `11`.
- Satellite default, English-preferred labels, vector roads/borders, selectable Street fallback.
- Public assets: `styles.css?v=155`, `demo_bootstrap.js?v=210`, `app.js?v=209`.
- Source changes in PRs #69, #72, #74 and #76 are merged into `main`, along with later map refinements. Start new shared features from current remote `main`.

Check `/api/status` and the installed release manifest for live identity. The historical 5,283-row evidence catalog (783 fused objects) belongs to the Kosovo evidence release; it is not the active Syria catalog count. Immutable profile/data versions and mutable scenario state are separate from the shared application release.

## Start here

- [Product context](docs/product-context.md) — current datasets, demo narrative and analyst-facing features.
- [Scenario operator runbook](llm_investigation_orchestrator_serbia_poc/docs/demo-scenarios.md) — isolation, switching, upgrades and recovery.
- [Architecture](docs/architecture.md) and [decisions](docs/decisions.md) — durable implementation contracts.
- `PROJECT_HANDOFF.md` — current deployment state, operational constraints, verification results, and continuation guidance.
- `llm_investigation_orchestrator_serbia_poc/README.md` — detailed application architecture and commands.
- `.ai/work/capabilities/evidence-semantic-fusion/` — latest evidence-tool design, tests, checkpoint, and handoff.
- `.ai/work/capabilities/mobile-agent-run-recovery/` — mobile background/recovery capability.
- `.ai/work/capabilities/talia-enemy-assessments/` — Talia assessment capability.
- `.ai/work/capabilities/satellite-reference-overlay/` — current basemap composition, tests, deployment, and rollback notes.

## Safety and data boundary

The dataset is synthetic. Evaluator truth and evaluator-label files are offline quality assets and must never be loaded into agent prompts, runtime retrieval, evidence creation, or user-facing layers.

Before changing or deploying the project, fetch the current remote state, inspect the working tree for unrelated changes, and follow `AGENTS.md` plus the relevant capability artifacts.
