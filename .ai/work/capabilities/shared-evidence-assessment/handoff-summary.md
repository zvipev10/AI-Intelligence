# Handoff Summary

## Current outcome

The capability is now framed generally as **Collaborative Scenario Playback**.

The brief and four AI-authored role reviews define:

- entry from supported objects, investigations, questions, or prepared scenarios;
- a persistent shared workstream as the system of record;
- versioned scenario manifests with typed stages and transitions;
- generic agent assignments and automatic bounded reevaluation;
- scenario-declared human decisions;
- domain adapters that isolate object-specific behavior;
- strict future-record visibility enforcement across UI and agent retrieval;
- fixture-independence, concurrency, history, recovery, RTL, and accessibility gates.

`TGT-D4DC7A7EBE02` is retained only as a possible reference fixture. It must not appear in reusable schemas, APIs, component contracts, or generic acceptance tests.

## Current gate

The human Product owner approved the revised Phase 1 boundary and instructed implementation to begin. Broader capability reviews remain pending.

## Decisions still required

Phase 1 decisions are recorded in `decisions.md` and `execution-plan.md`. Individual Investigation Memory item selection is explicitly deferred. Slice 1 persistence/API implementation is approved by Development/Architecture and QA in `checkpoint-001.md`.

Broader decisions still required:

1. Approve manual versus condition-driven stage advance.
2. Approve manifest, adapter, visibility, and stale-run contracts.
3. Accept demo-global state as a deployment limitation or require per-user state.
4. Choose the later workstream-context assembly and memory-promotion experience.

## Next step

Merge PR #31 and define the Slice 2 chat-based creation flow. The current Product direction is to add `מעקב` to the existing plus menu, gather details conversationally, and require an explicitly attached layer. Product/UX still need to settle confirmation, minimum information, reopen, and error behavior before implementation.

## Publishing

Planning PR #24 is merged. Slice 1 is on `capability/workstream-phase1` under issue #30 and is ready for a separate implementation PR.
# Handoff Summary

## Current state

Phase 1 is merged to `main`: PR #31 provides persistence/API support and PR #33 provides the approved chat-based creation and interaction flow.

## What is new

The existing chat now supports creation of a durable workstream through `+` → `מעקב`, one explicit layer attachment, an objective message, and an agent-style confirmation. Active workstreams expose only a minimal header indicator; pressing it returns status and actions into chat.

## What remains unchanged

Investigation Memory, Hermes query behavior, and layer ingestion remain separate. The slice adds no automatic agent execution, scenario playback, artifact model, or LLM-generated status.

## Review outcome

The human Product owner approved the checkpoint and instructed implementation to proceed on 2026-07-24. No blocking review comments or CI checks are present on PR #33.

## Evidence

- Checkpoint: `checkpoint-002.md`
- Decision: `decisions.md`
- Execution plan: `execution-plan.md`
- Focused UI assertions: `llm_investigation_orchestrator_serbia_poc/test_workstream_ui.py`

## Next step

Product approved `artifact-001-target-assessment-lead.md` and narrowed indication entry to manual `REC-...` identifiers in chat. Artifact-specific Development/Architecture, UX, and QA draft reviews define the envelope/API/revision contract, chat resolution/confirmation flow, and validation strategy. They remain pending human acceptance. No execution plan or product code is authorized yet.
