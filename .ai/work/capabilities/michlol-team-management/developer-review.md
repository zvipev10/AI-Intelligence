# Developer Review - מכלול Team Management

## Review status

Approved for execution planning and Slice 1 implementation.

## Reviewer/source of input

AI developer review based on Product-approved scope from `product-review.md` and current UI structure.

## Feasibility

The MVP is low-risk because it can be implemented as a static, read-only UI addition near the existing investigation-name combo.

No backend, authentication, permission, or investigation persistence change is required for Slice 1.

## Likely affected files

- `llm_investigation_orchestrator_serbia_poc/index.html`
- `llm_investigation_orchestrator_serbia_poc/styles.css`
- `llm_investigation_orchestrator_serbia_poc/assets/michlol/*.png`

## Data shape

Use stable ids that can later map to real users or agents:

| id | display_name | role_label | member_type | avatar |
|---|---|---|---|---|
| `moshe-targets-officer` | משה | קצין מטרות | `user` | local PNG |
| `talia-tama-officer` | טליה | קצינת תמא | `user` | local PNG |
| `naama-field-officer` | נעמה | קצינת שטח | `user` | local PNG |
| `gadi-collection-officer` | גדי | קצין איסוף | `user` | local PNG |
| `yahli-processing-officer` | יהלי | קצין עיבוד | `user` | local PNG |

For Slice 1 this can live directly in markup. If later slices need selection, assignment, or server memory, move the same shape into a small JS constant or backend endpoint.

## Recommended approach

- Add a compact `מכלול` member strip inside the existing investigation switcher.
- Keep the row read-only.
- Use local generated PNG assets under `assets/michlol/`.
- Include initials fallback for broken/missing images.
- Bump CSS cache version in `index.html`.

## Technical risks

- Header width pressure on desktop/tablet because the investigation switcher already occupies the center grid column.
- Mobile wrapping may increase header height.
- Generated pictures are static assets; future real user photos will need a different source.

## Test strategy

- Static check: `git diff --check`.
- Browser smoke: load UI, confirm the `מכלול` row renders near the investigation combo.
- Verify avatar images return HTTP 200 from local server.
- Mobile viewport smoke for header wrapping.
- Regression glance: investigation combo still opens and create button remains usable.

## Proposed execution slices

1. Slice 1: static predefined team list, generated local avatars, compact header UI.
2. Slice 2: optional per-investigation team selection/persistence if Product asks for it.
3. Slice 3: future real users/agents integration after identity/agent semantics are defined.
