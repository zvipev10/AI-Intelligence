# UX Review

- Status: Ready for planning (interaction contract approved by explicit develop request)
- Use a dedicated pin icon button in the first column of raw event tables.
- Label: “הצג במפה” / “Show on map”; include the record ID in the accessible label.
- On activation, keep the table state intact, switch to the map, center closely, and open a popup for the exact record.
- Popup content: record ID, timestamp, entity, location, and summary.
- Rows without coordinates show a disabled pin rather than silently failing.
- Do not make the entire row clickable.
