# Issue 81 — Playback retrieval visibility

## Purpose

Enforce the active scenario stage as the authoritative evidence boundary across
all retrieval and presentation paths.

## Owner role

Development/Architecture and QA/Security.

## Inputs

- `playback-execution-plan.md`
- approved checkpoint 014
- active scenario run state

## Expected output

- server-owned visibility policy;
- retrieval, aggregation, semantic, expansion, object, presentation, and fusion
  enforcement;
- leakage and inactive-playback regression tests;
- checkpoint 015.

## Completion criteria

- unreleased events cannot be returned or indirectly summarized;
- inactive playback preserves existing behavior;
- malformed or mismatched active policy fails closed;
- full test discovery passes;
- code and artifacts are published;
- Product owner approves proceeding to Slice 3.
