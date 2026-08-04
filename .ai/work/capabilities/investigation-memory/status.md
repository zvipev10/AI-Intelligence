# Capability Status

## Capability
Investigation Memory (`investigation-memory`)

## Current Phase
Checkpoint 006 deployed; final user validation.

## Overall Status
The investigation-isolation fix is deployed and validated. Startup no longer adopts a stale investigation ID from workstream fallback and no longer resets historical playback.

## Who Needs To Act Now

| Role | Status | Required Action | Due Before |
|---|---|---|---|
| Development | Complete | Investigation isolation deployed and publicly verified. | Done |
| Product | Review needed | Confirm restore/context behavior and catalog-only visual restore limitation. | Before merge |
| UX | Review needed | Confirm restored layers/filters appear as expected when switching investigations. | Before merge |
| QA | Review needed | Validate save, switch investigation, restore layers/filters, and agent context continuity. | Before merge |
| Architecture/Security | Not blocking | Review server-side persistence and authorization before productionizing. | Production |

## Current Blockers
None.

## Current Risks
- No production authorization model for server-side investigation memory yet.
- Future memory-saved layer restore must avoid persisting full row payloads.
- Slice 2 summary is deterministic and compact, not an LLM-authored narrative summary.
- Slice 3 saves layer/filter metadata only; it does not persist full layer rows.
- Slice 4 visually reopens catalog-backed saved layers only; result-derived saved layers remain available to the agent as context.

## Next Expected Artifact
Review of `checkpoint-004.md` and `checkpoint-005.md`, then final QA/acceptance.

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
Checkpoint 006 makes the browser-selected investigation authoritative: workstream loading uses an exact investigation ID and application boot performs no playback reset.
