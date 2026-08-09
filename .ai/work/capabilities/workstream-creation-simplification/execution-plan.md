# Execution Plan — Main-based workstream simplification

## Gate

- Product behavior approved by the user.
- Main-based developer, UX, and QA reviews ready.
- Clean baseline: `origin/main` commit `01c21ff`.

## Slice 1

1. Update persistent Moshe instructions.
2. Update main's runtime Moshe instructions without changing playback authorization.
3. Update the creation MCP description.
4. Add alignment, boundary, and evaluation coverage.
5. Run focused tests and broad current-main regression suites.
6. Publish the implementation and checkpoint; do not deploy in this slice.

## Rollback

Revert the focused implementation commit. No migration is involved.
