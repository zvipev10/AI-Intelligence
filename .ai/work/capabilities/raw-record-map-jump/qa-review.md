# QA Review

- Status: Ready for planning
- Happy path: raw event with canonical location switches to map, centers, and opens exact-record popup.
- Fallback: event-provided latitude/longitude works when the location catalog entry is absent.
- Negative: no coordinates produces a disabled action.
- Repeated action: previous popup is removed.
- Regression: filters and sorting ignore the action column; map aggregation and target popups remain unchanged.
- Locale/accessibility: Hebrew and English labels; native button keyboard activation.
- Validation: focused automated test, existing relevant UI tests, deployed-browser smoke check.
