# Product Review — Decisions 2026-07-18

## Status

Partially approved; three questions remain before execution planning.

## Accepted decisions

- The visible global layer is named `attack targets`.
- It contains both Moshe-created drafts and approved targets; status must be visible and filterable.
- The bank is global within V2 rather than tied to one investigation.
- Moshe does not run automatically. A user explicitly assigns a specific mission.
- Moshe is planned as a distinct Hermes agent/profile.
- Before creating a draft, Moshe searches the global bank for an existing compatible target at that location.
- Discovery follows a geographic-first process, then tests whether records in each candidate cluster are semantically and evidentially linked to the same object.

## Remaining decisions

- Human approval authority.
- Freshness/staleness policy by mobility class.
- Whether uncertain counts are acceptable when presence is independently corroborated.

## Planning recommendation

Allow presence and count to have separate confidence fields. A target may be corroborated as present while its count remains a range or unknown. Staleness should reduce current-presence confidence according to mobility class without deleting the historical artifact.

## Clarification — staleness

Staleness answers: “How long can this observation support a claim that the object is still there?” It does not make the historical observation false and it does not delete the artifact.

- A fixed installation changes slowly, so evidence stays current longer.
- A checkpoint or parked equipment is semi-mobile, so it becomes stale sooner.
- A moving convoy, vehicle, or personnel group can leave quickly, so current-presence confidence decays fastest.

The bank should store `last_confirmed_at`, `mobility_class`, `freshness_status`, and `refresh_due_at`. When evidence ages past the class policy, the artifact becomes `stale` or `verification_required`, remains searchable, and cannot be described as currently present without new evidence. Exact time thresholds remain a Product/QA decision and should be configurable rather than embedded in the prompt.

## Clarification — uncertain count

Two independent sources may agree that the same object/group is present at the same location while disagreeing about count because of occlusion, different observation times, partial fields of view, or ambiguous grouping. This should not necessarily invalidate presence corroboration.

Store separate assessments:

- `presence_confidence`
- `identity_confidence`
- `location_confidence`
- `count_min`, `count_max`, and `count_confidence`

For example, two independent observations may support “armored vehicles are present” while only justifying a count range. A single exact count must not be invented. Product still needs to decide whether any object classes require count confirmation before approval.
