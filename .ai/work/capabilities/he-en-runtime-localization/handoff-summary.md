# Handoff Summary

## Current state
The v2/v2.1 English event/location/entity projections are deployed and clean, but checkpoint 004 shows that the complete English solution still has Hebrew data paths through MCP, target candidates, entity metadata defaults, and workstreams.

## Published baseline
Commit `eb9168c` on `origin/codex/he-en-localization` contains the brief, developer review, QA review, execution plan, and status dashboard.

## Key finding
The screenshot was caused by partially translated `.en` assets, not by the English UI toggle. The old generator accepted mixed Hebrew/English output. The regenerated active v2.1 runtime contains 14,800 rows with zero Hebrew matches; the TikTok subset contains 1,101 clean rows.

## Next action
Implement checkpoint 004 remediation: MCP locale-specific data/results, target-bank English presentation fields, localized entity defaults, and localized workstream metadata. Then rerun all-layer production scanning and mobile QA.

## Publishing status
Code/data commit `763253c` is pushed and deployed. The deployment checkpoint is pending its artifact commit and push. Draft PR creation remains unavailable because GitHub CLI is not installed.

## Deployment evidence
The previous VM assets are recoverable from `/opt/serbia-poc-ui/backups/he-en-data-20260808T162503Z`. After restart, the public API reported 14,800 English v2.1 rows and the complete 1,101-row TikTok payload contained zero Hebrew characters.

## Latest QA evidence
All 14 public English layers were inspected. Event and location layers passed, but the entity metadata and target-candidate layers contributed 9,002 Hebrew characters. The active MCP processes still read Hebrew v2.1 source files. See `checkpoint-004.md` for field-level counts and remediation requirements.

## Durable docs recommendation
Add the Option A locale-contract decision to `docs/decisions.md` after the MCP implementation proves the cache/interface design. Update `docs/architecture.md` with the bilingual data flow at that same checkpoint. No stable product-context update is needed yet.

## Issue status
Parent/child GitHub issues have not been created. The parent capability remains open; Slice 1 remains active.
