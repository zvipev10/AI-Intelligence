# Checkpoint 002 — Cross-investigation update isolation

## Status

Implemented and validated locally; ready for targeted production deployment.

## Defect

The playback timeframe is intentionally global, but playback status serialized the
active run's latest investigation-memory update for every requested investigation.
After reload, the browser rendered the same update once under each investigation.
This exposed KFOR-specific saved-memory references inside unrelated investigations.

## Correction

- Preserve the approved global playback timeframe and active run.
- Key persisted memory-update claims by revision and investigation ID.
- Serialize an update only when its stored investigation ID matches the requested
  investigation, including backward-compatible reads of legacy revision-only data.
- Resume a running update only for its owning investigation.
- Reject missing or mismatched update ownership in the browser before rendering.
- Build browser deduplication keys from the update owner rather than current UI state.

## Validation

- 44 focused playback, UI-contract, and production-manifest tests pass.
- The regression reproduces two investigations sharing one global playback run and
  confirms the second investigation receives `memory_update: null`.
- A persistence regression confirms two investigations can claim the same run revision
  without colliding.
- JavaScript syntax, Python compilation, and Git whitespace checks pass.
- Full discovery ran 126 tests: 124 passed; the manifest failure was resolved by the
  v172 manifest, and `test_moshe_profile` could not import because local PyYAML is absent.

## Release candidate

- Public script version: `app.js?v=170`.
- Source manifest: `deployment/SHA256SUMS-v172.txt`.
- Targeted runtime files: `app.js`, `index.html`, `server.py`, and
  `scenario_playback.py`.

## Review

### Blocking issues

None in the isolation change.

### Non-blocking comments

Install PyYAML in the local test runtime to include `test_moshe_profile` in future
full-discovery runs.

### Recommendation

Approve targeted deployment, production two-investigation verification, and merge to
remote `main`.
