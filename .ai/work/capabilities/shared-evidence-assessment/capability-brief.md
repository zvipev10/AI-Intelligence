# Capability Brief

## Capability name

Persistent Target Validation with Staged Scenario Replay

## Capability slug

`shared-evidence-assessment`

The existing slug and issue tree are retained because this is a refinement of the same collaborative-artifact capability, not a separate capability.

## Parent issue

GitHub issue #25; local source: `issues/000-parent-capability.md`

## Current status

Product direction is provisionally defined from the human discussion. AI-authored Product, Development, UX, and QA/Security reviews are ready for human review. Execution planning remains blocked until those reviews are approved.

## Product direction

Build a persistent collaborative intelligence workspace in which humans and agents jointly own tasks and evolving artifacts. Chat remains a place to discuss and redirect work, but it is not the system of record for the work.

Every agent collaborator must expose a functional advantage: work it can perform at a scale, speed, consistency, or technical depth that the user cannot reasonably perform manually or should not have to perform alone.

## User problem

The current product can answer follow-up messages and update filtered result layers, but continuity depends on the user prompting again and reconstructing meaning from chat. It does not demonstrate that an agent:

- owns an ongoing analytical responsibility;
- notices material evidence when the evidence environment changes;
- updates a durable artifact without waiting for another user prompt;
- distinguishes its proposed interpretation from an accepted conclusion;
- asks for human judgment at a precise unresolved decision.

A demo based on a static dataset also risks pretending to be live intelligence unless the historical replay is explicit and reproducible.

## Proposed capability

An analyst opens an existing candidate target and starts a **Target Validation Workstream**. The workstream has:

- a persistent objective and scope;
- a working assessment and explicit unresolved questions;
- supporting, contradicting, and potentially related evidence;
- agent-owned and human-owned next actions;
- attributable revisions and decisions;
- a visible historical replay clock in demo mode.

For the demo, the system plays a fixed historical scenario one stage at a time. Each stage makes only a defined subset of records available to both the UI and agent tools. Advancing the scenario triggers Moshe to re-evaluate the workstream automatically. Moshe may add proposed evidence, revise his working interpretation, identify a conflict, or request a bounded human decision. He may not silently accept the target or conceal prior interpretations.

This turns a stale dataset into an honest simulation of changing evidence while demonstrating persistent agent responsibility.

## Concrete demo scenario

### Anchor target

`TGT-D4DC7A7EBE02` — the candidate roadblock north of Gazivoda associated with NATO regional reserve forces.

The target is suitable because it already has a coherent three-record evidence chain, a plausible hard negative involving another force at the same location, later movement reporting, and a later cluster whose relationship to the original object is genuinely ambiguous.

### Scenario stages

| Stage | Simulated time / evidence release | Expected collaborative behavior |
|---|---|---|
| 0 — Open workstream | Baseline includes `REC-V2-006772`, `REC-V2-012725`, and `REC-V2-010155`; the candidate target already exists. `REC-V2-011567` is available as a same-place, different-entity challenge. | Analyst starts validation from the target. Moshe inventories the evidence, warns that three visible source groups do not prove three independent underlying sources, and records the different-entity report as contradicting or confounding evidence. |
| 1 — Movement update | Release `REC-V2-007576` at 19:14:21Z: UAV reporting of the same entity/location/object class, approximately 20 personnel, moving east. | Moshe re-evaluates without a new prompt, links the record as a possible evolution of the target, updates the workstream, and marks the prior static-location interpretation stale or revised. |
| 2 — Later checkpoint cluster | Release `REC-V2-011027`, `REC-V2-006585`, and `REC-V2-008550` from 23:25:58Z through 01:19:16Z: approximately 21 personnel and later withdrawal west. | Moshe detects a coherent later cluster but cannot establish whether it is the same evolving roadblock or a second roadblock. He creates two alternatives, explains the evidence for each, and requests a human identity judgment. |
| 3 — Human resolution | No hidden evidence is released. | Analyst chooses “same evolving object,” “separate object,” or “insufficient evidence,” adds rationale, or assigns a follow-up. Moshe updates the artifact around that decision while preserving the rejected alternative and uncertainty. |

Evaluator-only truth labels must never be exposed to the runtime or user. They may be used only by QA to verify that the staged record manifest is correctly assembled.

## Moshe's functional advantage

Moshe provides value that is materially different from follow-up chat:

- repeatedly searches and correlates a corpus much larger than a user should scan manually;
- performs the same validation checks after every evidence release;
- keeps the evidence-to-claim graph and raw references current;
- checks apparent corroboration for duplicate or shared-source risk;
- detects competing object interpretations and changes over time;
- owns the monitoring task and requests attention only when human judgment or authority is needed.

The analyst provides intent, contextual interpretation, responsibility for identity decisions, correction, prioritization, and acceptance.

## Agent value contract for the first slice

| Contract field | Moshe |
|---|---|
| Functional advantage | Continuous, repeatable corpus-scale target validation and provenance bookkeeping. |
| Required inputs | Target, workstream objective, visible replay stage, existing artifact state, and permitted record tools. |
| Produced contribution | Proposed evidence links, assessment revisions, alternatives, gaps, and attention requests. |
| Evidence and provenance | Stable raw record references, timestamps, source metadata, and contribution history. |
| Limits | Cannot prove underlying source independence from visible metadata; cannot decide ambiguous physical identity; cannot use unreleased or evaluator-only data. |
| Authority | May add and revise proposed agent work; may mark its own conclusions stale; may not accept the target, overwrite human decisions, or advance the scenario. |
| Completion signal | Current for replay stage, needs human decision, blocked, failed, or stale after stage/context change. |

## Primary user flow

1. The analyst opens `TGT-D4DC7A7EBE02` in the target bank.
2. The analyst selects **Start validation workstream**; the product creates a persistent artifact with a scoped default objective derived from the target.
3. The workspace shows the target, current evidence, workstream status, replay stage/time, contributor responsibilities, and Moshe's value and limits.
4. Moshe performs the baseline pass and adds attributable proposed findings.
5. The presenter or analyst selects **Advance scenario**.
6. The newly released record becomes visible everywhere it is permitted, and Moshe automatically starts one bounded re-evaluation.
7. The artifact shows what changed, why it changed, and whether attention is required. Chat may explain or redirect the work but does not contain the only copy of the update.
8. At the ambiguity stage, Moshe requests one explicit human decision with alternatives and evidence.
9. The analyst decides, defers, or assigns follow-up work. The workstream preserves the decision and prior alternative.
10. **Reset scenario** restores the deterministic demo baseline without mutating the underlying target database.

## Context model

Context is layered and promoted deliberately:

- **Investigation context:** broad shared mission and saved constraints.
- **Workstream context:** objective, scope, responsibilities, status, and unresolved questions.
- **Artifact context:** accepted/proposed evidence, assessment revisions, alternatives, and decisions.
- **Agent run context:** temporary retrieval and reasoning state for one bounded pass.

Agent run context is not durable by default. Only attributable contributions promoted into the artifact persist. Broader investigation context may be shared by other workstreams and team members without forcing all details into one memory blob.

## MVP scope

- One demo-only scenario manifest anchored to `TGT-D4DC7A7EBE02`.
- Start, advance one stage, and reset controls with a visible simulated time and demo label.
- One persistent target-validation workstream.
- Moshe as the only agent collaborator.
- Automatic, bounded Moshe re-evaluation after a successful stage advance.
- Structured evidence, alternatives, working assessment, gaps, and attention requests.
- Proposed, human-decided, superseded, stale, and unresolved contribution states.
- Human decision among the three identity outcomes.
- Attribution, timestamps, raw references, stage provenance, and revision history.
- Visibility enforcement across UI retrieval and all agent/MCP retrieval paths.
- Deterministic reset without modifying the source event corpus or production target row.

## Non-goals

- A general scenario authoring studio.
- Live ingestion or claims that the replay is real-time intelligence.
- Multiple simultaneous scenarios or multiple agent collaborators.
- Autonomous multi-agent planning or delegation.
- Real-time multi-user co-editing.
- Production identity, authorization, or organization roles.
- Automatic target acceptance or production target-bank mutation.
- Continuous background monitoring outside an active demo scenario.
- Establishing true source independence when lineage data is unavailable.

## Acceptance criteria

- The scenario clearly identifies itself as a historical simulation and displays current replay time/stage.
- Before release, future-stage records cannot be retrieved through UI, raw-record APIs, semantic search, fusion, or any Moshe tool.
- Starting from the target creates or reopens one durable validation workstream without requiring an artificial assessment statement.
- Advancing a stage atomically updates replay visibility and schedules exactly one bounded Moshe re-evaluation.
- Moshe's update appears in the shared artifact without a new user prompt and identifies what changed.
- The later cluster results in explicit alternatives and a bounded human decision request rather than a fabricated identity conclusion.
- Human decisions and rationale are attributable and cannot be overwritten by Moshe.
- Prior and superseded interpretations remain reviewable.
- Reset is deterministic and does not mutate the event corpus or target-bank record.
- Failure, timeout, refresh, or duplicate advance cannot corrupt accepted human work or expose future records.
- Existing non-demo investigation, chat, layers, memory, and target-bank behavior remains unchanged when replay mode is inactive.

## Technical constraints

- Replay visibility is a data-access boundary, not a prompt instruction. The UI server and every MCP retrieval path must resolve the same current scenario state.
- Existing process-global event indexes and semantic search can expose future records unless made visibility-aware.
- The simplest first slice is one explicitly demo-global scenario state. This must be isolated, prominently labeled, access-controlled as appropriate for the environment, and resettable. Per-user replay requires a larger request-context design.
- Scenario state and workstream state must be separate from investigation memory and the target database.
- Agent contributions must be additive or revision-based, auditable, and protected against stale runs.
- Only one scenario-advance job may run at a time. A run must bind to a scenario revision and be rejected or marked stale if the stage changes.
- VM memory and process topology constrain additional long-lived workers; prefer bounded reuse of the existing Moshe gateway.
- Evaluator-only truth remains outside runtime.

## UX principles

- Lead with the workstream and evolving artifact, not a transcript.
- Make the simulated clock and released-versus-future boundary unmistakable.
- Show a compact “what changed” diff after each stage.
- Separate agent proposals from human decisions through labels, visual treatment, and permissions.
- Treat uncertainty, contradictory evidence, and deferred decisions as valid states.
- Notify the analyst only for material updates, blockers, failures, or required judgment.
- Keep chat available for discussion and redirection, with durable outcomes promoted to the workstream.

## Key risks

- Hidden records may leak through one overlooked retrieval or semantic-search path.
- A global demo state can affect concurrent users or processes.
- Automatic agent runs can duplicate, race, or apply to the wrong stage.
- The UI may still feel like chat plus a status card if artifact changes are not first-class.
- Users may interpret source-group counts as proven independence.
- A deterministic script may feel theatrical unless the agent's evidence-linked changes remain inspectable and honest.
- Static/local identities cannot support production-grade authorization.

## Required reviews and gate

- Product: approve the start-from-target flow, agent/human authority, demo-global replay boundary, and decision semantics.
- Development/Architecture: approve visibility enforcement, state model, stale-run protection, and process integration.
- UX: approve the workstream layout, staged reveal, change presentation, and attention states.
- QA/Security: approve leakage tests, concurrency/recovery invariants, and demo access boundary.

No `execution-plan.md` or product implementation should be created until these reviews are human-approved.
