# [Capability] Recorded workstream messages

## Capability

Enable saved recordings for workstream-creation confirmations and opened
workstream detail cards.

## Current phase

Definition and role review.

## Overall status

Pending review.

## Operational status

See `.ai/work/capabilities/recorded-workstream-messages/status.md`.

## User problem

Recordings omit two key workstream messages, preventing complete repeatable demos.

## MVP scope

Save, list, replay, and delete structured read-only snapshots of the creation
confirmation and opened workstream detail card.

## Acceptance criteria

- [ ] Both workstream message types can be recorded.
- [ ] Replay reproduces the card without agent execution or state mutation.
- [ ] Existing investigation recordings remain compatible.
- [ ] Localized and security-focused regression tests pass.

## Child tasks

- [ ] Product/UX review: `001-product-ux-review.md`
- [ ] Developer/QA review: `002-developer-qa-review.md`
- [ ] Execution plan
- [ ] Implementation slices
- [ ] Final QA and handoff

## Artifacts

- Brief: `../capability-brief.md`
- Status: `../status.md`

## Closure rule

Keep open until both message types pass read-only replay acceptance and final QA.
