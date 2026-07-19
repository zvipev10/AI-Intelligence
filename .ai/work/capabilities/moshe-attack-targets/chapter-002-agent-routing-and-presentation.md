# Chapter 2 - Agent Routing and Shared Presentation

## Status

Product and Development approved the shared routing and presentation architecture on 2026-07-19. Architecture/security, QA, and UX review remain required before execution planning.

## Invocation and routing

- Only `@משה` in the current user message routes that message to Moshe.
- Mentions in history, quotes, agent responses, or tool output do not trigger routing.
- A message without `@משה` goes to the general agent.
- There is no sticky routing mode and no direct Moshe mission form.
- The first message in a consecutive run of `@משה` messages creates a mission and Hermes Moshe session.
- Consecutive `@משה` messages reuse the same mission and Hermes session.
- The first message without `@משה` closes the current Moshe mission.
- A later `@משה` message starts a new mission/session.

## Context and clarification

- Hermes native session resumption maintains Moshe's context between consecutive messages.
- The application router owns the mapping between conversation, mission, and Hermes session IDs.
- On mission start, the general-chat backend supplies relevant prior context, resolved IDs, evidence IDs, and accepted assumptions.
- Moshe owns clarification and may ask the user for missing or ambiguous information.
- A clarification reply must mention `@משה` to return to Moshe.
- Moshe must satisfy schema evidence requirements before writing a candidate.

## Agent responsibilities

Moshe owns:

- Clarification dialogue.
- Investigation and tool use.
- Source-aware fusion and object classification.
- Candidate creation/update.
- Result explanation and presentation selection.

The general path owns only routing for `@משה` and shared infrastructure. It must not reinterpret Moshe's assessment.

## Hermes mechanism

- Use the installed Hermes Agent v0.14.0 native profile/session capabilities.
- Moshe has a dedicated profile identity and restricted toolset.
- Do not run a second permanent gateway for the MVP; invoke/resume Moshe on demand through shared backend orchestration.
- SQLite is Moshe's persistent operational memory; Hermes session context covers the active consecutive conversation.

## Tool policy

- Reuse existing Serbia investigation tools for both agents.
- Add shared fusion/source-independence tools and target-bank tools to the same MCP service.
- Moshe receives candidate read/write and presentation-capable target tools.
- General may receive target-read tools but not candidate-write tools.
- Moshe receives no shell, filesystem, raw SQL, evaluator, generator, validation, deletion, or lifecycle-status tools.

## Evaluator-truth isolation

- Evaluator-only artifacts remain physically absent from production runtime directories.
- Runtime configuration, modules, prompts, tool outputs, and SQLite contain no evaluator paths, truth IDs, or derived labels.
- Evaluation runs separately after Moshe and compares exported candidate/evidence IDs to truth.
- Automated deployment, configuration, import, schema, content, and tool-contract checks enforce the boundary.

## Execution limits

- No application-level evidence-record, candidate-count, or mission-duration limits for the MVP.
- Infrastructure timeouts and transactional write safety still apply.
- No silent truncation is allowed.

## Shared backend and presentation refactor

General and Moshe must use the same modules for:

- Hermes invocation and session resumption.
- Streaming/events/error handling.
- Tool-result normalization.
- Shared result envelope construction.
- Layer construction.
- Frontend result application and map/table/timeline rendering.

Agent-specific configuration is limited to identity, session, tool allowlist, permissions, and mission context.

The shared result envelope adds:

- `responding_agent`
- `session_id`
- optional `mission_run_id`
- `attack_target_layers`

Add `attack_targets` as a shared layer kind with table and map capabilities. Do not create `applyMosheResult()` or a separate Moshe UI. Refactor the existing frontend result application into a generic agent-result path with agent attribution.

## Presentation responsibility

- Moshe selects and explains the results to present.
- Target read/presentation tools return UI-compatible target data.
- The shared backend validates and normalizes IDs and resolves canonical entity/location presentation data.
- The shared frontend renders Moshe's result directly and attributes it to `משה`.
- The general agent does not rewrite, reclassify, or change Moshe's evidence.

## Required Development review

- Identify extraction boundaries in the current server request handler and nested normalization helpers.
- Define a shared Hermes client/router interface.
- Define the shared result envelope and `attack_targets` layer contract.
- Confirm how an on-demand named profile is invoked/resumed without a second persistent gateway.
- Propose regression coverage for existing General-agent results and all current layer types.
