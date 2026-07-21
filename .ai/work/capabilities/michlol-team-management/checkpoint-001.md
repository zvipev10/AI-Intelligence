# Checkpoint 001 - Static מכלול Team Strip

## Date

2026-07-17

## Scope

Implemented Slice 1 of `מכלול`: a static predefined investigation team list with generated pictures, displayed compactly near the investigation-name combo.

## What changed

- Generated five consistent local avatar assets:
  - `llm_investigation_orchestrator_serbia_poc/assets/michlol/moshe.png`
  - `llm_investigation_orchestrator_serbia_poc/assets/michlol/talia.png`
  - `llm_investigation_orchestrator_serbia_poc/assets/michlol/naama.png`
  - `llm_investigation_orchestrator_serbia_poc/assets/michlol/gadi.png`
  - `llm_investigation_orchestrator_serbia_poc/assets/michlol/yahli.png`
- Added read-only `מכלול` list markup beside the investigation combo.
- Added compact avatar/name chip styling and responsive wrapping.
- Added initials fallback for broken avatar images.
- Bumped stylesheet cache version from `styles.css?v=81` to `styles.css?v=82`.

## Product behavior

The header now presents the approved predefined users:

- משה - קצין מטרות
- טליה - קצינת תמא
- נעמה - קצינת שטח
- גדי - קצין איסוף
- יהלי - קצין עיבוד

The list is static/read-only and does not assign users to investigations.

## Decisions

- Store generated pictures as local project assets.
- Keep Slice 1 independent from backend, authentication, investigation memory, and agent behavior.
- Keep visible text compact: show first name, expose role in tooltip/ARIA label.

## Tests/checks

- `git diff --check` passed.
- Verified all five generated avatars are valid `256x256` RGB PNG files.
- Static HTTP smoke from `http://127.0.0.1:8770/` confirmed:
  - index serves `styles.css?v=82`
  - index contains the `michlol-team` strip
  - all five avatar URLs return HTTP 200
  - stylesheet contains the expected `michlol-*` rules
- Edge/Playwright browser smoke using local Edge executable confirmed:
  - desktop viewport has 5 members
  - mobile viewport has 5 members
  - all five images load in-browser
  - team strip remains inside the header on desktop and mobile
  - investigation combo input focus and add button remain usable

Note: browser smoke against the static server reported expected 404 console messages for API/server-backed resources that are not served by `python -m http.server`; these were not related to the new `מכלול` assets.

## Incomplete

- No per-investigation team selection.
- No real users.
- No agents.
- No team persistence.

## Review needed

Product/UX should review the compact placement near the investigation-name combo.

QA should validate desktop/mobile header behavior and avatar loading.
