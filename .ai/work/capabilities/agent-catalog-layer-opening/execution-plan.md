# Execution Plan

## Gate
Capability, developer, UX, and QA reviews are approved under the user's explicit
end-to-end instruction.

## Slice 1 — Structured action
Add `open_catalog_layers`, schema/handler, deployment allow-list, audit extraction,
catalog prompt context, and strict gateway validation.

## Slice 2 — Browser execution
Consume validated actions, call `openCatalogLayer`, activate the requested view,
and expose explicit action outcomes in the result flow.

## Slice 3 — Validation and release
Run focused/full regression checks, deploy UI and MCP assets, execute the exact
Telegram request, verify tab/map state, and record rollback and handoff evidence.

## Rollback
Restore versioned UI/server files and MCP server from production backups, restart
their services, and revert the isolated commits if required.

