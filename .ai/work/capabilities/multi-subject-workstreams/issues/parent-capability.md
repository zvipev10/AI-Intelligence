# [Capability] Multi-subject and question-based workstreams

## Capability
`multi-subject-workstreams`

## Current phase
Capability definition and review.

## Overall status
Draft pending product, development, UX, and QA review.

## Operational status
See `.ai/work/capabilities/multi-subject-workstreams/status.md`.

## User problem
Workstreams can currently mention several subjects or a general question only in free text. They cannot preserve several tracked subjects as structured, independently managed scope.

## MVP scope
- Question-only, subjects-only, and hybrid workstreams.
- Multiple typed subject references.
- Subject lifecycle and multi-subject artifact associations.
- Backward-compatible schema-v1 reads.

## Acceptance criteria
- [ ] Question-only workstream can be created and reopened.
- [ ] Workstream with at least two subjects can be created and reopened.
- [ ] Hybrid scope is preserved through later analysis.
- [ ] Artifacts may reference several subjects or the general workstream.
- [ ] Existing workstreams continue to load.
- [ ] Investigation isolation remains unchanged.

## Child tasks
- [ ] Product review
- [ ] Developer review
- [ ] UX review
- [ ] QA review
- [ ] Execution plan
- [ ] Schema/API implementation
- [ ] UI implementation
- [ ] Artifact/agent-context implementation
- [ ] Final QA
- [ ] Final handoff

## Artifacts
- Capability brief: `.ai/work/capabilities/multi-subject-workstreams/capability-brief.md`
- Status: `.ai/work/capabilities/multi-subject-workstreams/status.md`

## Closure rule
Keep this parent issue open until all required tasks, acceptance criteria, final QA, deployment, and handoff are complete.
