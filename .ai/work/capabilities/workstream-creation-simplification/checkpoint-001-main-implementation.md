# Checkpoint 001 — Main-based implementation

## Result

Evidence-first workstream creation is implemented and published from a clean `origin/main` baseline.
It is not deployed.

## Baseline

- Base: `origin/main`
- Base commit: `01c21ff` (`Merge restored result UI behaviors`)
- Feature branch: `codex/workstream-simplification-main`
- Implementation commit: `ca49cc2`

## Changes

- Moshe resolves every supplied `TGT-*` and `REC-*` before requesting metadata.
- Targets use `get_target_candidate` for canonical details and evidence.
- Raw records use `search_target_candidates(record_id)` and read-only
  `prepare_target_candidate` for additional candidate context.
- Moshe infers title, objective, and responsibility and asks at most one focused blocking question.
- Unresolved IDs must be named explicitly.
- Ordinary creation cannot persist or update targets.
- Authorized playback retains its existing eligible target create/update contract.
- Persistent profile, runtime instructions, and MCP description are aligned.
- Evaluation coverage now includes target, multi-target, raw-record, mixed/partial, and playback cases.

## Validation

- Complete UI/backend discovery: 122 passed.
- Focused profile/workstream/result/UI/playback run: 76 passed; one command-name error referenced a
  nonexistent module and was corrected by full discovery.
- Focused MCP workstream/target-boundary/catalog tests: 22 passed.
- Full MCP discovery: 50 passed, 1 skipped, 1 unrelated pre-existing backup-retention failure.
- Python compilation passed for app server, MCP server, and profile provisioner.
- `git diff --check` passed.

## Known unrelated failure

`test_target_bank.TargetBankTests.test_backup_retains_latest_five_and_reset_requires_confirmation`
can delete a just-returned backup when several files receive tied modification times. No target-bank
or backup code changed in this capability. The failure is recorded and not silently treated as green.

## Review recommendation

Approve the focused implementation for deployment planning. Deployment must use the main-based branch
and a narrow file list; the legacy broad deployment incident must not be repeated.
