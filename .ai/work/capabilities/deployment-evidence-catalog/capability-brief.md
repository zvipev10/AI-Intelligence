# Capability Brief — Deployment Evidence Catalog

## Goal
Precompute a versioned evidence catalog from the fixed demo dataset during UI deployment and expose it as a normal, demand-opened layer.

## Accepted product decision
The evidence layer is part of the layer catalog. It does not open automatically and does not imply that every item is fused or verified.

## Semantics
- Every canonical raw record projects to one `reported` or `observed` evidence row with a `REC-*` provenance reference.
- Deterministic fusion is attempted only within a canonical location, entity, structured object class, and six-hour bucket.
- Public reports may join a structured group only when they contain an exact known object-class term.
- A fused row requires at least two independent supporting source groups and medium/high confidence.
- Ambiguous or rejected groups remain projected evidence; they are never silently upgraded.

## Acceptance criteria
- Deployment creates a reproducible v2.1 evidence catalog for Hebrew and English.
- Catalog exposes `evidence:all` with map, table, and timeline capabilities.
- Opening the layer performs no semantic search or live fusion.
- Evidence rows retain source record IDs and statuses.
- The Ibar Bridge catalog query completes locally without model/MCP work.

## Non-goals
- Talia assessments.
- Automatic target creation.
- Continuous ingestion or incremental production processing.
- Claimed external MIL-STD certification.
