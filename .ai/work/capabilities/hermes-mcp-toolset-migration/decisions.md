# Hermes MCP toolset migration decisions

- Treat `mcp_servers` mapping keys as the canonical names used by `platform_toolsets`.
- Do not preserve generated `mcp-*` aliases in provisioned profiles.
- Fail migration when any API toolset does not resolve to a configured MCP server; do not silently drop unknown names.
- Keep Moshe restricted to `serbia-events-poc`; keep both configured data servers available to General profiles.
- Validate with real application requests and MCP audit-visible tool sequences, not service health alone.
