# Execution Plan

## Status and gate
Approved for execution by explicit user instruction on 2026-09-10. Product, developer, UX, and QA reviews are ready under delegated authority.

## Slice 1 — semantic model and visual adapter
Add a versioned mapping registry, record classification, organization-presence grouping, UAV observation descriptors, accessible MIL-STD marker renderer, and legend. Keep the implementation within the canonical static client.

## Slice 2 — viewer integration and confidence
Connect organization symbols to organization details and observation symbols to raw records. Present claim state, evidence count/time, and uncertainty without changing affiliation semantics.

## Slice 3 — QA, review, release
Run focused and regression checks, document checkpoints and durable architecture decisions, publish a draft PR, resolve findings, deploy to the VM, smoke-test, merge, and close issues.

## Likely files
`app.js`, `styles.css`, `index.html`, focused Python contract tests, deployment manifest/readme, capability artifacts, and durable architecture/decision notes.

## Rollback
Restore the prior static app files from the VM backup or revert the isolated feature commits. No stored-data migration is involved.

