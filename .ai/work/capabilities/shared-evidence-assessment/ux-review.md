# UX Review

## Status

Phase 1 Slice 2 direction and implemented checkpoint approved by the human Product owner on 2026-07-24. Broader scenario-playback UX remains a draft.

## Phase 1 Slice 2 approved flow

- Enter tracking from the existing plus menu with `מעקב`.
- Keep creation inside chat rather than introducing a separate form or management surface.
- Require one explicitly attached layer and use the user's message as the objective.
- Show derived title and initial responsibility in an agent-style chat preview before persistence.
- Keep the active header indicator minimal.
- On indicator press, return description, status, and user actions as an agent message in chat.
- Ask the user to choose in chat when multiple workstreams are active.
- Keep all updates manual and deterministic in this slice; automation may replace some messages later.
- Require a second, explicit chat action before archiving.

## Phase 1 Slice 2 review focus

- Is tracking mode sufficiently distinct from ordinary chat?
- Is the one-layer requirement clear at the point of attachment and submission?
- Does the preview make the persistence boundary understandable?
- Does the minimal indicator remain discoverable without becoming a management panel?
- Are multiple-workstream selection and archive confirmation clear and accessible?

## Experience goal

Show durable human-agent collaboration across changing scenario state without making the experience depend on a particular target, evidence type, or decision.

## Generic entry

Users may:

- choose a prepared scenario;
- start a supported scenario from a domain object;
- start from an investigation or broader context.

The scenario supplies a default objective and responsibilities. Users can refine scope without inventing an assessment from nothing.

## Information hierarchy

1. Scenario/workstream purpose and current context.
2. Playback status, stage, and simulated time when applicable.
3. What changed in the latest transition.
4. Evolving domain artifacts rendered through appropriate adapters.
5. Responsibilities and participant status.
6. Alternatives, gaps, uncertainty, and attention requests.
7. Collapsible contribution and decision history.

The shell is generic; domain adapters provide object summaries and artifact views.

## Interaction model

- Advance previews the transition boundary, not unreleased content.
- The UI immediately acknowledges the transition.
- Affected assignments show reevaluation status.
- Completed changes show a concise before/after explanation.
- Decision requests use scenario-declared prompt, options, supporting context, and authority.
- Reset communicates whether the current run will be archived or cleared.

## Generic states

- Scenario: Not started, Active, Transitioning, Complete, Failed.
- Assignment: Current, Reviewing, Needs input, Blocked, Failed, Stale.
- Contribution: Proposed, Superseded, Stale.
- Human action: Decided, Deferred, Corrected.

Avoid domain claims such as “verified” in the platform vocabulary.

## Required UX properties

- Historical/simulated playback is unmistakable.
- Agent proposals and human decisions are distinguishable without color alone.
- Artifact changes are primary; chat is supplementary.
- Async changes are accessible and do not steal focus.
- Mixed RTL/LTR domain data remains usable.
- Empty, no-change, unsupported-context, stale-run, failure, concurrent-change, and completed states are defined.

## Questions requiring UX review

- Should the workstream be a dedicated view or a reusable panel shell?
- How do adapters declare their artifact renderer and compact summary?
- Where do attention requests appear outside the workstream?
- What generic diff representation works across artifact types?
- What is the default archive/reset experience?

## Approval

- [ ] Approved
- [ ] Approved with changes recorded below
- [ ] Changes requested

Human reviewer:

Date:

Notes:
