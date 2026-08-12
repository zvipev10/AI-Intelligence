# Capability Brief

## Capability name

Investigation memory update on time-slice progression

## User problem

Time-slice progression currently produces Moshe assessments for active workstreams, but it does not produce an investigation-level synthesis grounded in the investigation's saved memory.

## Proposed behavior

After a real-time slice advances, a general agent generates one investigation update using the current investigation memory as its primary context and the newly released slice as the source of potential change. This flow is fully independent of Moshe and all workstream-update processing.

The first slice should produce a read-only update containing:

- what changed since the previous slice;
- how the new situation relates to saved findings and layers;
- confirmations and contradictions;
- intelligence gaps;
- suggested next questions or actions;
- explicit evidence and memory references.

## Recommended orchestration

1. Advance the time slice and release the new data window.
2. Check whether the investigation has saved memory; if it is empty, do nothing.
3. Independently load the investigation memory and run the general agent against the newly released slice.
4. Present the result as a distinct “Investigation update” in chat only.
5. Let the analyst explicitly save the update to investigation memory; do not auto-write memory in the first slice.

## Why this boundary

- Moshe remains responsible for targets and workstream artifacts.
- The general agent synthesizes across the investigation without reading, waiting for, modifying, or reporting the status of specialist work.
- Human confirmation prevents generated summaries from recursively becoming trusted memory without review.
- Independent execution isolates latency and failures between the general investigation update and workstream processing.

## Inputs

- investigation ID and locale;
- scenario run ID, revision, and newly released timeframe;
- saved chat summaries;
- saved memory layers, filters, counts, and sample evidence IDs;
- optionally, the previous generated investigation update for delta comparison.

Workstream records, workstream presentations, Moshe results, and target-bank state are explicitly excluded inputs.

## Output contract

The agent should return structured data rather than only prose:

- `summary`
- `changes[]`
- `confirmations[]`
- `contradictions[]`
- `gaps[]`
- `suggested_actions[]`
- `evidence_ids[]`
- `memory_references[]`
- `no_material_change`

## Trigger and ordering recommendation

Trigger once per successful time-slice revision as an independent job. It must not wait for, poll, consume, or disclose Moshe/workstream-update state. Either job may succeed or fail without affecting the other.

## Persistence and idempotency

- Store the generated update with the scenario run/revision, not directly inside trusted investigation memory.
- Use `(investigation_id, scenario_run_id, revision)` as the idempotency key.
- Provide an explicit analyst action to save an accepted update as a chat-summary memory item.

## Empty-memory behavior

If investigation memory has no saved summaries or layers, do nothing: do not start the agent, create a chat message, or create a stored update record.

## Non-goals for the first slice

- Automatically changing workstreams or target-bank records.
- Automatically writing generated content back into trusted investigation memory.
- Replacing Moshe's specialist reevaluation.
- Reading or incorporating workstream updates, presentations, or target-bank state.
- Broad, unconstrained rediscovery of historical events.

## Acceptance criteria

- One general-agent update is generated at most once per time-slice revision.
- The update uses saved investigation memory and identifies its memory references.
- The update appears in chat only and is labeled as a general investigation update.
- The update does not mutate workstreams, targets, or trusted memory.
- The general update neither waits for nor consumes workstream processing.
- Failures are isolated: either update path may fail without affecting the other or undoing the slice advance.
- Empty investigation memory produces no agent run, chat message, or update record.
- The analyst can explicitly save an accepted update to memory.
- No-material-change output is concise and does not invent developments.

## Approved product decisions

1. Empty investigation memory produces no action.
2. The update appears only in chat.
3. General-agent generation is fully independent of workstream updates: no waiting, no workstream inputs, and no shared failure state.

## Main risks

- Recursive contamination if generated updates are automatically fed back into trusted memory.
- Unsupported synthesis if memory references are not preserved in the output.
- Concurrent general and specialist agent jobs may compete for runtime capacity unless execution limits are defined.
- Duplicate updates after retries unless revision-level idempotency is enforced.
