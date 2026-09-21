# Execution Plan

## Capability

Cellular Calls raw data source

## Related issues

Local issue drafts under `issues/`; remote issues are not required for this execution.

## Plan status

Approved

## Role actions

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | In progress | Execute slices and record checkpoints | Final QA |
| UX | Approved | Verify responsive localized viewer | Slice 2 completion |
| QA | Approved | Execute automated and manual checks | Handoff |
| Product | Approved | Review final capability | Merge/deploy |

## What changed since previous review

The user corrected Side B semantics to a different existing location in Kosovo and approved implementation on top of `2fe94be`.

## Prerequisite review gate

- Product brief: approved through explicit implementation approval
- Developer review: Approved
- UX review: Approved
- QA review: Approved
- Architecture/Security review: synthetic-only constraint accepted
- Blocking questions resolved or accepted as assumptions: 24 calls and generated simulated audio with transcript accepted

## Goal

Deliver a localized raw Cellular Calls source with a repeated Side A trail across the three scenario locations, independently located Side B endpoints, playable recordings, full retrieval support, and a dedicated raw viewer.

## Context used

Capability brief, role reviews, current event projection, dynamic catalog layer creation, MCP public event projection, record viewer/media behavior, dataset generator, and existing test patterns.

## Approved scope

Dataset and audio generation, additive raw-event fields, localized catalog behavior, MCP retrieval, specialized responsive viewer, tests, and capability handoff artifacts.

## Non-goals

Live interception, real subscriber data, external TTS, new evidence/fusion semantics, automatic assessments, or automatic layer presentation.

## Proposed approach

Generate deterministic call records and WAV assets from the V2.1 generator, append nullable call columns to the shared projection, expose fields through the public event contract, and route cellular records to a dedicated viewer section while preserving standard map/table/timeline behavior.

## Files/services likely affected

V2.1 generator and projections, static audio assets, MCP public event projection, UI JavaScript/CSS, and focused test modules.

## Data/API changes

Add `call_id`, `call_started_at_utc`, `call_duration_seconds`, Side A/B phone, IMEI and location IDs, `audio_url`, and `call_transcript`. Existing records receive blank values.

## UX changes

Add a cellular-call raw viewer with two endpoint cards, simulation badge, timing, recording player, transcript, provenance, localized labels, mobile stacking, and numeric bidi isolation.

## Test plan

Validate generator determinism and chain distribution, identifier/location constraints, WAV validity, catalog localization, public event fields, viewer classification/rendering, missing-value handling, and non-cellular regressions.

## Execution slices

### Slice 1

Goal: Dataset, media, and API contract.
Expected changes: generator, projections, WAV assets, public event fields, data/API tests.
Risk: Medium—shared event schema.
Reviewer: Development/QA.
Stop after slice? No; record checkpoint and continue under explicit approval if tests pass.

### Slice 2

Goal: Dedicated viewer and localization.
Expected changes: cellular record detection, endpoint layout, recording/transcript, CSS, UI tests.
Risk: Medium—responsive raw viewer.
Reviewer: UX/QA.
Stop after slice? No; record checkpoint and continue under explicit approval if tests pass.

### Slice 3

Goal: Integrated verification and handoff.
Expected changes: end-to-end/regression results, final artifacts, documentation notes.
Risk: Low.
Reviewer: Product/QA.
Stop after slice? Yes—merge/deploy remains a separate explicit action.

## Stop conditions

Stop if shared-schema regressions appear, media cannot be served reliably, unrelated base changes conflict, or implementation would require new fusion/assessment behavior.

## Rollback/fallback notes

The source is additive. Rollback removes call rows/assets/fields and the viewer branch without changing existing records. If audio serving fails, retain metadata/transcript and show the localized unavailable state.

## Required approval before implementation

Granted by the user on 2026-09-21 for implementation on top of commit `2fe94be`.
