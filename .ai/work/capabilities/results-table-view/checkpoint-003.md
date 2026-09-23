# Checkpoint 003 — IPDR fields correction

User correction: IPDR has IP address and IMEI, not actor/location. Reuse the same results table but render IPDR-specific columns: record ID, time, reliability, certainty, IP address, IMEI, summary. Remove the map action and actor/location columns. Hide actor/location fields in the IPDR viewer and filter field list. Preserve real IP/IMEI strings (including leading zeros), record opening, filtering/sorting and other source layouts. No dataset change.

Checks: Node Table regression includes IP/IMEI values and headers, no actor/location/map columns, viewer/filter fields, other-source layout preserved; media tests and JS syntax pass. Publish in existing #76 / #75, then deploy static assets JS version 205 without restarting agents.
