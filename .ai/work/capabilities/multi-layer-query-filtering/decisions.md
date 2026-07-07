# Capability Decisions

Record accepted capability decisions here. Keep this file short and append-only.

## 2026-07-07 - Capability is standalone from chat and agent results

Decision:
Layer selection and filtering are standalone workflows independent of chat, agent runs, and chat-step result loading.

Owner:
Product and Development.

Context:
The capability needs users to select data layers directly rather than depend on results returned by chat or agent flows.

Rationale:
This creates a predictable user workflow and a reusable presentation model for table, map, and timeline.

Impact:
The implementation needs API-backed layer catalog and row-loading paths.

Follow-ups:
Keep existing chat/agent presentation behavior intact while adding standalone selection.

## 2026-07-07 - MVP row loading has no row limit

Decision:
Selected layer rows are loaded through the API with no MVP row limit.

Owner:
Development with Product acceptance.

Context:
MVP delivery prioritized complete layer visibility over pagination or backend filtering.

Rationale:
No-limit loading keeps the MVP API and client filtering model simple.

Impact:
Performance risk is accepted for MVP.

Follow-ups:
Revisit pagination, limits, or server-side filtering if large datasets affect browser stability.

## 2026-07-07 - MVP filtering is client-side over loaded rows

Decision:
Filters run client-side against API-loaded rows for MVP.

Owner:
Development.

Context:
The first version needs per-layer field/value filters without adding a generic server-side filter contract.

Rationale:
Client-side filtering is simpler and fits the local POC scope.

Impact:
Filtering only applies to loaded rows and may need server-side support later.

Follow-ups:
Design backend filter parameters if the POC pattern becomes production scope.

## 2026-07-07 - Filter state uses draft and applied filters per layer

Decision:
Opened layers own separate `draftFilters` and `appliedFilters` state.

Owner:
Product, UX, and Development.

Context:
Users need to edit filters without changing displayed results until Apply.

Rationale:
Separate draft and applied state makes Apply semantics explicit and keeps layers independent.

Impact:
Layer objects need filter state initialization and presentation helpers.

Follow-ups:
Ensure table, map, and timeline all consume applied-filtered items.

## 2026-07-07 - Raw field names are acceptable for MVP

Decision:
MVP filter fields use raw field names rather than translated or friendly labels.

Owner:
Product/UX.

Context:
Friendly labels would add scope and terminology decisions.

Rationale:
Raw names are sufficient for MVP validation.

Impact:
UX may be less polished but implementation remains focused.

Follow-ups:
Consider friendly labels in a later UX enhancement.

## 2026-07-07 - Duplicate filters are allowed for MVP

Decision:
Duplicate same field/value filters are allowed.

Owner:
Product and Development.

Context:
Duplicate filters are redundant under AND logic but not harmful.

Rationale:
Blocking duplicates is extra product and UI logic not required for MVP.

Impact:
QA should confirm duplicates do not break filtering.

Follow-ups:
Revisit duplicate prevention if users find it confusing.

## 2026-07-07 - Selector must be compact and not a visible section

Decision:
Remove the separate visible selector section/header/count. Keep only a compact search/autocomplete line.

Owner:
Product/UX.

Context:
Product reviewed Slice 1 and rejected the visible "Data layers / Layer selection / available layers" block.

Rationale:
Layer selection should be a small affordance, not a dominant workspace section.

Impact:
Slice 1 is reopened for Development correction before Slice 2.

Follow-ups:
Development must publish `checkpoint-002.md`; Product/UX must review the corrected selector.
