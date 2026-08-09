# Developer Review — Main-based implementation

## Status

Ready for implementation. The user explicitly requested implementation from `origin/main` on 2026-08-09.

## Baseline and findings

- Branch point: `origin/main` at `01c21ff` (`Merge restored result UI behaviors`).
- Workstream persistence, proposals, playback updates, target lookup/preparation, and Moshe's tool
  allowlist are present.
- The over-questioning root cause exists in `moshe_profile/SOUL.md`, the Moshe runtime block in
  `server.py`, and the `prepare_workstream_creation` MCP description.
- No schema, endpoint, dependency, or new permission is needed.
- Ordinary chat must not persist targets; authorized playback retains its existing create/update rule.

## Approach

Align all three instruction surfaces around lookup-before-question behavior, automatic field inference,
one focused blocking question, explicit partial-resolution handling, and the existing playback boundary.

## Risks and tests

- Prevent prompt drift with alignment assertions.
- Protect playback and ordinary-chat boundaries with explicit regression assertions.
- Run existing profile, workstream, MCP, playback, localization, presentation, and UI suites.

## Recommendation

Continue with one focused implementation slice.
