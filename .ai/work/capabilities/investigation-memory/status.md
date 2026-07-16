# Capability Status

## Capability
Investigation Memory (`investigation-memory`)

## Current Phase
Slice 2 developer review.

## Overall Status
Slice 2 manual chat/result memory save is implemented and ready for developer/product review. Product decisions remain: memory updates are manual only, memory is stored server-side, and selecting an investigation later should load memory and reopen memory-saved layers with their filters.

## Who Needs To Act Now

| Role | Status | Required Action | Due Before |
|---|---|---|---|
| Development | Review needed | Review Slice 2 manual save-to-memory UI and API append endpoint. | Before Slice 3 |
| Product | Review needed | Confirm the explicit save-to-memory action and compact summary shape match MVP intent. | Before Slice 3 |
| UX | Review needed | Review final-answer action placement and button copy. | Before Slice 3 |
| QA | Not blocking | Review persistence and restore checklist before restore slice. | Slice 4 |
| Architecture/Security | Not blocking | Review server-side persistence and authorization before productionizing. | Production |

## Current Blockers
None.

## Current Risks
- No production authorization model for server-side investigation memory yet.
- Future memory-saved layer restore must avoid persisting full row payloads.
- Slice 2 summary is deterministic and compact, not an LLM-authored narrative summary.

## Next Expected Artifact
Review of `checkpoint-002.md`, then Slice 3 manual layer memory save.

## Parent Issue
Not created yet. Local issue body can be added if this capability continues beyond Slice 1.

## Child Issues

| Local Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| TBD | Development | Server memory store foundation. | Complete in `checkpoint-001.md`; approved | No |
| TBD | Development/Product/UX | Manual chat/result save to investigation memory. | Complete in `checkpoint-002.md`; awaiting review | No |

## Latest Change Since Previous Review
Slice 2 added an explicit final-answer action that appends a compact chat/result summary to server-side investigation memory.
