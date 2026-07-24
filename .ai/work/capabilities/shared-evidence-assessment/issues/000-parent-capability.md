# [Capability] Persistent Target Validation with Staged Scenario Replay

GitHub issue: #25

## Capability

Demonstrate a persistent human-agent validation workstream by replaying historical evidence around a real candidate target in deterministic stages.

## Current phase

Role-review gate

## Overall status

Draft role reviews ready - pending human approval

## Operational status

See `.ai/work/capabilities/shared-evidence-assessment/status.md`.

## User problem

Follow-up chat can update answers and layers, but it does not show an agent owning an ongoing validation task, reacting autonomously to changed evidence, or maintaining a durable shared artifact.

## MVP scope

- Start a persistent validation workstream from `TGT-D4DC7A7EBE02`.
- Explicit historical replay with a visible simulated clock.
- Deterministic staged evidence release enforced across UI and agent tools.
- Automatic bounded Moshe reevaluation after each advance.
- Structured evidence, alternatives, gaps, human decisions, and history.
- Deterministic reset without source-corpus or target mutation.

## Acceptance criteria

- [ ] Future-stage records cannot leak through any retrieval path.
- [ ] Workstream state survives reload and agent runs remain revision-bound.
- [ ] Moshe updates the artifact after stage advance without a new prompt.
- [ ] Ambiguous identity becomes a bounded human decision.
- [ ] Human decisions and prior interpretations remain attributable.
- [ ] Replay reset is deterministic and does not mutate source data.
- [ ] Existing non-replay behavior does not regress.

## Child tasks

- [ ] Product review: GitHub #26; `010-product-review.md`
- [ ] Developer/architecture review: GitHub #27; `020-developer-architecture-review.md`
- [ ] UX review: GitHub #28; `030-ux-review.md`
- [ ] QA/security review: GitHub #29; `040-qa-security-review.md`
- [ ] Execution plan
- [ ] Slice 1 implementation
- [ ] Slice 1 review
- [ ] Final QA
- [ ] Final handoff

## Artifacts

- Capability brief: `.ai/work/capabilities/shared-evidence-assessment/capability-brief.md`
- Status: `.ai/work/capabilities/shared-evidence-assessment/status.md`
- Product review: `.ai/work/capabilities/shared-evidence-assessment/product-review.md`
- Developer review: `.ai/work/capabilities/shared-evidence-assessment/developer-review.md`
- UX review: `.ai/work/capabilities/shared-evidence-assessment/ux-review.md`
- QA review: `.ai/work/capabilities/shared-evidence-assessment/qa-review.md`
- Execution plan: pending
- Checkpoints: pending
- Handoff: pending

## Closure rule

Keep this parent issue open until all required child tasks are closed, acceptance criteria are satisfied, final QA is complete, and final handoff is published.
