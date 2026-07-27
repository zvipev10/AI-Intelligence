# Checkpoint 009 — Desktop workstream indicator recovery

## Scope completed

- Confirmed production workstreams are persisted under one server investigation ID while desktop browsers may generate a different local ID.
- Added an opt-in `fallback=latest` workstream-list mode.
- Preserved exact investigation scoping whenever the requested investigation already has workstreams.
- When an exact lookup is empty, return the most recently updated persisted workstream group and its canonical investigation ID.
- Made the browser adopt and persist that canonical ID before restoring investigation memory.
- Advanced public asset cache version to `v118`.

## Validation

- Focused workstream API/UI suite: 23 tests passed.
- Full test discovery: 83 tests passed.
- Added regression coverage for fallback adoption and exact-match precedence.
- `git diff --check` passed.

## Review findings

### Blocking issues

None.

### Non-blocking comments

- The fallback reflects the current single-user demo model. A future multi-user release should replace it with authenticated, server-owned investigation identity.

### Missing tests

None for the current demo boundary.

## Recommendation

Deploy to the VM, verify the public page serves asset version `v118`, and confirm a previously unseen desktop investigation ID receives the canonical workstream group.

## VM deployment

- Deployed commit `f329903`.
- UI service: active.
- General Hermes gateway service: active.
- Moshe gateway service: active.
- Public assets use cache version `v118`.
- A new desktop smoke investigation resolved to canonical investigation `investigation-1784224653197-e2581839825b48`.
- The recovery response returned five workstreams, four active.
- Rollback backup: `/opt/serbia-poc-ui-backups/workstream-desktop-20260727T2041Z`.
