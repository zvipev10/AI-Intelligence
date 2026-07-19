# Architecture and Security Review

## Review status

Approved on 2026-07-19. The user explicitly approved the proposed architecture/security gate.

## SQLite placement and ownership

- Store the production database at `/opt/serbia-poc/data/attack_targets/attack_targets.db`.
- The existing `ubuntu` service account owns the directory and database.
- Directory mode: `0700`.
- Database mode: `0600`.
- Only the Serbia MCP service opens SQLite directly.
- The UI and agents never receive the database path or raw SQL access.

## Runtime access policy

- Moshe accesses targets only through constrained MCP tools.
- Moshe may search, read, create, and update candidates and attach evidence.
- All MVP targets remain `candidate`.
- Moshe may not delete targets, execute SQL, modify raw evidence, or modify canonical locations/entities.
- General may receive target-read/presentation tools but not candidate-write tools.
- Other Hermes agents receive no target-bank tools unless explicitly configured later.

## Evaluator-truth isolation

- Evaluator labels and `fusion_target_truth_v2_1.jsonl` remain outside production runtime directories.
- Production configuration contains no evaluator paths, environment variables, truth IDs, or test-mode switches.
- Runtime MCP modules do not import evaluator, generator, or truth-validation modules.
- Moshe-accessible tools, prompts, SQLite schema/content, and presentation results contain no evaluator-derived fields.
- Evaluation runs after Moshe in a separate development/test process and compares exported target/evidence IDs to truth.
- Deployment, configuration, import, schema, target-content, tool-contract, and runtime-without-truth tests enforce the boundary.

## Backup and restore

- Create a timestamped SQLite backup before deployments that change target-bank code or schema.
- Use SQLite's backup operation rather than copying a live writable file.
- Keep the latest five backups under `/opt/serbia-poc/backups/attack_targets/`.
- Restore is an administrator-only manual operation with target writes stopped.
- Verify target and evidence counts after restoration.
- Scheduled backups are deferred until the bank carries real operational value.

## Deletion and reset

- Expose no target deletion to Moshe or the UI in the MVP.
- Provide an administrator-only full-bank reset for development/evaluation.
- Reset requires an explicit database path and confirmation flag and creates a backup first.
- Individual target deletion is deferred.

## Operational safeguards

- Candidate and evidence writes occur within SQLite transactions.
- Concurrent writes are serialized.
- Infrastructure timeouts may exist even though the MVP adds no application-level mission limits.
- Failures never silently truncate results or expose evaluator data.

## Approval impact

Architecture/security does not block execution planning once QA and UX reviews are complete. Exact implementation details must preserve these approved boundaries.
