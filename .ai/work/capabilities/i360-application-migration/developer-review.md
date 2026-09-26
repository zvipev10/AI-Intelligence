# Developer review: I360 application migration

## Review status

Ready for planning with explicit validation gates. AI-authored technical review based on the current repository and public I360 contract; live authenticated behavior remains unverified.

## Feasibility

Feasible in two releases through an application-side provider boundary. The non-agent application can ship first. A later application-owned controller can use I360 `llm/chat` for inference and the first release's services as tools.

## Recommended architecture

```text
Current frontend
  -> existing application API
    -> domain services and MCP investigation tools
      -> IntelligenceDataProvider
        -> LocalDataProvider (migration fallback and deterministic tests)
        -> I360DataProvider (items, entities, context, aggregates, media)
```

The provider returns the application's canonical event/entity/location structures. Existing tools retain their deterministic filtering, linkage, conflict, sequence, and hypothesis logic where I360 does not provide equivalent semantics.

## Tool conversion classes

### Endpoint-backed

- `search_events` and `semantic_search_events`: I360 item search.
- `get_objects`: item detail, entity detail, context, and media references.
- `aggregate_events`: I360 aggregate where semantics match; bounded application aggregation otherwise.
- location/entity resolution: place and entity search with canonical mapping.
- Agent inference: excluded from Part 1; Part 2 validates I360 `llm/chat` and retains Hermes as a fallback until parity acceptance.

### Retrieval replaced, reasoning retained

- `resolve_event_reference`
- `find_actor_history`
- `trace_identifier`
- `trace_semantic_clues`
- `find_related_events`
- `compare_location_claims`
- `challenge_hypothesis`
- `explain_linkage`
- `build_event_sequence`

These tools should request candidates through the provider and perform their current bounded reasoning over normalized results.

### Application-owned persistence

- investigations, memory, saved questions, and saved layers;
- target-candidate CRUD, duplicate detection, and evidence membership.

These require reviewed I360 entity schemas, actor visibility, update-conflict behavior, and deletion semantics. They can temporarily remain behind their current repositories while evidence reads move to I360.

## Key technical risks

- Search and aggregation semantics may differ from current exhaustive local behavior.
- Optional embeddings, geo clustering, place lookup, and signed media can vary by installation.
- I360 warnings and empty context responses can indicate incomplete retrieval rather than absence.
- Direct entity GET and search may enforce visibility differently.
- No exposed optimistic-concurrency contract has been established for mutable application records.
- Current code is concentrated in large server and MCP modules; adapter extraction must avoid broad refactoring.

## Required engineering gates

1. Contract tests against recorded I360 responses before wiring production code.
2. Live read-only proof with ordinary users before creating I360 schemas.
3. Architecture/security approval before identity forwarding or writable entity types.
4. Product and QA comparison of current versus I360-backed results before default-provider cutover.
