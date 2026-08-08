# Checkpoint Summary

## Checkpoint
005 — Locale-isolated target-bank architecture

## Checkpoint status
Design ready for human review; no code or production database changes made.

## Product decision
Target persistence must use two physically separate SQLite database instances, matching the locale separation used for raw data.

## Proposed production layout
- Hebrew DB: `/opt/serbia-poc/data/attack_targets/he/attack_targets.db`
- English DB: `/opt/serbia-poc/data/attack_targets/en/attack_targets.db`
- Hebrew backups: `/opt/serbia-poc/backups/attack_targets/he/`
- English backups: `/opt/serbia-poc/backups/attack_targets/en/`

## Migration behavior
1. Stop target writes during the migration window.
2. Create a timestamped safety backup of the current shared DB.
3. Run SQLite integrity and row-count checks.
4. Copy the current shared DB, including its 21 Hebrew targets and evidence, to the Hebrew path.
5. Initialize a new empty English DB with the same schema.
6. Preserve the shared DB as a rollback artifact until both locales pass production verification.
7. Restart the relevant MCP and UI services only after configuration and file permissions are validated.

Existing Hebrew records are preserved rather than translated or copied into English. The English target bank starts with zero targets.

## Runtime routing contract
- Normalize locale to `he` or `en`; omitted/invalid locale remains `he` for backward compatibility.
- `search_target_candidates`, `get_target_candidate`, `create_target_candidate`, `update_target_candidate`, `attach_target_evidence`, duplicate detection, and requested-result target materialization must select the locale-specific `TargetBank`.
- The UI target catalog reader must select the database from the request locale.
- Target backup/reset/restore administration must require an explicit locale and may operate on only one bank at a time.
- Hebrew target IDs never resolve in English mode, and English target IDs never resolve in Hebrew mode.

## English creation guard
English writes must reject Hebrew characters in all user-facing persisted fields:
- candidate `title`, `summary`, `object_class`, and `fusion_explanation`
- evidence `source_type`, `reported_object`, `relevant_text`, and `evidence_role`
- mutable updates to the same candidate fields

Identifiers, timestamps, counts, entity IDs, location IDs, record IDs, mission IDs, and source-group IDs remain language-neutral and are not translated.

The Hebrew bank may contain Hebrew and English identifiers as required by the original source contract.

## Code changes required
- Replace the singleton `TARGET_BANK` with a locale-keyed bank registry.
- Add locale to target MCP tool schemas and handlers.
- Propagate session locale through target tool calls and requested-result presentation.
- Route UI target catalog reads by locale.
- Make deployment configuration expose separate DB and backup paths.
- Update target-bank administrative tooling for explicit locale selection.

## Test requirements
- Two temporary DBs remain isolated across create/search/get/update/attach operations.
- Omitted locale routes to Hebrew.
- English writes containing any Hebrew character are rejected atomically.
- Failed English writes leave target and evidence counts unchanged.
- Hebrew target IDs are absent in English searches and vice versa.
- UI `attack-targets:all?lang=en` reads only the English DB.
- Backup/reset/restore affect only the selected locale.
- Migration preserves Hebrew counts and produces an empty English bank.
- Production post-migration scan reports zero Hebrew in the English target layer.

## Rollback
Restore the pre-migration shared database and previous environment variables/configuration, then restart services. Do not delete either locale DB during the verification window.

## Review gate
This change affects data persistence, API/tool contracts, deployment configuration, and production state. Human approval is required before implementation and migration.
