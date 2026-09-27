# Application-package instructions

The repository-wide instructions in `../AGENTS.md` are mandatory. This file
adds package-local guidance for chats whose working directory starts here.

## Start here

Before investigating, planning, changing, testing, or deploying this
application, read these repository documents in this order:

1. `../docs/product-context.md` — scope, users, and product vocabulary.
2. `../docs/architecture.md` — components, data flow, and interfaces.
3. `../docs/product.md` — supported analyst workflows and UI behavior.
4. `../docs/operations.md` — local run, validation, deployment, and recovery.
5. `../docs/decisions.md` — decisions that should not be silently reversed.
6. `../docs/demo-scenarios.md` — active datasets, scenarios, and fixtures when
   the task concerns data or demonstrations.

Read the relevant files fully before proposing an implementation. For a
change that touches a specific subsystem, inspect its current source and
tests as well: documentation provides durable context, while code and tests
define the current executable behavior.

## Establish the current state

At the start of every task, check `git status` and the recent commit history.
Do not overwrite unrelated work in a dirty worktree. Use the deployment and
verification procedures in `../docs/operations.md`; do not infer production
details from an old conversation.

## Keep context durable

When a change establishes or alters a lasting product, architecture, data,
operational, or deployment decision, update the relevant file under `../docs/`
in the same change. Keep sensitive values out of documentation: record only
the name and approved location of a secret, never the secret itself.

For a new conversation, the opening instruction should be: "Read AGENTS.md
and the relevant repository documentation before working."
