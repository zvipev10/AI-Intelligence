# Checkpoint 010 — Raw-record target lookup

## Outcome

Moshe can find every existing candidate target that contains an exact raw-data record ID by calling `search_target_candidates` with `record_id`.

## Contract

- The lookup is read-only and exact.
- It returns all matching candidate targets.
- Matching is implemented with an indexed `EXISTS` predicate so each result retains its full target summary, evidence count, source types, and raw-data references.
- The General Agent is aware that the capability exists but does not receive target-bank tool permissions and does not route to Moshe without an explicit `@משה`.
- Moshe's runtime instructions and persistent profile both direct him to use this lookup when the user supplies a `REC-*` identifier.

## Validation

- 31 focused MCP, target-bank, fusion, and boundary tests passed on Linux.
- UI server Python compilation passed.
- Production search for `REC-V2-009058` returned both existing matching targets and preserved their full evidence counts.
- SQLite counts remained unchanged at 7 targets and 30 evidence links.
- SQLite integrity remained `ok`.
- `idx_target_evidence_record` exists in production.
- General gateway, Moshe gateway, and UI services are active; both gateway health endpoints and the served UI page passed.

## Deployment

- VM: `151.145.93.180`
- Code rollback backup: `/home/ubuntu/deploy-backups/raw-record-target-lookup-20260723T120000Z`
- Database backup: `/opt/serbia-poc/backups/attack_targets/attack_targets-pre-record-lookup-20260723T120000Z.db`

## Observation

The production smoke record currently belongs to two targets: `TGT-70C964B0ECC0` and `TGT-5D4598097339`. This lookup correctly exposes that existing overlap; it does not create or repair it.
