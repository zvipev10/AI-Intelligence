# Developer Review

## Capability

Compact upper-section controls

## Review status

Draft - pending human approval

## Reviewer / input source

AI-prepared draft based on repository inspection; not human-approved.

## Context reviewed

Latest `main`, including the bilingual WIP app's `index.html`, `styles.css`, and `app.js`.

## Product requirements understood

Reduce header density, compact the language selector to `E`/`ע`, and convert verbose service statuses into concise indicators with on-demand details.

## Feasibility

The existing status DOM and runtime updates are straightforward to restyle and enrich accessibly. The switch exists as `#languageToggle`, with full labels adjacent to its track.

## Likely affected files/services

- `llm_investigation_orchestrator_serbia_poc_english_wip_20260806_0718/index.html`
- `llm_investigation_orchestrator_serbia_poc_english_wip_20260806_0718/styles.css`
- `llm_investigation_orchestrator_serbia_poc_english_wip_20260806_0718/app.js`
- No backend/API change.

## Existing patterns to follow

The header already uses dynamic text nodes and state classes (`ready`, `agent-live`, `agent-error`) driven by `/api/status` and dataset loading.

## Implementation options

### Option 1

CSS tooltip with focus support and full status text retained in the DOM. Lowest complexity, but tap behavior is limited.

### Option 2

Small button-triggered popovers that open on hover/focus and toggle on tap. Slightly more JavaScript, with better cross-input behavior.

## Recommended approach

Use compact button-like status indicators with a small anchored detail surface and retain the existing text IDs as visually hidden dynamic descriptions. Prefer native popover only if browser support matches the deployment target; otherwise use a minimal reusable DOM pattern.

## Technical risks

- Renaming dataset availability to database connectivity would misrepresent the current signal.
- Dynamic class updates currently target text and dot elements separately and should be normalized carefully.
- Language direction changes could affect the full page, not only the switch.

## Data/API considerations

No data/API changes. The first compact indicator continues to represent dataset load status and count/version detail.

## Test strategy

DOM/state tests if available, plus manual checks for loading/success/error/local-demo, keyboard focus, touch/click, RTL/LTR, and responsive layout.

## Proposed execution slices

1. Implement in-track `E`/`ע` labels and compact status markup/styles.
2. Preserve dynamic dataset/Hermes detail updates and add accessible hover/focus/tap behavior.
3. Validate all state transitions and responsive/accessibility behavior.

## Required review gates before coding

Human approval of UX interaction and service terminology, followed by an execution plan.

## Blocking questions before execution planning

- None on source location or dataset semantics; both are confirmed.
