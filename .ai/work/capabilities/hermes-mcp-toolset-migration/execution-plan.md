# Hermes MCP toolset migration execution plan

1. Trace the legacy names in application and Hermes history.
2. Correct every deployment and profile provisioning path.
3. Add a validating atomic migration and regression tests.
4. Back up and migrate the three production profiles.
5. Restart gateways and verify capability endpoints.
6. Run read-only end-to-end tool-call smokes for General, persistent General, and Moshe.
7. Commit and push the durable fix.
