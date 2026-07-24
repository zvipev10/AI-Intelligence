# Capability Status

## Capability

Moshe Attack Targets MVP

## Current phase

Slice 8 evidence-reference layer planning is pending Product and UX review.

## Overall status

In progress

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Final acceptance pending | Accept checkpoint 009 and residual risks | Complete capability |
| Development | Draft plan ready | Review the proposed shared result-contract extension after Product approval | Slice 8.1 |
| UX | Review requested | Review structured evidence-layer links, states, identifiers, and accessibility | Slice 8.2 |
| QA | Release evidence ready | Accept checkpoint 009 | Complete capability |
| Architecture/Security | Slice 2 approved | Review evaluator isolation and deterministic source boundary | Slice 4 |

## Latest change since previous review

The Slice 8 draft separates requested-result presentation from explicit, structured evidence-reference layers.

## Current blockers

- Final Product/QA capability acceptance is not yet recorded.
- Capability artifacts and Slice 1 code are published on `codex/moshe-attack-targets`; draft PR creation is still pending.
- Remote parent and child issues have not been created.

## Current risks

- False merges from shared canonical areas or copied public reporting.
- Production VM memory/swap pressure during sustained semantic workloads.

## Next expected artifact

Product decision on `slice-008-evidence-reference-layers-plan.md`, followed by Developer and UX review.

## Parent issue

Pending remote creation; local draft at `issues/parent-capability.md`.

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| Pending | Development | SQLite schema and tool-contract review | Approved locally | No |
| Pending | Development | Shared agent/backend presentation refactor | Approved locally | No |
| Pending | UX | Moshe attribution and candidate target layer presentation | Approved locally | No |
| Pending | QA | V2.1 evaluation plan | Approved locally | No |
| Pending | Architecture/Security | Runtime security boundary | Approved locally | No |
| Pending | Product and QA | Execution plan and thresholds | Approved thresholds now pass | No |
| Pending | Development | Slice 1 shared agent pipeline | Approved and complete | No |
| Pending | Development | Slice 2 SQLite target bank | Approved and complete | No |
| Pending | Development | Slice 3 fusion tools | Approved and complete | No |
| Pending | Development | Slice 4 Moshe routing and sessions | Deployed; user accepted | No |
| Pending | Development and UX | Slice 5 shared presentation | Approved, deployed, validated | No |
| Pending | QA | Slice 6 full evaluation | Approved, deployed, and verified | No |
| Pending | Operations and QA | Slice 7 release and handoff | Technically complete; acceptance pending | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Decisions: `decisions.md`
- Chapter 1 schema: `chapter-001-target-bank-schema.md`
- Chapter 2 routing/presentation: `chapter-002-agent-routing-and-presentation.md`
- Developer review: `developer-review.md`
- UX review: `ux-review.md`
- QA review: `qa-review.md`
- Architecture/security review: `architecture-security-review.md`
- Execution plan: `execution-plan.md`
- Slice 6 recovery plan: `slice-006-quality-recovery-plan.md`
- Slice 8 evidence-reference plan: `slice-008-evidence-reference-layers-plan.md`
- Latest checkpoint: `checkpoint-013-manual-result-presentation.md`
- Handoff: `handoff-summary.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current.
