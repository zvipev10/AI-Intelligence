# Project overview

Build a Hebrew, right-to-left intelligence-analysis application that demonstrates how an analyst can recover meaningful occurrences from a large volume of heterogeneous raw events. The current synthetic dataset contains 2,044 events from multiple source types and nine geographic locations.

The purpose is not merely to display anomalies. It is to show how multiple weak, distributed indicators can be cross-referenced into a coherent occurrence, while distinguishing suspicious occurrences from plausible benign activity.

# Users

- Primary user: intelligence analyst reviewing large, noisy event streams.
- Secondary user: product or architecture stakeholder evaluating LLM-assisted cross-reference capabilities.
- The interface must support rapid scanning, comparison, evidence inspection, and explanation.

# Domain terminology

- `אירוע גולמי` (raw event): one observation from one source. It has a source-based ID such as `PORT-0090`, `CUST-0101`, or `FIN-0098`.
- `התרחשות` (occurrence): an analytical narrative assembled by linking multiple raw events. Occurrences are displayed as `התרחשות 1`, `התרחשות 2`, etc. Do not invent artificial occurrence codes.
- `חשוד`: an occurrence with patterns suggesting concealment or coordinated activity.
- `תמים`: an occurrence whose evidence supports a normal operational explanation.
- `מסלול`: the ordered geographic movement associated with an occurrence.
- Raw-event IDs describe source type only. They must never reveal whether an event is suspicious or benign.

# Current occurrence set

- Occurrence 1: suspicious irrigation-pump shipment and concealed movement from Haifa toward Beit She'an/Jordan River Crossing.
- Occurrence 2: suspicious water-filter shipment, refrigerated handling, fragmented transfer, and movement toward Tzemach.
- Occurrence 3: benign agricultural shipment.
- Occurrence 4: legitimate fuel convoy.
- Occurrence 5: generator maintenance in Beit She'an.
- Occurrence 6: legitimate medical-aid shipment.

# Core interaction contract

- Selecting an occurrence updates all linked views together: occurrence detail, search/filter field, raw-event table, and map.
- Manual text search filters both the raw-event table and the map using the same result set.
- `הצג את כל התוצאות` clears filtering and displays all 2,044 events.
- `הצג רק את ההתרחשות הנבחרת` displays exactly the raw events assigned to the selected occurrence.
- Clicking `הצג בטבלה` on an evidence item filters to the occurrence and brings the corresponding table row into view.
- The default broad search intentionally returns many results to demonstrate why keyword search alone is insufficient.

# Map contract

- Use the latitude and longitude values from `locations.csv`.
- Prefer a real interactive map component such as MapLibre GL with OpenStreetMap-compatible tiles, or Google Maps only if an API key and billing arrangement are explicitly provided.
- The map and table always show the same filtered event set.
- Each location displays a rectangular label containing the location name and filtered event count.
- In occurrence mode, draw the occurrence route and place numbered circles directly on route locations to show movement order.
- Event counts must never use numbered circles; this prevents confusion with route order.
- Avoid decorative regions, arbitrary boundaries, unexplained lines, and fake geographic shapes.

# Data rules

- Treat `events.csv` and `locations.csv` as the transferable application data.
- All 2,044 events have a valid `location_id` referencing one of nine locations.
- Preserve Hebrew text as UTF-8 and timestamps as UTC ISO 8601 strings.
- Keep the raw data separate from occurrence definitions in the application architecture.
- Never expose private answer keys, old-to-new ID mappings, or benchmark evaluation files in client bundles.

# Design guidelines

- Full Hebrew RTL interface.
- Quiet, operational, work-focused visual design.
- Dense but readable information hierarchy suitable for repeated analyst use.
- Use restrained neutral colors, red only for suspicious analytical state, green only for benign state, and blue for neutral selection/navigation.
- Cards have at most 8px radius. Do not nest decorative cards.
- Avoid marketing-style hero sections, oversized typography, gradients, decorative blobs, and illustrative filler.
- The application must work on desktop and remain usable on tablet/mobile.
- Keep terminology consistent: always use `התרחשות`, never `סיפור` or `תרחיש` for the analytical narrative.

# Architecture preferences

- React and TypeScript with strict typing.
- Separate data loading, filtering, occurrence definitions, table rendering, and map rendering.
- Derive table rows and map aggregates from one shared filtered-event selector.
- Use stable source-based raw-event IDs as keys.
- Preserve the ability to replace static CSV data with APIs or streaming sources later.
- Add focused tests for filtering, occurrence selection, route ordering, and table/map synchronization.

# Security and evaluation constraints

- This is synthetic data, but design the application as if intelligence data were sensitive.
- Do not send dataset content to third-party services unless explicitly authorized.
- Do not infer ground truth from filenames or hidden labels.
- Never include private answer-key or ID-mapping files in the frontend.

# Things to avoid

- Do not redesign before reproducing current behavior.
- Do not rename raw-event IDs.
- Do not add occurrence codes.
- Do not label every raw event as suspicious or benign by its identifier.
- Do not create separate filtering logic for the table and map.
- Do not replace the occurrence explanation with a generic dashboard.
