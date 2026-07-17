# Product Review - מכלול Team Management

## Review status

Approved for developer, UX, and QA review.

## Reviewer/source of input

Human Product input from 2026-07-17.

## Product definition

`מכלול` is a team/workgroup that works with the analyst on investigations.

For the MVP:

- Use a predefined set of five users.
- Each user has a name and generated picture.
- Display the list compactly near the investigation-name combo.
- Future direction should allow real users or agents, but the MVP does not implement those.

## Predefined users

| Stable id | Display name | Role label | Member type | Picture |
|---|---|---|---|---|
| `moshe-targets-officer` | משה | קצין מטרות | `user` | Generate picture |
| `talia-tama-officer` | טליה | קצינת תמא | `user` | Generate picture |
| `naama-field-officer` | נעמה | קצינת שטח | `user` | Generate picture |
| `gadi-collection-officer` | גדי | קצין איסוף | `user` | Generate picture |
| `yahli-processing-officer` | יהלי | קצין עיבוד | `user` | Generate picture |

## Product decisions

- MVP team list is predefined.
- MVP placement is near the investigation-name combo.
- Pictures should be generated for all five predefined users.
- Real users and agents are future-compatible model concerns, not MVP behavior.

## Clarifications still needed

No blocking product clarification is required before developer and UX review.

Non-blocking details for implementation planning:

- Generated picture style.
- Exact compact layout near the investigation-name combo.
- Whether to reserve a distinct visual style for future agents.

## Handoff to UX

Define the compact list presentation near the investigation-name combo, including avatar size, name/role visibility, overflow behavior, broken-image fallback, and mobile behavior.

## Handoff to development

Review the simplest static member data shape and asset strategy for generated pictures while preserving future support for real users and agents.
