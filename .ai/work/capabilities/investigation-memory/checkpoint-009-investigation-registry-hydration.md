# Checkpoint 009 — Investigation registry hydration

## Status

Implemented, published, and deployed for Product validation.

## Problem

The investigation selector was populated only from browser `localStorage`. A
server-backed investigation therefore disappeared from the UI when its local
registry entry was absent, even though `/api/investigations` and its saved
memory remained intact.

## Change

- Fetch `/api/investigations` during application boot.
- Merge server-backed investigations into the local selector registry by stable
  investigation ID, with normalized name as a fallback.
- Preserve browser-only investigations and the active selection.
- Persist the merged registry locally and continue booting if hydration fails.
- Use the locale-aware API URL in the bilingual production asset.

## Checks

- JavaScript syntax check passed for the repository and production-forward-port
  assets.
- Git whitespace validation passed.

## Deployment

- Published commit: `53f1047` on `codex/investigation-memory-layer-presentation`.
- Forward-ported the focused change onto the current bilingual production asset.
- Public cache version: `app.js?v=150`.
- Updated only `app.js` and `index.html`.
- `serbia-poc-ui.service` is active with zero automatic restarts.
- The deployed and staged asset hashes match.
- Hebrew and English `/api/investigations` responses both contain `KFOR involvement`
  with two chat summaries and one saved layer.
- Rollback backup:
  `/opt/serbia-poc-ui-backups/investigation-registry-hydration-20260810T161001Z`.

## Remaining validation

Product should refresh the app, open the investigation selector, and confirm
that `KFOR involvement` is visible and opens its saved memory.
