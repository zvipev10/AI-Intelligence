# Product context

Current as of 2026-09-23, checked against main `7d1c325`. Historical capability checkpoints describe earlier releases; the current contracts below take precedence.

## One application, two demo packages

The bilingual Hebrew/English intelligence workspace has one shared codebase and reusable General, Moshe and Talia agent roles. Exactly one scenario is active on the VM at a time. Switching packages changes geography, data and isolated working state; it does not create a second deployment or a country-specific application branch.

| Package | Current profile / dataset | Content |
|---|---|---|
| Kosovo | profile 1 / `v2.1` | 14,833 records, including 24 simulated cellular calls; preserved investigations and agent state |
| Syria | profile 6 / `network-v1` | 208 synthetic records: 2 CCTV, 2 Satellite, 4 ADINT, 200 IPDR; 5 locations, 5 entities and 20 catalog definitions |

The last verified deployment has Syria active. Its initial camera is Damascus (longitude 36.2765, latitude 33.5138), zoom 11. The fictional convoy sites are elsewhere; opening results can fit the map to their geometry. Installed profiles, not this document, are authoritative for future versions.

## Syria demonstration data

The original sites are `LOC-SYR-001` at latitude 35.000 / longitude 38.500 and `LOC-SYR-002` at 35.045 / 38.500, approximately 5.004 km apart. Both media sources identify `ENT-SYR-CONVOY`.

- **CCTV:** one record and one five-second synthetic movie per site, representing the September 22 visit.
- **Satellite records:** one record per site, each containing its own three timestamped images. The convoy recurs on September 20, 21 and 22, 2026: Site 1 at 08:00 UTC, then Site 2 at 08:15 UTC. Visit metadata correlates the two sites; a viewer must not show the other site's images. Cross-site explanatory copy removed at the user's request must not be reintroduced into record summaries. Travel between captures and return journeys are not observed.
- **ADINT:** four synthetic advertising-device observations, one at Site 1 and three approximately 500 m north/east/west. Each includes an advertising ID, IP address, timestamp and location accuracy. IMEI is absent.
- **IPDR:** 200 synthetic sessions with IP address, IMEI, session bounds, source port, protocol and traffic byte counts. IPDR asserts neither an actor nor a location. Its table uses IP address and IMEI columns instead of Actor/Location, has no map action, and preserves leading zeros in IMEI. Its record details and filter choices omit actor/location fields.

Exactly one cross-source demo match exists: `REC-SYR-ADINT-001` at Site 1, September 22 at 08:00 UTC, has IP `192.0.2.10`. `REC-SYR-IPDR-137` shares that IP, spans 07:58–08:04 UTC and supplies IMEI `000000000001370`. Other IPDR rows do not match an ADINT IP. Verify IP equality and time overlap together. This is a constructed fixture relation, not proof of real-world identity. No ADINT-device association with the convoy is pre-established. Addresses use documentation ranges; all media and observations remain visibly synthetic.

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

## Separation and operating constraints

Scenario selection preserves Kosovo work and does not copy its example investigations or learned memory into Syria. Locale isolation continues inside scenario state. Agents serve the active scenario only; concurrent scenario runtimes are outside the accepted scope. One bounded application execution slot and offline semantic-index builds accommodate the constrained VM. Shared messaging integrations can briefly pause during a switch, as accepted by the user.

For exact paths, switching, upgrades, recovery and cache commands, see the [operator runbook](../llm_investigation_orchestrator_serbia_poc/docs/demo-scenarios.md). For ownership and interfaces, see [architecture](architecture.md). Evaluator truth remains offline and must never enter runtime retrieval or prompts.
