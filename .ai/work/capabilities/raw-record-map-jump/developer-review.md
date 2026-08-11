# Developer Review

- Status: Ready for planning (user explicitly requested development and deployment)
- Feasibility: High; client-side only.
- Affected files: `app.js`, `styles.css`, focused regression test, asset cache keys.
- Recommended approach: add a focused-popup state handle, coordinate resolver, event-row action, delegated click handler, and a `showEventOnMap` function that activates the map before flying to the location and opening an escaped event popup.
- Key constraint: `activateView("map")` schedules `renderMap()`, which fits all visible markers. Schedule the focused fly/open action after that render so it becomes the final camera action.
- Risk: action columns must be excluded from generic table sorting/filtering enhancement.
- Test strategy: static focused regression plus existing UI suites, then browser smoke test on the deployed VM.
