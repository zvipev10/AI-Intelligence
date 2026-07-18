# Capability Brief — Moshe Position Intelligence Agent

## Capability slug

`moshe-position-bank-agent`

## Phase and boundary

Planning only. No product code, agent prompt, autonomous execution, or production data write is authorized in this phase.

This capability is limited to the repository's synthetic Serbia/Kosovo training scenario. It may assess and preserve evidence-backed enemy-position knowledge. It must not ingest live operational sources, recommend attacks, select or pair weapons, calculate effects, prioritize targets for engagement, or support real-world strike execution.

## User problem

Analysts currently have raw events, entity metadata, location metadata, investigation memory, and presentation layers, but no durable fused layer that represents corroborated observations of the same object at the same place. Moshe needs to turn repeated raw observations into reviewable position assessments and answer questions about accepted assessments later.

## Product goal

Introduce Moshe as the first specialized team agent and introduce a durable **Position Intelligence Bank** knowledge layer. Moshe should:

1. search all authorized synthetic raw-data layers;
2. identify candidate observations that may describe the same object near the same time and place;
3. require corroboration from at least two independent sources;
4. create an evidence-backed position artifact only when validation rules pass;
5. save accepted artifacts to a distinct knowledge bank;
6. answer questions about the bank with citations to both the artifact and its raw evidence.

## Primary persona

Moshe, currently represented by `moshe-targets-officer` in the static Michlol team catalog. The future agent identity should be a separate stable identity, proposed as `agent-moshe-position-intelligence`, linked to the visible team-member profile rather than silently changing the existing `member_type=user` record.

## Proposed operating workflow

### 1. Candidate discovery

- Search every authorized raw event source, including public/social reporting and synthetic Serbian UAV observations.
- Normalize candidate object class, entity, timestamp, location, movement state, and source provenance.
- Group observations into candidate clusters using spatial, temporal, object-class, and entity compatibility.

### 2. Independence test

Two records count as corroboration only when they have different `source_family_id` values and do not derive from the same upstream report or copied social post.

Examples:

- UAV observation + independent public report: potentially independent.
- Two reposts of one social post: one source, not two.
- Two UAV clips from the same mission and continuous pass: normally one source family.
- Two UAV missions separated in time: may be independent observations, but should not automatically prove continuous presence.

### 3. Same-object test

The records must be compatible on:

- normalized object class;
- entity/affiliation, when known;
- distinctive attributes, when available;
- count range, allowing an explicit tolerance;
- movement/status consistency;
- temporal separation appropriate to the object's mobility.

The agent must preserve ambiguity. It must not merge two observations merely because both mention a generic vehicle or unit.

### 4. Same-location test

- Resolve every observation to coordinates or a bounded geometry with stated uncertainty.
- Require spatial overlap after accounting for source accuracy and object mobility.
- Produce a fused location with an uncertainty radius, not false point precision.
- Preserve all original location claims and the fusion method.

### 5. Assessment and review

- Calculate a transparent confidence assessment from source independence, identification confidence, geolocation confidence, temporal consistency, and contradictions.
- Record supporting and contradicting evidence.
- Proposed default: Moshe may draft an artifact, but a human analyst must approve its first publication to the bank.
- Later automated promotion may be considered only after measured precision and false-fusion rates are accepted.

### 6. Bank publication

Accepted artifacts become a new catalog layer, proposed id `position-bank:all`. Raw data remains immutable. Updates create revisions rather than overwriting prior assessments.

### 7. Expert retrieval

Moshe should answer bank questions using bank-specific tools first, then cite artifact ids and evidence record ids. Answers must distinguish:

- bank fact;
- analyst/agent assessment;
- uncertainty;
- stale or superseded information;
- unresolved contradiction.

## Proposed knowledge artifact

```json
{
  "artifact_id": "POS-V2-000001",
  "artifact_type": "assessed_position",
  "dataset_version": "v2",
  "status": "draft|accepted|rejected|superseded|expired",
  "object_class": "normalized class",
  "entity_id": "optional canonical entity",
  "display_label": "human-readable label",
  "fused_location": {
    "latitude": 0.0,
    "longitude": 0.0,
    "uncertainty_radius_m": 0,
    "location_id": "optional canonical location"
  },
  "observation_window": {
    "first_seen_utc": "ISO-8601",
    "last_seen_utc": "ISO-8601"
  },
  "estimated_count": {
    "min": 0,
    "max": 0,
    "basis": "source-derived explanation"
  },
  "confidence": {
    "level": "low|medium|high",
    "score": 0.0,
    "factors": []
  },
  "evidence": [
    {
      "record_id": "REC-V2-000001",
      "source_family_id": "source-family-id",
      "support": "supports|contradicts|context",
      "observation_role": "identity|location|count|presence"
    }
  ],
  "fusion_method_version": "position-fusion-v1",
  "reasoning_summary": "concise auditable explanation",
  "created_by": "agent-moshe-position-intelligence",
  "reviewed_by": "optional human id",
  "created_at_utc": "ISO-8601",
  "updated_at_utc": "ISO-8601",
  "revision": 1,
  "supersedes_artifact_id": null
}
```

## Required source-model additions

The current projection has source type and reliability but does not reliably encode upstream independence. Planning assumes these fields will be added or derived before automated fusion:

- `source_id`
- `source_family_id`
- `upstream_report_id`
- `observation_geometry` or coordinates plus uncertainty
- normalized `object_class`
- normalized count range
- source observation/collection time distinct from processing time

Without source-family lineage, “at least two sources” cannot be enforced safely.

## Proposed bank operations

Read operations:

- list/search assessed positions;
- get artifact with evidence and revision history;
- query by entity, object class, area, time window, status, and confidence;
- find stale, contradicted, or superseded artifacts;
- explain why an artifact exists and which independent sources support it.

Write operations, initially approval-gated:

- create draft;
- submit for review;
- accept/reject;
- append evidence;
- revise fused position/count/confidence;
- supersede or expire.

## MVP scope

- One specialized Moshe agent profile for the synthetic scenario.
- Read access to all V2 raw-data layers.
- Deterministic candidate clustering before LLM reasoning.
- Minimum two independent source families.
- Draft artifact creation with provenance and contradiction capture.
- Human approval before bank publication.
- Separate persisted position-bank store and UI layer.
- Bank-specific question answering with artifact/evidence citations.
- Immutable revisions and audit log.

## Non-goals

- Weapon selection, weapon suitability, attack sequencing, effects estimation, collateral analysis, strike recommendation, or target prioritization.
- Live intelligence feeds or real-world operational use.
- Automatic publication without review.
- Changing or deleting raw records.
- Inferring exact coordinates beyond evidence accuracy.
- Treating two copied reports as independent corroboration.
- Multi-agent orchestration for other Michlol members.

## Acceptance criteria for a future implementation

- No artifact can reach `accepted` with fewer than two independent source families.
- Every accepted artifact cites all supporting and contradicting raw record ids.
- Every fused coordinate includes an uncertainty radius and fusion-method version.
- Generic same-class observations are not merged without additional identity/location compatibility.
- Raw records remain unchanged.
- Revision history is append-only and an artifact can be superseded or expired.
- Moshe can answer bank questions and cite artifact ids plus underlying record ids.
- Answers clearly label confidence, staleness, and contradictions.
- Dataset V1 and V2 banks are isolated.
- All write actions are authenticated/audited or, for the current POC, explicitly bound to an approval action and audit record.
- No response or artifact contains weapon pairing or attack recommendations.

## Principal risks

- False fusion: two different objects are merged.
- False independence: copied or derivative reports are counted twice.
- False precision: a broad area becomes an unjustified point coordinate.
- Mobility/staleness: a valid observation becomes obsolete quickly.
- Confirmation bias: contradictory evidence is suppressed.
- Prompt injection or malformed raw text influencing agent behavior.
- Bank answers presenting assessment as established fact.
- Performance cost of all-source clustering over 14,800+ records.

## Required reviews before execution planning

- Product: approve terminology, human-review workflow, and simulation-only boundary.
- Development/architecture: choose persistence, source-lineage model, fusion pipeline, and agent/tool boundary.
- UX: design draft/review/accepted states and map/layer presentation.
- QA: define gold clusters, false-fusion tests, provenance tests, and regression plan.
- Security: approve write authorization, auditability, prompt/data isolation, and prohibition of live operational use.

## Blocking product questions

1. Should the visible layer be named “Position Intelligence Bank” or “Target Bank” in the simulation UI? The recommended neutral name is “Position Intelligence Bank.”
2. Who may approve a draft: any analyst, only Moshe’s human role owner, or a designated reviewer?
3. What is the initial artifact freshness policy for stationary sites, parked vehicles, moving vehicles, and maneuvering units?
4. Should an accepted artifact belong globally to dataset V2 or also be linked to the investigation that produced it?
5. Is count agreement mandatory, or may two independent sources confirm presence while count remains a range/unknown?
