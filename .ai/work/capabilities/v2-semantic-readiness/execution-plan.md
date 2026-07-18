# Execution Plan

## Prerequisite gate

| Input | Status |
|---|---|
| Product scope | Approved by user request |
| Developer review | Ready |
| QA plan | Ready |
| UX review | Not triggered; no UI change |

## Slice 1 — V2 structured semantic fields

- Extend V2 projection schema.
- Regenerate only V2 artifacts.
- Validate UAV field preservation and V1 hashes.

## Slice 2 — Semantic concepts and indexing

- Extend semantic document and deterministic concept features.
- Bump semantic index version.
- Add regression probes.
- Rebuild and measure the V2 index.

## Slice 3 — Runtime/deployment verification

- Run loader/tool smoke checks.
- Deploy only after local validation.
- Verify V2 semantic tool output and cache manifest remotely.

## Stop condition

Stop before Moshe implementation and report remaining semantic limitations.
