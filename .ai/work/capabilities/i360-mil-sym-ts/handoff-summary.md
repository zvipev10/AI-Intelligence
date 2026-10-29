# Selective integration handoff

Main PR #92 merged as 10aa537: renderer plus English-only Kosovo package. i360 integration starts at 4740321 and carries renderer/adapter/vendor, map styles and own-coordinate support, cache versions, static allowlist and Docker packaging only. Existing i360 authentication, mapping, data and persistence are retained. Parent #93; child #95.

Validation: 66 fake-HL API/backend tests pass. UI discovery initially found an expected stale asset-version assertion; updated it for this release. All 13 JavaScript suites pass and all 44 actual SVG variants render using development-only native canvas. Final Python UI results are recorded in status.md. Browser verification waived; Docker image and LAMBDA deployment not run/requested.

Assumption: unclassified i360 images stay ordinary markers until explicit supported collection/object fields exist. No guessed military classification. Architecture, operations and decisions docs updated; no further documentation update required. Next: merge focused PR into feature/i360-only, then use its normal deployment process when requested.
