# Selective i360 symbology integration

User explicitly authorized merging the already-validated renderer and English Kosovo release into main, and symbology alone into feature/i360-only. Main PR #92 is merged. This work starts at i360 commit 4740321 and retains the i360 authentication, HL API, data mapping and persistence model.

Developer review: copy the pinned adapter/vendor and rendering integration; adapt static allowlist and own-coordinate records; retain unknown affiliation for observations. Do not infer object class from Satellite/ADINT source names. Do not import English Kosovo data, locale overrides, VM release machinery or AI functionality.

Execution: port renderer and CSS, load assets before app startup, bump branch-specific cache keys, add endpoint and own-coordinate tests, run required fake-HL backend and UI suites, document baseline failures if any, publish a PR targeting feature/i360-only and merge after checks. Browser verification remains waived. No production deployment requested.

Acceptance: supported classes render verified symbols, unsupported items remain ordinary markers, record viewer links and direct coordinates work, and only renderer-related files/docs/tests differ from the i360 base.
