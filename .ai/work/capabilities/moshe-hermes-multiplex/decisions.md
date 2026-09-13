# Moshe Hermes multiplex decisions

- Use Hermes's `/p/moshe` API prefix rather than a second port.
- Use a distinct Moshe API key; never authenticate a named profile with the default key.
- Keep the standalone systemd unit installed but disabled for rollback.
- Give Moshe's MCP registration a unique server key to avoid Hermes's process-global MCP name collision.
- Register the unique Moshe MCP server in the default gateway for startup discovery, but exclude it from General's explicit API toolset.
- Disable Moshe's own port-binding and WhatsApp adapters; the default profile owns shared transports.
- Do not add a WhatsApp `profile_route` until the exact group JID is supplied or verified.
