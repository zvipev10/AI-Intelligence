# Execution Plan

## Prerequisite gate

- Product direction: approved by the user's `Deploy it` instruction on 2026-08-09.
- Developer review: ready for execution (`developer-review.md`).
- UX review: ready for execution (`ux-review.md`).
- QA/Security review: ready for execution (`qa-review.md`).

## Slice 1 — Evidence-first creation instructions

1. Update persistent Moshe guidance.
2. Update server-injected Moshe guidance.
3. Update the creation tool description.
4. Add regression assertions and evaluation cases.
5. Run focused profile, workstream, target-boundary, syntax, and diff checks.
6. Deploy with backup, restart Moshe/UI services, and verify health plus installed contracts.

## Rollback

Restore the deployment backup produced by the existing workstream deployment script and restart the
Moshe and UI services.

## Review gate

Stop and report if tests, deployment verification, or service health fail.
