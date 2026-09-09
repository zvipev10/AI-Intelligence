# Execution Plan

## Capability and issues
Record and organization viewers. Parent #48, review #49, draft PR #50.

## Plan status
Approved under the user's explicit delegation on 2026-09-09.

## Prerequisite review gate
- Product brief: approved by user, with targets removed.
- Developer, UX, QA: approved under delegated authority; see adjacent review artifacts.
- Architecture/security: no new service or permission surface; current visibility-scoped client rows and allowlisted media URLs.
- Blocking questions: resolved. Missing media renders as unavailable.

## Goal and scope
Open one raw record or organization through the same in-app dialog from its grid row, an ungrouped map marker, or an explicit assistant reference. Show text/metadata and source-appropriate media when a valid URL exists. Targets and grouped-marker selection are excluded.

## Approach and affected files
- `index.html`: accessible details dialog.
- `app.js`: typed resolution, safe media mapping, rendering, entry-point controls, state cleanup.
- `styles.css`: responsive dialog, metadata, media, and open-control styles.
- focused tests plus capability checkpoints and durable decision notes.

No server/data-model changes or dependencies.

## Test plan
Static/behavior contracts for dialog, resolver, media allowlist, three entry points, grouped-marker exclusion, and target exclusion; syntax check; relevant existing UI tests.

## Slices
1. Viewer foundation and map/grid opening. Medium UX risk; developer/UX/QA review after checks.
2. Assistant opening, media/error behavior, full regression and handoff. Medium interaction risk; final QA/product acceptance.

## Rollback
Revert the isolated app asset and test commits. Existing layers and APIs remain unchanged.
