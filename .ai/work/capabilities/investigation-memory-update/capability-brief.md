# Capability Brief

## Capability name

Investigation memory update on time-slice progression

## User problem

Time-slice progression currently produces Moshe assessments for active workstreams, but it does not produce an investigation-level synthesis grounded in the investigation's saved memory.

## Proposed behavior

After a real-time slice advances, a general agent generates one investigation update using the current investigation memory as its primary context. The update is separate from Moshe's specialist workstream updates.

The first slice should produce a read-only update containing:

- what changed since the previous slice;
- how the new situation relates to saved findings and layers;
- confirmations and contradictions;
- intelligence gaps;
- suggested next questions or actions;
- explicit evidence and memory references.

## Recommended orchestration

1. Advance the time slice and release the new data window.
2. Run Moshe's existing workstream reevaluations.
3. Load the investigation memory and current workstream presentation summaries.
4. Run the general agent as an investigation synthesizer.
5. Present the result as a distinct “Investigation update” in the conversation/activity UI.
6. Let the analyst explicitly save the update to investigation memory; do not auto-write memory in the first slice.

## Why this boundary

- Moshe remains responsible for targets and workstream artifacts.
- The general agent synthesizes across the investigation rather than modifying specialist work.
- Human confirmation prevents generated summaries from recursively becoming trusted memory without review.
- Running after specialist updates lets the general synthesis include their latest conclusions.

## Inputs

- investigation ID and locale;
- scenario run ID, revision, and newly released timeframe;
- saved chat summaries;
- saved memory layers, filters, counts, and sample evidence IDs;
- current active-workstream presentation summaries;
- optionally, the previous generated investigation update for delta comparison.

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
- `workstream_references[]`
- `no_material_change`

## Trigger and ordering recommendation

Trigger once per successful time-slice revision, after Moshe has completed or failed. A Moshe failure should not block the general update; the output should disclose unavailable specialist context.

## Persistence and idempotency

- Store the generated update with the scenario run/revision, not directly inside trusted investigation memory.
- Use `(investigation_id, scenario_run_id, revision)` as the idempotency key.
- Provide an explicit analyst action to save an accepted update as a chat-summary memory item.

## Empty-memory behavior

If investigation memory has no saved summaries or layers, do not pretend to be memory-grounded. Either skip with a clear reason or generate a visibly labeled baseline update from current workstreams and the new slice. Product must choose which behavior is preferred.

## Non-goals for the first slice

- Automatically changing workstreams or target-bank records.
- Automatically writing generated content back into trusted investigation memory.
- Replacing Moshe's specialist reevaluation.
- Broad, unconstrained rediscovery of historical events.

## Acceptance criteria

- One general-agent update is generated at most once per time-slice revision.
- The update uses saved investigation memory and identifies its memory references.
- Moshe and general-agent outputs are visually and semantically distinct.
- The update does not mutate workstreams, targets, or trusted memory.
- Failures are isolated: Moshe failure does not prevent synthesis, and synthesis failure does not undo the slice advance.
- The analyst can explicitly save an accepted update to memory.
- No-material-change output is concise and does not invent developments.

## Open product decisions

1. Should empty memory cause a skip, or a labeled baseline update?
2. Should the update appear only in chat, or also as an investigation-level activity card?
3. Should generation wait for all specialist workstreams or use a bounded timeout and disclose pending work?

## Main risks

- Recursive contamination if generated updates are automatically fed back into trusted memory.
- Unsupported synthesis if memory references are not preserved in the output.
- Latency when multiple workstreams must finish before the general update starts.
- Duplicate updates after retries unless revision-level idempotency is enforced.
