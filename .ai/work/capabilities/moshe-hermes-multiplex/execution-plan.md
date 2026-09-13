# Moshe Hermes multiplex execution plan

1. Verify the installed Hermes multiplex and prefixed-API contracts.
2. Add profile-aware API paths and credentials to the application transport.
3. Convert Moshe to a non-listening secondary profile with a unique MCP registration.
4. Enable multiplexing on the default gateway with a Moshe-only allowlist.
5. Back up production, stop user traffic, and perform the cutover.
6. Verify Moshe and General tool calls independently.
7. Disable the standalone Moshe service after successful smokes.
8. Harden future deployment scripts and publish the change.
