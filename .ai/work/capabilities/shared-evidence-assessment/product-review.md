# Product Review

## Status

AI-authored draft — pending human Product approval

## Recommendation

Approve the capability direction with these product decisions:

1. Start from an existing target candidate. The product derives a scoped validation objective; the analyst may refine it but does not need to invent an assessment.
2. Treat the workstream artifact, not chat, as the durable system of record.
3. Let Moshe autonomously add or revise only proposed agent contributions and attention requests.
4. Reserve target identity resolution, acceptance, and human-authored decisions for the analyst.
5. Use an explicitly labeled, deterministic historical replay for the first demo.
6. Use one demo-global replay state for the first slice, provided the environment prevents misleading concurrent use.

## Product rationale

This is materially different from continuous chat because the agent owns an ongoing validation task, reacts to a changed evidence environment without another prompt, updates an inspectable artifact, and escalates a precise judgment instead of returning another answer.

The selected target supports the story without inventing evidence. It also exposes a useful division of labor: Moshe can correlate, recheck, and preserve provenance; the analyst must decide whether later observations represent the same physical object.

## Human/agent authority

| Action | Moshe | Analyst |
|---|---:|---:|
| Search visible corpus and propose links | Yes | Yes |
| Add/revise agent-authored proposed interpretation | Yes | No approval required per edit |
| Mark an agent proposal stale/superseded | Yes, with history | Yes |
| Advance/reset replay | No | Yes |
| Decide same object versus separate object | No | Yes |
| Accept/reject a proposed contribution | No | Yes |
| Mutate the production target row | No | Out of MVP |

## MVP decision semantics

The bounded human decision is one of:

- same evolving object;
- separate object;
- insufficient evidence.

The decision has an optional rationale and does not imply production target acceptance. Agent contributions use `proposed`, `stale`, `superseded`, or `needs-human-decision`; human decisions use `decided` or `deferred`.

## Changes from the earlier brief

- Replaced “create an assessment and invite Moshe” with “open a target and start a persistent validation workstream.”
- Added automatic agent reevaluation on scenario advance.
- Added historical replay honesty and data-visibility requirements.
- Narrowed the demo to one real target and one identity ambiguity.
- Removed contribution-by-contribution workflow complexity not needed to demonstrate the core value.

## Product questions requiring explicit human approval

- Is demo-global replay acceptable for the first slice?
- Should only the presenter advance stages, or any demo user?
- Is the three-outcome identity decision sufficient for the demo?

## Approval

- [ ] Approved
- [ ] Approved with changes recorded below
- [ ] Changes requested

Human reviewer:

Date:

Notes:
