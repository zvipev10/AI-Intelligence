# Capability Status

## Capability

Serbian Intelligence Dataset V2

## Current phase

Activated locally; deployment pending

## Overall status

Implementation complete

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Approved | None. | Done |
| Development | Complete | Deploy the committed activation when requested. | Deployment |
| UX | Complete | Dynamic V2 dataset/location loading and version display. | Done |
| QA | Complete | Loader, API, rollback, syntax, and identifier smoke tests passed. | Done |
| Architecture/Security | Watch | Preserve synthetic/public provenance boundaries. | Ongoing |

## Latest change since previous review

Checkpoint 002 makes V2 the default runtime dataset while retaining an environment-controlled V1 rollback.

## Current blockers

None. UAV observations are regular event records; detected objects and estimated counts are available in their text.

## Current risks

- Production deployment has not yet been verified.
- UAV counts are synthetic intelligence estimates, not ground truth.

## Next expected artifact

Production deployment and smoke test.

Published branch: `codex/serbian-intelligence-dataset-v2` (`433976c`).

## Parent issue

Local draft: `issues/parent-capability.md`

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/010-generate-v2.md` | Development | Generate and validate v2 dataset. | Complete | No |
| `issues/020-qa-v2.md` | QA | Review generated dataset and activation. | Complete | No |

## Artifact links

- Capability brief: `capability-brief.md`
- Developer review: `developer-review.md`
- QA review: `qa-review.md`
- Execution plan: `execution-plan.md`
- Latest checkpoint: `checkpoint-002.md`

## Gate checklist

- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue links are current.
