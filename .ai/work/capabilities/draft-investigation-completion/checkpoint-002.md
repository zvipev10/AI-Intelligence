# Checkpoint 002 — Simplified creation modal

## Scope

Removed the participant presentation from the draft-to-investigation creation modal. The modal now asks only for the investigation name. After creation, the workspace continues to render the complete regular participant team through the existing investigation flow.

## Files changed

- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- UI contract tests and deployment provenance

## Validation

- Full Python test suite: 133 tests passed.
- `node --check app.js`: passed.
- `git diff --check`: passed.

## Production data operation

Removed the exact production investigation named `ניסיון` after backing up its JSON record. Backup: `/opt/serbia-poc-ui-backups/investigation-cleanup-20260813T182246Z`.

Renamed the exact production investigation `NATO involvement` to `NATO deployment` without changing its ID or saved content. Backup: `/opt/serbia-poc-ui-backups/investigation-rename-20260813T182606Z`.

## Release

Approved by the user's explicit request to deploy and merge to `main` after implementation.
