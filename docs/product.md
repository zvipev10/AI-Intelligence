# Product guide

Owns analyst-facing behavior. Dataset details belong to [demo scenarios](demo-scenarios.md); runtime commands belong to [operations](operations.md).

## Workspace and agent roles

One bilingual Hebrew/English application serves one active scenario at a time. General investigates with semantic and deterministic retrieval; Moshe (`@משה` / `@Moshe`) prepares evidence-backed target candidates; Talia (`@טליה` / `@Talia`) maintains enemy assessments and their supporting evidence. Evidence presentation does not authorize target or assessment changes.

Draft exploration is ephemeral until an investigation is created. Saved investigation memory, workstreams, targets and assessments retain their own ownership boundaries. Selecting an investigation changes its request context, while staged playback and its cumulative visible timeframe remain global to the active runtime. Next advances available data; later slices may trigger separate memory and workstream updates. Mobile reconnection recovers the same server-side agent run.

## Results and record exploration

| Presentation | Appropriate use |
|---|---|
| Map | Spatial questions and results with usable geometry |
| Timeline | Event sequence, recurrence and chronology |
| Table | Raw records, identifier comparison, and results without geometry |

Table is a standalone tab beside Map and Timeline, using the same component as the table beneath the map. Layer selection, filters, sorting and record opening are shared. Switching views retains table state and the overlay's minimized preference. Geometry-free rows remain accessible; IPDR defaults to Table. Older `evidence` view recommendations are interpreted as Table, without renaming evidence objects or the Evidence Layer.

General and specialist presentation instructions recognize all three views. Named catalog requests use the live catalog and preserve filters; a unique close naming match can be recovered, while ambiguous candidates require clarification. A queued action is not proof that the browser opened a layer. Saved layers and explicitly selected result/evidence layers retain their separate presentation contracts.

## Geographic context and media

Satellite is the default basemap. The compact Street/Satellite selector switches between CARTO streets and Esri imagery with CARTO roads, administrative boundaries and English-preferred labels. Where no English name exists, available source naming is retained. Satellite reference styling does not change investigation markers, routes or MIL-STD symbols. Street restores original styling and is the visible fallback when imagery fails.

**Satellite basemap imagery is not the Satellite data source.** Basemap imagery provides geographic context, may have different dates/resolution, and is not tied to the demo observation timestamps. Satellite records hold the explicitly dated synthetic convoy images. Source attribution remains visible on the map.

Normal operation has no persistent Syria/scenario label at the bottom. Queue, restart and scenario-change notices still appear when needed. Existing investigation guide and capabilities-guide media remain part of the installed application; switching scenarios must preserve these shared assets.

## Saved work and additive results

Selected final structured results can be presented automatically. Intermediate tool output is not automatically a new layer. Show adds or focuses a result layer; Hide changes its visibility across views; Close removes it and frees its color. Showing a closed result recreates it. Filters affect the selected layer. Raw records remain the provenance source; organizations and records open in the shared side drawer, and unavailable media does not hide textual evidence.

Saved questions restore complete answers, steps and result presentation without rerunning Hermes. Recorded demonstrations replay captured real agent responses; follow-up questions run live. Save and replay preserve scenario, dataset and locale ownership.

## Separation and operating constraints

Scenario selection preserves Kosovo work and does not copy its example investigations or learned memory into Syria. Locale isolation continues inside scenario state. Agents serve the active scenario only; concurrent scenario runtimes are outside the accepted scope. One bounded application execution slot and offline semantic-index builds accommodate the constrained VM. Shared messaging integrations can briefly pause during a switch, as accepted by the user.

See [architecture](architecture.md) for interfaces and state ownership. All demonstration data is synthetic. Evaluator truth stays offline and must never enter runtime retrieval, prompts, evidence creation or user-facing layers.
