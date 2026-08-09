# Checkpoint 002 — Main-based validation deployment

## Status

Deployed for user validation on 2026-08-09. Branch remains unmerged.

## Deployment method

Applied only the intended workstream changes to the current production baseline:

- context-applied the Moshe runtime instruction hunk to the current UI `server.py`;
- context-applied the persistent instruction hunk to Moshe's installed `SOUL.md`;
- additively merged main's missing workstream MCP functions, tool schemas, and handlers into the newer
  production MCP server while preserving its bilingual/classification functionality.

No HTML, JavaScript, CSS, result pipeline, artifact implementation, data, or workstream state was
replaced.

## Rollback

Exact pre-deployment backup:

`/opt/serbia-poc-ui-backups/workstream-simplification-main-20260809T132901Z`

It contains the previous UI server, MCP server, Moshe profile, and Moshe configuration.

## Verification

- UI service: active
- Moshe service: active
- Locale-aware v2.1 health endpoint: 200, 14,800 rows
- UI and MCP Python compilation: pass
- Evidence-first UI instruction: present
- Ordinary-chat/playback boundary: present
- All three workstream MCP tools and handlers: present
- Newer bilingual MCP marker `looks_english`: preserved
- Installed Moshe profile and tool allowlist: present
- Public root: 200

## Live target smoke

- Prompt: `@משה צור מעקב אחר TGT-F2CA47CB9859`
- Investigation: `main-simplification-smoke-1786282171482`
- Workstream: `ws_20260809_133013_d8da9a35`
- Result: created in one turn with inferred title, objective, and responsibility; no metadata question.

## Live raw-record smoke

- Prompt: `@משה צור מעקב אחר REC-V2-000001`
- Investigation: `main-simplification-raw-smoke-1786282227572`
- Workstream: `ws_20260809_133133_7e0f903a`
- Tool sequence: `classify_question_intent`, `search_target_candidates`, `search_events`,
  `prepare_target_candidate`, `prepare_workstream_creation`, `present_requested_results`
- Result: created in one turn with inferred fields.
- Target safety: no target create/update tool was called.

## Merge status

Do not merge until the user completes product validation.
