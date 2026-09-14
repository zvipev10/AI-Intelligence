# Migrate the investigation application to I360 data

## Purpose

Move non-Workstream, non-playback application data access and investigation capabilities to I360 while preserving the current user experience and application-owned reasoning.

## Completion criteria

- All functional acceptance criteria in `capability-brief.md` pass.
- Slices 0–8 have reviewed checkpoints.
- I360 is the default provider in the approved environments with a documented rollback.
- Workstream and playback remain outside this issue.

## Child tasks to create

1. Verify authenticated I360 estate and field mapping.
2. Add provider boundary and local implementation.
3. Implement read-only I360 provider.
4. Convert core MCP evidence tools.
5. Convert reasoning tools.
6. Integrate application API and frontend states.
7. Decide and implement investigation persistence boundary.
8. Migrate target candidates.
9. Run cutover acceptance and operational handoff.
