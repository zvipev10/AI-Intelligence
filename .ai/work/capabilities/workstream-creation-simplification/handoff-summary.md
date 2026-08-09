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
- Deployment: not performed

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

Review the focused diff and prepare a narrow, hash-guarded deployment from this branch. Do not deploy
the old `codex/workstream-creation-simplification` branch or its broad legacy deployment script.

## Suggested durable documentation updates

After live acceptance, record the evidence-first creation policy and ordinary-chat/playback target
persistence boundary in `docs/product-context.md` and `docs/decisions.md`. No architecture update is
needed because APIs, schema, permissions, and data flow are unchanged.
