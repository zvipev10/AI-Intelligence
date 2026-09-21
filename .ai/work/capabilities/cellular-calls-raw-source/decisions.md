# Capability Decisions

## 2026-09-21 — Calls use a neutral two-endpoint map model

Decision: A cellular call is one raw record with two endpoint markers and one connecting line. A/B and the line all open the same record; no MIL-STD symbol is assigned.

Rationale: The geometry communicates the relationship between two located parties without incorrectly turning communications metadata into an observed military object or duplicating the record.

## 2026-09-21 — Cellular call endpoints use distinct catalog locations

Decision: Side A follows the requested three-location scenario. Side B uses a different existing canonical location elsewhere in Kosovo for every call.

Rationale: This models two independently located endpoints without inventing sub-location precision.

## 2026-09-21 — Synthetic-only demo communications

Decision: Generate 24 deterministic call records, synthetic phone/IMEI identifiers, one local simulated recording per call, and a visible synthetic transcript. No real PII or voices are used.

Rationale: The demo needs playable, reproducible data without external services or privacy exposure.

## 2026-09-21 — Additive raw-event schema

Decision: Extend the existing projected event contract with nullable call fields and use the existing dynamic raw-layer mechanism.

Rationale: This preserves normal catalog/search/map/timeline behavior and avoids a parallel service.
