# Capability Brief

## Capability name

Recorded workstream messages

## Capability slug

`recorded-workstream-messages`

## Parent issue

Draft: `issues/parent-capability.md`

## Current status

Definition ready for Product, Development, UX, and QA review. See `status.md`.

## User problem

The Recordings area can save and replay agent investigation answers, but cannot
capture the two workstream messages needed for a repeatable demonstration:

1. the confirmation shown after a workstream is created;
2. the detailed workstream card shown after pressing the workstream indicator.

## Business goal

Allow demonstrations to replay the complete workstream flow reliably without
rerunning the agent or depending on mutable live workstream state.

## Target users

Analysts and presenters using saved recordings to demonstrate investigation and
workstream workflows.

## Proposed behavior

- Both supported workstream cards expose the existing `Save recording` action.
- A saved entry is typed as a workstream-message recording and stores a sanitized
  display snapshot plus enough metadata to label it in the Recordings modal.
- Opening the recording appends the same workstream message/card to chat.
- Replay is read-only: it does not create, update, select, or archive a workstream
  and does not invoke an agent.
- Existing recorded investigation answers continue to work unchanged.

## MVP scope

- Workstream-creation confirmation message.
- Workstream detail message produced by pressing/selecting a workstream.
- Save, list, open, and delete through the existing Recordings UI.
- Hebrew and English localized runtime compatibility.

## Non-goals

- Recreating a deleted workstream from a recording.
- Executing workstream action buttons from historical snapshots.
- Recording every intermediate workstream update or playback reevaluation.
- Changing scenario playback behavior.

## Acceptance criteria

- [ ] The creation confirmation can be saved from its chat message.
- [ ] The opened workstream detail card can be saved from its chat message.
- [ ] Each saved card appears in Recordings with a clear workstream type label.
- [ ] Opening either entry reproduces the recorded chat card without API mutation
      or agent execution.
- [ ] Snapshot action buttons are absent or disabled during replay.
- [ ] Existing saved investigation questions still save, list, open, and delete.
- [ ] Invalid or obsolete workstream recordings fail safely with localized copy.
- [ ] Automated tests cover both message types, legacy recordings, validation,
      and read-only replay.

## Edge cases

- The underlying workstream is later archived or deleted.
- Two recordings refer to the same workstream at different revisions.
- The same card is saved more than once.
- A recording was created in a different locale.
- Stored snapshot content contains unsafe HTML.

## Technical constraints

- Current saved-question persistence requires `question` and `result.answer`.
- Workstream cards currently render outside `applyAgentResult`.
- Stored HTML must not become a trusted-XSS path; prefer structured card data and
  the existing renderer over raw HTML persistence.
- Schema changes must remain backward-compatible with existing JSON recordings.

## UX notes

The replayed card should look like the original but communicate that it is a
recording and must not expose live mutation actions. The modal should distinguish
investigation-answer and workstream-message entries.

## QA notes

Verify no POST/PUT/archive request occurs during replay. Test recording after the
underlying workstream changes to prove snapshot stability.

## Risks

- Accidentally replaying live action buttons could mutate current state.
- Persisting rendered HTML would create security and compatibility risks.
- Capturing current server state instead of a snapshot would make demos unstable.

## Open questions

- Product: should duplicate snapshots of the same workstream be allowed?
- UX: should replay show an explicit `Recorded` badge on the card?
- Product/UX: should the creation confirmation and opened detail use separate
  type labels in the modal?

## Missing inputs

Product and UX approval of the read-only snapshot behavior and labels.

## Required reviewers

Product, Development, UX, and QA.

## Required child issues

- [ ] Product/UX behavior review
- [ ] Developer/API review
- [ ] QA review
- [ ] Execution planning

## Proposed execution checkpoints

1. Backward-compatible typed recording schema and API validation.
2. Save actions and structured workstream-card snapshots.
3. Read-only modal listing/replay plus regression validation.

## Handoff to developer

Questions for developer:

- Which structured fields are the minimum stable card contract?
- Can both live cards share one renderer before snapshot persistence is added?
- How should existing saved-question endpoints expose typed metadata compatibly?

Expected developer output: feasibility, schema/API approach, affected renderers,
test strategy, risks, and reviewable execution slices.
