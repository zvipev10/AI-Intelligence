# Developer Review

## Status

Ready for execution; user authorized implementation and deployment on 2026-08-09.

## Findings

- Existing Moshe tools are sufficient: `get_target_candidate` resolves targets,
  `search_target_candidates(record_id)` checks record membership, and read-only
  `prepare_target_candidate` discovers corroboration and candidate context.
- No schema, API, permission, or new dependency is required.
- The root cause is duplicated prompt guidance in `moshe_profile/SOUL.md`, the app-server runtime
  instruction, and the `prepare_workstream_creation` tool description.

## Approach

Align all three instruction surfaces around lookup-before-question behavior. Preserve the existing
structured creation handoff and prohibit target-bank persistence during creation.

## Risks and controls

- Prompt drift: cover persistent, runtime, and tool-description text in one regression test.
- Hidden target write: explicitly prohibit `create_target_candidate` and retain the existing allowlist
  and persistence checks.
- Partial lookup: require explicit reporting of unresolved IDs and one focused question.

## Test strategy

- Profile/runtime contract assertions.
- Existing workstream tool tests.
- Existing target-tool-boundary tests.
- Deployment service, health, and installed-profile checks.

## Recommendation

Continue with one implementation slice.
