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

Phase 1 decisions are recorded in `decisions.md` and `execution-plan.md`. Individual Investigation Memory item selection is explicitly deferred. Slice 1 persistence/API implementation is complete in `checkpoint-001.md`.

Broader decisions still required:

1. Approve manual versus condition-driven stage advance.
2. Approve manifest, adapter, visibility, and stale-run contracts.
3. Accept demo-global state as a deployment limitation or require per-user state.
4. Choose the later workstream-context assembly and memory-promotion experience.

## Next step

Review `checkpoint-001.md` and the Phase 1 implementation PR. Do not begin the minimal UI shell until Development/Architecture and QA approve the dedicated store and API boundary.

## Publishing

Planning PR #24 is merged. Slice 1 is on `capability/workstream-phase1` under issue #30 and is ready for a separate implementation PR.
