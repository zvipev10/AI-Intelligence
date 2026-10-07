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
checkout. The authoritative live branch inventory is:

`git ls-remote --heads https://github.com/zvipev10/AI-Intelligence.git`

Use only its `refs/heads/*` output to decide which branches exist. Never infer
the live remote namespace from local branches, remote-tracking refs, tags, or
cached bare-repository refs. If it lists only `main`, there are no other branch
tips to compare.

If ancestry comparison is required and a direct remote comparison method cannot
prove it, use this authorized fallback: create a fresh disposable bare Git
repository in a temporary directory, fetch exactly the live branch refs listed
by `git ls-remote --heads`, and use Git ancestry checks. Do not reuse cached
refs; the scratch repository must be removed after the check. It is only a
remote-verification aid, not the application clone, and must not be used for
development.

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

On branch `feature/i360-only`, read `docs/architecture.md` and
`docs/operations.md` first; AI, playback and VM material in the other
documents describes `main`.

Those documents are the durable project record. Do not rely on an earlier chat
transcript, a historical artifact, or remembered VM state. Inspect current
source and tests as well: documentation defines the intended contract; code
and tests define executable behavior.

## Scope boundary

For AI Intelligence work, use only files under this repository. Do not infer
the AI Intelligence architecture, deployment process, data model, or current
state from files outside this repository.

## Production deployment

On branch `feature/i360-only` the app is a container on the LAMBDA cluster in
front of platform-hl-api; there is no VM. Read `docs/operations.md` and the
project's `DEPLOY-GITHUB-CODE-TO-LAMBDA.md` before deploying. Never commit
credentials, tokens, private keys, mutable runtime state, or backups. Do not
sign in to i360 on a user's behalf; the user runs `tools/provision_types.py`
and estate checks with their own login.

Run the backend tests against the fake HL API
(`python3 -m unittest discover -s tests -t .`) and the UI tests before any
change is proposed.

## Working conventions

Check the active source repository's `git status` and recent history at the
start of a task. Preserve unrelated changes. When work changes a durable
product, architecture, data, deployment, or operational decision, update the
relevant document in `docs/` in the same change.
