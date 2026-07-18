# QA Review — Draft Test Strategy

## Status

Draft recommendations pending QA/human approval.

## Required test corpus

Create labeled synthetic cases for:

- true same-object corroboration;
- same place but different objects;
- same object moving between places;
- copied reports with different source labels;
- conflicting counts;
- conflicting affiliations;
- broad-area report plus precise UAV observation;
- stale evidence;
- contradicting later evidence;
- insufficient one-source evidence.

## Quality measures

- artifact precision and recall against gold clusters;
- false-fusion rate;
- false-independence rate;
- coordinate error and uncertainty containment;
- evidence/provenance completeness;
- staleness and supersession correctness;
- bank-answer citation accuracy;
- write authorization/audit coverage;
- latency over the 14,800-record V2 corpus.

## Required negative tests

- Reject acceptance with fewer than two independent source families.
- Reject duplicated/copy-derived corroboration.
- Reject missing uncertainty for fused geometry.
- Prevent raw-record mutation.
- Prevent cross-version V1/V2 evidence links.
- Preserve contradictory evidence.
- Prevent prompt-like raw text from changing policy or tool permissions.
- Prevent weapon-pairing or attack-recommendation content.

