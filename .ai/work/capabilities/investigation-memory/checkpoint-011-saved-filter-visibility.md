# Checkpoint 011 — Saved-filter visibility

## Status

Implemented, published, deployed, and ready for Product validation.

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

- Forward-ported the focused change onto the current bilingual production asset.
- Updated only `app.js` and `index.html`.
- Production cache version: `app.js?v=151`.
- Local staging and deployed file hashes match.
- `serbia-poc-ui.service` is active with zero automatic restarts.
- Hebrew v2.1 status reports 14,800 rows.
- Rollback backup:
  `/opt/serbia-poc-ui-backups/saved-filter-visibility-20260810T175132Z`.

## Review request

Restore a saved layer with applied filters and confirm that the filter panel
opens with the saved field/value chips visible.
