# AI Workflow

This repository uses an AI-assisted workflow for new capabilities.

## Core model

- Skills define how AI works.
- Repo docs preserve durable context.
- Issues define current task context.
- `.ai/work/capabilities/` stores active capability artifacts.
- Draft PRs expose partial execution.
- Checkpoints allow professionals to review partial results.
- Final handoff preserves context for future work.

## Capability workflow

1. Capability initiation by Product
2. Shared feature definition
3. Role enrichment by Development / UX / QA / Architecture / Security as needed
4. Execution plan
5. Controlled execution in slices
6. Checkpoint reviews
7. Final independent review
8. QA/product acceptance
9. Context update

## Publishing workflow

Every artifact handoff should be published through Git so the next role can work from repository state, not local files or chat history.

After each workflow step that creates or updates shared artifacts:
1. Run `git status --short`.
2. Separate current-task files from unrelated dirty files.
3. Stage only current-task files.
4. Commit with a clear message.
5. Push to a shared branch.
6. Prefer a draft PR for capability work so partial execution is visible and reviewable.
7. Update the PR description or issue with the relevant artifact paths.

Do not push directly to `main` unless explicitly instructed.

If publishing cannot be completed, the checkpoint or handoff must say exactly what remains local and why.

## Per-step publishing expectations

1. Capability initiation:
   Publish `capability-brief.md` before developer review begins.

2. Role enrichment:
   Publish `developer-review.md`, `ux-review.md`, and `qa-review.md` after each role completes its artifact.

3. Execution planning:
   Publish `execution-plan.md` before implementation begins.

4. Controlled execution:
   Publish each implementation slice and its `checkpoint-00N.md` before requesting checkpoint review.

5. Checkpoint review:
   Publish review notes, requested changes, or updated checkpoint artifacts before continuation.

6. Final review and acceptance:
   Publish final PR summary, acceptance status, and test results before merge or release handoff.

7. Context update:
   Publish `handoff-summary.md` and any accepted durable doc updates.

## PM-to-developer handoff

The handoff from Product to Development is not a long chat.

The handoff is the saved artifact:

`.ai/work/capabilities/<capability-slug>/capability-brief.md`

The developer should start from that file and create:

`.ai/work/capabilities/<capability-slug>/developer-review.md`

Only after role reviews and execution planning should product code implementation begin.

## Review checkpoint policy

Human review is required before continuing when a slice affects:
- product behavior
- UX
- API/interface
- data model
- architecture
- security
- permissions
- performance
- release scope

## Token-efficiency rule

Do not continue long chats just for continuity.

Use:
- `AGENTS.md` for shared repo guidance
- skills for reusable workflow
- capability artifacts for active task handoff
- issues/PRs for task context
- checkpoint summaries for compressed state
- `docs/decisions.md` for durable decisions

## Publishing safety rule

Publishing should be scoped. The agent must not stage or commit unrelated local changes.

Before any commit, the agent should call out unrelated dirty files and leave them untouched unless explicitly instructed otherwise.
