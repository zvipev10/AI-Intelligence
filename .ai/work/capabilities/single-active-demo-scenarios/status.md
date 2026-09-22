# Single-active-demo scenario status

Phase: capability definition and draft delivery proposal.
Overall: planning complete; reviews pending, implementation not started.
Parent: [#67](https://github.com/zvipev10/AI-Intelligence/issues/67).
Review child: [#68](https://github.com/zvipev10/AI-Intelligence/issues/68).

| Role | Required action | Due before |
|---|---|---|
| Product/user | Confirm operator-only switching/preserved-state assumptions; specify Syria data/map and future features | Implementation/content approval |
| Development/architecture | Review manifest, namespaces, admission queue, safe activation and rollback | Formal execution plan |
| UX | Review maintenance, stale-tab, queued and failure states | Behavior changes |
| QA | Review migration/round-trip tests and capacity measurement gates | Implementation acceptance |

Confirmed constraint: only one scenario active at a time. Proposed architecture: one shared codebase and endpoint, separate packages/state, active workers only.
Current blockers: none for planning. Syria content specification and role approval are prerequisites to execution.
Risks: existing 1 GB VM headroom; mutable global data and audit state; safe migration of Kosovo state; stale clients/background work; unspecified new features.
Next expected artifact: reviewed role recommendations, then execution-plan.md and child implementation issues. No execution-plan.md is claimed approved or created before that gate.
Latest: inspected main d475d2e, captured seven proposed phases and testable completion criteria; no product or VM changes.

Artifacts: [brief](capability-brief.md), [proposal](proposed-plan.md), [developer review](developer-review.md), [UX review](ux-review.md), [QA review](qa-review.md), [decisions](decisions.md), [checkpoint](checkpoint-001.md), [handoff](handoff-summary.md).
