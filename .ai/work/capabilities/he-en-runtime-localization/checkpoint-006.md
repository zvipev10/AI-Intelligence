# Checkpoint 006 — Locale-isolated target banks deployed

## Scope
Implemented and deployed the approved two-instance target-bank design. Per the final product direction, no existing records were migrated: both active banks were initialized empty.

## Implementation
- Added locale-keyed Hebrew and English `TargetBank` instances and routed MCP target operations by normalized locale.
- Added locale routing to UI target-catalog reads and explicit `--locale he|en` administration.
- Added English-source projection lookup for target evidence.
- Rejects Hebrew characters in persisted English target presentation and evidence fields on create, update, and evidence attachment.
- Configured distinct database and backup paths for each locale.

## Production state
- Hebrew: `/opt/serbia-poc/data/attack_targets/he/attack_targets.db`
- English: `/opt/serbia-poc/data/attack_targets/en/attack_targets.db`
- Both finish with 0 targets and 0 evidence.
- The prior shared database was removed from the active path and retained at `/opt/serbia-poc/backups/attack_targets/locale-split-20260808T165742Z/attack_targets.shared.pre-split.db`.

## Verification
- 34 focused local tests passed; 1 unrelated optional test was skipped.
- Python compilation passed for the changed target-bank, admin, MCP, and UI server modules.
- Both production banks passed create and update smoke tests, then were reset to empty.
- A Hebrew update against the English bank was rejected without changing the stored row.
- SQLite `integrity_check` returned `ok` for both banks.
- Database files are distinct and mode `0600`; containing directories are mode `0700`.
- `hermes-gateway`, `hermes-moshe-gateway`, and `serbia-poc-ui` are active.
- Hebrew and English `attack-targets:all` UI endpoints each return zero rows.

## QA review

### Blocking issues
None for the target-bank split.

### Non-blocking comments
Other mutable runtime stores identified in checkpoint 004 remain outside this slice.

### Missing tests
No missing blocking tests for target creation/update isolation. Full bilingual investigation acceptance remains a later capability checkpoint.

### Recommendation
Approve this target-bank slice. Development may continue to the remaining localized MCP/entity/workstream paths; the parent localization capability remains open.
