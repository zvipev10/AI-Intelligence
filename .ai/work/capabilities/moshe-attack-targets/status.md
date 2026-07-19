# Capability Status

## Capability

Moshe Attack Targets MVP

## Current phase

Slice 4 persistent Moshe gateway deployed; user routing/resource test in progress.

## Overall status

Pending review

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Slice 1 approved | Approve proposed quantitative thresholds before full evaluation | Slice 6 |
| Development | Deployed | Monitor dual-gateway routing and VM resources during user test | Slice 5 |
| UX | Approved | Routing experience, attribution, candidate presentation, evidence, and states accepted | Complete |
| QA | Pending threshold review | Approve quantitative thresholds and release gates | Slice 6 |
| Architecture/Security | Slice 2 approved | Review evaluator isolation and deterministic source boundary | Slice 4 |

## Latest change since previous review

Deployed the persistent Moshe gateway and verified General routing, exact `@משה` routing, consecutive-session continuity, mission closure, target-bank permissions, service health, and initial resource use.

## Current blockers

- Proposed quantitative fusion-quality thresholds require Product and QA approval before Slice 6.
- User routing/security/resource acceptance after deployed testing.
- Capability artifacts and Slice 1 code are published on `codex/moshe-attack-targets`; draft PR creation is still pending.
- Remote parent and child issues have not been created.

## Current risks

- False merges from shared canonical areas or copied public reporting.
- Production VM memory/swap pressure during sustained semantic workloads.

## Next expected artifact

User acceptance of deployed Slice 4 in `checkpoint-004.md`.

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
| Pending | Development | Slice 4 Moshe routing and sessions | Deployed; user testing | Yes |
| Pending | Development and UX | Slice 5 shared presentation | Not started | Yes |
| Pending | QA | Slice 6 full evaluation | Not started | Yes |
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
- Latest checkpoint: `checkpoint-003.md`
- Handoff: pending

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [ ] Parent and child issue links are current.
