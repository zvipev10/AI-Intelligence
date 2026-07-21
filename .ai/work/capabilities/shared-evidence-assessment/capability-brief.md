# Capability Brief

## Capability name

Shared Evidence Assessment

## Capability slug

`shared-evidence-assessment`

## Parent issue

GitHub issue #25; local source: `issues/000-parent-capability.md`

## Current status

See `status.md` for operational owner, blockers, and next action.

## Product direction

Build a persistent collaborative intelligence workspace in which humans and agents contribute to shared tasks and evolving artifacts, while every contribution, uncertainty, disagreement, and decision remains attributable and reviewable.

Every participating agent must also have a legible functional advantage: work it can perform at a scale, speed, consistency, or technical depth that the user cannot reasonably perform manually or should not have to perform alone.

## User problem

The current product can route a prompt to an agent and present its answer, steps, and result layers, but the analytical work remains primarily conversational. A user cannot open one durable assessment, share responsibility for developing it with an agent, see how each contributor changed it, or distinguish an agent's proposed contribution from an accepted intelligence conclusion.

The roster also describes roles without explaining the concrete work advantage each future agent provides.

## Business goal

Prove the collaborative-workspace direction with one durable, jointly maintained intelligence artifact that makes both human judgment and agent leverage visible.

## Target users

- Intelligence analysts developing an assessment from large volumes of raw reporting.
- Reviewers who need to understand evidence, reasoning, uncertainty, and contribution history.
- Specialist agents contributing bounded analytical work to a shared investigation.

## Proposed capability

An analyst creates a **Shared Evidence Assessment** inside an investigation for one explicit intelligence question, hypothesis, or candidate object.

The assessment is both:

- a shared task: it records the objective, contributors, current work, blockers, and next actions;
- a shared artifact: it contains the working assessment, supporting evidence, contradicting evidence, alternatives, gaps, and contribution history.

For the first slice, the analyst can invite Moshe to contribute. Moshe does not merely return a chat answer. He performs a bounded evidence pass and adds reviewable proposed contributions to the assessment.

The analyst can add evidence and notes, correct scope, accept or reject individual agent contributions, revise the working assessment, and request another bounded pass. Moshe can identify gaps, propose follow-up tasks, and revise his contribution in response to review.

The artifact always preserves who contributed what and whether a contribution is proposed, accepted, rejected, superseded, or unresolved.

## Why Moshe provides a functional advantage

For this capability, Moshe's advantage is not personality or fluent explanation. It is the ability to:

- search and correlate the 14,800-record V2.1 corpus repeatedly;
- discover candidate evidence beyond the records already visible to the analyst;
- compare source families and test source independence consistently;
- detect possible duplicates and competing object interpretations;
- preserve raw record references and structured provenance;
- repeat the same bounded evaluation after the analyst changes the scope or adds evidence.

The analyst should not have to manually scan thousands of records, reproduce deterministic fusion checks, or maintain cross-reference bookkeeping. The analyst remains essential for intent, contextual interpretation, correction, prioritization, and acceptance.

## Agent value contract

Every agent exposed as a collaborator must eventually declare:

| Contract field | Meaning |
|---|---|
| Functional advantage | The work the agent performs that the user should not have to do manually. |
| Required inputs | The minimum task, artifact, and context needed to work reliably. |
| Produced contribution | The structured change the agent can make to shared work. |
| Evidence and provenance | How the contribution can be inspected and traced. |
| Limits | What the agent cannot establish or should not decide. |
| Authority | What it may propose, modify, or finalize without human action. |
| Completion signal | How the workspace knows the contribution is complete, blocked, or stale. |

The first Moshe value contract should be visible from the assessment invitation/assignment flow, not hidden in system documentation.

## Core user flow

1. From an investigation, the analyst creates an assessment and states the intelligence question or hypothesis.
2. The analyst optionally attaches existing layers, records, saved memory, or an attack-target candidate as starting context.
3. The workspace shows the shared artifact with the analyst as a contributor and no implied agent work yet.
4. The analyst invites Moshe and sees his functional advantage, required inputs, permissions, and expected output.
5. Moshe performs one bounded contribution run and updates his task state from working to completed, blocked, or needs review.
6. Proposed evidence, gaps, alternatives, and assessment changes appear inside the artifact with Moshe attribution and raw references.
7. The analyst accepts, rejects, edits, comments on, or requests revision of individual contributions.
8. The artifact retains the decision and contribution history rather than replacing prior states silently.
9. The analyst may mark the assessment reviewed when the required evidence and review conditions are satisfied.

## MVP scope

- Create one Shared Evidence Assessment within the active investigation.
- Support an explicit intelligence question or hypothesis as its objective.
- Attach selected existing layers/records or a target candidate as initial context.
- Show human and agent contributors with distinct identity and status.
- Invite Moshe for one bounded evidence contribution at a time.
- Display Moshe's functional advantage and limits before assignment.
- Store structured supporting evidence, contradicting evidence, alternatives, gaps, and working assessment.
- Mark each contribution as proposed, accepted, rejected, superseded, or unresolved.
- Preserve attribution, timestamps, raw references, and review decisions.
- Allow analyst-authored contributions and review actions.
- Persist and reopen the assessment within its investigation.
- Surface whether Moshe is working, blocked, complete, or awaiting review.

## Non-goals

- A generic project-management system.
- Multiple new agent runtimes in the first slice.
- Autonomous multi-agent planning or delegation.
- Real-time multi-user collaboration.
- Authentication, organizational roles, or production authorization.
- Automatic acceptance of agent conclusions.
- Full report authoring or publication workflow.
- Continuous background monitoring.
- Replacing the current chat, map, timeline, table, target bank, or investigation-memory experiences.

## Acceptance criteria

- An assessment survives page reload and investigation switching.
- The assessment objective, contributors, task state, evidence sections, working assessment, and review state are visible without reconstructing them from chat.
- The analyst can understand Moshe's specific functional advantage and limits before inviting him.
- Moshe's run produces structured contributions to the assessment rather than only a chat response.
- Agent-proposed content is visually and semantically distinct from analyst-accepted content.
- The analyst can accept, reject, edit, or request revision of individual agent contributions.
- Supporting and contradicting evidence retain raw record references and provenance.
- A rejected or superseded contribution remains in history.
- Moshe cannot silently finalize the assessment or erase human contributions.
- The existing investigation, chat, result-layer, memory, and target-bank flows continue to work.

## Edge cases

- The agent finds no relevant evidence.
- The attached context is too broad, missing, stale, or references a closed layer.
- Supporting and contradicting evidence point to the same raw record family.
- The agent discovers that the objective combines multiple possible real-world objects.
- The analyst edits the objective while an agent contribution is running.
- A contribution run fails or times out after adding no changes.
- The analyst rejects every proposed contribution.
- The same record is proposed more than once across revision runs.
- An accepted contribution becomes stale after the artifact objective changes.
- The artifact is reopened when Moshe's runtime is unavailable.

## Technical constraints

- Reuse the existing investigation identity, Moshe routing boundary, typed result pipeline, raw references, and target evidence primitives where feasible.
- Do not treat current browser-local member records as authenticated identities.
- Persist structured assessment state server-side; do not store full duplicated source rows in the artifact.
- Store stable record/layer/target references and refetch display data through constrained APIs.
- Agent writes must be additive or revision-based and auditable; no silent destructive overwrite.
- Keep evaluator-only V2.1 truth outside runtime and assessment data.
- Production authorization and data isolation require architecture/security review before real-user release.

## UX notes

- The assessment should feel like a shared working surface, not an agent transcript embedded in a card.
- Contributions should appear in the relevant artifact section, with activity history available separately.
- Agent status must distinguish working, blocked, awaiting review, and completed.
- Review controls should operate on meaningful contributions, not require accepting an entire answer at once.
- The functional-advantage explanation should be concise and task-specific.
- Disagreement and contradicting evidence must remain first-class, not visually demoted as errors.

## QA notes

- Validate persistence, attribution, contribution-state transitions, and immutable history.
- Validate that agent failure cannot corrupt or partially overwrite accepted human work.
- Validate raw-reference integrity and duplicate handling.
- Validate stale objective/context behavior.
- Validate RTL layout and accessible status/review controls.
- Regress existing chat, Moshe routing, investigation memory, layers, filters, and attack-target catalog behavior.

## Risks

- “Joint ownership” may be implemented as superficial co-author labels without genuinely shared, editable work.
- Too many contribution states could make the artifact difficult to scan.
- Reusing investigation memory directly may blur curated memory with live collaborative artifact state.
- Agent-generated task proposals could create noise without clear attention rules.
- Users may infer that accepted evidence automatically makes the working assessment correct.
- Current lack of authentication limits identity and authorization claims.

## Open questions

1. Should the first assessment start from a free intelligence question, an existing target candidate, or support both?
2. Can Moshe directly revise his own proposed contribution, or must each pass create a new revision?
3. What minimum review action changes a contribution from proposed to accepted?
4. Can the analyst edit an agent contribution directly, or should editing create a separate human-authored revision?
5. When the objective changes, which accepted contributions become stale automatically?
6. Is “reviewed” sufficient for MVP, or is a separate “accepted intelligence” state required?
7. Where should assessment attention requests appear in the existing workspace?

## Missing inputs

- Product decision on the assessment starting object.
- Product decision on review/acceptance semantics.
- UX definition for artifact layout, contribution comparison, and attention states.
- Developer review of persistence, revision, and agent-write boundaries.
- QA/security review of immutable history, permissions, and failure recovery.

## Required reviewers

- Product: objective, joint-ownership semantics, review authority, and MVP boundary.
- Development/Architecture: assessment schema, persistence, revision model, and Moshe contribution contract.
- UX: shared artifact flow, contribution states, disagreement, and attention management.
- QA: integrity, state transitions, regressions, and recovery.
- Security: agent write permissions and future human identity/authorization boundary.

## Required child issues

- [ ] Product review
- [ ] Developer/architecture review
- [ ] UX review
- [ ] QA/security review
- [ ] Execution planning

## Proposed execution checkpoints

1. Product review of the shared artifact and agent value contract.
2. Developer/architecture review of assessment persistence and revision semantics.
3. UX and QA/security review of contribution, disagreement, and approval states.
4. Human-approved execution plan.
5. Slice 1: persistent analyst-authored assessment shell.
6. Slice 2: bounded Moshe contribution and attribution.
7. Slice 3: contribution review, revision history, and recovery validation.
8. Final product/UX/QA acceptance.

## Handoff to developer

Questions for developer:

- Which existing investigation-memory and target-bank primitives can be reused without coupling distinct state models?
- What minimal assessment and contribution schemas preserve attribution and revision history?
- How should a bounded Moshe contribution run write proposed changes atomically?
- How can stale runs be rejected when the analyst changes the objective or attached context?
- Which APIs can refetch referenced records without persisting full source rows?
- What authorization boundary should be designed now even though MVP identity remains local/static?

Expected developer output:

- feasibility notes
- likely affected files/services
- implementation options
- recommended approach
- technical risks
- test strategy
- proposed execution slices
