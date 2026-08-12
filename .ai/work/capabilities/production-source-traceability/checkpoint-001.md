# Checkpoint 001 — Exact VM source snapshot

## Summary

Captured the exact non-secret top-level source files from the active VM into
`llm_investigation_orchestrator_serbia_poc/deployment/vm-production-v162/`.

## Safety

The VM was accessed read-only. No files were uploaded, moved, edited, or
deleted, and no service was restarted.

## Provenance

- VM: `151.145.93.180`
- Runtime path: `/opt/serbia-poc-ui`
- Public asset version: `app.js?v=162`
- Capture date: 2026-08-12
- File hashes: `SHA256SUMS.txt`

## Exclusions

Secrets, datasets, investigation/workstream state, scenario runs, recordings,
caches, logs, and other generated runtime content.

## Validation

- Fresh read-only SHA-256 calculation on the VM matches every entry in
  `SHA256SUMS.txt`.
- `node --check app.js` passes for the captured production asset.
- `python -m py_compile` passes for all captured Python source files.
- The unchanged canonical package passes its full regression suite: 142 tests.
- Git attributes disable text conversion for the snapshot so committed blobs
  retain the production bytes exactly.
