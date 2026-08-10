# Capability Status

## Capability
Investigation Memory (`investigation-memory`)

## Current Phase
Checkpoint 011 deployed; Product validation.

## Overall Status
Server-backed investigations are hydrated and dedicated saved-layer routing is deployed. Checkpoint 011 makes restored saved filters immediately visible on the active layer and preserves saved filter fields in the selector. Automatic layer restoration remains unchanged by Product direction.

## Who Needs To Act Now

| Role | Status | Required Action | Due Before |
|---|---|---|---|
| Development | Complete | Saved-filter visibility correction is deployed and production-verified. | Done |
| Product | Review needed | Restore a filtered saved layer and confirm its filter panel and chips are visible. | Before merge |
| UX | Review needed | Confirm partial/unavailable messaging and normal-layer presentation. | Before merge |
| QA | Deferred by Product | No new tests requested for this slice; validate manually after deployment if authorized. | Before merge |
| Architecture/Security | Not blocking | Review server-side persistence and authorization before productionizing. | Production |

## Current Blockers
None.

## Current Risks
- No production authorization model for server-side investigation memory yet.
- Reconstruction stores typed IDs rather than full row payloads; a saved layer is capped at 5,000 IDs.
- Slice 2 summary is deterministic and compact, not an LLM-authored narrative summary.
- Slice 3 saves layer/filter metadata only; it does not persist full layer rows.
- Existing result-derived memory records without reconstruction metadata remain context-only because migration was explicitly excluded.

## Next Expected Artifact
Product validation of saved-filter visibility.

## Parent Issue
Not created yet. Local issue body can be added if this capability continues beyond Slice 1.

## Child Issues

| Local Issue | Role | Purpose | Status | Blocking? |
|---|---|---|---|---|
| TBD | Development | Server memory store foundation. | Complete in `checkpoint-001.md`; approved | No |
| TBD | Development/Product/UX | Manual chat/result save to investigation memory. | Complete in `checkpoint-002.md`; product comment addressed | No |
| TBD | Development/Product/UX | Manual layer/filter save to investigation memory. | Complete in `checkpoint-003.md` | No |
| TBD | Development/Product/UX/QA | Load memory and reopen saved layers. | Complete in `checkpoint-004.md`; awaiting review | No |
| TBD | Development/Product/QA | Provide saved memory to agent prompt context. | Complete in `checkpoint-005.md`; awaiting review | No |

## Latest Change Since Previous Review
Checkpoint 011 opens restored saved filters visibly and keeps saved filter fields available in the selector.
