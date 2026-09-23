# AI Agent Instructions

This repository uses an AI-assisted delivery workflow.

## Always follow

1. Use `.ai/skills/base-team-workflow/SKILL.md` for every meaningful task.
2. For new capabilities or meaningful feature changes, use `.ai/skills/end-to-end-feature-delivery/SKILL.md`.
3. For PR review, checkpoint review, QA planning, validation, or product acceptance, use `.ai/skills/review-and-qa/SKILL.md`.
4. At the end of meaningful work, use `.ai/skills/context-maintenance/SKILL.md`.

## Context loading rule

Do not load all docs by default.

Start with:
- the current user request, issue, or PR
- this `AGENTS.md`
- the relevant skill file
- directly relevant source files
- the active capability artifact under `.ai/work/capabilities/<capability-slug>/` when working on a capability

Only load these docs if needed:
- `docs/ai-workflow.md`
- `docs/decisions.md`
- `docs/product-context.md`
- `docs/architecture.md`
- `docs/glossary.md`

If a needed doc does not exist, say so and continue with the available context.

## Capability workspace rule

For every meaningful new capability, create or use:

`.ai/work/capabilities/<capability-slug>/`

Use this workspace to store:
- `capability-brief.md`
- `developer-review.md`
- `ux-review.md`
- `qa-review.md`
- `execution-plan.md`
- `checkpoint-001.md`, `checkpoint-002.md`, etc.
- `handoff-summary.md`

Do not rely on chat history as the handoff between roles.

The handoff from product to development is the saved capability artifact, usually:
- `capability-brief.md`
- then `developer-review.md`
- then `execution-plan.md`

## Publishing rule

Shared artifacts must not remain only in a local workspace when they are needed for another role.

After creating or updating any capability artifact, checkpoint artifact, handoff artifact, repo workflow doc, issue template, or PR template:
1. Run `git status --short`.
2. Identify files changed by the current task.
3. Identify unrelated dirty files.
4. Stage only files related to the current task.
5. Commit the intended files with a clear message.
6. Push the commit to a shared branch.
7. Prefer a draft PR for reviewable work; update the PR description with links or paths to the relevant artifacts.

Do not stage unrelated files unless explicitly instructed.

Do not push directly to `main` unless explicitly instructed.

If publishing is blocked by missing credentials, permissions, remote configuration, or human approval, say so clearly and provide the exact files that still need to be published.

## Execution rule

For meaningful capabilities, do not implement everything in one hidden pass.

Create:
1. capability brief
2. role reviews as needed
3. execution plan
4. execution slices
5. checkpoint summaries
6. final handoff

Stop for human review when the change affects:
- product behavior
- UX
- API/interface
- data model
- architecture
- security
- permissions
- performance
- release scope

## Scope rule

Keep changes focused on the task.

Do not:
- make unrelated refactors
- change public behavior without saying so
- add dependencies without explaining why
- silently ignore failing tests
- invent product requirements
- change architecture without a checkpoint
- implement product code during capability definition or role-review phases

## Output rule

Every meaningful session must end with:
- summary
- changed files
- tests/checks run
- publishing status
- assumptions
- risks
- next step
- suggested docs updates
