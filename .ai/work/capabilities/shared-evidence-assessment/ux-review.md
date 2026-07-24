# UX Review

## Status

AI-authored draft — pending human UX approval

## Experience goal

Make the user feel that Moshe owns a continuing validation responsibility inside a shared workspace—not that a scripted chat response appears after each click.

## Entry

From the target details for `TGT-D4DC7A7EBE02`, show **Start validation workstream**. The action opens a workstream with a derived objective such as:

> Validate whether the reported roadblock is one evolving object, whether its evidence is meaningfully corroborated, and what remains unresolved.

The analyst may edit scope but is not forced to author an assessment from nothing.

## Workstream information hierarchy

1. Target identity and working assessment.
2. Prominent **Historical replay** banner with simulated time, stage, and released-evidence count.
3. “What changed” since the previous stage.
4. Evidence grouped as supporting, contradicting/confounding, and possibly related.
5. Alternatives and the current unresolved question.
6. Responsibilities/status for Moshe and the analyst.
7. Collapsible contribution and decision history.

Chat remains adjacent or accessible for questions and redirection, but artifact updates do not live only in chat.

## Stage interaction

- **Advance scenario** shows which simulated time boundary will be crossed, not the content of unreleased evidence.
- After advancing, show immediate acknowledgement and Moshe status: `Reviewing newly available evidence`.
- When complete, highlight the artifact sections that changed and provide a concise before/after explanation.
- Disable or idempotently handle repeated advance while a transition is active.
- Keep **Run again** as an explicit recovery action only after failure or when the analyst changes scope.

## Human attention request

At Stage 2, present one bounded decision:

**Do the later reports describe the same evolving roadblock?**

- Same evolving object
- Separate object
- Insufficient evidence

Show evidence for and against each alternative, Moshe's limit, and an optional rationale field. Choosing an option records a decision; it does not silently mark the target accepted.

## State vocabulary

Use plain, distinct labels:

- Moshe: Reviewing, Current, Needs your decision, Failed, Stale.
- Contribution: Proposed, Superseded, Stale.
- Human decision: Decided, Deferred.
- Replay: Not started, Stage N of 3, Complete.

Avoid ambiguous “done” or “verified.”

## Demo honesty

The historical replay label and simulated timestamp remain visible throughout. Reset explains that it resets demo state and workstream history for this scenario, not source data. The UI must never imply that new real-world reporting is arriving.

## RTL and accessibility

- Test Hebrew RTL layout for timeline direction, evidence metadata, diff indicators, and mixed Latin IDs.
- Do not encode human versus agent or proposed versus decided by color alone.
- Stage controls, status changes, and decision options must be keyboard accessible and screen-reader labeled.
- Announce asynchronous status changes without moving focus unexpectedly.

## Empty/error/recovery states

- No workstream yet.
- No new relevant evidence at a stage.
- Moshe finds evidence but cannot classify it.
- Agent timeout/failure after stage advance.
- Browser refresh while Moshe is reviewing.
- Workstream is stale because another user advanced/reset the global scenario.
- Replay already complete.

## UX risks

- Too much process chrome can make the workstream resemble project management.
- A polished scripted transition can obscure the provenance and limits that make the demo credible.
- Repeated notifications can overwhelm the analyst; only material changes and required decisions should demand attention.
- Global scenario state can surprise concurrent viewers and needs a visible state-change notice.

## Questions requiring human UX review

- Should the workstream replace the target detail panel, open beside it, or be a dedicated view?
- Where should attention requests appear outside the workstream?
- What minimum diff presentation makes an autonomous revision understandable?
- Should reset delete demo workstream history or archive a prior run?

## Approval

- [ ] Approved
- [ ] Approved with changes recorded below
- [ ] Changes requested

Human reviewer:

Date:

Notes:

