# Capability Status

## Capability

Moshe Attack Targets MVP

## Current phase

Slice 6 quality recovery is implemented and all approved evaluation gates pass. Deployment review is pending.

## Overall status

Pending review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Recovery result pending review | Accept checkpoint 008 metrics and residual risk | Slice 6 |
| Development | Recovery complete | Await deployment approval | Slice 7 preparation |
| UX | Approved | Routing experience, attribution, candidate presentation, evidence, and states accepted | Complete |
| QA | Gates pass | Review checkpoint 008 and approve deployment preparation | Slice 6 |
| Architecture/Security | Slice 2 approved | Review evaluator isolation and deterministic source boundary | Slice 4 |

## Latest change since previous review

`prepare_target_candidate` now performs bounded discovery and pair ranking internally. The complete isolated rerun passes every gate: 93.67% chain recall, 92.10% evidence precision, 95.89% evidence recall, 100% hard-negative rejection, and 1.27% false merges.

## Current blockers

- Checkpoint 008 requires human acceptance before deployment preparation.
- Capability artifacts and Slice 1 code are published on `codex/moshe-attack-targets`; draft PR creation is still pending.
- Remote parent and child issues have not been created.

## Current risks

- False merges from shared canonical areas or copied public reporting.
- Production VM memory/swap pressure during sustained semantic workloads.

## Next expected artifact

Product and QA acceptance of `checkpoint-008-quality-recovery.md`.

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
| Pending | QA | Slice 6 full evaluation | Recovery passes; acceptance pending | Yes |
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
- Latest checkpoint: `checkpoint-008-quality-recovery.md`
- Handoff: `handoff-summary.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current.
