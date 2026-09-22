# Single-active-demo scenarios

Parent: [#67](https://github.com/zvipev10/AI-Intelligence/issues/67). Review: [#68](https://github.com/zvipev10/AI-Intelligence/issues/68).
Status: planning proposal; see [status.md](status.md).

## Confirmed user intent
Retain Kosovo and introduce a Syria demo with a different dataset and map, sharing the application and future feature development. Exactly one demo scenario runs at a time. This task requests a plan, not implementation or deployment.

## Proposed outcome
One repository, short feature branches into main, versioned application releases and independently versioned demo packages. One public application endpoint and one active runtime on the current VM. Inactive packages and state remain on disk; their agent workers, data indexes and scheduled jobs do not run. An operator switches packages using a controlled stop/start operation. Kosovo can be reactivated without losing its investigations or agent memory.

## MVP
Externalize scenario configuration; isolate scenario and agent state; migrate existing Kosovo safely; package Syria content; implement controlled activation, rollback and bounded work admission; validate resource use and complete deployment assets. Keep existing source layout initially to avoid a simultaneous broad rename. Shared capabilities remain in the application; scenario-specific content and feature enablement live in packages.

## Non-goals
Parallel demos, two permanently running deployments, live in-session geography changes, cross-scenario search, a second VM, an infrastructure migration, a new admin UI, or implementation of as-yet unspecified new features. Dataset creation is planned but its actual content awaits inputs.

## Acceptance
- Kosovo behavior and existing saved work survive configuration extraction and migration.
- One active scenario identity is consistent across UI, gateway, MCP, agents and background jobs.
- Kosovo -> Syria -> Kosovo restores each scenario's own state; no data, memory, routing, playback or browser-storage crossover.
- One global agent execution slot covers chat, specialists and background updates initially; inactive work cannot consume it.
- Switches stop admission, drain safely, unload old workers before starting new ones, and publish readiness only after checks. Failed switches restore the previous known-good configuration.
- All APIs that start work or mutate state reject stale scenario/generation identifiers from old tabs and workers.
- Dataset/profile/release compatibility and all referenced media/map/index assets are checked before activation.
- Representative workloads meet an agreed resource budget on the existing VM; no promise is made that 1 GB is sufficient for all future features.

## Assumptions for review
Operator-controlled switching from the deployment tooling; short maintenance interval acceptable; preserve previous work by default, with reset a separate explicit operation. Common agent roles remain reusable; no Syria-specific doctrine, entities or behavior is invented. No new infrastructure dependency is assumed.

## Inputs still needed
Syria area of interest, time range, available or to-be-generated dataset and owner, supported languages, required sources/entity types, map/overlay assets, desired demo narrative and the new-feature list. These do not block the platform plan; they block final Syria content and acceptance scripts.

## Review and handoff
Developer/architecture, UX and QA recommendations are drafts. Review them with the proposed sequence before authorizing code. See [proposed-plan.md](proposed-plan.md), [developer-review.md](developer-review.md), [ux-review.md](ux-review.md), [qa-review.md](qa-review.md).
