# Checkpoint 002 — Rendering correction

## User findings addressed
1. Opening the 4,165-row evidence layer could overload per-item DOM marker rendering and appear to refresh the application.
2. Raw event layers still used MIL-STD symbology despite raw records being provenance rather than normalized evidence.

## Changes
- Raw event layers now aggregate into neutral location dots.
- Focusing an individual raw record also uses a neutral marker.
- MIL-STD rendering remains for normalized evidence and entity presence layers.
- Equivalent evidence descriptors are coalesced by location, symbol, icon, and affiliation.
- Evidence map rendering is capped at 400 groups; table, timeline, viewer, and provenance retain every row.

## QA
- Focused evidence/MIL-STD/viewer/catalog suite: 32 passed.
- JavaScript syntax and diff checks passed.
