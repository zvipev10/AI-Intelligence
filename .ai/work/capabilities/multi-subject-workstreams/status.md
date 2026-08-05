# Capability Status

## Capability
Multi-subject and question-based workstreams (`multi-subject-workstreams`)

## Current phase
Capability definition.

## Overall status
Draft pending review.

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Review needed | Approve scope modes, subject kinds, and MVP behavior. | Developer planning |
| Development | Review needed | Validate schema migration and API/tool compatibility. | Execution plan |
| UX | Review needed | Define creation and subject-management interactions. | Execution plan |
| QA | Review needed | Review compatibility, isolation, and edge-case coverage. | Execution plan |
| Architecture/Security | Not blocking | Review only if ownership/authorization scope changes. | Production |

## Latest change since previous review
Initial capability brief created from current workstream contract inspection.

## Current blockers
Product behavior and data-contract review are required before implementation planning.

## Current risks
- Backward compatibility with single-`target_id` artifacts.
- Prompt growth from large subject lists.
- UI complexity for subject management.

## Next expected artifact
`developer-review.md` after product confirms the proposed MVP direction.

## Parent issue
Draft: `issues/parent-capability.md`.

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| TBD | Product | Approve behavior and scope. | Pending | Yes |
| TBD | Development | Review schema and migration. | Pending | Yes |
| TBD | UX | Review creation and management flow. | Pending | Yes |
| TBD | QA | Review acceptance and regression plan. | Pending | Yes |

## Artifact links
- Capability brief: `capability-brief.md`
- Parent issue draft: `issues/parent-capability.md`
- Developer review: pending
- UX review: pending
- QA review: pending
- Execution plan: pending

## Gate checklist
- [x] Current owner is explicit.
- [x] Required action is explicit.
- [x] Blockers are separated from risks.
- [x] Next artifact is explicit.
- [x] Parent and child issue placeholders are current.
