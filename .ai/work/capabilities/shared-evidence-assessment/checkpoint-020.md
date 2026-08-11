# Checkpoint 020 — Production investigation cleanup

## Outcome

The deployed registry now contains only `KFOR involvement` and `NATO involvement`.
All other investigation memory, workstream, and scenario-run records were moved to
a recoverable VM backup. The removed active run's visibility file was archived
with the run to avoid a dangling playback reference.

The server is now authoritative during client hydration. Stale browser-local
investigations are replaced by the server registry and are not uploaded again.
New investigations continue to register when they are created.

## Validation

- Focused investigation/UI suite: 32 tests passed.
- Full Python discovery: 135 tests passed.
- JavaScript syntax passed.
- Production API returned exactly `KFOR involvement` and `NATO involvement`.
- Public page served `app.js?v=157`.
- UI and both Hermes gateway services were active.

## Recovery

The 36 archived files and manifest are stored at:
`/home/ubuntu/deploy-backups/investigation-cleanup-20260811T163026Z`.
