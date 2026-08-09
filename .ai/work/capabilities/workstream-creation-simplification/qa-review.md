# QA/Security Review — Main-based implementation

## Status

Ready for implementation under the user's explicit request.

## Required coverage

- Target lookup and raw-record membership lookup precede clarification.
- Candidate preparation remains read-only during ordinary creation.
- Required fields are inferred when evidence permits.
- At most one focused question is allowed and partial resolution is disclosed.
- Playback may still create/update eligible targets under its existing authorization.
- Proposal confirmation, localization, result presentation, header, playback, and UI regressions pass.

## Recommendation

Continue, but do not deploy until broad main regression checks pass.
