# [Developer Review] Shared Agent Backend and Presentation Refactor

## Purpose

Review the Product-approved requirement that General and Moshe share Hermes invocation, result normalization, layer construction, and frontend presentation modules.

## Required action

Inspect the current server request handler, nested normalization helpers, frontend `applyHermesResult()`, and shared layer state. Propose extraction boundaries, interfaces, regression coverage, and implementation slices without modifying product code.

## Owner role

Development

## Inputs

- `chapter-002-agent-routing-and-presentation.md`
- `capability-brief.md`
- Existing `server.py`, `app.js`, and Serbia MCP tool result contracts

## Expected output

Updated `developer-review.md` covering the expanded architecture and a recommendation for execution planning.

## Blocking

Blocks execution planning and Moshe implementation.

## Completion criteria

- [x] Shared agent router and Hermes client architecture approved.
- [x] Shared result envelope direction approved.
- [x] Generic frontend agent-result path and attribution approved.
- [x] `attack_targets` as a shared layer kind approved.
- [ ] Exact normalization extraction boundaries remain for execution planning.
- [ ] Regression test strategy requires QA review.

## Related artifacts

- `.ai/work/capabilities/moshe-attack-targets/chapter-002-agent-routing-and-presentation.md`
- `.ai/work/capabilities/moshe-attack-targets/status.md`

## Parent capability

Moshe Attack Targets MVP; remote parent issue pending.
