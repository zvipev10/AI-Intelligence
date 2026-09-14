# Migrate the investigation application to I360 data

## Purpose

Move non-Workstream, non-playback application data access and investigation capabilities to I360 while preserving the current user experience and application-owned reasoning.

## Completion criteria

- All functional acceptance criteria in `capability-brief.md` pass.
- Slices 0–8 have reviewed checkpoints.
- I360 is the default provider in the approved environments with a documented rollback.
- Workstream and playback remain outside this issue.

## Child tasks to create

1. Part 1: verify the authenticated I360 estate and field mapping.
2. Part 1: add provider boundary and local implementation.
3. Part 1: implement the read-only I360 provider.
4. Part 1: integrate non-chat application services and frontend.
5. Part 1: decide persistence, migrate targets, and complete cutover.
6. Part 2: prove I360 `llm/chat` agent prerequisites.
7. Part 2: implement the agent controller and tools.
8. Part 2: integrate chat, live steps, memory, and presentation actions.
9. Part 2: run Hermes parity and agent cutover.
