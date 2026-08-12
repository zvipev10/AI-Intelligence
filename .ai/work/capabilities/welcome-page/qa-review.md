# QA Review

## Status

Ready for planning.

## Acceptance coverage

- Initial view is welcome after refresh.
- No new-investigation action appears on welcome.
- Real ribbon uses registry name and existing members.
- Attention, participation, activity, progress, and milestone data stay inside each ribbon.
- Pointer and keyboard activation enter the workspace in place.
- App name returns to welcome.
- Nested invite/join actions do not enter the workspace and clearly show demo behavior.
- `E / ע` updates welcome copy, direction, and existing workspace copy.
- Map renders after workspace reveal.
- Existing health, map, conversation, workstream, and layer controls remain operational.

## Edge and regression tests

Test absent/corrupt local storage, avatar fallback, loading/error health, long titles, desktop/narrow viewport, RTL/LTR, Enter/Space activation, Escape/modal close, and repeated welcome/workspace transitions.

## Automation recommendation

Add a lightweight production-source contract test and run existing member/workstream UI regression tests plus browser smoke checks.
