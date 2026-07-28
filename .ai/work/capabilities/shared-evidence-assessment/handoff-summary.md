# Handoff Summary

## Current state

The generic timeframe-stage playback foundation is implemented in checkpoint
014 and is pending Product approval. It is intentionally inactive: retrieval
filtering, UI controls, agent triggers, and deployment remain in later,
separately approved slices.

## Delivered in Slice 2

- non-persisting proposal and decision MCP tools;
- natural-language Moshe instructions and evaluation cases;
- bounded active-workstream context;
- structured proposal/action result-envelope fields;
- browser-memory proposal staging;
- distinct-later-turn confirmation;
- app-server-owned, independently validated artifact creation and revision;
- ordinary-chat success/conflict feedback with no new UX surface.
- workstream creation without mandatory layer selection;
- per-indication canonical source resolution and provenance;
- full active-artifact summary when the workstream indicator returns the workstream to chat.

## Validation

- 93 automated tests passed.
- Python compilation and `git diff --check` passed.
- Concurrent advances produce one successful transition and one revision
  conflict.
- Duplicate transition keys replay the original response and cannot be reused
  for another action.
- Existing workstream, artifact, routing, target catalog, and UI tests remain
  green.

## Accepted limitation

An unconfirmed proposal is lost on refresh. This is the explicitly approved MVP behavior; confirmed artifacts remain durable and revisioned.

## Next step

Review `checkpoint-014.md`. Do not begin Slice 2 retrieval visibility
enforcement until the Product owner explicitly confirms the next step.
