# QA Review

## Status

Approved for execution under the user's explicit direction.

## Required checks

- V1 and V2 byte hashes are unchanged.
- V2.1 generation is deterministic.
- Exactly 14,800 unique records and 3,800 UAV observations.
- At least 300 positive chains, each with distinct UAV and public collection families and two distinct public platforms.
- Positive-chain records share truth actor, location, event, and permitted observation window.
- Count descriptions include exact, approximate, and range language without forcing public structured counts.
- At least 100 evaluator-only hard negatives.
- No truth ID or truth role occurs in raw CSV, raw JSONL, UAV JSONL, or runtime projection.
- Projection remains loadable by the current MCP server.

## Regression areas

- Semantic search cache signatures and dataset selection.
- Hebrew CSV/JSON encoding.
- Entity and location referential integrity.
- Friendly-force public-only constraint.
