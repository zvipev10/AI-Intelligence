# Checkpoint 005 — Raw records persisted as workstream artifacts

## Outcome

Raw records supplied in an explicit workstream-creation request are now persisted as indications in
one initial `target_assessment_lead` artifact.

## Behavior

- `prepare_workstream_creation` validates, deduplicates, and carries `record_ids`.
- The application creates an initial active artifact when `record_ids` is non-empty.
- The inferred workstream objective becomes the initial lead statement.
- Each verified record is stored as a `context` indication with canonical event metadata.
- Target-only creation continues without an artifact.
- Mixed creation retains root `target_ids` and links a single validated target as the artifact subject.
- Low confidence, missing corroboration, or no existing target does not block an explicitly requested
  evidence-tracking workstream; it still blocks unauthorized target persistence.

## Automated verification

- Application/backend suite: 126 passed.
- MCP suite: 54 passed, 1 skipped.
- Python compilation and diff checks: passed.

## Deployment

- Artifact deployment backup: `/opt/serbia-poc-ui-backups/workstream-record-artifact-20260809T135718Z`
- Low-confidence orchestration backup: `/opt/serbia-poc-ui-backups/workstream-low-confidence-20260809T140226Z`
- Mixed-target fallback backup: `/opt/serbia-poc-ui-backups/workstream-mixed-target-20260809T140600Z`
- UI and Moshe services are active; locale-aware v2.1 health is 200 with 14,800 rows.

## Live verification

- English: `ws_20260809_140015_fba03778`
- Hebrew: `ws_20260809_140407_790c1516`
- Both saved workstreams contain one active `target_assessment_lead` artifact.
- Both artifacts contain `REC-V2-000001` as an indication.
- The Hebrew first smoke exposed and then verified the correction for low-confidence stopping behavior.

## Merge status

Branch remains unmerged pending user product validation.

