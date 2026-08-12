# Checkpoint 001 — Single canonical v162 source tree

## Summary

Promoted the 11 exact production v162 source files into the package root and
removed the duplicate editable snapshot tree. The VM was not contacted or
modified during consolidation.

## Validation

- All 11 canonical files match `deployment/SHA256SUMS-v162.txt`.
- `node --check app.js` passes.
- All six promoted Python modules compile.
- 121 active regression tests pass.
- Three new tests enforce the v162 hashes, absence of a duplicate tree, and the
  bilingual playback/workstream UI contract.

## Test migration

Twenty-four source-string assertions for the superseded implementation were
removed from discovery and replaced by the v162 contract tests. Backend tests
now expect the deployed single real-time playback flow and the versioned,
locale-specific workstream path.

## Production safety

No deployment, upload, SSH write, service restart, database mutation, or VM
filesystem change occurred.
