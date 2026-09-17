# QA review

Status: Ready for implementation; acceptance cases agreed in conversation.

## Required checks

- Structured object classes are never overwritten.
- Relevant Hebrew paraphrases resolve to the canonical class.
- Unrelated text stays unresolved.
- Rolling grouping crosses a wall-clock boundary but does not bridge gaps larger than the configured window.
- Fused records retain exact raw provenance.
- Talia can retrieve every fused ID used by an assessment.
- Runtime processing never reads evaluator truth or evaluator labels.
