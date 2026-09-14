# Capability brief: I360 application migration

## Status

Ready for implementation planning. Product direction was supplied by the user on 2026-09-14.

## Problem

The application reads evidence, locations, entities, semantic indexes, and target records from local stores. This prevents it from using I360 as the governed source of intelligence data and makes the current demo data contracts part of the runtime architecture.

## Goal

Run the existing investigation experience on I360 data while preserving the current map, timeline, catalog, object viewer, chat, investigation tools, and target-candidate workflows.

## Users and expected behavior

Analysts should be able to:

- search and browse authorized I360 items using text, semantic, temporal, geographic, source, and entity constraints;
- open source details and media with stable citations;
- use the current investigation tools over the same authorized I360 population;
- save and reopen investigations, memory, layers, questions, and target candidates where the approved I360 model supports them;
- see explicit degraded states when an I360 capability is unavailable or a query is incomplete.

## Scope

- I360 authentication and identity forwarding through the application server.
- A provider interface with local and I360 implementations during migration.
- Canonical mapping between I360 items/entities and current event, location, entity, layer, and object-view contracts.
- Evidence search, retrieval, aggregation, context, media, and entity lookup.
- Existing reasoning tools operating over the I360 provider.
- Investigation state, saved questions/layers/memory, and target candidates after their I360 schemas and access rules are approved.
- Frontend integration through the existing application API.
- English and Hebrew behavior, permissions, observability, fallback, and controlled cutover.

## Explicit non-goals

- Workstream UI, APIs, MCP tools, artifacts, persistence, notifications, or migration.
- Scenario playback, Next/reset behavior, or playback-driven reevaluation.
- Replacing Hermes, General, or Moshe with I360 Agentic Studio.
- Building an ingestion pipeline through the high-level API.
- Unrelated frontend redesign.

Existing Workstream code may remain in the repository, but no implementation slice may modify or depend on it. The migrated runtime must be testable with Workstream disabled.

## Functional acceptance criteria

1. An ordinary user sees only I360 items and entities they are authorized to access.
2. Search, map, timeline, catalog, object viewer, and media access use I360-backed records and preserve stable source references.
3. Current non-Workstream investigation tools return evidence-grounded results over I360 and expose incomplete or degraded retrieval.
4. Saved investigation state and target candidates can be reopened with intact evidence references, or remain on the current store behind an explicitly approved temporary boundary.
5. English and Hebrew queries and displayed source text pass representative acceptance samples.
6. The application can switch between local and I360 providers by configuration until cutover is accepted.
7. I360 outages, expired authentication, missing embeddings, unsupported geo operations, and partial results produce actionable UI/API states.
8. Workstream and playback are absent from migration acceptance and do not block release.

## Assumptions

- Required source data is already ingested into the target I360 estate by a platform-owned process.
- The application server can hold or forward an approved I360 credential without exposing it to browser code.
- Existing frontend contracts are the compatibility boundary for the first migration release.
- I360 feature availability will be discovered at runtime and verified with ordinary-user accounts.

## Blocking inputs for production cutover

- Target I360 environment, authentication method, and test identities.
- Representative item/entity IDs and permission scenarios.
- Confirmed field mapping for reliability, certainty, source, location, entity links, original text, translations, and media.
- Decision on storage and concurrency for investigation state and target candidates.

## Evidence

- `docs/reviews/i360-frontend-feasibility.md`
- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/target_bank.py`
