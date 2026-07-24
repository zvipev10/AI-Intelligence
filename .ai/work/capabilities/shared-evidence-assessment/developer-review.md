# Developer / Architecture Review

## Status

AI-authored draft — pending human Development/Architecture approval

## Feasibility

Feasible as a reusable scenario runtime if domain-specific content is isolated in adapters and fixture manifests. Prompt-only visibility remains invalid.

## Recommended architecture

### Versioned scenario definition

Define a validated manifest with:

- metadata and version;
- generic context references;
- stages and typed transitions/releases;
- assignments and triggers;
- artifact contribution contracts;
- decision-point contracts;
- visibility and reset policies.

The core runtime must not understand a specific target class, record ID, decision wording, or named agent.

### Domain adapters

Adapters resolve stable scenario references, apply visibility to domain retrieval, render domain summaries, and validate permitted artifact changes. The first evidence-corpus adapter can support the reference fixture without becoming the platform contract.

### Runtime and workstream state

Persist separately:

- scenario runtime: definition/version, stage, revision, transition status;
- workstream: responsibilities, artifacts, decisions, history, attention;
- agent runs: assignment, trigger, input revision, status, result reference.

Keep these separate from investigation memory and domain databases.

### Transition and trigger flow

1. Validate expected runtime revision and transition eligibility.
2. Apply one stage's typed changes atomically.
3. Calculate affected assignments.
4. Schedule exactly one bounded run per affected assignment.
5. Accept results only for the bound revision and contribution contract.
6. Persist changes as attributable revisions.

### Generic API candidates

- `GET /api/scenarios`
- `POST /api/scenario-runs`
- `GET /api/scenario-runs/{run_id}`
- `POST /api/scenario-runs/{run_id}/advance`
- `POST /api/scenario-runs/{run_id}/reset`
- `GET /api/workstreams/{workstream_id}`
- `POST /api/workstreams/{workstream_id}/decisions`

Avoid target IDs in endpoint structure.

## Visibility boundary

Every domain adapter must enforce the active release policy for direct lookup, batch retrieval, search, semantic retrieval, aggregation, fusion/correlation, counts, and agent tools. Hidden information must behave as unavailable.

## Alternatives

- Hard-coded demo flow: rejected because it prevents reuse and hides coupling.
- Prompt-only scenario: rejected because it leaks unreleased information.
- Generic event-sourcing framework first: likely excessive for MVP.
- Per-user runtime: desirable later; global demo state may be an initial deployment limitation.

## Required architecture decisions

- Manifest schema and extension/versioning strategy.
- Stable generic reference envelope and adapter interface.
- Atomic persistence mechanism for runtime/workstream revisions.
- Assignment trigger and stale-result contract.
- Contribution-type validation.
- Global versus request-scoped runtime deployment.

## Proposed slices after approval

1. Generic manifest validation, runtime state, adapter contract, and fixture-independence tests.
2. First domain adapter plus exhaustive visibility tests.
3. Generic workstream and artifact contribution model.
4. Transition-triggered agent assignment and stale-run protection.
5. Human decision points, history, reset/recovery, and reference fixture.

These are review inputs, not an execution plan.

## Approval

- [ ] Approved
- [ ] Approved with changes recorded below
- [ ] Changes requested

Human reviewer:

Date:

Notes:
