# Checkpoint 003 - Compact Header Correction

## Date

2026-07-17

## Scope

Product requested a more compact upper header presentation after reviewing the deployed `מכלול` Slice 1 build.

## Requested correction

1. Put Hermes status and DB status one under the other.
2. Change the name from `סביבת חקירה` to `סביבת מודיעין`.
3. Narrow the active-investigation combo by about half and align `חקירה פעילה` vertically with the combo.
4. Put `מכלול` and names nearby, not underneath.
5. Show the first 3 teammates and use a three-dot sign to expand and see the others.

## What changed

- Renamed the page title and header title to `סביבת מודיעין`.
- Bumped stylesheet cache version from `styles.css?v=82` to `styles.css?v=83`.
- Reduced desktop header height from 92px to 68px.
- Shortened the investigation combo to a 250px desktop track.
- Aligned `חקירה פעילה` with the combo.
- Moved `מכלול` inline beside the combo.
- Kept only the first three teammates visible:
  - משה
  - טליה
  - נעמה
- Added native `details/summary` three-dot expansion for:
  - גדי
  - יהלי
- Stacked dataset and Hermes status into two status lines.

## Validation

- `git diff --check` passed.
- Static HTTP smoke confirmed:
  - `styles.css?v=83`
  - `סביבת מודיעין`
  - `michlol-more`
  - stacked status lines
- Static CSS smoke confirmed:
  - 250px combo track
  - `michlol-more` rules
  - stacked `header-status`
  - workspace height based on 68px header
- Edge/Playwright smoke with local Edge executable confirmed desktop, tablet, and mobile:
  - title is `סביבת מודיעין`
  - header is 68px on desktop/tablet
  - combo is 250px desktop and 220px tablet
  - `חקירה פעילה` is vertically aligned with combo
  - status has two lines
  - only the first three teammates are visible before expansion
  - ellipsis expands to show גדי and יהלי

Note: browser smoke against the static server reported expected 404 console messages for API/server-backed resources that are not served by `python -m http.server`; these were unrelated to the header correction.

## Review needed

Product/UX/QA should review the corrected compact header after VM deployment.
