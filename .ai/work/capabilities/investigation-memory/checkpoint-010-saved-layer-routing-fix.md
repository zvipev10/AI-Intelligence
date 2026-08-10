# Checkpoint 010 — Saved-layer routing fix

## Status

Implemented and ready for VM deployment.

## Scope

- Add `present_saved_memory_layers` to the general Hermes deployment allowlist.
- Tell the general agent that a successful saved-layer presentation replaces the
  generic `present_requested_results` call for that request.
- Recover evidence-reference requests that specify an unsupported view by using
  a supported map or timeline view when the layer supports one.
- Keep automatic restoration of saved layers unchanged, per Product direction.

## Checks

- 16 MCP boundary tests passed.
- 18 agent-result-pipeline tests passed.
- Python compilation passed for the UI server, MCP server, and deployment script.
- Git whitespace validation passed.

## Deployment

Pending. Production files require a focused forward-port because their bilingual
baseline is newer than the repository copies.

