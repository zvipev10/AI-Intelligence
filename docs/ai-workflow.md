# AI Workflow

This repository uses an AI-assisted workflow for new capabilities.

## Core model

- Skills define how AI works.
- Repo docs preserve durable context.
- Issues define current task context and role-owned work.
- `.ai/work/capabilities/` stores active capability artifacts.
- `status.md` is the first file to read for any active capability.
- Draft PRs expose partial execution.
- Checkpoints allow professionals to review partial results.
- Final handoff preserves context for future work.

## Capability workflow

1. Capability initiation by Product
2. Parent capability issue and `status.md`
3. Shared feature definition
4. Child issues for Product / Development / UX / QA / Architecture / Security tasks as needed
5. Execution plan
6. Child issues for implementation slices and checkpoint reviews
7. Controlled execution in slices
8. Checkpoint reviews
9. Final independent review
10. QA/product acceptance
11. Context update

## Issue model

Use issues as a Jira-like task layer:
- One parent issue per capability.
- One child issue per actionable task, review, implementation slice, QA task, or handoff.
- The parent issue tracks overall status and links to all child tasks.
- Child issues track exact owner, required action, inputs, expected output, blockers, and completion criteria.
- Pull requests should close child issues with `Closes #N`, `Fixes #N`, or `Resolves #N`.
- Keep the parent issue open until all required child issues are closed, final QA is complete, acceptance criteria are satisfied, and final handoff is published.

If remote issue creation is blocked, create local issue bodies under:

`.ai/work/capabilities/<capability-slug>/issues/`

## Capability status file

Every active capability must have:

`.ai/work/capabilities/<capability-slug>/status.md`

This file answers:
- current phase
- overall status
- who needs to act now
- exact required action
- blockers
- risks
- next expected artifact
- parent issue
- child issue table
- latest change since previous review

Each role should be able to decide whether they need to act by reading `status.md` before reading detailed artifacts.

## Role-boundary gates

Execution planning must not be created as part of the same handoff that first gives Development the product brief, unless the user explicitly asks to bypass the gate.

Before `execution-plan.md` is created:
1. Product must publish `capability-brief.md`.
2. Product or Codex must publish `status.md` and create or draft the parent capability issue.
3. Development must have a real review opportunity through a child issue and publish `developer-review.md`.
4. Required UX, QA, Architecture, or Security reviews must be either completed, tracked as child issues, or explicitly marked not required.
5. Any blocking open questions from role reviews must be answered or accepted as assumptions.

If a user says "developer stage", treat that as role enrichment by default. Produce or update `developer-review.md`; do not produce `execution-plan.md` unless the user explicitly says to create the execution plan after developer review.

Role reviews are owned by the corresponding human role owner unless the user explicitly delegates that role decision to the AI. AI may prepare a draft review by inspecting the repo and proposing technical input, but draft AI-authored role reviews must be marked `Draft` or `Pending human review`. The AI must not mark a role review `Approved` from its own analysis alone. Phrases such as "developer stage", "UX stage", or "QA stage" are not approval and are not delegation.

Every execution plan must include a prerequisite review gate that lists the role-review artifacts used and their approval/status.
Every execution plan must also list related parent and child issues.

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
8. Update `status.md` with the current owner, blockers, next artifact, and issue state.

Do not push directly to `main` unless explicitly instructed.

If publishing cannot be completed, the checkpoint or handoff must say exactly what remains local and why.

## Per-step publishing expectations

1. Capability initiation:
   Publish `capability-brief.md`, `status.md`, and the parent capability issue before developer review begins.

2. Role enrichment:
   Publish `developer-review.md`, `ux-review.md`, and `qa-review.md` after each role completes its artifact, or publish an AI-prepared draft clearly marked as pending human approval. Update the matching child issue.

3. Execution planning:
   Publish `execution-plan.md` and child slice issues before implementation begins.

4. Controlled execution:
   Publish each implementation slice and its `checkpoint-00N.md` before requesting checkpoint review. Close only the child issue fully completed by the PR.

5. Checkpoint review:
   Publish review notes, requested changes, or updated checkpoint artifacts before continuation.

6. Final review and acceptance:
   Publish final PR summary, acceptance status, and test results before merge or release handoff.

7. Context update:
   Publish `handoff-summary.md`, parent issue closure checklist, child issue closure status, and any accepted durable doc updates.

## PM-to-developer handoff

The handoff from Product to Development is not a long chat.

The handoff is the saved artifact:

`.ai/work/capabilities/<capability-slug>/capability-brief.md`

The developer should start from that file and create:

`.ai/work/capabilities/<capability-slug>/developer-review.md`

Only after role reviews and execution planning should product code implementation begin.

Development owns the technical input step. The developer review should record who reviewed the product brief, what context they inspected, what technical constraints they found, which product questions block execution planning, and whether the artifact is ready for execution planning.

If Codex helps during developer stage, it should default to a facilitation pattern:
1. Inspect relevant code and prepare draft notes.
2. Mark the artifact as `Draft - pending human approval`.
3. Ask the developer to accept, edit, or reject the recommendations.
4. Only after explicit developer approval, update the review status to `Approved`.

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
- parent issues for capability status
- child issues/PRs for role-owned task context
- `status.md` for current owner, blocker, and next action
- checkpoint summaries for compressed state
- `docs/decisions.md` for durable decisions

## Publishing safety rule

Publishing should be scoped. The agent must not stage or commit unrelated local changes.

Before any commit, the agent should call out unrelated dirty files and leave them untouched unless explicitly instructed otherwise.
