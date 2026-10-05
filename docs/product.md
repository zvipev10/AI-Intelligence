# Product guide

Owns analyst-facing behavior. Dataset details belong to [demo scenarios](demo-scenarios.md); runtime commands belong to [operations](operations.md).

## Workspace and agent roles

One bilingual Hebrew/English application serves one active scenario at a time. The header provides separate direct Hebrew and English links, each with its own shareable `?lang=` URL; it does not use an in-place language toggle. General investigates with semantic and deterministic retrieval; Moshe (`@משה` / `@Moshe`) prepares evidence-backed target candidates; Talia (`@טליה` / `@Talia`) maintains enemy assessments and their supporting evidence. Evidence presentation does not authorize target or assessment changes.

Draft exploration is ephemeral until an investigation is created. Saved investigation memory, workstreams, targets and assessments retain their own ownership boundaries. Selecting an investigation changes its request context, while staged playback and its cumulative visible timeframe remain global to the active runtime. Next advances available data; later slices may trigger separate memory and workstream updates. Mobile reconnection recovers the same server-side agent run.

### Specialist role workspaces

Team-member selection is available only inside a saved investigation workspace, never on the welcome page or during draft exploration. Naama is the SIGINT Officer and Gadi is the VISINT Officer. Selecting either applies a client-side source workspace: it limits the visible/openable catalog and result layers for that role without deleting other investigation layers.

The welcome page separates the analyst's own investigations from **Investigations you invited to join** and **Similar investigations to join**. Invitation and proposal ribbons use the same button treatment as Invite/Add. Joining an invitation opens that investigation's workspace immediately; **Suspicious military convoy** is invitation-only and is excluded from My investigations. Request-to-join remains a scenario demonstration affordance and does not send a notification.

| Member | Allowed Syria source layers | Default presentation |
|---|---|---|
| Naama / SIGINT Officer | ADINT, IPDR, Cellular Geolocations, Cellular Calls | Opens Cellular Calls in Timeline and docks the latest available call viewer. |
| Gadi / VISINT Officer | CCTV, Satellite | Opens Satellite in Map. |

Selecting the active member again returns to the general workspace. This is a presentation boundary, not a server-side access-control boundary: the existing general-agent routing and data permissions remain unchanged.

## Results and record exploration

| Presentation | Appropriate use |
|---|---|
| Map | Spatial questions and results with usable geometry |
| Timeline | Calls by default; event sequence, recurrence and chronology |
| Table | Raw records, identifier comparison, and results without geometry |

Table is a standalone tab beside Map and Timeline, using the same component as the table beneath the map. Layer selection, filters, sorting and record opening are shared. Switching views retains table state and the overlay's minimized preference. Geometry-free rows remain accessible; IPDR defaults to Table. IPDR places the canonical `REC-*` ID first, followed by the source record ID; the remaining native fields retain their source order. Older `evidence` view recommendations are interpreted as Table, without renaming evidence objects or the Evidence Layer.

Cellular Geolocations display their native device and subscriber fields: IMEI, SIM, target and operator MSISDN, and target and operator IMSI. These remain raw record values; matching identifiers do not by themselves establish subscriber ownership or identity.

Entity references shown in an item viewer resolve against the active dataset's entity directory. A reference is rendered as an opener only when its target entity is available, and opens that entity in the shared item viewer; unresolved identifiers remain plain code rather than inert controls.

General and specialist presentation instructions recognize all three views. Named catalog requests use the live catalog and preserve filters; a unique close naming match can be recovered, while ambiguous candidates require clarification. A queued action is not proof that the browser opened a layer. Saved layers and explicitly selected result/evidence layers retain their separate presentation contracts.

### Calls presentation

Cellular Calls default to Timeline even when endpoint coordinates are present. Like Table, Timeline presents only the currently focused open layer; selecting another source tab replaces the Timeline contents instead of combining all visible layers. The call presentation is a dense register with identically aligned Date & time, Side A, Side B and Location header/data tracks; the Location cell exposes the resolved call coordinates. Selecting a row keeps it highlighted and opens a map-and-conversation viewer beside the register. The viewer retains the native audio player and requests immediate playback when opened; browser autoplay policy may still require the analyst to press Play. The resolved call location map and bilingual transcript remain in the adjacent viewer. Switching away from Timeline closes the docked viewer and stops its media. On narrow screens the panels stack. Explicit Map/Table choices remain available; mixed-source results keep their existing defaults.

## Geographic context and media

Satellite is the default basemap. The compact Street/Satellite selector switches between CARTO streets and Esri imagery with CARTO roads, administrative boundaries and English-preferred labels. Where no English name exists, available source naming is retained. Satellite reference styling does not change investigation markers, routes or MIL-STD symbols. Street restores original styling and is the visible fallback when imagery fails.

**Satellite basemap imagery is not the Satellite data source.** Basemap imagery provides geographic context, may have different dates/resolution, and is not tied to the demo observation timestamps. Satellite records hold the explicitly dated synthetic convoy images. Source attribution remains visible on the map.

Satellite and CCTV source media can be expanded in an in-app full-viewport overlay, with a visible close control and Escape to restore the record view. This avoids relying on browser-native full-screen support and works on mobile browsers.

Normal operation has no persistent Syria/scenario label at the bottom. Queue, restart and scenario-change notices still appear when needed. Existing investigation guide and capabilities-guide media remain part of the installed application; switching scenarios must preserve these shared assets.

### Map polygons

Use the translucent polygon icon at the bottom-right of Map to place vertices. Click the first point after at least three distinct points to close the polygon. Escape or the icon cancels an unfinished shape. Completed polygons remain on the current page and across basemap switches. Clicking a completed polygon opens an optional comment step and saves the polygon as an investigation-memory area; it does not trigger search or filtering.

Submitting a collection request automatically opens the corresponding raw-data layer in its preferred presentation: Map for ADINT, Cellular Geolocations, Satellite and CCTV; Table for IPDR; and Timeline for Cellular Calls. The request remains recorded in investigation Memory.

For the convoy demonstration, the existing collection-source selection dialog remains the entry point and has no comments field. Selecting ADINT or CCTV for a completed map polygon opens that source's dedicated task screen. Selecting Cellular Geolocations or Cellular Calls for an IMEI opens a source-specific cellular task screen. The CCTV screen captures camera, stream, field-of-view, recognition-alert, period and authorization criteria; the Cellular Calls screen captures identifiers, target, call content, processing and approval criteria. Submitting or sending a task for approval opens the matching existing results layer in its preferred presentation without sending an external request, approval, scheduler, or data mutation.

## Saved work and additive results

### Investigation memory

Within an active investigation, an analyst can save a chat finding, a layer state, one table/viewer object, or a drawn map area to Memory. Every save opens the same optional comment step. Saves are additive, including repeated objects or areas with different comments. The investigation header exposes a Memory screen that groups saved chat findings, layers, objects, and areas with timestamps and comments. Saved layers reopen in their captured Map, Timeline, or Table presentation; objects reopen in their source viewer; areas reopen on Map with their saved polygon. Every entry has a delete action that removes only that memory item. Chat summaries remain a compact review record because the complete original agent result is not persisted. Saved comments and compact object/area metadata are supplied with saved memory to the investigation agent; Memory is not a new presentation type.

Selected final structured results can be presented automatically. Intermediate tool output is not automatically a new layer. Show adds or focuses a result layer; Hide changes its visibility across views; Close removes it and frees its color. Showing a closed result recreates it. Filters affect the selected layer. Raw records remain the provenance source; organizations and records open in the shared side drawer, and unavailable media does not hide textual evidence.

Saved questions restore complete answers, steps and result presentation without rerunning Hermes. Recorded demonstrations replay captured real agent responses; follow-up questions run live. Save and replay preserve scenario, dataset and locale ownership.

## Separation and operating constraints

Scenario selection preserves Kosovo work and does not copy its example investigations or learned memory into Syria. Locale isolation continues inside scenario state. Agents serve the active scenario only; concurrent scenario runtimes are outside the accepted scope. One bounded application execution slot and offline semantic-index builds accommodate the constrained VM. Shared messaging integrations can briefly pause during a switch, as accepted by the user.

See [architecture](architecture.md) for interfaces and state ownership. Scenario metadata is demonstration data. Supplied media retains its stated provenance; its authenticity is not independently established. Evaluator truth stays offline and must never enter runtime retrieval, prompts, evidence creation or user-facing layers.

## IPDR evidence packages

The general Evidence layer shows one IPDR package object; there is no additional IPDR-specific evidence layer. Open its package ID to inspect metadata, checksum, synthetic classification, coverage and validation totals. Choose **Open package records** to open the raw IPDR layer. All 300 individual REC records belong only to raw IPDR data; they do not appear as Evidence layer objects. Raw record viewers retain package links and native fields; their Timeline shows session intervals and validation. Package objects are presented in Table and the detail viewer, with no Map or Timeline placement.

Chat can open a specific retrieved raw record, evidence/package, or entity directly in its item viewer. The requested canonical ID is validated against the active dataset and its owning layer before the browser opens it; a queued action is not confirmation that the viewer opened.
