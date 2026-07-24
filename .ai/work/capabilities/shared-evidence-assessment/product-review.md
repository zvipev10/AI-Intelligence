# Product Review

## Status

Phase 1 scope approved by the human Product owner on 2026-07-24. Broader capability decisions remain pending.

## Recommendation

Approve **Collaborative Scenario Playback** as a general capability with these decisions:

1. A scenario can start from any supported object, investigation, question, or prepared context.
2. The scenario definition declares stages, responsibilities, artifact types, visibility, decision points, and reset behavior.
3. The workstream—not chat—is the durable system of record.
4. Agents may autonomously update only contribution types allowed by their assignment contract.
5. Human authority is required for protected decisions declared by the scenario.
6. Historical scenarios are explicitly labeled and deterministic.
7. A concrete target and record sequence are fixture data, not product semantics.

## Why this is different from chat

The agent owns a declared responsibility over time, reacts to relevant state changes without another prompt, updates durable artifacts, and escalates bounded decisions. Scenario playback provides the changing environment needed to demonstrate that behavior reproducibly.

## Generic authority model

| Action | Agent | Authorized human |
|---|---:|---:|
| Observe currently released scenario state | Yes | Yes |
| Add/revise permitted proposed contributions | Yes | Yes |
| Mark its own prior contribution stale | Yes, with history | Yes |
| Advance/reset scenario | Only if scenario explicitly allows | Yes |
| Make protected scenario decision | No | Yes |
| Overwrite another participant's decision | No | No |
| Mutate protected production objects | Out of MVP | Out of MVP |

## Product questions requiring approval

- Which starting contexts must the first platform slice support?
- Is manual advance sufficient for MVP, with condition-driven advance deferred?
- Is one agent assignment sufficient to prove the generic model?
- Should reset archive a run by default or clear its workstream instance?
- Is a demo-global runtime acceptable as a deployment limitation, separate from product semantics?

## Approved Phase 1 boundary

- Persist a minimal workstream associated with an investigation.
- Include title, objective, participants, initial responsibilities, status, and optional generic starting-source reference.
- Do not select, copy, or reference individual Investigation Memory items.
- Defer scenario playback, artifacts, agent triggers, and human decisions.
- Keep Investigation Memory behavior unchanged.

## Approval

- [x] Phase 1 scope approved
- [ ] Full capability approved
- [ ] Approved with changes recorded below
- [ ] Changes requested

Human reviewer:

Date:

Notes:
