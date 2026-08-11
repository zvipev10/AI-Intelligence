# Handoff Summary

## Current state

Implementation and deployment are current through checkpoint 018. The playback run, visibility
boundary, status, mode, reset, and Next transition now share one global scope.
Switching investigations preserves and advances the existing run instead of
attempting to create a conflicting run. Investigation-scoped workstream state
remains separate from this global scenario clock. The correction is live on the
locale-aware VM build and pending Product/QA hands-on acceptance.

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

- Checkpoint 018 focused scenario playback suite: 16 tests passed.
- Checkpoint 018 full Python discovery: 132 tests passed.
- Checkpoint 018 cross-investigation regression confirms one run advances to
  revision 2 and no second run is created.
- Production smoke confirmed different investigation IDs return the same global
  run ID/revision, both services are active, and public arrow assets are correct.
- Rollback backup: `/home/ubuntu/deploy-backups/global-playback-arrow-20260811T160526Z`.
- Checkpoint 017 focused JavaScript/API/playback suite: 45 tests passed.
- Checkpoint 017 full discovery: 113 tests passed.
- JavaScript syntax and `git diff --check` passed for checkpoint 017.
- Public `app.js?v=131` matches the committed SHA-256; Hermes is configured on
  V2.1 with 14,800 rows and all three services are active.
- 95 automated tests passed.
- Python compilation and `git diff --check` passed.
- Search, semantic, aggregate, related-event, direct-object, presentation, and
  fusion paths share one fail-closed playback boundary.
- Concurrent advances produce one successful transition and one revision
  conflict.
- Duplicate transition keys replay the original response and cannot be reused
  for another action.
- Existing workstream, artifact, routing, target catalog, and UI tests remain
  green.

## Accepted limitation

An unconfirmed proposal is lost on refresh. This is the explicitly approved MVP behavior; confirmed artifacts remain durable and revisioned.

## Next step

Review `checkpoint-018.md` in the live UI and verify Next after switching
investigations plus the collapsed workstream arrow direction. Then complete the
outstanding checkpoint 017 and checkpoint 016 acceptance work.
