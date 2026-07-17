# [Capability] מכלול - Investigation Team Management

## Capability

מכלול - investigation team management

## Current phase

Capability initiation

## Overall status

Draft / Pending review

## Operational status

See `.ai/work/capabilities/michlol-team-management/status.md`.

## User problem

The analyst needs a visible team/workgroup context for investigations. In the future, this team may include real users or agents. For the MVP, the product starts with a predefined set of users, each with a picture and name.

## MVP scope

- Define and show a predefined team member set.
- Each member has a stable id, name, picture, and initial member type `user`.
- Keep the first version independent from authentication, permissions, real-time collaboration, and agent execution.

## Acceptance criteria

- [ ] `מכלול` is represented in the investigation workspace.
- [ ] The MVP uses the five predefined members approved in `product-review.md`.
- [ ] Every predefined member has a name and picture.
- [ ] The compact list is displayed near the investigation-name combo.
- [x] Slice 1 is deployed to the shared VM for Product/UX/QA review.
- [ ] The model leaves room for future real users and agents.
- [ ] Existing chat, layer, filter, map, timeline, table, and investigation-memory behavior is not regressed.

## Child tasks

- [x] Product review: `010-product-review.md`
- [ ] Developer review: `020-developer-review.md`
- [ ] UX review: `030-ux-review.md`
- [ ] QA review: `040-qa-review.md`
- [ ] Execution plan:
- [ ] Slice 1 implementation:
- [ ] Slice 1 review:
- [ ] Final QA:
- [ ] Final handoff:

## Artifacts

- Capability brief: `.ai/work/capabilities/michlol-team-management/capability-brief.md`
- Status: `.ai/work/capabilities/michlol-team-management/status.md`
- Product review: `.ai/work/capabilities/michlol-team-management/product-review.md`
- Decisions:
- Developer review:
- UX review:
- QA review:
- Execution plan:
- Checkpoints:
- Handoff:

## Closure rule

Keep this parent issue open until all required child tasks are closed, acceptance criteria are satisfied, final QA is complete, and final handoff is published.
