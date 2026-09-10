# Execution Plan

## Gate
Product, developer, UX, and QA decisions are approved under explicit end-to-end delegation.

## Slice 1
Add deterministic bounded record coordinates to the UI event loading contract and unit tests.

## Slice 2
Render raw events at their record coordinates, connect MIL-STD observations to the same coordinates, retain canonical organization placement, and add approximate-position labels.

## Slice 3
Run full QA, publish the PR, deploy with rollback, smoke-test, merge, and close the capability.

## Rollback
Revert the isolated server/client changes or restore the prior VM static files. No stored-data migration is required.

