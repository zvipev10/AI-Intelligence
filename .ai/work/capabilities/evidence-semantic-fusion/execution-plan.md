# Execution plan

Review gate: capability scope and architectural direction were explicitly approved by the user.

1. Implement and test shared semantic object-class resolution.
2. Integrate normalization into evidence projection and live fusion.
3. replace fixed catalog buckets with rolling temporal components.
4. Add the generated catalog as a read seed for the MCP evidence repository.
5. Validate the three Ibar Bridge chains and run regression tests.
6. Record checkpoint, architecture update, and handoff.

Rollback: retain SQLite as the writable store and allow catalog seed reads to be disabled by omitting the catalog path.
