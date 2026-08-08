# Final Result Auto-Visualization

Status: Approved for implementation by explicit user delegation on 2026-08-08.

## Problem

Agent final answers currently render in chat, but their structured result layers are only presented automatically in the restore-only path. Live, continued, and recorded results require a separate manual action.

## Expected behavior

- Every agent final result uses the shared result pipeline.
- Structured final-result layers become visible automatically.
- The UI opens the agent-selected `map` or `timeline` view.
- Missing or unsupported recommendations fall back deterministically to a compatible map/timeline view.
- Research steps remain collapsed by default and individually expandable.

## Non-goals

- Changing agent routing, tool execution, data contracts, or evidence-reference visibility.
- Automatically showing supporting evidence-reference layers.

## Acceptance criteria

1. Live, continuation, recorded, and restore-only results share one presentation function.
2. `recommended_view: timeline` activates timeline; `map` activates map.
3. An unsupported/missing view resolves from layer capabilities, then falls back to map.
4. Final layers are visible and query context reflects the final answer.
5. Existing collapsed-step tests and focused result-pipeline tests pass.

