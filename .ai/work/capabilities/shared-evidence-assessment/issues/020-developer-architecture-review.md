# Developer/Architecture Review - Shared Evidence Assessment

## Purpose

Define a feasible persistence, API, revision, and bounded agent-write model.

## Owner role

Development / Architecture

## Inputs

- `../capability-brief.md`
- Approved Product review
- Existing investigation memory, Moshe routing, target bank, and typed-layer implementation

## Required action

Evaluate schemas, API boundaries, atomic contribution writes, stale-run protection, raw-reference refetching, identity limitations, and implementation slices.

## Expected output

`developer-review.md` with recommendation, risks, tests, and review gates.

## Blocking relationship

Blocks execution planning.

## Completion criteria

- Recommended persistence and revision model is explicit.
- Agent-write authority and stale-run behavior are explicit.
- Reuse versus separation from investigation memory is explicit.
- Testable implementation slices are proposed.
