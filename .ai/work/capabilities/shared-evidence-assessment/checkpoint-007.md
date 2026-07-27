# Checkpoint 007 — Teammate Selection Toggle

## Scope completed

- Pressing the currently selected teammate again clears the selection.
- Deselecting restores general-chat routing and placeholder behavior.
- Any pending teammate opening response is invalidated and its welcome message is removed.
- Deselecting Moshe exits the Moshe-only workstream composer mode.
- Explicit mentions already typed in the composer remain recognized.

## Validation

- Main test discovery: 79 tests passed.
- Added regression coverage for selection toggle, welcome cleanup, and workstream-mode exit.
- `git diff --check` passed.

## Review findings

No blocking issues.

## Recommendation

Deploy and verify select → deselect → general-chat behavior.
