# Checkpoint 004 — Propagate explicit affiliation to UAV observations

## Root cause
`milStdObservationDescriptor()` hard-coded every supported UAV observation to `unknown`, ignoring the record's `entity_id`. The preceding hostile registry correction therefore affected organization layers only.

## Fix
- Resolve UAV affiliation from `MIL_STD_ORGANIZATIONS[event.entity_id]`.
- Fall back to `unknown` when the entity has no explicit registry mapping.
- Advance the script to `app.js?v=174`.
- Update regression and production-manifest contracts.

## Expected data effect
The current v2.1 projection contains 1,509 supported UAV observations. Of these, 508 reference the five explicitly hostile KFOR/NATO entities and will render hostile; observations tied to unmapped entities remain unknown.

## Preserved behavior
Object class, confidence, claim state, location, evidence traceability, and viewer navigation are unchanged.

## Release plan
Validate, push directly to remote `main` under the user's explicit instruction, back up current production assets, deploy v177, and verify the public script and service.
