# Decisions — Talia Enemy Assessments

## 2026-09-16 — Assessment and evidence remain separate objects
Evidence is created by deterministic projection/fusion services. Talia creates analytical assessments that cite Evidence IDs and may add higher-order spatial conclusions. Assessment overlays are explicitly analytical and never replace or silently upgrade Evidence.

## 2026-09-16 — Controlled overlay vocabulary
The first release supports validated point, assessed-area, route/axis, and confidence-envelope features. Geometry, semantics, confidence, validity, and supporting Evidence IDs are required and rendered by the application; Talia cannot send arbitrary markup or styling.

## 2026-09-16 — Talia has no target-bank write authority
Talia may read shared evidence and assessments and request neutral fusion. Target-bank creation and mutation remain Moshe-only workflows with their existing eligibility controls.
