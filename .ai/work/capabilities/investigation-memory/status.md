# Capability Status

## Capability
Investigation Memory (`investigation-memory`)

## Current Phase
Slice 3 developer/product/UX review.

## Overall Status
Slice 3 manual layer memory save is implemented and ready for developer/product/UX review. Product decisions remain: memory updates are manual only, memory is stored server-side, and selecting an investigation later should load memory and reopen memory-saved layers with their filters.

## Who Needs To Act Now

| Role | Status | Required Action | Due Before |
|---|---|---|---|
| Development | Review needed | Review Slice 3 manual layer memory save API and tab action. | Before Slice 4 |
| Product | Review needed | Confirm explicit layer-save action and saved layer metadata shape. | Before Slice 4 |
| UX | Review needed | Confirm layer tab bookmark action and final-answer memory button styling correction. | Before Slice 4 |
| QA | Not blocking | Review persistence and restore checklist before restore slice. | Slice 4 |
| Architecture/Security | Not blocking | Review server-side persistence and authorization before productionizing. | Production |

## Current Blockers
None.

## Current Risks
- No production authorization model for server-side investigation memory yet.
- Future memory-saved layer restore must avoid persisting full row payloads.
- Slice 2 summary is deterministic and compact, not an LLM-authored narrative summary.
- Slice 3 saves layer/filter metadata only; it does not persist full layer rows.

## Next Expected Artifact
Review of `checkpoint-003.md`, then Slice 4 load memory and reopen saved layers.

## Parent Issue
Not created yet. Local issue body can be added if this capability continues beyond Slice 1.

## Child Issues

| Local Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| TBD | Development | Server memory store foundation. | Complete in `checkpoint-001.md`; approved | No |
| TBD | Development/Product/UX | Manual chat/result save to investigation memory. | Complete in `checkpoint-002.md`; product comment addressed | No |
| TBD | Development/Product/UX | Manual layer/filter save to investigation memory. | Complete in `checkpoint-003.md`; awaiting review | No |

## Latest Change Since Previous Review
Slice 3 added an explicit layer-tab action that appends saved layer/filter metadata to server-side investigation memory. Product feedback from Slice 2 was addressed by making the final-answer memory button visually match the neighboring final-answer buttons.
