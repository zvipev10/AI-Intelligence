# Checkpoint 010 — Saved-layer routing fix

## Status

Implemented, published, deployed, and production-verified.

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

The focused changes were forward-ported onto the newer bilingual production
baseline.

- Published commit: `97250f1` on `codex/investigation-memory-layer-presentation`.
- Updated `/opt/serbia-poc-ui/server.py`,
  `/opt/serbia-poc/mcp_server/server.py`, and
  `/home/ubuntu/.hermes/config.yaml`.
- General Hermes and UI services are active with zero automatic restarts.
- General Hermes registered 19 Serbia tools, including
  `mcp_serbia_events_poc_present_saved_memory_layers`.
- Rollback backup:
  `/opt/serbia-poc-ui-backups/saved-layer-routing-20260810T174056Z`.

## Production smoke

Prompt: `תראה לי את השכבה השמורה של טיקטוק`

- Run: `run_eb1f72cf96d4482a82c1948d97fc1d70`.
- Tools used: `classify_question_intent`, then
  `present_saved_memory_layers`.
- Returned one `present` action for
  `layer_20260810_171537_e94d77`.
- Returned zero generic requested-result layers and zero evidence-reference
  layers.
- The presentation endpoint fully restored all 1,092 saved TikTok events with
  zero missing IDs.
