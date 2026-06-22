# Acceptance Tests

## Data integrity

- [ ] The application loads exactly 2,044 raw events.
- [ ] Every event retains its original source-based `event_id`.
- [ ] Every event resolves to one of the nine locations.
- [ ] Hebrew text renders correctly without encoding artifacts.
- [ ] Timestamps remain UTC ISO 8601 values.

## Terminology

- [ ] The UI uses `התרחשות` consistently.
- [ ] Occurrences are named `התרחשות 1` through `התרחשות 6`.
- [ ] No artificial codes such as `OF-4482`, `CF-7719`, or `GA-2201` appear as occurrence titles.
- [ ] Raw-event identifiers continue to use source prefixes such as `PORT`, `CUST`, `FIN`, `TEL`, `MOVE`, and `SIG`.

## Occurrence selection

- [ ] Six occurrence cards are visible.
- [ ] Occurrences 1 and 2 are marked suspicious.
- [ ] Occurrences 3 through 6 are marked benign.
- [ ] Selecting an occurrence updates the detail panel.
- [ ] Selecting an occurrence updates the search field.
- [ ] Selecting an occurrence filters the table.
- [ ] Selecting an occurrence filters the map.
- [ ] Occurrence 1 displays 13 linked events.
- [ ] Occurrence 2 displays 10 linked events.

## Search and filtering

- [ ] Typing in the search field switches to manual-search mode.
- [ ] Search matches raw-event ID, event summary, actor/entity, and relevant location/source text.
- [ ] The table and map consume exactly the same filtered event array.
- [ ] `הצג את כל התוצאות` empties the search and shows 2,044 table events.
- [ ] `הצג רק את ההתרחשות הנבחרת` restores occurrence mode.
- [ ] The UI shows the number of currently displayed events.

## Evidence navigation

- [ ] Every occurrence evidence item shows event ID, source type, reliability, timestamp, location, actor/entity, and summary.
- [ ] Clicking `הצג בטבלה` brings the correct event row into view.
- [ ] The selected event row is visually highlighted.
- [ ] The corresponding map location is visibly emphasized.

## Map

- [ ] The map uses the latitude/longitude data in `locations.csv`.
- [ ] The basemap resembles a familiar real map and remains visually quiet.
- [ ] Each active location has a rectangular label containing location name and filtered-event count.
- [ ] Count labels are not circles.
- [ ] Manual search shows no occurrence route.
- [ ] Occurrence mode draws one ordered route.
- [ ] Route order is displayed inside numbered circles placed at route locations.
- [ ] Occurrence 1 shows route steps 1 through 7.
- [ ] The map does not show decorative regions, fake boundaries, or unexplained lines.

## Visual and responsive behavior

- [ ] The whole interface is RTL.
- [ ] Desktop layout supports dense analyst workflows without overlapping text.
- [ ] Tablet/mobile layouts remain usable and do not overflow horizontally.
- [ ] Suspicious and benign states are distinguishable without dominating the interface.
- [ ] No nested decorative cards or marketing-style sections are introduced.

## Security

- [ ] No answer-key files are included in the frontend.
- [ ] No private old/new event-ID mapping is included in the frontend.
- [ ] No dataset content is transmitted to an external service without explicit authorization.
