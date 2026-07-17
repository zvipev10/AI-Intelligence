# Execution Plan

## Capability

Serbian Intelligence Dataset V2

## Plan status

Generation and local activation complete; deployment remains.

## Prerequisite review gate

- Product brief: approved scope recorded in `capability-brief.md`.
- Developer review: implementation guidance recorded.
- QA review: test plan recorded.
- Blocking questions accepted as assumptions: structured UAV records, no media assets.

## Goal

Generate a separate deterministic v2 corpus near 15,000 rows without modifying v1.

## Proposed approach

- Copy and perspective-filter pre-escalation records into v2.
- Generate replacement escalation records from a controlled event/source/entity/location model.
- Produce dedicated UAV exploitation records and canonical runtime projections.
- Validate immutability, distributions, chronology, and references.

## Files likely affected

- New generator under `llm_investigation_orchestrator_serbia_poc/data/`.
- New files with `_v2` in the same data directory.
- New capability artifacts only.

## Data/API changes

- New raw fields for collection provenance and observation metadata.
- Existing canonical runtime schema unchanged.
- No API change and no runtime activation.

## Execution slices

### Slice 1
Goal: implement deterministic generator and validation.
Risk: medium.
Reviewer: Development/QA.

### Slice 2
Goal: generate v2 files and run integrity/distribution checks.
Risk: medium.
Reviewer: Product/QA.

### Slice 3
Goal: activate V2 in the UI, API, MCP server, and deployment configuration while preserving V1 rollback.
Risk: high.
Reviewer: Product/Development/QA.
Status: Complete locally.

### Slice 4
Goal: deploy and smoke-test the activated runtime.
Risk: medium.
Reviewer: Development/QA.
Status: Pending.

## Rollback/fallback

Delete only `_v2` files and generator; v1 remains untouched.
