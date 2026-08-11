# Execution Plan

## Review gate

- Product/UX behavior: approved by explicit user input.
- Developer review: ready for planning.
- QA review: ready for planning.

## Slice 1 — Typed recording persistence

- Extend metadata/load/create validation for legacy investigation recordings and
  structured workstream-message recordings.
- Allow duplicate saves by generating independent saved IDs.
- Add API unit tests for both workstream message types and malformed payloads.

## Slice 2 — Save and replay UI

- Share structured renderers between live and replayed workstream messages.
- Add existing-style Save recording controls to creation and detail messages.
- List typed entries in the existing modal and replay them read-only.
- Preserve existing recording behavior and add static/behavioral regression tests.

## Validation

Focused recording/workstream tests, full Python discovery, JavaScript syntax,
Python compilation, diff checks, and hands-on localized replay verification.

## Rollback

Legacy records remain readable. Deployment backs up adapted runtime files before
replacement and rolls back on service or smoke-test failure.
