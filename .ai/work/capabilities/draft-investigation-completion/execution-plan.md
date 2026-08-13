# Execution Plan

## Capability

Complete draft investigation creation

## Plan status

Approved by explicit Product decisions

## Prerequisite review gate

- Product brief: approved
- Developer review: ready
- UX review: approved by Product decisions
- QA review: ready
- Architecture/Security: not required
- Blocking questions: resolved

## Goal

Keep draft exploration independent of investigation persistence until explicit creation or the first investigation-memory save.

## Approved scope

- Ephemeral draft session with stable ID.
- Draft-only create button replacing selector/team controls.
- Compact name modal with welcome-style participants.
- Unique-name validation.
- Register the same draft ID on creation.
- Resume one pending layer or result-memory save.
- Do not load workstreams, playback, or memory for drafts.

## Non-goals

Real invitations, participant selection/persistence, backend schema changes, or changes to saved-run behavior.

## Proposed approach

Keep `draftSessionActive` outside the registry. Starting from welcome resets the workspace onto a new ephemeral ID without registry writes or investigation-owned loads. Toggle the header into a single create action. Convert by validating and registering a unique name, then adding the normal local record. Memory saves intercept drafts and retain one single-use continuation.

## Files/services likely affected

`index.html`, `styles.css`, `app.js`, UI tests, deployment manifest/docs, and capability artifacts.

## Data/API changes

None; reuse `POST /api/investigations` and current memory endpoints.

## Test plan

Contract tests, full POC suite, JavaScript syntax, diff check, and bilingual Edge interaction checks.

## Execution slices

### Slice 1

Goal: Implement the approved lifecycle coherently.

Expected changes: draft state, header toggle, modal, validation, registration, pending saves, and tests.

Risk: Medium.

Reviewer: Product/UX/QA.

Stop after slice: Yes, before deployment.

## Stop conditions

Any need for participant persistence, API/schema changes, or loss of workspace state.

## Rollback/fallback notes

Revert the UI commit; existing server endpoints remain compatible.

## Required approval before implementation

Satisfied by the user’s explicit approvals.
