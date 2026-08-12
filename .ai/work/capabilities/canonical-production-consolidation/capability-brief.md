# Capability Brief — Canonical production consolidation

## Goal

Make the source currently represented by the exact production v162 snapshot the
single canonical application source in the package root, without modifying the
deployed VM.

## Acceptance criteria

- The package-root application files are byte-identical to the captured v162
  production files before any test-only changes.
- There is no second editable application source tree under `deployment/`.
- The repository tests validate the v162 behavior rather than the superseded
  variant.
- JavaScript, Python, and repository regression checks pass.
- No command writes to, restarts, or deploys the VM.

## Scope

Canonical source files, tests that encode the superseded implementation, the
production hash manifest, and repository documentation.

## Non-goals

Deployment, VM changes, runtime-data changes, feature changes, or refactoring
the captured production implementation.

## Assumptions

The user's instruction to consolidate now authorizes replacing the superseded
canonical implementation and updating its tests. Production v162 behavior is
the accepted product contract.
