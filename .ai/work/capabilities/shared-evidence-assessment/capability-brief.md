# Capability Brief

## Capability name

Collaborative Scenario Playback

## Capability slug

`shared-evidence-assessment`

The existing slug and issue tree are retained to preserve review history. The capability itself is general and is not coupled to a target, record type, domain object, or named agent.

## Current status

Product, Development, UX, and QA/Security drafts are pending human approval. No execution plan or product code is authorized yet.

## Product direction

Build a persistent collaborative workspace where humans and agents jointly own tasks and evolving artifacts. Chat supports discussion and redirection, but the workstream is the durable system of record.

Each agent must expose a functional advantage: work it can perform with scale, speed, consistency, or technical depth that the user cannot reasonably perform manually or should not have to perform alone.

## User problem

Continuous chat can ingest follow-up inputs and change result layers, but it does not demonstrate persistent responsibility. Users cannot clearly see that an agent:

- owns an ongoing task;
- reacts when relevant scenario state changes;
- updates shared artifacts without another prompt;
- preserves what changed and why;
- distinguishes proposed work from human decisions;
- requests attention only where human judgment or authority is required.

Static demo data also needs an honest, repeatable way to represent change over time.

## Proposed capability

A user starts or opens a **Scenario Workstream** from a supported domain object, investigation, question, or prepared scenario.

The system plays the scenario one stage at a time. A stage can:

- release data;
- change object or environment state;
- introduce a constraint;
- complete an external action;
- advance simulated time;
- require a human or agent response.

After a stage change, only affected agent responsibilities are reevaluated. Agents update typed shared artifacts, identify conflicts or stale assumptions, and request bounded human decisions when needed. They may not use unreleased information, silently finalize protected decisions, or erase prior interpretations.

## General scenario model

### Scenario definition

- Identity, title, purpose, domain, and version.
- Starting context expressed through stable references.
- Ordered stages with entry conditions and optional simulated time.
- Stage changes expressed as released references or typed state transitions.
- Human and agent roles, responsibilities, authority, and limits.
- Artifact types that participants may update.
- Optional decision points and permitted outcomes.
- Visibility policy for unreleased information.
- Completion and reset policy.

### Workstream instance

- Scenario definition/version and current stage/revision.
- Context currently in scope.
- Human-owned and agent-owned responsibilities.
- Evolving artifacts and attributable revisions.
- Proposed changes, decisions, alternatives, gaps, and uncertainty.
- Active agent runs, blockers, and attention requests.

### Generic lifecycle

| Phase | System behavior | Collaborative behavior |
|---|---|---|
| Initialize | Create or reopen a workstream from declared starting context. | Participants receive explicit responsibilities and limits. |
| Change | Apply one stage's releases or transitions atomically. | Affected agent responsibilities become stale and reevaluate. |
| Interpret | Persist attributable artifact changes and provenance. | Agents explain what changed and separate observation from inference. |
| Decide | Surface a bounded choice, approval, correction, or prioritization request. | The human decides, defers, or assigns follow-up. |
| Continue | Use the decision and current artifacts as context for later stages. | Agents adapt without overwriting human decisions. |
| Complete/reset | Complete the scenario or restore its declared baseline. | History is retained, archived, or cleared according to policy. |

## Agent value contract

Every scenario assignment declares:

| Field | Meaning |
|---|---|
| Functional advantage | Work the agent performs beyond reasonable manual effort. |
| Trigger | Stage changes or artifact changes that require reevaluation. |
| Required inputs | Visible scenario state, responsibility, artifact state, and permitted tools. |
| Produced contribution | Typed artifact or status changes the agent may propose. |
| Provenance | How inputs, tool use, and changes remain inspectable. |
| Limits | What the agent cannot establish or decide. |
| Authority | What it may propose, revise, or finalize. |
| Completion signal | Current, needs human input, blocked, failed, or stale. |

The first implementation may assign Moshe, but the data model and APIs must use agent/role identifiers rather than encode Moshe-specific behavior.

## Primary user flow

1. The user chooses a prepared scenario or starts playback from supported context.
2. The product creates or reopens a scenario workstream.
3. The workspace shows context, artifacts, current stage/time, responsibilities, and participant authority.
4. Assigned agents perform baseline responsibilities and add attributable proposed changes.
5. An authorized user advances the scenario, or a declared condition advances it.
6. Stage changes become visible through every permitted surface.
7. Affected agents reevaluate automatically without a new prompt.
8. The artifact shows what changed, why, provenance, uncertainty, and attention needs.
9. The human decides, corrects, defers, or redirects where required.
10. Later stages continue from durable artifact state; reset follows declared policy.

## Context model

- **Workspace/investigation context:** durable shared mission and constraints.
- **Scenario context:** definition, current stage, releases, and roles.
- **Workstream context:** objective, responsibilities, status, and unresolved questions.
- **Artifact context:** proposed and accepted changes, alternatives, evidence, and decisions.
- **Agent-run context:** temporary retrieval and reasoning for one bounded reevaluation.

Only attributable promoted contributions persist from agent-run context.

## MVP scope

- Reusable versioned scenario manifest format.
- One configuration-authored reference fixture.
- Start, advance, complete, and reset controls.
- Visible stage and simulated time when applicable.
- One persistent scenario workstream at a time.
- One agent assignment in the first implementation without coupling the contract to its identity.
- Automatic bounded reevaluation after relevant stage changes.
- Typed artifact updates, alternatives, gaps, and attention requests.
- Human decisions protected from agent overwrite.
- Attribution, stable references, stage provenance, and revision history.
- Visibility enforcement across UI and all agent/tool retrieval paths.
- Deterministic reset without protected source-data mutation.

## Non-goals

- Visual scenario authoring studio.
- Live ingestion.
- Multiple simultaneous scenarios or autonomous multi-agent delegation.
- Real-time multi-user co-editing.
- Production identity and authorization.
- Domain-specific decision taxonomies in the platform contract.
- Automatic mutation or acceptance of protected production objects.
- Replacing chat, domain views, layers, or investigation memory.

## Acceptance criteria

- A scenario definition can reference different supported contexts without changing platform code.
- No reusable schema, API, or component requires a specific target, record ID, object class, decision wording, or named agent.
- Historical/simulated playback is clearly labeled.
- Future-stage information cannot be retrieved, counted, inferred, fused, or referenced through any user or agent path.
- Start/reopen produces one durable workstream from declared context.
- Stage advance atomically changes visibility/state and schedules exactly one reevaluation for each affected assignment.
- Artifact changes appear without a new user prompt and explain what changed.
- Scenario-declared decision points create bounded human attention requests.
- Human decisions cannot be overwritten by agents.
- Superseded and stale interpretations remain reviewable.
- Reset is deterministic and does not mutate protected source data or domain objects.
- Failure, timeout, refresh, concurrency, or duplicate advance cannot corrupt accepted human work.
- Existing behavior is unchanged when playback is inactive.

## Technical constraints

- Visibility is a data-access boundary, not a prompt instruction.
- Scenario definitions use stable references and typed transitions, not embedded domain rows or UI commands.
- Workstream, scenario runtime, investigation memory, and domain databases remain separate state models.
- Agent contributions are additive or revision-based and bound to a scenario revision.
- Only affected assignments run after a stage change.
- Duplicate transitions and runs are idempotent; stale results cannot apply.
- Evaluator-only or answer-key data is never part of runtime scenario definitions.
- A demo-global runtime may be the first deployment choice, but it is an environment constraint—not part of the capability contract.

## Reference fixture

`TGT-D4DC7A7EBE02` and its historical record sequence remain a suitable first fixture because they provide staged changes and a genuine human judgment point.

They belong only in fixture configuration, demo instructions, and fixture-specific QA. They must not appear in reusable schemas, endpoint semantics, UI component contracts, or generic acceptance tests.

Other scenarios may start from a broader investigation, monitored area, collection plan, developing report, operational task, or another collaborative domain.

## Required reviews and gate

- Product: approve generic entry contexts, responsibility semantics, decision authority, and MVP boundary.
- Development/Architecture: approve manifest extensibility, visibility enforcement, state separation, and trigger model.
- UX: approve generic workstream, stage-change presentation, artifact diffs, and attention model.
- QA/Security: approve contract tests, information-leakage tests, concurrency/recovery, and fixture independence.

No `execution-plan.md` or implementation should be created until the reviews are human-approved.
