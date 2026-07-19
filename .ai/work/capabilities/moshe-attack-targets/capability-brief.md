# Capability Brief

## Capability name

Moshe Attack Targets MVP

## Capability slug

`moshe-attack-targets`

## Parent issue

Pending remote creation. Draft: `issues/parent-capability.md`.

## Current status

Product definition in progress. Chapter 1, the target-bank persistence and schema contract, is approved. See `status.md`.

## User problem

Analysts need to invoke a specialist Hermes agent, Moshe, from the general chat to fuse end-state V2.1 evidence into explainable attack-target candidates and present them through the existing application layers.

## Business goal

Validate that agent-led geographic, semantic, temporal, and source-aware fusion can create useful, auditable target candidates from V2.1 without exposing evaluator truth to the agent.

## Target users

- Analyst invoking Moshe for a bounded mission.
- Human reviewer approving or rejecting candidates.

## Proposed behavior

Messages explicitly containing `@משה` are routed to a dedicated Moshe Hermes session. Moshe uses shared investigation and presentation infrastructure plus specialized fusion and candidate-write tools, creates summarized candidates in a global SQLite target bank, and presents them through the shared layer pipeline.

## MVP scope

- Moshe runs against the final state of V2.1 and is invoked only by `@משה` in the current user message.
- Consecutive `@משה` messages continue the same Moshe mission and Hermes session; a message without `@משה` closes that mission and routes to the general agent.
- Moshe owns clarification dialogue, investigation, fusion, candidate creation, and presentation.
- SQLite-backed global `attack targets` layer.
- Final-state targets with one current `location_id` and `entity_id`.
- MVP targets use only `candidate`; human approval/rejection is deferred.
- Confidence: `medium` or `high`; low-confidence clusters are reported but not saved.
- At least two independent source groups per saved candidate.
- Evidence record references, compact snapshots, fusion explanation, and quantity assessment.
- Duplicate prevention before candidate creation.
- Shared backend invocation, result normalization, layer construction, and frontend rendering for General and Moshe.
- No application-level evidence, candidate-count, or mission-duration limits for the MVP.

## Non-goals

- Movement and location history.
- Immutable target revisions.
- Staleness or revocation workflows.
- Concurrent-session conflict resolution.
- Cross-mission merge/split workflows.
- Nearby-location fusion in the MVP.
- Human approval/rejection and its UI/API workflow.
- Sticky routing without an explicit `@משה` mention.
- A separate direct Moshe mission form.

## Acceptance criteria

- Moshe can create a candidate only from at least two independent source groups supporting the same object, entity, canonical location, and compatible time window.
- Every candidate includes a summary, final object classification, confidence, quantity assessment, fusion explanation, mission/run identity, and supporting evidence.
- Evidence stores V2.1 record IDs plus compact source snapshots; evaluator truth is never read or copied.
- Targets reference the existing location and entity layers by ID rather than duplicating their canonical data.
- Moshe can update an existing candidate when evidence overlaps.
- Every message routed to Moshe contains `@משה`; all other messages are handled by the general agent.
- The first consecutive `@משה` message creates a Moshe mission/session and later consecutive mentions resume it using Hermes session continuity.
- Moshe may request missing information directly from the user before investigation or saving.
- The target bank can be exposed through the existing layer API and UI conventions.
- General and Moshe results pass through the same normalized result envelope and presentation pipeline, with explicit `responding_agent` attribution.

## Technical constraints

- Use SQLite.
- Keep the schema minimal: `targets` and `target_evidence`.
- Reuse canonical location and entity resolution.
- Object classification is a Moshe fusion assessment supported by tools, not a database mapping function.
- V2.1 evaluator-only labels and truth remain inaccessible to runtime code.
- Refactor the current agent-specific request/normalization code into shared agent routing, Hermes invocation, result normalization, layer construction, and frontend result application modules.
- Add `attack_targets` as a new layer kind rather than a Moshe-specific renderer.

## Risks

- Same location and object class do not prove identical physical identity.
- Public reposts can falsely appear independent.
- Agent summaries may overstate quantity or location precision unless tool outputs preserve uncertainty.
- The production VM has limited memory and significant swap usage under semantic-cache verification.

## Open questions

- Exact Moshe profile configuration and shared Hermes invocation API.
- Fusion-tool scoring and source-lineage contract.
- Target-layer table/map presentation details.

## Required reviewers

- Development for persistence, MCP tool, and Hermes feasibility.
- QA for V2.1 positive/hard-negative evaluation.
- UX for the target layer and human review flow.
- Architecture/security for write permissions and runtime truth isolation.

## Proposed execution checkpoints

1. Developer review of SQLite schema and existing persistence patterns.
2. Schema/tool contract approval before global writes.
3. Fusion-tool subset evaluation against V2.1.
4. Moshe bounded-mission evaluation without evaluator access.
5. Shared presentation refactor and target-layer acceptance.
6. Production release and rollback verification.

## Handoff to developer

Review the shared agent/presentation refactor in `chapter-002-agent-routing-and-presentation.md`, inspect the current monolithic request normalization path, and draft—not implement—the shared result envelope and execution slices.
