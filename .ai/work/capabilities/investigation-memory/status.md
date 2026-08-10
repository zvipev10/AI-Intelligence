# Capability Status

## Capability
Investigation Memory (`investigation-memory`)

## Current Phase
Checkpoint 008 implementation complete; Product review before deployment.

## Overall Status
Newly saved result-derived layers now carry a reconstruction definition and can be resolved through the standard typed-layer presentation path. Agent requests can return structured saved-layer presentation actions. Existing context-only memory is intentionally not migrated.

## Who Needs To Act Now

| Role | Status | Required Action | Due Before |
|---|---|---|---|
| Development | Complete | Saved result-layer reconstruction implementation is ready. | Done |
| Product | Review needed | Review Checkpoint 008 and authorize deployment. | Before deployment |
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
Product review of `checkpoint-008-saved-layer-presentation.md`, followed by deployment authorization or requested changes.

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
Checkpoint 008 implements reconstructable saved result layers and structured agent-driven presentation without migration or new tests.
