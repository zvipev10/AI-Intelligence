# Checkpoint 004 — Center welcome chat control

## Scope

Fix the welcome-page chat composer so its generic prompt-form margins cannot override its centered layout.

## Changes

- Increased the welcome composer selector specificity while preserving its existing width and vertical spacing.
- Advanced the stylesheet cache key to `styles.css?v=138`.
- Added a regression test for the selector and centered auto margins.

## Risk

Low. The selector targets only the welcome composer and does not change workspace composer behavior.

## Validation

- All 132 discovered POC tests pass.
- JavaScript syntax and Git diff checks pass.
- Local Edge geometry at 1440 px reports `left=360`, `right=1080`, and a center delta of `0`.
- Production deployment and browser verification remain pending.
