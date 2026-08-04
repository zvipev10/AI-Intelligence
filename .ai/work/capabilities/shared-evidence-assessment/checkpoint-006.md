# Checkpoint 006 — Selected-Teammate Chat Routing

## Scope completed

- Made the selected upper-bar teammate the implicit addressee for subsequent chat turns.
- Applied the same selected-addressee behavior to continuation requests and live-step polling.
- Preserved the exact user-authored text in the visible conversation.
- Kept explicit `@name` mentions authoritative when present.
- Preserved Moshe mission routing by supplying the selected Moshe identity to the existing current-message router.

## Validation

- Main test discovery: 78 tests passed.
- Added regression coverage for implicit selection, explicit-mention precedence, visible-message preservation, main-turn routing, and continuation routing.
- `git diff --check` passed.

## Review findings

### Blocking issues

None.

### Non-blocking limitations

- Moshe is the only teammate with a dedicated backend profile. Other selected teammate identities are transmitted through the shared agent backend until their individual profiles exist.

## Recommendation

Deploy and verify that selecting Moshe, then sending a message without `@משה`, returns `responding_agent=moshe`.

## VM deployment

- Deployed commit `1ca8c5c`.
- UI service: active.
- Moshe gateway service: active.
- Dataset: `v2.1`, 14,800 rows.
- Public assets use cache version `v115`.
- Public JavaScript contains `addressedPromptForSelectedMember`.
- Existing workstream, thinking-indicator, MCP, and Moshe-profile contracts remain present.
- Rollback backup: `/opt/serbia-poc-ui-backups/workstream-slice2-20260727T163233Z`.
