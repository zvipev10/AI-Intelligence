# Checkpoint 002 — Runtime Activation

## Decision

V2 is the default runtime dataset. Set `INTELLIGENCE_POC_DATASET_VERSION=v1` to roll back without modifying either corpus.

UAV observations remain ordinary event records. Their `event_summary` text contains the detected object type and estimated count; no UAV-specific API, parser, or UI is required.

## Implemented

- UI and API load the V2 projection and V2 locations dynamically from `/api/status`.
- MCP tools default to V2 events, entities, locations, and a versioned semantic index.
- V2 record and location identifiers are accepted by UI/API/MCP validation.
- The investigation prompt frames the corpus as incomplete, opposition-focused Serbian intelligence collection and identifies UAV counts as estimates.
- Saved questions, investigations, recorded runs, and performance logs use V2-specific directories; V1 keeps its legacy paths.
- Deployment scripts and example Hermes configuration include the V2 runtime files and environment variables.

## Verification

- JavaScript syntax check passed.
- Python modules parsed successfully.
- UI and MCP loaders read 14,800 V2 rows, 28 entities, and 170 locations.
- API status and static-file smoke test returned V2 paths and 14,800 rows.
- V1 rollback loaded 10,000 rows and 155 locations.
- V2 identifiers were recognized across runtime layers.
- Git whitespace validation passed.

## Remaining work

Deploy the committed activation and repeat the API/UI/MCP smoke checks against the production host.
