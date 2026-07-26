# Execution Plan — Indication Artifact MVP

## Status

Ready for human checkpoint review. Product, Development/Architecture, UX, and QA/Security prerequisites are approved. No product-code implementation is authorized until this plan is accepted.

## Related work

- Parent capability: #25
- Artifact definition: `artifact-001-target-assessment-lead.md`
- Development/Architecture review: `artifact-001-developer-review.md`
- UX review: `artifact-001-ux-review.md`
- QA/Security review: `artifact-001-qa-review.md`
- Slice 1: #41
- Slice 2: #42
- Final validation: #43

## Goal

Allow Moshe to interpret natural-language requests in the existing general chat, construct a reviewable set of `REC-...` indications around an optional `TGT-...` subject, and persist the accepted result as a revisioned workstream artifact only after a distinct user confirmation turn.

## Non-goals

- Assessment execution.
- New target creation or existing target mutation.
- Direct MCP writes to the app-server workstream store.
- Automatic monitoring or background ingestion.
- Predefined command phrases, saved expressions, dedicated composer, buttons, layer selection, or artifact screen.
- Removing the existing explicit `@משה` routing requirement.
- Production authentication or multi-user authorization.
- Investigation Memory integration or scenario playback.

## Architecture boundary

The app server owns workstream persistence. Hermes/Moshe runs with MCP tools in a separate runtime and must not write the app server's workstream files directly.

The integration therefore uses a structured handoff:

1. The browser sends the ordinary user message plus active workstream context to `/api/investigate`.
2. Existing routing sends explicit `@משה` turns to Moshe.
3. Read-only MCP tools resolve referenced events and optional target subjects and return a structured proposal.
4. The web server extracts and normalizes that proposal from the Hermes audit/result pipeline.
5. The browser renders Moshe's natural-language explanation and retains the staged proposal in conversation state; no artifact mutation occurs.
6. On a later user turn, Moshe interprets confirmation, rejection, correction, or ambiguity.
7. A bounded MCP decision tool returns a structured proposal action.
8. The web server independently validates the workstream, proposal, current revision, references, actor, and allowed action before applying it through the local artifact service.
9. The normalized response includes the committed artifact/revision or a conflict/error state for Moshe to explain.

The target bank is read-only throughout this flow.

## Data model

### Artifact envelope

- `schema_version`
- `artifact_id`
- `artifact_type`
- `status`
- `revision`
- `content`
- `created_by`
- `created_at_utc`
- `updated_at_utc`
- `revisions`

### `target_assessment_lead` content

- optional `subject_reference: {kind: "target", target_id}`
- `lead_statement`
- `indications`
- `supporting_signals`
- `contradictions`
- `assessment_questions`
- `gaps`
- `assigned_to`
- optional annotation

### Indication reference

- server-owned `indication_id`
- `source_reference: {kind: "event_record", layer_id, record_id}`
- observed claim and observation time from the resolved source
- provenance summary
- relevance
- role: `supports`, `contradicts`, or `context`
- annotation
- contributor and timestamp
- state: `active` or `removed`

### Revision entry

- server-owned revision number and timestamp
- actor participant/kind
- action
- prior revision
- bounded change summary
- attributable user-turn reference when the action required confirmation

## Local app-server API

- `GET /api/workstreams/{workstream_id}/artifacts`
- `POST /api/workstreams/{workstream_id}/artifacts`
- `GET /api/workstreams/{workstream_id}/artifacts/{artifact_id}`
- `POST /api/workstreams/{workstream_id}/artifacts/{artifact_id}/revisions`

Every mutation includes `expected_revision`. Stale writes return `409` with the current artifact revision. The server owns IDs and timestamps and rejects archived workstreams.

Supported actions:

- create accepted artifact from a confirmed proposal;
- add/remove indication;
- update annotation or lead framing;
- record contradiction/gap/question changes;
- reject proposal;
- request completion;
- mark `ready_for_assessment`.

`ready_for_assessment` is a status only and invokes nothing.

## MCP proposal contract

Add read-only/non-persisting tools:

- `prepare_workstream_indication_proposal`
  - input: workstream objective/context, `REC-...` identifiers, optional `TGT-...`, current artifact summary;
  - resolves references and returns structured proposal, unresolved references, contradictions, gaps, and explanation;
  - never creates an artifact or target.

- `decide_workstream_indication_proposal`
  - input: staged proposal, current revision, current user turn, intended decision;
  - returns a structured `confirm`, `reject`, `correct`, `clarify`, or `send_to_assessment` action;
  - never persists state.

The app server treats all MCP output as untrusted input and revalidates it before local persistence.

## Moshe instruction changes

Moshe must:

- interpret ordinary natural language rather than match predefined expressions;
- treat `REC-...` as evidence and optional `TGT-...` as subject, never evidence;
- resolve references with tools before making claims;
- distinguish observation, inference, contradiction, and gap;
- propose before persistence;
- require a distinct later user turn before a write;
- ask for clarification when confirmation is ambiguous;
- explain that `ready_for_assessment` does not mean assessed or targeted;
- never call target create/update tools from this artifact workflow.

The current explicit `@משה` routing remains unchanged.

## Result-envelope changes

Extend the shared agent result contract with validated optional fields:

- `workstream_proposal`
- `workstream_action`
- `workstream_artifact`
- `workstream_conflict`

Keep these generic at the envelope level. Type-specific payload validation belongs to the artifact registry.

## Slice 1 — Artifact persistence and API

Issue: #41

Changes:

- add a focused artifact service/module;
- implement generic envelope and type registry;
- implement the first content validator;
- resolve `REC-...` from the attached event layer;
- resolve optional `TGT-...` read-only from the target catalog;
- add optimistic revisions, append-only history, atomic writes, and APIs;
- initialize existing workstreams safely when artifact fields are absent;
- add focused API/service tests.

Risk: Medium — changes persistent state and API.

Checkpoint reviewer: Development/Architecture and QA/Security.

Stop after slice: Yes.

## Slice 2 — Moshe general-chat integration

Issue: #42

Prerequisite: accepted Slice 1 checkpoint.

Changes:

- add non-persisting MCP proposal/decision tools and schemas;
- add Moshe instructions and evaluation fixtures;
- pass bounded active-workstream context into Moshe turns;
- normalize proposal/action audit results into the shared result envelope;
- stage proposals without artifact mutation;
- apply confirmed actions only after a distinct later user turn and independent app-server validation;
- render explanations, previews, ambiguity, conflicts, success, and errors in ordinary chat;
- preserve current indicator and existing `@משה` routing;
- add tool-boundary, pipeline, routing, chat, and regression tests.

Risk: High — changes agent behavior, cross-runtime contracts, and UX.

Checkpoint reviewer: Product, Development/Architecture, UX, and QA/Security.

Stop after slice: Yes.

## Final validation

Issue: #43

- run all artifact API/service tests;
- run existing workstream, routing, result-pipeline, target-bank, Investigation Memory, and UI regressions;
- evaluate varied natural-language proposals, confirmations, rejections, corrections, and ambiguous replies;
- verify proposal turns do not persist;
- verify distinct confirmation turns do persist exactly once;
- verify stale revisions return conflict without lost updates;
- verify `TGT-...` never counts as evidence;
- verify no artifact path writes target-bank data;
- restart/refresh and reopen the accepted artifact;
- execute the historical demo flow using real stale-dataset `REC-...` and optional `TGT-...` references.

## Rollback

- Artifact APIs and service are additive.
- Existing workstreams with empty/missing artifacts remain readable.
- Moshe artifact tools can be removed from the profile/tool list independently.
- Result-envelope fields are optional and ignored by older clients.
- No migration or rollback touches Investigation Memory, raw layers, or target-bank records.

## Accepted assumptions

- This is a bounded synthetic single-user demo.
- Client/user attribution is auditable metadata, not production authorization.
- Explicit `@משה` remains the route to Moshe in general chat.
- A staged proposal may be lost on refresh before confirmation; only accepted artifacts are durable in this MVP.

## Checkpoint decision required

Approve or revise:

1. the structured cross-runtime handoff rather than direct MCP workstream writes;
2. the two implementation slices and their stop points;
3. the accepted non-durable pending-proposal limitation;
4. retaining explicit `@משה` routing for the MVP.

