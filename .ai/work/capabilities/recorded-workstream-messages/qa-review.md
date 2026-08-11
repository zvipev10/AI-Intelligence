# QA Review

## Status

Ready for planning based on the user's explicit implementation direction.

## Required coverage

- Save each supported workstream message and verify immediate modal appearance.
- Allow duplicate saves and produce distinct IDs.
- Replay both types without agent, POST, PUT, or archive calls.
- Preserve existing saved investigation-answer save/list/open/delete behavior.
- Reject malformed type/payload combinations and unsafe unstructured content.
- Verify replay after underlying workstream mutation or deletion.
- Verify Hebrew and localized English runtime rendering.

## Recommendation

Continue with the two implementation slices, then run focused and full suites.
