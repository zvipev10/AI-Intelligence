# Checkpoint 004 — Durable target references deployed

## Outcome

The acceptance-blocking target-reference gap is corrected and deployed for product retest.

## Decision

Resolved existing targets supplied to or discovered by Moshe are persisted as root-level
`target_ids`. Creation does not synthesize a target-assessment artifact and does not authorize target
creation or mutation.

## Implementation

- Creation MCP validates, deduplicates, and returns `target_ids`.
- Application workstream creation persists `target_ids`.
- Workstream presentation includes root targets before any assessment artifact exists.
- Missing localized catalog rows produce a minimal target-ID presentation reference.
- Moshe's persistent and runtime instructions require all resolved existing targets in the handoff.

## Automated verification

- Application/backend suite: 124 passed.
- MCP suite: 53 passed, 1 skipped.
- Python compilation and diff checks: passed.

## Deployment

- Main correction backup: `/opt/serbia-poc-ui-backups/workstream-target-fix-20260809T134616Z`
- Presentation fallback backup: `/opt/serbia-poc-ui-backups/workstream-target-fallback-20260809T135221Z`
- UI and Moshe services: active.
- Locale-aware v2.1 health: 200, 14,800 rows.
- Newer production bilingual behavior was preserved.

## Live verification

- Hebrew workstream: `ws_20260809_134902_873828a4`
- English workstream: `ws_20260809_134943_34806f6a`
- Both saved JSON files contain `target_ids: ["TGT-F2CA47CB9859"]`.
- Both presentation responses contain a target row.
- English uses the stable target ID as its display title because the English target catalog currently
  has no localized row for this target.

## Merge status

Do not merge until the user completes the next product test and explicitly approves.

