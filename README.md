# AI Intelligence

This repository contains the Serbia/North Kosovo intelligence-analysis proof of concept. The active application is a bilingual Hebrew/English analyst workspace backed by Hermes profiles and constrained MCP tools over a synthetic 14,833-record V2.1 dataset, including 24 simulated cellular-call records.

Current capabilities include:

- General investigation with semantic and deterministic retrieval.
- Additive map, timeline, table, entity, location, evidence, target, and assessment layers.
- Raw-record viewing with simulated UAV video for UAV observations.
- A precomputed Evidence Layer plus on-demand evidence preparation and neutral fusion.
- Moshe (`@משה` / `@Moshe`) for evidence-backed target-candidate workflows.
- Talia (`@טליה`) for durable enemy assessments, supporting evidence, and assessment graphics.
- Investigation memory, saved questions, workstreams, and mobile agent-run recovery.
- Multiplexed Hermes routing through one gateway while retaining profile-specific tools, memory, and authorization boundaries.

## Current production state

- Evidence implementation baseline on `main`: `9e6cef1`.
- UI root: `/opt/serbia-poc-ui`
- MCP root: `/opt/serbia-poc`
- UI service: `serbia-poc-ui.service`, port `8769`
- Hermes service: `hermes-gateway.service`
- Active dataset: `v2.1`
- Evidence catalog schema: `evidence-catalog-v2`
- Current catalog: 5,283 rows, including 783 fused evidence objects.

The latest evidence update reuses the existing semantic concept vocabulary in `prepare_evidence`, applies normalized classes to `prepare_fused_evidence`, uses an eight-hour rolling catalog window, and exposes cataloged fused evidence through the same repository interface consumed by Talia. The UI catalog and Talia profile were deployed and verified together on 2026-09-17.

## Start here

- `PROJECT_HANDOFF.md` — current deployment state, operational constraints, verification results, and continuation guidance.
- `llm_investigation_orchestrator_serbia_poc/README.md` — detailed application architecture and commands.
- `.ai/work/capabilities/evidence-semantic-fusion/` — latest evidence-tool design, tests, checkpoint, and handoff.
- `.ai/work/capabilities/mobile-agent-run-recovery/` — mobile background/recovery capability.
- `.ai/work/capabilities/talia-enemy-assessments/` — Talia assessment capability.

## Safety and data boundary

The dataset is synthetic. Evaluator truth and evaluator-label files are offline quality assets and must never be loaded into agent prompts, runtime retrieval, evidence creation, or user-facing layers.

Before changing or deploying the project, fetch the current remote state, inspect the working tree for unrelated changes, and follow `AGENTS.md` plus the relevant capability artifacts.
