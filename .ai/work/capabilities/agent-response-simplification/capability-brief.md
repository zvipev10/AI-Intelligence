# Agent response simplification

## Problem

Agent answers are technically rich but difficult to scan in the narrow chat panel. The final answer, evidence identifiers, research trace, workstream state, routine status updates, and technical errors can all appear at the same visual priority. Prompt instructions ask for short answers, but the product does not enforce a stable response shape.

## Goal

Make every agent response understandable in a few seconds while keeping evidence, coverage, and technical trace available on demand.

## Proposed visible structure

Every durable chat answer should use this order:

1. Direct answer or status headline.
2. Up to three key findings.
3. One confidence, coverage, or limitation line when relevant.
4. One useful next action when relevant.
5. Collapsed evidence and research details.

## Proposed response contract

```json
{
  "kind": "retrieval|investigation|clarification|no_result|workstream|target|status|error",
  "headline": "Direct answer or outcome",
  "findings": ["At most three short findings"],
  "confidence": "high|medium|low|null",
  "uncertainty": "One short limitation or null",
  "coverage": {
    "checked": 0,
    "returned": 0,
    "complete": true,
    "note": "Optional short scope note"
  },
  "next_action": "One action or null"
}
```

Evidence layers, raw records, map layers, research steps, and tool arguments remain separate structured fields. The current free-text `answer` remains a temporary fallback during migration.

## Situation rules

| Situation | Default visible response |
|---|---|
| Welcome | One sentence and two or three starter actions. |
| Retrieval | One result sentence and, when needed, one coverage sentence. |
| Investigation | Verdict, two or three supporting findings, and one limitation. |
| Clarification | One question; optionally one short reason. No research trace. |
| No result | “No match found,” scope checked, and one refinement suggestion. |
| Partial/truncated result | Best available answer plus exact checked/total coverage warning. |
| Moshe/target | Decision status, subject, independent-source count, one next action. |
| Workstream created | Created confirmation, title, and one-line objective. |
| Workstream updated | What changed, current assessment, and top gap; indications collapsed behind a count. |
| Playback status | Transient UI status, not a permanent chat message. Only material assessment changes enter chat. |
| Continuation | New answer delta and newly added steps only; reference prior context by count. |
| Saved replay | Same structured answer with a saved badge; details remain collapsed. |
| Error | Human-readable summary and recovery action; technical details collapsed. |

## Research trace rules

- Default each step to one line: status, user-facing tool label, and outcome/count.
- Keep rationale behind expansion.
- Let the query action own raw arguments and the result action own raw data.
- Show at most three list items followed by “and N more.”
- Never show raw JSON arrays or internal tool names by default.
- Summarize the collapsed trace, for example: “4 checks completed · 9,783 records covered · 1 limitation.”

## Constraints

- Do not remove uncertainty or incomplete-coverage warnings to achieve brevity.
- Do not hard-truncate generated prose without preserving its meaning.
- Do not inline long record/location IDs when the evidence section already provides navigation.
- Keep raw data and full auditability accessible, but secondary.

## Acceptance criteria

- The default visible answer contains no more than one headline, three findings, one limitation, and one action.
- Raw JSON, internal tool names, and backend paths are not visible by default.
- Clarifications and routine status messages do not render empty or irrelevant research sections.
- Continuations do not duplicate prior steps.
- Partial/no-result responses state the searched scope and completeness.
- Every response kind has contract and UI regression fixtures.

## Proposed delivery checkpoints

1. Approve the response contract and situation matrix.
2. Simplify research-step summaries and detail disclosures.
3. Add the typed answer renderer with legacy fallback.
4. Add gateway validation, prompt alignment, and regression fixtures.
5. Validate with real live-agent runs before deployment.

