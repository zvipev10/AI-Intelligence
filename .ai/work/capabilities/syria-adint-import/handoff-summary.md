# Syria ADINT import handoff

## Historical initial delivery

Syria adint-v1/profile7 is active on VM 151.145.93.180. Deployed source commit 04abab48b1e9083253c2d3a7c34afafab0de4882. Four former ADINT rows were replaced by all 120 supplied observations, with 84 new coordinate locations and 12 device identities. Total 324 rows, 86 locations and 13 entities. Other 204 source rows and Kosovo data/profile unchanged. Previous package and state retained; source/state backup: /opt/demo-runtime/backups/syria-adint-09d48be7.

## Source mapping

The 11 source fields are retained. Observation IDs map to REC-SYR-ADINT-<observation_id> for existing application identity contracts; device identities are deterministic hashes with the original device_id as canonical name/alias. Native numeric/null values are returned through MCP; CSV blanks represent missing values. Legacy advertising_id/ip_address/location_accuracy_m are compatibility aliases, not additional inferred observations. No person, missing coordinate, missing IP or device-to-convoy relationship is inferred. Imported ADINT dates September1-5 do not overlap preserved September22 IPDR sessions.

## Validation

18 focused import/network/scenario tests passed, JavaScript syntax passed, and isolated viewer/coordinate checks passed. VM activation checked UI/gateway and actual role identity/counts. Live public CSV matched every supplied field for all 120 observations; 36 lack geometry, 51 lack IP, 76 lack keyboard language. Real browser verified ADINT 120 catalog entry, all native table columns, and OBS-01-004 opening with absent coordinate fields and disabled map action. Blank CSV coordinate handling was corrected after browser testing (empty strings must not become zero). Live prebuilt index and identifier retrieval passed using the deployed system-Python engine; an initial diagnostic using Hermes' different venv engine rejected the Python cache, so qualification was rerun with the correct MCP interpreter.

## Publishing and limits

Published branch codex/syria-adint-import and draft PR #82; issue #81 tracks the work. Not merged in this request. Documentation updated in demo-scenarios.md and operations.md. Runtime source and dataset changes are deployed; later handoff/test-only commits do not require a redeploy. Existing saved work was copied at a stopped transition; references to removed historical ADINT records may remain historical references. No full-suite or new live LLM investigation was claimed. Next: user can refresh and open ADINT; PR remains available for review/merge.

## Follow-up: media relocation (2026-09-24)

User requested selecting two ADINT locations for the existing CCTV/Satellite records. Deployed 4796185b as adint-v2/profile8: Site1 uses LOC-SYR-ADINT-002 (35.077055,36.333669); Site2 uses LOC-SYR-ADINT-001 (35.108621,36.312140). All image own/paired location references and record summaries agree. Media, dates, identities and all non-media rows unchanged. The existing two original location definitions remain in the catalog; no records reference them. 19 focused tests pass, live search retrieves ADINT/CCTV/Satellite at each point, all four public row locations verified and all six images/two movies accessible. UI/gateway/role readiness and prebuilt index passed. Backup: /opt/demo-runtime/backups/syria-media-adint-4796185b. No separate browser interaction was needed for this data-only follow-up; viewer/map behavior was validated in the preceding release. PR82 updated; no merge requested.

## ADINT2 replacement (2026-09-24)

Deployed adint-v3/profile13 at b11912a5. All 120 live ADINT records match every ADINT2 field; supplied coordinates verified against the live location catalog. Total remains 424 records, 88 locations and 13 entities. 23 focused tests passed; semantic cache rebuilt. Service health/identity checks passed and maintenance is disabled. Backup: /opt/demo-runtime/backups/syria-adint2-b11912a5. Draft PR82 published, unmerged. Next: refresh application. No architecture changes or additional documentation decisions required.
