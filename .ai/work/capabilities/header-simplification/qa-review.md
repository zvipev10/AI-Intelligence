# QA Review

## Capability

Compact upper-section controls

## Review status

Ready for execution by explicit user delegation

## Test strategy

- Static DOM assertions for compact language/status markup and localized accessible text.
- Browser validation in Hebrew and English at desktop and responsive widths.
- Keyboard focus and pointer hover validation for status detail surfaces.
- Runtime verification of dataset ready/failure and Hermes connected/demo state mappings.
- Post-deployment service, API status, HTML asset-version, and public HTTPS checks.

## Regression areas

- RTL switch-thumb direction.
- Existing locale persistence and `?lang=` URL behavior.
- Header grid width and mobile stacking.
- Existing `datasetStatus` and `agentStatus` dynamic updates.

## Acceptance recommendation

Proceed with a focused header-only implementation and require passing local plus VM smoke checks.
