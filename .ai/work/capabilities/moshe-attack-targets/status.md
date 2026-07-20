# Capability Status

## Capability

Moshe Attack Targets MVP

## Current phase

Slice 6 QA gates remain failed; a focused quality-recovery plan is ready for review. The separate Moshe answer-title follow-up is deployed and verified.

## Overall status

Pending review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Recovery review pending | Approve or amend recovery slices A-D | Slice 6 |
| Development | Recovery plan ready | Await plan approval | Slice 6 |
| UX | Approved | Routing experience, attribution, candidate presentation, evidence, and states accepted | Complete |
| QA | Recovery review pending | Review synthetic gates, evaluator freeze, and aggregate-only feedback | Slice 6 |
| Architecture/Security | Slice 2 approved | Review evaluator isolation and deterministic source boundary | Slice 4 |

## Latest change since previous review

Added `slice-006-quality-recovery-plan.md`: bounded sparse retrieval, explainable evidence-pair scoring, conservative ambiguity handling, and a frozen isolated 400-case rerun. No implementation has begun.

## Current blockers

- Slice 6 quality thresholds fail; evidence discovery/ranking must improve before release closure.
- Capability artifacts and Slice 1 code are published on `codex/moshe-attack-targets`; draft PR creation is still pending.
- Remote parent and child issues have not been created.

## Current risks

- False merges from shared canonical areas or copied public reporting.
- Production VM memory/swap pressure during sustained semantic workloads.

## Next expected artifact

Product and QA review of `slice-006-quality-recovery-plan.md`.

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
| Pending | Product and QA | Execution plan and thresholds | Slice 1 authorized; thresholds pending | No until Slice 6 |
| Pending | Development | Slice 1 shared agent pipeline | Approved and complete | No |
| Pending | Development | Slice 2 SQLite target bank | Approved and complete | No |
| Pending | Development | Slice 3 fusion tools | Approved and complete | No |
| Pending | Development | Slice 4 Moshe routing and sessions | Deployed; user accepted | No |
| Pending | Development and UX | Slice 5 shared presentation | Approved, deployed, validated | No |
| Pending | QA | Slice 6 full evaluation | Completed; request changes | Yes |
| Pending | Operations and QA | Slice 7 release and handoff | Not started | Yes |

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
- Latest checkpoint: `checkpoint-007-moshe-answer-title.md`
- Handoff: `handoff-summary.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current.
