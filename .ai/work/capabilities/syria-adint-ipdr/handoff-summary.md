# Syria ADINT/IPDR handoff

User-authorized feature deployed as Syria network-v1/profile 5, runtime c7c331911d76d575a92b9aba434ede0434a4d818. PR #74 stacked on #72 (which depends on #69); issue #73 closes on merge. Source is published, not merged into main.

Four ADINT observations: LOC-SYR-001 and LOC-SYR-003/004/005, approximately 500m north/east/west. Each has synthetic advertising ID, IP, timestamp and location accuracy; no IMEI. 200 IPDR sessions have IP, synthetic IMEI, session start/end, port/protocol/byte counts and no asserted GPS location. Existing four CCTV/Satellite records are unchanged (208 total, 20 catalog layers). Five entities comprise the existing convoy plus four advertising-device identifiers; no convoy/device association is pre-established.

Expected correlation: REC-SYR-ADINT-001 at 2026-09-22 08:00 UTC has IP 192.0.2.10. Only REC-SYR-IPDR-137 shares that IP; its 07:58–08:04 session contains the observation and reports synthetic IMEI 000000000001370. Other IPDR records do not match any ADINT IP. All addresses use documentation ranges. The data generator is deterministic and standard-library only.

Changed files: new dataset/generator/profile; MCP public fields and searchable identifiers/tool guidance; record viewer identifier/session labels; asset versions/deployment list; fixture/retrieval/field visibility tests and runbook. Kosovo profile/data have no diff. No new VM dependency.

Checks: 17 focused tests pass (counts, distance, unique join, time overlap, preserved prior rows, MCP retrieval); viewer field harness and JS syntax pass. Full suite 237 tests with the same 8 baseline failures. MCP 72 pass/2 skip. Public API verifies counts and unique match. Public proof: /opt/demo-runtime/control/syria-network-qualification.json. Real-browser visual acceptance is pending; no connected browser is available.

Release/state: source backup /opt/demo-runtime/backups/syria-network-c7c3319; prior convoy-v3 and its state retained. Current Syria state copied at a stopped upgrade, prebuilt search index installed and readiness checks passed for all roles. Single scenario remains active. No prior saved work was deliberately removed.

Next: refresh http://151.145.93.180, open ADINT/IPDR, or ask the agent to find the IMEI for the ADINT observation at Site 1 using matching IP/session time. Reviewer should merge dependency PRs in order. Focused operator documentation updated; suggested product-context update is to list the two added raw source types.

Live agent qualification passed in 41.79 seconds: retrieved REC-SYR-ADINT-001 and REC-SYR-IPDR-137, verified session overlap and returned IMEI 000000000001370 without an error. Evidence: /opt/demo-runtime/control/syria-network-agent-qualification.json.
