# Checkpoint 009 — Investigation registry hydration

## Status

Implemented and ready for VM deployment.

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

Pending.

