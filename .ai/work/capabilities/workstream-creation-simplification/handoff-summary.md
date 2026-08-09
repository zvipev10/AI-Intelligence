# Handoff Summary

## Summary

The complete workstream-creation simplification has been rebuilt from clean `origin/main` rather than
ported from the old workstream branch.

## Changed files

- `llm_investigation_orchestrator_serbia_poc/moshe_profile/SOUL.md`
- `llm_investigation_orchestrator_serbia_poc/server.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/server.py`
- `llm_investigation_orchestrator_serbia_poc/test_moshe_profile.py`
- `llm_investigation_orchestrator_serbia_poc/moshe_profile/workstream_evaluation_cases.json`
- capability artifacts under `.ai/work/capabilities/workstream-creation-simplification/`

## Publishing

- Branch: `codex/workstream-simplification-main`
- Base: `origin/main` at `01c21ff`
- Implementation: `ca49cc2`
- Deployment: accepted after bilingual target and raw-record validation; rollback paths are recorded
  in checkpoints 002, 004, and 005.

## Assumptions

- Raw-record workstream creation may discover and prepare candidate context but may not silently
  persist a target outside authorized playback.
- One coherent workstream is preferred for related targets; materially unrelated targets justify one
  focused scope question.

## Risks

- Tool ordering is instruction-driven and should receive a live smoke after safe deployment.
- Raw-record preparation may increase latency.
- One unrelated target-bank backup-retention test remains unstable/failing on this worktree.

## Next step

Product accepted the target and raw-record behavior and explicitly requested merge to `main`. Publish
the final capability commit, fast-forward `main`, and push it. Keep the existing production rollback
backups available; no additional deployment is required because the accepted commits are already live.

After that merge, product found that target-only workstreams lacked the visible results toggle. The
presentation API was already correct; the UI eligibility predicate ignored root `target_ids`. Branch
`codex/workstream-target-results-toggle` adds root targets to the shared predicate and is deployed with
rollback backup `/opt/serbia-poc-ui-backups/workstream-target-toggle-20260809T142447Z`. Await explicit
product approval before merging this correction.

## Suggested durable documentation updates

The evidence-first creation and target-persistence boundary is recorded in `docs/decisions.md`.
`docs/product-context.md` does not exist. No architecture update is needed.
