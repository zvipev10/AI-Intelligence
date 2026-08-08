# Developer Review

## Status
Ready for planning; user delegated execution by asking Codex to start from the supplied plan.

## Findings
- Latest `main` contains an isolated English WIP with localized assets and substantial server/UI work.
- The canonical Hebrew workspace does not contain `.en` projections and its MCP server has no locale-aware state.
- Copying the WIP wholesale would overwrite newer canonical behavior and preserve duplication.

## Recommended approach
Use the plan's Option A: add optional `locale` to the MCP tool contract and maintain per-locale immutable runtime caches. Port reviewed WIP changes into the canonical workspace by concern, with Hebrew as fallback.

## Likely affected areas
`data/`, `mcp_server/server.py`, `server.py`, `app.js`, `index.html`, `help.html`, `styles.css`, and focused tests.

## Risks
- Module globals currently bind all tools to one dataset.
- Semantic caches must be keyed by locale and dataset version.
- Some MCP heuristics are Hebrew-specific and may need bilingual marker sets.
- English WIP diverged from canonical mainline after it was copied.

## Test strategy
Schema checks, locale fallback tests, Hebrew/English retrieval assertions, semantic cache isolation, server request locale propagation, UI string/direction regression tests, and existing suites.

## Proposed slices
1. Assets and MCP locale runtime.
2. Prompt/routing.
3. UI merge.
4. Full regression and manual QA.

## Checkpoint 007 refinement
For inspection findings 1 and 4, use a manifest-validated `DatasetRuntime` registry rather than adding more parallel globals. Separate semantic cache identity by locale and checksum. Split workstream persistence physically by locale, treat untagged legacy records as Hebrew, and start English empty. Do not implement translation or migration in these slices.
