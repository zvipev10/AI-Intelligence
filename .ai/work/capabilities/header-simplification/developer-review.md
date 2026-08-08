# Developer Review

## Capability

Compact upper-section controls

## Review status

Draft - pending human approval

## Reviewer / input source

AI-prepared draft based on repository inspection; not human-approved.

## Context reviewed

`llm_investigation_orchestrator_serbia_poc/index.html`, `styles.css`, and status logic in `app.js`.

## Product requirements understood

Reduce header density, compact the language selector to `E`/`ע`, and convert verbose service statuses into concise indicators with on-demand details.

## Feasibility

The existing status DOM and runtime updates are straightforward to restyle and enrich accessibly. Language-switch feasibility cannot be finalized because no switch/state was found locally.

## Likely affected files/services

- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- No backend change unless true DB connectivity is not present in `/api/status`.

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

No data/API changes for visual compaction. A separate DB status requires confirmation that `/api/status` supplies it.

## Test strategy

DOM/state tests if available, plus manual checks for loading/success/error/local-demo, keyboard focus, touch/click, RTL/LTR, and responsive layout.

## Proposed execution slices

1. Confirm service semantics and locate language state.
2. Implement compact controls and accessible detail behavior.
3. Validate all state transitions and responsive/accessibility behavior.

## Required review gates before coding

Human approval of UX interaction and service terminology, followed by an execution plan.

## Blocking questions before execution planning

- Which source/branch contains the current English/Hebrew switch?
- Does “DB connection” mean the current loaded dataset state or a distinct backend database health signal?
