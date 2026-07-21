# Checkpoint 011 — Canonical UAV source type and target evidence columns

Date: 2026-07-21

## Approved behavior

- `וידאו מכטב"מ` replaces `חיל האוויר הסרבי - ניצול וידאו מכטב״ם` as the canonical V2.1 `source_type`; it is not a presentation alias.
- Existing persisted target evidence is migrated to the canonical value during deployment.
- The attack-target table separates evidence provenance into:
  - independent sources: distinct `source_group` count;
  - source types: unique `source_type` values for the target;
  - raw records: total attached evidence records.

## Implementation

- Updated all five V2.1 dataset projections containing the source value and the dataset generator constant.
- Corrected the catalog projection field from `independent_source_count` to the UI contract `source_group_count`.
- Added `source_types` and `evidence_count` consistently to catalog reads, target-bank reads, and normalized agent results.
- Added an exact, transactional, idempotent migration for existing persisted evidence rows.
- Preserved raw evidence references and the existing evidence detail control.

## Validation

- V2.1 projection: 14,800 total rows; 3,800 canonical UAV-video rows; 0 legacy UAV-video rows.
- JavaScript syntax passed on the deployment VM.
- UI/API/normalizer tests: 21 passed.
- Target-bank/catalog-reader tests: 11 passed.
- Read-only production integration before migration returned target group/record counts of 5/5, 5/6, and 2/3.

## Deployment guard

Back up the target SQLite database and deployed V2.1 projection before migration. Update only `target_evidence.source_type` rows matching the exact legacy value; verify target/evidence counts remain unchanged.
