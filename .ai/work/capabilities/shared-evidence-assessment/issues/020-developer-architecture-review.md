# Developer/Architecture Review - Staged Scenario Replay

GitHub issue: #27; parent: #25

## Purpose

Approve a feasible replay visibility boundary, shared state, workstream persistence, and bounded automatic agent-run model.

## Owner role

Development / Architecture

## Inputs

- `../capability-brief.md`
- `../developer-review.md`
- Existing UI event loading, MCP retrieval/indexes, Moshe routing, target bank, and semantic search

## Required action

Review the draft, enumerate all retrieval paths, choose global versus request-scoped replay state, and approve atomic stage/run revision behavior.

## Expected output

Human approval or requested changes recorded in `../developer-review.md`.

## Blocking relationship

Blocks execution planning.

## Completion criteria

- Future-record visibility enforcement is complete and testable.
- Persistence, concurrency, and stale-run behavior are explicit.
- Workstream, memory, target DB, and replay-state boundaries are explicit.
- Proposed implementation slices are feasible.
