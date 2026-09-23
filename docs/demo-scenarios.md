# Demo scenarios

Owns versioned dataset contents, fixtures and narratives. For activation, migration and recovery, use [operations](operations.md). Installed profiles remain authoritative as packages evolve.

## One application, two demo packages

The bilingual Hebrew/English intelligence workspace has one shared codebase and reusable General, Moshe and Talia agent roles. Exactly one scenario is active on the VM at a time. Switching packages changes geography, data and isolated working state; it does not create a second deployment or a country-specific application branch.

| Package | Current profile / dataset | Content |
|---|---|---|
| Kosovo | profile 1 / `v2.1` | 14,833 records, including 24 simulated cellular calls; preserved investigations and agent state |
| Syria | profile 6 / `network-v1` | 208 synthetic records: 2 CCTV, 2 Satellite, 4 ADINT, 200 IPDR; 5 locations, 5 entities and 20 catalog definitions |

Deployment identity must be checked through `/api/status`; this is an installed-package inventory, not a live status assertion. Syria's initial camera is Damascus (longitude 36.2765, latitude 33.5138), zoom 11. The fictional convoy sites are elsewhere; opening results can fit the map to their geometry. Installed profiles, not this document, are authoritative for future versions.

## Syria demonstration data

The original sites are `LOC-SYR-001` at latitude 35.000 / longitude 38.500 and `LOC-SYR-002` at 35.045 / 38.500, approximately 5.004 km apart. Both media sources identify `ENT-SYR-CONVOY`.

- **CCTV:** one record and one five-second synthetic movie per site, representing the September 22 visit.
- **Satellite records:** one record per site, each containing its own three timestamped images. The convoy recurs on September 20, 21 and 22, 2026: Site 1 at 08:00 UTC, then Site 2 at 08:15 UTC. Visit metadata correlates the two sites; a viewer must not show the other site's images. Cross-site explanatory copy removed at the user's request must not be reintroduced into record summaries. Travel between captures and return journeys are not observed.
- **ADINT:** four synthetic advertising-device observations, one at Site 1 and three approximately 500 m north/east/west. Each includes an advertising ID, IP address, timestamp and location accuracy. IMEI is absent.
- **IPDR:** 200 synthetic sessions with IP address, IMEI, session bounds, source port, protocol and traffic byte counts. IPDR asserts neither an actor nor a location. Its table uses IP address and IMEI columns instead of Actor/Location, has no map action, and preserves leading zeros in IMEI. Its record details and filter choices omit actor/location fields.

Exactly one cross-source demo match exists: `REC-SYR-ADINT-001` at Site 1, September 22 at 08:00 UTC, has IP `192.0.2.10`. `REC-SYR-IPDR-137` shares that IP, spans 07:58–08:04 UTC and supplies IMEI `000000000001370`. Other IPDR rows do not match an ADINT IP. Verify IP equality and time overlap together. This is a constructed fixture relation, not proof of real-world identity. No ADINT-device association with the convoy is pre-established. Addresses use documentation ranges; all media and observations remain visibly synthetic.

## Syria package history


| Profile | Dataset | Historical change |
|---|---|---|
| 1 | `empty-v1` | Same original catalog definitions, no content |
| 2 | `convoy-v1` | Three CCTV and three Satellite records per site; superseded |
| 3 | `convoy-v2` | One record per source/site; three paired Satellite visits; viewers corrected to show only their own site |
| 4 | `convoy-v3` | Removed cross-site explanation from summaries without changing media/timestamps |
| 5 | `network-v1` | Added four ADINT observations and 200 IPDR sessions; preserved four media records |
| 6 | `network-v1` | Current profile; initial map moved to Damascus, data unchanged |

Earlier packages and state remain available for controlled recovery. Historical backups include `/opt/demo-runtime/backups/syria-convoy-dd6b362`, `syria-convoy-v2-0ba309b` and `syria-network-c7c3319`. They are evidence/recovery points, not the latest release selector. Inspect `/opt/demo-runtime/control/deployed-release.json`, the installed manifest and capability deployment checkpoints before choosing a restore point.

The convoy fixture generator `build_syria_convoy_demo.py` uses Pillow/imageio-ffmpeg offline; the network generator `build_syria_network_demo.py` uses the standard library. These are authoring tools, not commands to run against mutable production state. Do not regenerate a released package in place. The active network-v1 media references are inherited from the convoy packages.

## Demonstration sequence

1. Open CCTV and Satellite at Site 1, then Site 2. Each viewer contains only its own site media.
2. Compare the three paired Satellite dates in Timeline; distinguish repeated observations from unobserved travel.
3. Open the four ADINT observations on Map, then inspect the Site 1 record.
4. Open IPDR in Table and correlate the documented IP and overlapping session to obtain IMEI. Do not infer a convoy-device link from the fixture alone.
5. Switch to Kosovo only through the operator procedure and confirm its own saved state returns.

Kosovo retains the bilingual V2.1 corpus, including 24 synthetic cellular calls. The historical 5,283-row evidence catalog (783 fused objects) belongs to its evidence release, not to Syria. Detailed prior demo scripts and quality results remain in [historical capability records](../.ai/work/capabilities/) and the [documentation archive](../.ai/work/capabilities/documentation-hierarchy/migration-map.md).
