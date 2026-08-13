# Checkpoint 001 — Draft conversion lifecycle

## Summary

Implemented the approved draft-investigation lifecycle without backend schema changes.

## Changes

- Draft exploration now uses a fresh ephemeral ID without adding or registering an investigation.
- Draft startup does not load investigation memory, workstreams, or playback.
- The header replaces normal investigation/team controls with one `Create investigation` button.
- A compact bilingual modal requires a unique name and reuses the welcome-page participant/avatar display.
- Creation registers the same ephemeral ID, adds the normal investigation record, restores all regular participants, and preserves chat/results/layers.
- Layer and message/result investigation-memory saves open the same modal and resume exactly once after creation.
- Workstream creation is hidden during draft exploration.
- Advanced assets to `app.js?v=168` and `styles.css?v=139`; added v169 manifest.

## Validation

- All 133 discovered POC tests pass.
- JavaScript syntax and Git diff checks pass.
- Local Edge smoke confirms draft-only header, hidden normal panels, five welcome-style participant avatars, conversion, restored normal controls, five regular participant buttons, and the saved name.

## Review

Product/UX/QA should review before deployment. No production change was made.
