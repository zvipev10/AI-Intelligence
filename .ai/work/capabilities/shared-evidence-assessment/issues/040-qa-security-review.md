# QA/Security Review - Shared Evidence Assessment

## Purpose

Define integrity, provenance, permissions, recovery, and regression requirements for shared human-agent artifact writes.

## Owner role

QA / Security

## Inputs

- `../capability-brief.md`
- Approved Product review
- Developer/architecture draft when available

## Required action

Define state-transition tests, immutable-history expectations, raw-reference integrity, duplicate/stale contribution behavior, partial-write recovery, agent permission boundaries, and regression coverage.

## Expected output

`qa-review.md` with security gates and an executable validation strategy.

## Blocking relationship

Blocks execution planning and implementation authorization.

## Completion criteria

- Contribution-state and revision invariants are testable.
- Failure and recovery behavior are defined.
- Agent write boundaries are reviewable.
- Existing product regression surface is covered.
