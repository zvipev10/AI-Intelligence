# Calls timeline and docked viewer

Implemented timeline defaults for call-only results and catalog actions, including agent guidance and restored call layers. Compact call buttons show UTC time, duration, endpoint numbers and one-line summary. Viewer docks nonmodally beside the timeline with the audio controls visible; narrow screens stack the panels. Switching view closes the docked viewer and releases media/map resources. Other viewer contexts remain unchanged.

Verification: 11 Python tests and shared-results JavaScript harness pass. Browser verified catalog Timeline default, adjacent viewer, visible player, Enter-to-open, close and Map switching. Fixed stale table test fixtures to use the current 300-record IPDR import. No dataset changes.

Deployed f2951626 successfully to VM; backup /opt/demo-runtime/backups/syria-call-timeline-f2951626. Live browser verified the calls layer opens Timeline and Call 1 docks beside the compact entry, with audio controls visible. Hermes + MCP connected; 443 records remain. Published in draft PR85, not merged. Optional layout clarification received no response; implemented the stated narrow-list assumption. Refresh the application to load app219/styles157.
