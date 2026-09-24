# Calls timeline and docked viewer

Implemented timeline defaults for call-only results and catalog actions, including agent guidance and restored call layers. Compact call buttons show UTC time, duration, endpoint numbers and one-line summary. Viewer docks nonmodally beside the timeline with the audio controls visible; narrow screens stack the panels. Switching view closes the docked viewer and releases media/map resources. Other viewer contexts remain unchanged.

Verification: 11 Python tests and shared-results JavaScript harness pass. Browser verified catalog Timeline default, adjacent viewer, visible player, Enter-to-open, close and Map switching. Fixed stale table test fixtures to use the current 300-record IPDR import. No dataset changes.
