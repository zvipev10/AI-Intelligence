# Checkpoint 011 — Saved-filter visibility

## Status

Implemented and ready for VM deployment.

## Problem

Restored saved filters were applied internally, but the filter panel remained
closed. The layer could therefore look unfiltered even though its funnel state
and row filtering had been restored. A saved field not present in the
reconstructed row schema could also disappear from the filter-field selector.

## Change

- Open the active layer's filter panel automatically when restored saved filters
  exist.
- Keep a saved filter field visible and selected even when the reconstructed row
  schema does not currently advertise that field.
- Keep automatic layer restoration unchanged.

## Checks

- JavaScript syntax check passed.
- All 29 focused UI regression tests passed.
- Git whitespace validation passed.

## Deployment

Pending explicit deployment authorization.

