# Checkpoint 003 — KFOR and NATO hostile symbology

## Decision
The user explicitly classified all KFOR- and NATO-related catalog entities as enemy/hostile for this scenario presentation.

## Scope
- Map `ENT-KFOR-RCE`, `ENT-KFOR-KTRBN`, `ENT-KFOR-MSU`, `ENT-KFOR-AVIATION`, and `ENT-NATO-RESERVE` to `hostile`.
- Present hostile organization symbols with a red diamond frame.
- Advance assets to `app.js?v=173` and `styles.css?v=145`.
- Add regression coverage for all five mappings and the hostile frame styling.

## Preserved behavior
- Serbian Armed Forces organization entities remain friendly.
- UAV observations remain unknown affiliation.
- Confidence, claim state, evidence traceability, and object-viewer behavior are unchanged.

## Release plan
Validate, merge directly to remote `main` under the user's explicit instruction, back up the current production assets, deploy v176, and verify the public site and service.
