# Developer Review

Status: Ready for execution planning; explicitly delegated by the user.

## Approach

- Add a separate revision-keyed memory-update claim to scenario-run persistence.
- Trigger it from `/api/playback/next` only for non-baseline advances and non-empty memory.
- Run a separate general-agent background worker with saved memory and the released timeframe; exclude workstream context.
- Expose `memory_update` beside the existing `reevaluation` in playback status.
- Poll and render the result independently in chat.

## Constraints

- No shared claim, thread, status, input, or failure state with Moshe.
- Idempotency is scoped by scenario run/revision and investigation ID.
- Empty memory must avoid both claim creation and agent invocation.
- Generated output remains scenario-run state until the analyst explicitly saves it.

## Tests

- Claim/finish serialization and retry idempotency.
- Empty-memory skip.
- Parallel triggering with and without active workstreams.
- General-agent prompt/state excludes workstreams.
- Independent completion/failure paths.
- Client polling and one-time chat rendering.
