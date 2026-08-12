# Execution Plan

## Prerequisite gate

- Product decisions approved by the user.
- Developer, UX, and QA reviews are ready.
- No architecture, permission, or data-model migration is required.

## Slice 1 — Persistent independent job state

Add revision-keyed claim/finish functions and playback response serialization for `memory_update`.

## Slice 2 — General-agent worker and trigger

Skip empty memory; otherwise trigger a general-agent background worker using saved memory and the newly released timeframe, with no workstream inputs or dependencies.

## Slice 3 — Chat polling and presentation

Poll independently from Moshe, show localized processing/result/failure messages only in chat, and prevent duplicate rendering per page session.

## Slice 4 — Validation and release

Run full tests and browser smoke checks, deploy targeted changed application files with rollback backup, verify production, merge and push `main`.

## Rollback

Restore the prior application files. Scenario files tolerate the additional private `_memory_updates` field; no migration is required.
