# Checkpoint Summary

## Checkpoint
004 — Production English data-source inspection

## Checkpoint status
Complete inspection; request changes. The full English solution is not yet totally English.

## Scope inspected
- Deployed UI event, location, and entity projections for v1, v2, and v2.1
- Every public `/api/layers/*/rows?lang=en` response
- Persisted target-bank rows
- Active MCP event, location, entity, UAV, and semantic source configuration
- Recorded runs, saved questions, investigation memory, workstreams, scenario manifests/runs, and live-step state

## Passing sources

| Source | Result |
|---|---|
| Active v2.1 `.en` events | 14,800 rows; zero Hebrew characters |
| Active v2.1 `.en` locations | Zero Hebrew characters |
| Active v2.1 `.en` entities | Zero Hebrew characters |
| v2 compatibility `.en` events/locations/entities | Zero Hebrew characters |
| Public event-source layers | Clean English payloads |
| Public location metadata layer | Clean English payload |
| Scenario manifest | One file; zero Hebrew characters |
| Scenario run state | Two files; zero Hebrew characters |
| Recorded questions | No deployed v2.1 records; endpoint currently returns an empty list |
| Saved questions | No deployed v2.1 records; endpoint currently returns an empty list |
| Investigation memory | No deployed v2.1 records; endpoint currently returns an empty list |
| Live-step buffer | Empty during inspection |

## Blocking findings

### 1. Active MCP source corpus has no English projection
Both active MCP processes read the Hebrew v2.1 files under `/opt/serbia-poc/data/serbian_intelligence_v2_1/`, not the clean `.en` files deployed under `/opt/serbia-poc-ui`.

Observed Hebrew counts in active MCP sources:
- event projection: 2,081,327 characters
- locations: 8,535 characters
- entities: 886 characters
- UAV observations: 922,220 characters
- full raw CSV and JSONL: 5,727,697 characters each

Impact: live MCP tool results can still contain Hebrew. The English agent prompt requests English output, but that is not a substitute for a clean English tool/data boundary.

### 2. Target-bank source is Hebrew-only
The public English target-candidate layer returned 21 rows and 8,246 Hebrew characters. Every row contained Hebrew in:
- `title`
- `summary`
- `object_class`
- `fusion_explanation`

Impact: opening the target-candidate layer in English mode still exposes Hebrew.

### 3. Entity metadata response synthesizes Hebrew defaults
The underlying English entity JSON is clean, but the public English entity layer returned 756 Hebrew characters across 28 rows:
- `confidence`: 28 Hebrew values
- `basis`: 28 Hebrew values

Impact: the entity table is not fully English despite having a clean English source file.

### 4. Persisted workstream metadata is not localized
Two deployed v2.1 workstream files contain 36 Hebrew characters across:
- four `participants[].display_name` values
- two `participants[].role` values

Impact: workstream UI/API data is shared rather than locale-specific and can leak Hebrew into English sessions.

## Non-blocking or inactive findings

### Legacy v1 projection
The inactive v1 `.en` files remain incomplete:
- events: 478,165 Hebrew characters
- locations: 277 Hebrew characters
- entities: 200 Hebrew characters

The active VM uses v2.1, so this is not affecting the current result table, but v1 rollback would not be fully English.

### Empty mutable sources
Recorded runs, saved questions, and investigation memory currently have no v2.1 files. Their endpoints are clean only because they are empty. Saved questions, investigations, workstreams, and scenario artifacts do not all have a locale-isolated storage contract, so future Hebrew-created state may remain visible in English mode.

## Public API aggregate
- 14 layers inspected
- 15,019 total rows returned
- 9,002 Hebrew characters detected
- Leakage was isolated to the entity metadata and target-candidate layers; event and location layers were clean.

## QA recommendation
Request changes. Do not declare the bilingual capability complete until:
1. MCP tools accept/use a locale and read locale-specific projections or localize all returned fields deterministically.
2. Target-bank records have English fields or a locale-aware presentation projection.
3. Entity metadata defaults are locale-aware.
4. Workstream participant names/roles are locale-aware at the API boundary.
5. Regression tests scan every English API layer and live MCP tool payload for Hebrew.

## Next role
Development should implement the planned MCP locale boundary and the three remaining response/data projections. QA should rerun this exact production audit afterward.
