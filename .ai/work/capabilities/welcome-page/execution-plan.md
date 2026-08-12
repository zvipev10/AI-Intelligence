# Execution Plan

## Prerequisite gate

- Product: approved by user on 2026-08-12.
- Development: `developer-review.md`, ready.
- UX: `ux-review.md`, ready.
- QA: `qa-review.md`, ready.
- Baseline: `origin/main` at `340df4b`, byte-identical to production v162 assets.

## Implementation approach

Add a localized welcome view above the existing workspace, render the real investigation from current registry/team state, render mocked metadata/recommendations, and switch views in memory. Preserve current boot behavior and resize MapLibre after reveal.

## Data/API changes

None. All new supporting data and actions are explicitly mocked.

## Execution slices

1. Add markup/styles and view state for welcome, real investigation, same-page entry, and return.
2. Add participant/demo modal and similar-investigation actions.
3. Add automated contract coverage and browser regression checks.

## Rollback

Remove the welcome markup/styles/hooks and restore the workspace as the initial visible view. No stored or server data migration is involved.
