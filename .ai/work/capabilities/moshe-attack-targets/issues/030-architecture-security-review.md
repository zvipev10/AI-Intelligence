# [Architecture/Security Review] Moshe Runtime Boundaries

## Purpose

Approve SQLite placement, service ownership, Moshe permissions, evaluator-truth isolation, backup/restore, and reset behavior.

## Required action

Preserve the approved controls in implementation planning and verify them before production release.

## Owner role

Architecture/Security

## Inputs

- `architecture-security-review.md`
- `chapter-001-target-bank-schema.md`
- `chapter-002-agent-routing-and-presentation.md`

## Expected output

Approved runtime security contract and testable release controls.

## Blocking

No longer blocks planning; controls remain mandatory for implementation and release acceptance.

## Completion criteria

- [x] SQLite path, owner, and permissions approved.
- [x] Direct database access restricted to Serbia MCP.
- [x] Moshe tool permissions approved.
- [x] Evaluator-truth isolation controls approved.
- [x] Backup and restore policy approved.
- [x] Development/evaluation reset policy approved.

## Related artifacts

- `.ai/work/capabilities/moshe-attack-targets/architecture-security-review.md`

## Parent capability

Moshe Attack Targets MVP; remote parent issue pending.
