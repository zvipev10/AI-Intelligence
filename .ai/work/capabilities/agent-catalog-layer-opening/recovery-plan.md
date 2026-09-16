# Catalog-layer recovery — 2026-09-16

## Scope and authorization
User accepted the proposed recovery behavior and explicitly requested implementation.
Extend the existing capability; no unrelated I360 changes. Existing main backend hashes match production. Production app.js has one extra error log, which will be retained.

## Developer and UX review
AI implementation assessment: use the authoritative UI catalog at tool time, with a shared deterministic resolver for gateway defense. Exact ID wins; normalized labels/explicit aliases and conservative typo matching may recover a unique result. Similar candidates require clarification. Never pick across an explicit layer family. Fail closed when catalog retrieval fails.
Support explicit raw-layer location/entity/time/event filters. Canonicalization cannot discard them. Agent instructions must carry conversation constraints forward and must treat tool results as pending UI execution, not confirmed opening. Browser displays a success only after loading records, and keeps errors visible.
No new dependencies or permissions. Catalog HTTP lookup uses the existing localhost UI service and a bounded timeout. No inferred geographic expansion.

## QA review and execution slices
1. Resolver/tool: exact, Hebrew final-letter/quote variants, aliases, ambiguous near-matches, unrelated names, unavailable catalog, malformed requests. Publish checkpoint.
2. Filters/UI: validate filters, preserve through gateway, load bounded rows, distinguish filtered/unfiltered layers, retain saved filter semantics and explicit errors. Node browser-function tests plus Python regression.
3. Release: review diff, publish commits/draft PR, back up only affected production files, deploy, validate live catalog and the 492-record border scope, verify browser UI, record rollback/handoff.

## Assumptions and risks
An unambiguous typo is recoverable; semantic similarity alone is insufficient. Ambiguous requests must ask the analyst, not silently open multiple layers. A tool can queue an opening but cannot truthfully claim browser completion. New matching uses conservative thresholds and canonical candidates from the catalog only.
