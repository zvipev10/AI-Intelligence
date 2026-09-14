# Execution plan: I360 application migration in two releases

## Plan status

Draft — split into independently reviewable and releasable parts.

## Goal

First deliver the application on I360 without chat-based investigation or agents. Then add the agent experience using I360-backed tools and evaluate I360 `llm/chat` as the inference layer that replaces Hermes.

## Scope boundary

```text
Part 1: Analyst application
Browser -> Application API -> I360

Part 2: Agent investigation
Browser chat -> Application agent controller -> I360 llm/chat
                                      └──────> I360-backed domain tools
```

Part 1 must operate, be testable, and be releasable without Hermes, an agent controller, MCP tool selection, or chat-based investigation. Part 2 depends on the stable provider and application services delivered by Part 1.

Workstream and scenario playback remain outside both parts.

## Shared prerequisite gate

Before implementation, verify the target I360 environment with ordinary-user identities: authentication, permission behavior, item/entity schemas, field mappings, search capabilities, warnings, paging, geo, embeddings, media access, and representative records. Record the result in `checkpoint-001.md`.

# Part 1 — I360 application without chat investigation or agents

## Part 1 outcome

An analyst can use the application directly to discover and inspect authorized I360 data:

- text and semantic search;
- source, entity, time, and geographic filtering;
- map, timeline, list, and catalog views;
- item details, original/translated text, transcripts/OCR, and media;
- entity and location exploration;
- verified aggregations;
- saved investigations, questions, layers, and analyst notes;
- target-candidate search, creation, update, duplicate checks, and evidence attachment;
- English and Hebrew UI, permission errors, partial-result warnings, and diagnostics.

Chat entry points and automated investigative conclusions are disabled or absent in Part 1. Users search, filter, inspect, and save through explicit controls.

## Part 1 acceptance criteria

1. An ordinary user sees only authorized I360 records across every data path.
2. Search results consistently drive map, timeline, list, catalog, and object-view selections.
3. Every displayed record retains a stable I360 source reference and provenance.
4. Missing capabilities and incomplete results are distinguishable from no matches.
5. Saved state and target candidates reopen with valid evidence references and approved visibility.
6. Representative English and Hebrew behavior passes.
7. The release starts and functions with Hermes and agent chat disabled.
8. Provider rollback is proven before I360 becomes the default.

## Part 1 slices

### P1.0 — Authenticated estate discovery

Add a read-only diagnostic and redacted fixtures. Produce the approved capability, field, permission, and identifier matrix.

**Gate:** Architecture/Security and platform owner. Stop after slice.

### P1.1 — Provider boundary and canonical mapping

Define provider operations for search, semantic search, item detail, aggregation, context, entity/place lookup, and media. Put current local reads behind `LocalDataProvider`; define canonical IDs, time, source, reliability, certainty, location, entity, text, media, warnings, and coverage.

**Gate:** Development/Architecture. Existing local behavior must pass through the new boundary.

### P1.2 — Read-only I360 provider

Implement server-side authentication, transport, timeouts, safe retries, pagination, capability discovery, warning propagation, and normalized I360 operations. Add recorded-response contract tests and live ordinary-user permission tests.

**Gate:** Architecture/Security/QA. Denied records must remain inaccessible through every tested path.

### P1.3 — Non-chat application services

Route layer catalogs, layer rows, searches, filters, aggregates, object details, entity/location lookup, and media through the provider. This slice creates reusable domain services that Part 2 can later invoke.

**Gate:** Development/QA/Product. Search and aggregate coverage semantics must be explicit.

### P1.4 — Frontend conversion

Connect search controls, map, timeline, list, catalog, and object viewer to I360-backed services. Add authentication-expired, unavailable, denied, unsupported, partial, and stale-record states. Disable chat-based investigation in the Part 1 runtime configuration.

**Gate:** UX/Product/Security/QA. Complete the search-to-inspection flow in both locales.

### P1.5 — Application state and target candidates

Choose the approved persistence boundary for investigations, saved questions/layers/notes, and targets. If records move to I360, define entity types, actor visibility, soft deletion, evidence relationships, and conflict behavior. Otherwise retain current repositories temporarily while using I360 item IDs.

**Gate:** Product/Architecture/Security/QA. Multi-user visibility, save/reopen, stale evidence, duplicate targets, and concurrent writes must pass.

### P1.6 — Part 1 acceptance and cutover

Run functional, permission, bilingual, representative-volume, failure, and rollback tests. Make I360 the default data provider only after acceptance. Do not remove local stores in this slice.

**Gate:** Product/Operations/Security/QA. This is the release decision for Part 1.

# Part 2 — Chat-based investigation and agents

## Part 2 outcome

Restore conversational investigation on top of Part 1. An application-owned agent controller uses I360 `llm/chat` for inference, executes approved domain tools, preserves state, streams progress, and produces the existing answer and presentation contracts. Hermes can then be retired if parity is demonstrated.

## Part 2 acceptance criteria

1. General and Moshe routing, instructions, and session boundaries match approved behavior.
2. The controller performs bounded, validated multi-step tool loops over Part 1 services.
3. Answers cite authorized I360 items and every citation resolves for the current user.
4. Tool activity, progress, cancellation, timeout, retry, and failure states are visible and auditable.
5. Investigation memory and saved chat results reopen without an opaque provider session.
6. Evidence prompt injection cannot select unauthorized tools or override controller policy.
7. Representative investigations meet accepted quality, coverage, latency, and cost thresholds relative to Hermes.
8. Hermes remains selectable until rollback and parity acceptance are complete.

## Part 2 slices

### P2.0 — `llm/chat` capability proof

Verify models, structured JSON-schema output, streaming, context limits, cancellation, quotas, latency, identity propagation, and failure responses. Test multi-turn structured decisions without executing tools.

**Gate:** Architecture/Security/QA. Stop if reliable structured next-action output is unavailable.

### P2.1 — Agent controller foundation

Implement server-side conversation/run state, agent profiles, prompt construction, tool allowlists, argument validation, budgets, iteration limits, timeouts, cancellation, audit records, and final-answer assembly. Treat model output as untrusted input.

**Gate:** Architecture/Security/Development. No production tools are enabled yet.

### P2.2 — I360-backed agent tools

Expose Part 1 services as validated tools for search, semantic search, object retrieval, entity/location/reference resolution, aggregation, history, tracing, related events, claim comparison, hypothesis challenge, linkage, sequence building, and presentation. Preserve existing deterministic reasoning.

**Gate:** Development/QA/Product analyst. Tool contract and adversarial-input tests must pass.

### P2.3 — Multi-step investigation loop

Let the controller request a tool, execute it, append a bounded result, and call `llm/chat` again until completion or budget exhaustion. Add context compaction without losing citations, warnings, or authorization boundaries.

**Gate:** Product analyst/Security/QA. Grounding, stopping, coverage, and citation behavior must pass.

### P2.4 — Chat UI, live steps, and memory

Connect the existing chat to the new run lifecycle. Restore streaming, live steps, cancellation, saved results, presentation actions, and investigation memory. Do not depend on provider-managed memory unless its isolation and durability are proven.

**Gate:** UX/Product/Security/QA. Both locales and interrupted/reopened sessions must pass.

### P2.5 — Hermes parity and agent cutover

Run the same scenarios through Hermes and the I360-backed controller. Compare tool choice, evidence coverage, citations, conclusions, latency, failures, and cost. Accept explicit differences, switch the default agent provider, monitor, and retain a time-bounded Hermes rollback.

**Gate:** Product/Operations/Security/QA. Stop before disabling Hermes.

## Dependency and release decision

Part 1 does not depend on Part 2 and can be released alone. Part 2 depends on Part 1's provider, canonical model, services, identity propagation, and permission tests. Part 2 development may begin after P1.3 is stable; its production cutover should follow Part 1 acceptance.

## Stop conditions

- Required evidence is absent or lacks stable identifiers.
- Any I360 path exposes records outside the user's authorization.
- Warnings, caps, or incomplete coverage cannot be represented safely.
- Mutable records lack an accepted visibility or concurrency design.
- `llm/chat` cannot reliably produce schema-constrained next actions.
- The controller cannot enforce tool allowlists, budgets, citation grounding, or cancellation.

## Rollback

Part 1 retains provider selection between local and I360 until accepted. Part 2 retains agent-provider selection between Hermes and the new I360-backed controller until parity is accepted. Avoid dual writes unless a reconciliation design is separately reviewed.
