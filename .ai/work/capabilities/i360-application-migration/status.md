# Capability status: I360 application migration

## Current phase

Execution planning.

## Overall status

Draft — pending human architecture/product review before implementation.

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Pending | Accept preserved behavior, exclusions, and temporary persistence boundary option | Slice 0 |
| Development | Ready | Review provider boundary and slice ownership | Slice 1 |
| UX | Pending | Accept degraded and permission states | Slice 5 |
| QA | Ready | Turn matrix into cases after live samples exist | Slice 2 |
| Architecture/Security | Pending | Approve authentication, identity propagation, logging, and write model | Slice 0/2/6 |

## Latest change

Created a full migration plan. Workstream and playback are explicitly excluded.

## Current blockers

- No authenticated target-estate capability/field probe has been completed.
- Authentication and identity-forwarding design is not approved.
- Persistence and concurrency choices for investigation state and targets are unresolved.

## Current risks

- Installation-specific capabilities and search semantics may prevent parity.
- Permission enforcement may differ across I360 operations.
- Required metadata may not exist in ingested items.

## Next expected artifact

`checkpoint-001.md` containing Slice 0 capability and field verification results.

## Issue status

Parent and child issues have not been created. Local issue drafts are available in `issues/`.

## Artifact links

- `capability-brief.md`
- `decisions.md`
- `developer-review.md`
- `ux-review.md`
- `qa-review.md`
- `execution-plan.md`
- `handoff-summary.md`
