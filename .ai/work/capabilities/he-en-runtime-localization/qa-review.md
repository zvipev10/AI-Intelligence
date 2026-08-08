# QA Review

## Status
Ready for planning.

## Happy paths
- Omitted locale returns Hebrew data.
- `locale="he"` returns Hebrew data and metadata.
- `locale="en"` returns English data and metadata.
- Switching the UI updates text, number/date formatting, document direction, and subsequent API requests.

## Negative and edge cases
- Unknown locale falls back to Hebrew.
- Missing English asset fails safely without mixing partial locales.
- Alternating Hebrew/English calls do not leak cached data.
- Recorded and live responses use the requested locale.
- Existing saved investigations without a locale continue to open in Hebrew.

## Regression areas
All current MCP tools, semantic search/indexing, playback visibility, saved/recorded questions, workstreams, map/timeline/table layers, and Hebrew RTL layout.

## Automation
Extend MCP tests and benchmark inputs for both locales; add request-routing and UI static regression assertions; run existing Python suites.

## Acceptance recommendation
Continue slice-by-slice. Pause after any public tool-schema, prompt contract, or UI behavior checkpoint for review evidence.

## Checkpoint 007 additions
- Scan every English MCP payload, not only UI layer responses.
- Test missing/corrupt English manifests fail closed.
- Test exact, fusion, and semantic calls under alternating locales.
- Exercise the full workstream lifecycle and nested document validation in both locales.
- Assert cross-locale workstream IDs return not found and cannot mutate another store.
- Re-run the complete checkpoint-004 production inspection before acceptance.
