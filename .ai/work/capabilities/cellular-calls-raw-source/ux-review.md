# UX Review

## Capability

Cellular Calls raw data source

## Related issue

Draft: `issues/ux-review.md`

## Review status

Pending human review

## Role action

| Role | Status | Required action | Due before |
|---|---|---|---|
| UX | AI-prepared draft | Approve or request changes | Coding |

## What changed since previous review

Initial viewer proposal.

## Context reviewed

Current side-drawer raw viewer, mobile screenshots, RTL/LTR placement, generic media player, and UAV specialized section.

## User flow

Open catalog → select Cellular Calls → inspect map/table/timeline → open a call → compare Side A and Side B → play recording → inspect transcript and provenance → return to results.

## UI states

- Header: source badge, call ID, start time, duration, simulation badge.
- Party section: Side A and Side B cards with phone, IMEI, canonical location, and sector.
- Recording section: native audio controls with localized simulation label.
- Transcript/summary section.
- Collapsible technical/source metadata.

## Empty states

Missing values display localized “Unknown”; missing transcript omits the section; unavailable audio retains metadata and shows a localized unavailable state.

## Error states

Audio load failure is confined to the recording section and offers retry through native controls; the viewer remains usable.

## Disabled/loading states

Player shows metadata loading without blocking record details. No autoplay.

## Copy / terminology

- Hebrew source: `שיחות סלולר`
- English source: `Cellular Calls`
- `צד א׳` / `Side A`, `צד ב׳` / `Side B`
- `הקלטת שיחה מדומה` / `Simulated call recording`
- `אזור` / `Area`, `מגזר תא` / `Cell sector`

## Accessibility notes

Use semantic headings, explicit party labels, keyboard-operable native audio controls, sufficient contrast, and non-color-only differentiation between parties.

## UX edge cases

- On narrow screens, cards stack in logical A-then-B order.
- In RTL, labels and layout align naturally without reversing the semantic A/B sequence.
- IMEIs and numbers use LTR isolation inside Hebrew content.
- Long transcript text wraps and does not create horizontal scrolling.

## Product questions

Should the transcript be expanded by default for the demo? Recommendation: yes, because generated non-speech audio cannot convey the scenario alone.

## Developer questions

Can the generic metadata field list exclude fields already consumed by the specialized viewer to prevent duplication?

## Review recommendation

Approve with transcript expanded by default and with explicit area-versus-sector wording.
