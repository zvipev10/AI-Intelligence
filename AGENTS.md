# AI Intelligence — Codex project instructions

This folder is the AI Intelligence Codex project. Treat these instructions as
the single authoritative starting context for a new conversation.

## Project source and documentation

The current application source is in
`llm_investigation_orchestrator_serbia_poc/`. Before investigating, planning,
changing, testing, or deploying it, perform the following remote check **once,
at the beginning of a new conversation**. Do not repeat it for follow-up
requests in the same conversation unless the user explicitly asks for a
refresh. Inspect the remote `AI-Intelligence` repository directly and verify
that remote `main` contains the tip of every other remote branch: each branch
tip must be an ancestor of `main`. This is a commit-graph check, not a
timestamp comparison.

Do this before cloning, fetching into, pulling, or using any local application
checkout. First use a direct remote comparison method when available. If that
method cannot prove ancestry for every branch, use this authorized fallback:
create a disposable bare Git repository in a temporary directory, fetch only
the remote branch refs into it, and use Git ancestry checks to determine
whether every branch tip is an ancestor of `main`. This scratch repository is
only a remote-verification aid; it is not the application clone, must not be
used for development, and must be removed after the check.

When a local AI-Intelligence checkout already exists, compare its active `HEAD`
and the content hash of its `AGENTS.md` with the verified remote `main` commit
and that commit's `AGENTS.md`. If either differs, report the exact commit and
instruction-file relationship before using the checkout. Do not clone, pull,
reset, switch branches, overwrite `AGENTS.md`, or otherwise synchronize it
automatically. Ask the user whether to keep the local state, update it, or take
a fresh clone. A local checkout may be treated as authoritative only when both
its active commit and `AGENTS.md` match the verified remote `main`.

Collect the remote-branch result and local-alignment result before responding.
If another branch contains commits not merged into `main`, `main` is
unavailable, a local checkout differs, or verification fails, stop and give
one concise report covering every detected condition. Include affected branch
names and commit relationships, but do not enumerate every historical branch
unless the user asks. Ask the user for one decision: keep the local state,
update it, take a fresh clone, or proceed despite the reported branch state.

Only after remote `main` is confirmed to be the latest integrated branch, clone
or update a local checkout when authorized. Then verify that the local
checkout's `main` resolves to the exact remote `main` commit that was checked.
If it differs because the remote changed, a checkout is stale, or the state
cannot be verified, stop, report the mismatch, and ask for next instructions.
Do not automatically pull, reset, or otherwise alter an existing clone. Only
after a checkout is confirmed to match the remote commit, read:

1. `docs/product-context.md`
2. `docs/architecture.md`
3. `docs/product.md`
4. `docs/operations.md`
5. `docs/decisions.md`
6. `docs/demo-scenarios.md` for scenario, dataset, or demonstration work.

Those documents are the durable project record. Do not rely on an earlier chat
transcript, a historical artifact, or remembered VM state. Inspect current
source and tests as well: documentation defines the intended contract; code
and tests define executable behavior.

## Scope boundary

For AI Intelligence work, use only files under this repository. Do not infer
the AI Intelligence architecture, deployment process, data model, or current
state from files outside this repository.

## Production deployment

Before any VM check, deployment, recovery, or scenario activation, read
`docs/operations.md` in full. For the maintained VM connection and deployment
helpers, inspect `llm_investigation_orchestrator_serbia_poc/mcp_server/remote_deploy_*.py`.
Do not guess a host, key, service name, copy procedure, or deployed version.

Establish live state from the VM's `/api/status` and its installed release
manifest before claiming what is deployed. Follow the operations guide's
separate procedures for UI-only, server/gateway, and dataset/index changes.
Never commit credentials, private keys, mutable runtime state, or backups.

## Working conventions

Check the active source repository's `git status` and recent history at the
start of a task. Preserve unrelated changes. When work changes a durable
product, architecture, data, deployment, or operational decision, update the
relevant document in `docs/` in the same change.
