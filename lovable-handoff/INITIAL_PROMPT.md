# Initial Lovable Prompt

Rebuild the attached Hebrew RTL intelligence-analysis prototype as a maintainable React + TypeScript application.

Before writing code, read the Project Knowledge and inspect:

- `current-prototype.html` for current behavior and visual hierarchy.
- `events.csv` for the 2,044 raw events.
- `locations.csv` for the nine real latitude/longitude points used by the synthetic benchmark.
- The attached screenshots for visual reference.

Your first goal is behavioral parity, not a redesign.

## Required first implementation

1. Build a Hebrew RTL analyst workspace.
2. Show six selectable occurrences: two suspicious and four benign.
3. Selecting an occurrence must update:
   - the selected card,
   - analytical hypothesis and explanation,
   - evidence list,
   - search/filter field,
   - raw-event table,
   - geographic map.
4. Manual search must filter the table and map from one shared filtered-event state.
5. The map must use the coordinates in `locations.csv` and should use MapLibre GL with an OpenStreetMap-compatible basemap unless a supported built-in map integration is preferable.
6. On the map:
   - show rectangular labels with location name and filtered-event count;
   - show no count circles;
   - in occurrence mode, draw the ordered route and show route order inside numbered circles at route locations.
7. `הצג את כל התוצאות` must clear the search and show all 2,044 events.
8. `הצג רק את ההתרחשות הנבחרת` must show exactly that occurrence's linked events.
9. Evidence actions must locate the corresponding event in the table.
10. Preserve source-based IDs such as `PORT-0090`; do not create occurrence codes.

## Implementation expectations

- Use reusable components and typed domain models.
- Keep occurrence definitions separate from raw event data.
- Use one selector/function to compute the filtered event collection consumed by both the table and map.
- Keep the UI quiet, dense, operational, and responsive.
- Do not expose any answer-key or private mapping data.
- Add tests for the acceptance criteria.

After implementing, report which acceptance tests pass and identify any remaining differences from the reference prototype.
