# Checkpoint 015 - Results table and query composer regression fix

## Date
2026-07-10

## Capability
Multi-Layer Query Filtering (`multi-layer-query-filtering`)

## Checkpoint status
Post-merge UI regression fix complete.

## Trigger
Product reported two regressions in the results table and requested a prompt-composer redesign:
- the horizontal results-table scrollbar was missing
- not all layer tabs were presented as expected
- the prompt area should look closer to a Codex text input, with plus and send-arrow controls under the text
- a pushable selected-layers component should appear under the text and reopen the layer-selection window

## What changed
- Results tabs now stay in one horizontal row and scroll instead of wrapping into the fixed-height header.
- The raw results table now has horizontal overflow enabled on all viewport sizes, with a stable wide table surface.
- The prompt composer is now a rounded Codex-style input:
  - text area on top
  - plus button under the text
  - up-arrow send button under the text
  - selected-layers pill under the text
- The selected-layers pill reflects the visible table layers that are sent as agent context.
- Clicking the selected-layers pill opens the layer-selection window.
- The layer-selection window now lists all open table-capable layers and uses checked state to decide which layers are selected/visible.
- Bumped cache versions:
  - `styles.css?v=74`
  - `app.js?v=97`

## Files changed
- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `.ai/work/capabilities/multi-layer-query-filtering/checkpoint-015.md`
- `.ai/work/capabilities/multi-layer-query-filtering/status.md`

## Validation
- JavaScript syntax:
  - bundled Node: `node.exe --check llm_investigation_orchestrator_serbia_poc/app.js`
- Local browser validation at `http://127.0.0.1:8768/`.
- Mobile viewport `390x844`:
  - composer controls render under the text
  - selected-layers pill opens the selection modal
  - five open layers produced five tabs
  - tabs strip overflow: `clientWidth 287`, `scrollWidth 934`, `overflow-x: auto`
  - table overflow: `clientWidth 346`, `scrollWidth 880`, `overflow-x: auto`
  - unchecking one layer changed the selected-layers pill from 5 to 4 selected layers
- Desktop viewport `1366x900`:
  - five open layers produced five tabs
  - table overflow: `clientWidth 979`, `scrollWidth 1139`, `overflow-x: auto`
  - tabs strip overflow remained `overflow-x: auto`
- Browser console check:
  - no warnings or errors reported.

## Not completed
- VM deployment was not performed in this checkpoint.
- No automated visual regression test was added; validation was manual browser automation against the local app.

## Risk
- The selected-layers pill intentionally follows the existing selected-layer context model: visible table-capable layers are the selected layers sent to the agent.
- Hiding a table layer from the selection modal removes it from the selected-layer prompt context while keeping the tab available as an open layer.

## Recommendation
Product/UX should review the composer visual treatment on the review environment after deployment.
