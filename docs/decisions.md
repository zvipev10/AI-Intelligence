# Decision Log

Use this file for durable product and technical decisions.

## Format

### YYYY-MM-DD — Decision title

Decision:
[What was decided]

Context:
[Why this came up]

Rationale:
[Why this option was chosen]

Alternatives considered:
[Short list]

Impact:
[Product/technical impact]

Follow-ups:
[Any needed actions]

### 2026-07-18 - Preserve V2 and add evaluator-grounded V2.1 fusion evidence

Decision:
Keep V1 and deployed V2 immutable. Create V2.1 from V2 with intentional cross-source shared-object evidence chains and evaluator-only truth labels.

Context:
V2 public and UAV records were sampled independently. They were aligned to the same scenario but could not reliably prove that two sources described the same physical object, which made Moshe fusion evaluation depend on accidental correlations.

Rationale:
A small version increment preserves reproducibility and rollback while providing measurable positive and negative cases. Evaluator truth remains outside raw and runtime projection data so the investigating agent cannot use it.

Alternatives considered:
Overwrite V2; infer truth from accidental V2 correlations; create an entirely unrelated dataset.

Impact:
V2.1 contains 300 positive cross-source chains and 100 hard negatives at the existing 14,800-record scale. Runtime selection is optional; production remains on V2 until separately released.

Follow-ups:
Use V2.1 to implement and evaluate Moshe, the global `attack targets` layer, duplicate detection, source-independence rules, and human approval.

### 2026-07-28 — Define playback scenarios as scoped timeframe stages

Decision:
Represent a reusable historical playback scenario as identity/version metadata,
one data scope, and an ordered list of stages with inclusive `from` and
exclusive `to` timestamps. Keep record IDs, targets, assignments, agent state,
and transition history outside the scenario artifact.

Context:
The initial playback design placed responsibilities, released references, and
other runtime concerns in the manifest. Product proposed that a list of
time-bounded stages was sufficient and explicitly approved the simplified
design.

Rationale:
Time windows describe when scenario information becomes visible without
coupling the platform contract to a particular record sequence. Runtime and
collaboration state evolve independently and belong in persistent run and
workstream models.

Alternatives considered:
- Embed record IDs in each stage.
- Put assignments and decisions in the scenario manifest.
- Encode a domain-specific target assessment sequence.

Impact:
Manifests are strict and reject unsupported fields. Playback visibility is
cumulative, stages may contain gaps but cannot overlap, and any historical
fixture can change its records without changing platform code.

Follow-ups:
Implement retrieval visibility enforcement before exposing playback controls,
then add UI and automatic agent reevaluation in separately approved slices.

### 2026-08-08 — Isolate mutable target persistence by locale

Decision:
Use separate Hebrew and English SQLite target-bank instances. Initialize both active databases empty without migrating the former shared targets. Route every target create, update, evidence attachment, read, backup, reset, and restore by normalized locale. Reject Hebrew characters in English persisted presentation and evidence fields.

Context:
The English UI could expose Hebrew target content because both locales shared one mutable target database even after immutable English projections were corrected.

Rationale:
Physical separation matches the raw-data locale model, prevents cross-locale reads and writes by construction, and gives each language an independent lifecycle. Empty initialization follows the approved product requirement and avoids carrying mixed or ambiguous legacy records forward.

Alternatives considered:
- Keep one database with a locale column.
- Migrate existing shared records into Hebrew.
- Translate or copy shared records into English.

Impact:
Hebrew remains the default for omitted locale values, while explicit English operations use only the English database. Future English writes fail atomically if protected text contains Hebrew. The former shared database is rollback-only and is no longer active.

Follow-ups:
Apply the same explicit locale-ownership review to remaining mutable stores and finish full bilingual runtime acceptance.

### 2026-08-08 — Select one complete MCP runtime per locale

Decision:
Represent each supported locale and dataset version as a complete, manifest-validated MCP runtime containing its event, location, entity, fusion, presentation, and semantic state. Select that runtime once at the tool-call boundary. English asset failures must fail closed and must not fall back to Hebrew.

Context:
The English UI used clean projections while MCP tools remained bound to Hebrew module globals and a shared semantic cache.

Rationale:
Selecting a complete runtime prevents mixed-locale results and cache contamination while preserving existing tool implementations through locale-dispatching containers. Manifest checks make source paths, checksums, and cache identity auditable.

Alternatives considered:
- Translate individual MCP results after retrieval.
- Run entirely separate MCP processes per locale.
- Continue adding parallel English globals.

Impact:
Hebrew remains the compatibility default. English calls use only validated English sources, generated payload text is checked for Hebrew, and semantic cache identity includes locale, dataset version, and source checksums. Production semantic caches should be prebuilt off-host for the current low-memory VM.

Follow-ups:
Recover the VM, upload the prebuilt English v2.1 cache, complete production semantic acceptance, and apply locale ownership to workstream persistence.
