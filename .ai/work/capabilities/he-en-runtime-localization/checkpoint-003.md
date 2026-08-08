# Checkpoint Summary

## Checkpoint
003 — VM deployment of clean English projections

## Checkpoint status
Complete. The six v2/v2.1 English projection files are deployed and the public v2.1 English API passes the no-Hebrew check.

## Pre-deployment evidence
- `serbia-poc-ui.service` was active.
- The deployed v2.1 English events file still contained 1,715,704 Hebrew characters.
- The deployed v2.1 English locations and entities files contained 912 and 519 Hebrew characters respectively.

## Deployment scope
Uploaded only the six regenerated `.en` event, location, and entity projection files for v2 and v2.1 to `/opt/serbia-poc-ui`. Hebrew source datasets, application code, runtime configuration, saved state, and MCP files were not replaced.

## Rollback
The previous six files were copied to:

`/opt/serbia-poc-ui/backups/he-en-data-20260808T162503Z`

The `serbia-poc-ui.service` service was restarted after file installation.

## Production verification
- Service state: `active`.
- Public status endpoint: build `serbia-poc-v2.1`, locale `en`, dataset version `v2.1`.
- Public English dataset rows: 14,800.
- Public TikTok layer rows: 1,101.
- Hebrew characters in the complete public TikTok layer payload: 0.
- Sample result fields were English for source type, certainty, actor, location, location type, and event summary.

## Remaining scope
- Perform a mobile browser visual check of the same result table.
- Localize legacy v1 and recorded playback assets only if those flows remain exposed.
- Continue the planned MCP locale/cache isolation slice before declaring the full bilingual capability complete.
