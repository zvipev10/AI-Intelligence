# QA Review

## Capability

Cellular Calls raw data source

## Related issue

Draft: `issues/qa-review.md`

## Review status

Pending human review

## Role action

| Role | Status | Required action | Due before |
|---|---|---|---|
| QA | AI-prepared draft | Approve or request changes | Coding |

## What changed since previous review

Initial QA strategy.

## Context reviewed

Dataset generator, dynamic catalog, public-event projection, viewer routing/media support, localization, and mobile layouts.

## Acceptance criteria review

Criteria are measurable after the open audio/location decisions are approved.

## Test strategy

Combine deterministic data assertions, API contract tests, static asset validation, browser component tests, and desktop/mobile visual smoke testing in both locales.

## Happy path tests

- Catalog lists the localized source and expected count.
- Opening a call shows both parties exactly once.
- Audio loads and plays.
- Search and object retrieval expose all call fields.
- Nine-record chain is discoverable across the three scenario locations.

## Edge cases

- Missing audio URL/file.
- Missing party field.
- Same canonical area with different sectors.
- Long Hebrew transcript and numeric bidi content.
- Reopening different call records stops/replaces the previous media context.

## Negative tests

- Reject duplicate call IDs.
- Reject identical Side A/Side B identity in a linked call.
- Reject linked records outside the three requested locations.
- Confirm cellular records do not activate the UAV viewer.
- Confirm non-cellular records do not show call sections.

## Regression areas

Raw catalog counts, CSV parsing, UAV video viewer, generic audio/image media, evidence layer, assessment viewer, map/table/timeline presentation, and English fallback translation.

## Automation suggestions

- Generator invariant test for 24 total and 3×3 linked distribution.
- WAV header/file-existence test for every `audio_url`.
- DOM assertions for viewer classification and deduplication.
- API snapshot additions for call fields.

## Test data needs

One repeated synthetic Side A identity, nine unique Side B identities, three sector pairs per location, and 15 unrelated background calls.

## Environment needs

Local test server and deployed static asset path with MIME support for WAV.

## Open questions

Whether production smoke testing must include iOS Safari audio playback. Recommendation: yes, given the mobile demo usage.

## QA recommendation

Approve after the product decisions are recorded; require iOS/mobile smoke verification before deployment.
