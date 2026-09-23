# Fixture and retrieval checkpoint

Issue #73 / parent #67. Four ADINT rows at Site 1 and three points 500m north/east/west. 200 IPDR rows, exactly one matching ADINT IP: REC-SYR-ADINT-001 -> 192.0.2.10 -> REC-SYR-IPDR-137. Observation 2026-09-22 08:00 UTC falls inside 07:58–08:04 session. IMEI exists only in IPDR. All addresses are documentation ranges; advertising IDs and IMEIs are synthetic, with IMEI-format check digits. IPDR does not assert GPS locations; no convoy identity is pre-assigned to devices.

Existing four CCTV/Satellite rows retained unchanged. New Syria network-v1/profile 5 has 208 rows and 20 catalog layers. Viewer exposes network identifier/session fields; existing MCP keyword retrieval searches and returns those fields. Agent tool guidance distinguishes session overlap from record-timestamp filters.

17 focused tests pass, including unique join, temporal overlap, 500m distances, preserved prior rows and MCP retrieval. Renderer field visibility passes. Full suite 237 tests with the same 8 baseline failures. No new runtime dependency. Next: backed-up stopped state upgrade and public/MCP verification with Syria left active.
