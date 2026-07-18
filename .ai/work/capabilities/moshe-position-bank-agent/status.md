# Capability Status

## Capability

Moshe Position Intelligence Agent and Position Bank

## Current phase

Capability definition and draft role review

## Overall status

Paused for human Product/Development/UX/QA/Security review; no implementation authorized.

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Product | Pending | Answer the five blocking product questions in `capability-brief.md`. | Execution plan |
| Development/Architecture | Draft ready | Review architecture, persistence, lineage, and execution slices. | Execution plan |
| UX | Pending | Define artifact review flow and bank-layer presentation. | Execution plan |
| QA | Draft ready | Approve gold-set strategy and quality thresholds. | Execution plan |
| Security | Pending | Review write authorization, audit, data isolation, and simulation-only boundary. | Execution plan |

## Current blockers

- Source independence cannot be enforced with the current projection alone; source-family lineage is required.
- Human approval role and freshness policies are undefined.
- UX and security reviews do not yet exist.

## Current risks

- False fusion and false source independence.
- False coordinate precision and stale mobile-object assessments.
- The term “target bank” may imply unsupported weapon/attack functionality.

## Next expected artifact

Human-reviewed product answers, then UX/security reviews. Only after those gates may an `execution-plan.md` be created.

## Parent issue

Local draft: `issues/000-parent-capability.md`

## Child issues

| Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| `issues/010-product-review.md` | Product | Resolve scope, terminology, approval, freshness, and ownership. | Pending | Yes |
| `issues/020-developer-architecture-review.md` | Development/Architecture | Approve technical approach and data contracts. | Pending | Yes |
| `issues/030-ux-review.md` | UX | Define draft/review/accepted interaction and map layer. | Pending | Yes |
| `issues/040-qa-security-review.md` | QA/Security | Define validation thresholds, permissions, and audit requirements. | Pending | Yes |

## Artifact links

- Capability brief: `capability-brief.md`
- Developer/architecture review: `developer-review.md`
- QA review: `qa-review.md`
- Execution plan: not created; gate intentionally closed

