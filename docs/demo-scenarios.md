# Demo scenarios

Owns versioned dataset contents, fixtures and narratives. For activation, migration and recovery, use [operations](operations.md). Installed profiles remain authoritative as packages evolve.

## One application, two demo packages

The bilingual Hebrew/English intelligence workspace has one shared codebase and reusable General, Moshe and Talia agent roles. Exactly one scenario is active on the VM at a time. Switching packages changes geography, data and isolated working state; it does not create a second deployment or a country-specific application branch.

| Package | Current profile / dataset | Content |
|---|---|---|
| Kosovo | profile 1 / `v2.1` | 14,833 records, including 24 simulated cellular calls; preserved investigations and agent state |
| Syria | profile 20 / `call-media-v3` | 443 records: 2 CCTV, 2 Satellite, 120 ADINT, 300 IPDR, 18 Cellular Geolocations, 1 Cellular Call; 102 locations, 13 entities and 21 catalog definitions |

Deployment identity must be checked through `/api/status`; this is an installed-package inventory, not a live status assertion. Syria's initial camera is Damascus (longitude 36.2765, latitude 33.5138), zoom 11. The fictional convoy sites are elsewhere; opening results can fit the map to their geometry. Installed profiles, not this document, are authoritative for future versions.

## Syria demonstration data

CCTV Site 1 uses `LOC-SYR-ADINT-002` (35.077055, 36.333669); Site 2 uses `LOC-SYR-ADINT-001` (35.108621, 36.312140). These reuse existing ADINT observation points. Both media sources identify `ENT-SYR-CONVOY`. Media/timestamps are unchanged; spatial co-location does not establish that the ADINT device is the convoy. Original site definitions remain historical catalog entries with no current media records.

- **CCTV:** one record and one five-second synthetic movie per site, representing the September 22 visit.
- **Satellite:** one supplied image per record, at dedicated Satellite observation sites 1/2, at user-supplied coordinates: site 1 (35.065212338738036, 36.28815755309795), site 2 (35.06503531383431, 36.289563371508734). No repeated visits, paired captures or return/movement narrative. Descriptions reflect visible vehicles, road and terrain. The supplied images visibly carry SYNTHETIC DEMO; originals and provenance remain intact. No capture-date/GPS metadata was supplied: existing record times are labeled scenario timestamps, and map coordinates are user-supplied positions. CCTV remains at the ADINT reference points.
- **ADINT:** 120 observations imported from the supplied `ADINT2` (preserved as `ADINT.json`), September 1–5, 2026, replacing the four original observations. Native fields: `observation_id`, `device_id`, `timestamp_utc`, `brand`, `model`, `os`, `keyboard_language`, `ip`, `latitude`, `longitude`, `accuracy_m`. Twelve device identities are not identified people. There are 84 distinct coordinate points and 36 geometry-free observations; all 120 IP values are populated and 76 keyboard-language values are null. Missing values are preserved, not inferred. The table/viewer expose these fields; geometry-free records remain accessible in Table.
- **IPDR:** 300 records from `IPDR-expanded.csv`, replacing the prior 200 sessions. Native fields: start_time, end_time, ip_source, ip_target, ip_public, ip_private, ip_out, record_id, source_port, target_port, public_port, protocol, bytes_sent, bytes_received, source_system, imei, mac, SUBNETMASK. Only two rows supply IMEI; absent values remain blank. No actor or location is asserted. Table/viewer show all source fields and no map action. Internal `source_record_id` retains the original record_id string separately from canonical application event IDs. SUBNETMASK header whitespace is trimmed; source values and original file bytes are retained.

The imported sessions are dated September 1-6. Records 3001185062876120 and 3495155497992130 contain an end date before the start date; these source values are preserved pending user clarification and must not be treated as valid time-overlap evidence. Match the appropriate IP role and valid session interval before drawing a correlation. Do not infer a convoy/device relationship from location sharing.

## Syria package history


| Profile | Dataset | Historical change |
|---|---|---|
| 1 | `empty-v1` | Same original catalog definitions, no content |
| 2 | `convoy-v1` | Three CCTV and three Satellite records per site; superseded |
| 3 | `convoy-v2` | One record per source/site; three paired Satellite visits; viewers corrected to show only their own site |
| 4 | `convoy-v3` | Removed cross-site explanation from summaries without changing media/timestamps |
| 5 | `network-v1` | Added four ADINT observations and 200 IPDR sessions; preserved four media records |
| 6 | `network-v1` | Initial map moved to Damascus, data unchanged |
| 7 | `adint-v1` | Replaced ADINT with 120 supplied observations and native fields; 84 new points, old ADINT-only points/devices removed; other sources unchanged |
| 8 | `adint-v2` | Moved both CCTV/Satellite site groups to existing ADINT points 002 and 001; image pair references updated, media/times and other sources unchanged |
| 9 | `ipdr-v1` | Replaced 200 IPDR sessions with 300 supplied records and the expanded native schema; other layers unchanged |
| 10 | `satellite-v1` | Replaced Satellite sequences with two supplied images; created two sites30m east; retained disclosed image provenance |
| 11 | `satellite-v2` | Updated the two Satellite site coordinates to user-supplied positions; records/media unchanged |
| 12 | `satellite-v3` | Swapped the two Satellite images and matching descriptions/counts; coordinates unchanged |
| 13 | `adint-v3` | Replaced all 120 ADINT records from ADINT2; all IPs populated, locations unchanged |

Earlier packages and state remain available for controlled recovery. Historical backups include `/opt/demo-runtime/backups/syria-convoy-dd6b362`, `syria-convoy-v2-0ba309b` and `syria-network-c7c3319`. They are evidence/recovery points, not the latest release selector. Inspect `/opt/demo-runtime/control/deployed-release.json`, the installed manifest and capability deployment checkpoints before choosing a restore point.

The convoy fixture generator `build_syria_convoy_demo.py` uses Pillow/imageio-ffmpeg offline; the network generator `build_syria_network_demo.py` uses the standard library. These are authoring tools, not commands to run against mutable production state. Do not regenerate a released package in place. The active network-v1 media references are inherited from the convoy packages.

## Demonstration sequence

1. Open CCTV and Satellite at Site 1, then Site 2. Each viewer contains only its own site media.
2. Open each Satellite record: one image, own Satellite site, explicit timestamp basis and accurate image description.
3. Open ADINT in Table to inspect all 120 observations; Map shows only observations with supplied coordinates.
4. Open IPDR in Table and compare IP plus session time. Respect missing identifiers and reject reversed session intervals when evaluating a temporal match.
5. Switch to Kosovo only through the operator procedure and confirm its own saved state returns.

Kosovo retains the bilingual V2.1 corpus, including 24 synthetic cellular calls. The historical 5,283-row evidence catalog (783 fused objects) belongs to its evidence release, not to Syria. Detailed prior demo scripts and quality results remain in [historical capability records](../.ai/work/capabilities/) and the [documentation archive](../.ai/work/capabilities/documentation-hierarchy/migration-map.md).

## Cellular samples

Syria cellular-v1/profile14 adds four synthetic Cellular Geolocations with string IMEI, SIM and canonical location_id, plus two synthetic Cellular Calls showing side_a_imei and side_b_imei. Two demo devices (990000000000001/2) use DEMO-SIM-SYR-001/002 at existing ADINT points 001/002 on September 1 at 09:00 and 10:00 UTC, with calls five minutes later. These are invented examples, not collected communications; no audio/transcript is supplied. Existing 424 rows and Kosovo data remain unchanged. Record IDs and timestamps support the standard viewer, map and timeline.

### Coastal route extension

cellular-v2/profile15 retains the four initial cellular observations and adds twelve device-1 observations from Satellite site 1 toward the Baniyas seafront on September 20, 08:30–11:15 UTC, at 15-minute intervals. These synthetic waypoints show a scenario route, not a verified road track. Both calls occur at Coastal route stop 05 (35.133, 36.117), at 09:46 and 09:50. Side B is at a separate new remote location (35.12, 36.03), with two matching device-2 geolocations. All existing non-call records and earlier location coordinates remain unchanged. Coastal geographic reference: [Baniyas](https://mapcarta.com/Baniyas).

cellular-v3/profile16 moves only the first route observation to LOC-SYR-CELL-START-001, a new point 60 metres north of Satellite site 1. The Satellite coordinates, other route observations and call endpoints remain unchanged.

cellular-v4/profile17 moves Side B of both calls and its two matching geolocations to new LOC-SYR-CALL-NORTH-001 (36.60,37.05), far north of every Side A route point. Side A and route coordinates are unchanged; the prior remote location remains historical with no current call references.

### Supplied Call 1 media

call-media-v1/profile18 attaches the supplied Arabic recording, original transcript and English translation to REC-SYR-CALL-001. The viewer presents caller details, a satellite endpoint map, bilingual conversation bubbles and audio controls. The original MP3 and text files are retained; a PCM WAV derivative supports browser playback. No per-line timestamps were supplied, so bubbles are not synchronized to audio. Scenario times, coordinates and existing IMEIs remain demo metadata. Transcript speaker IMEI 353294702931926 is displayed separately from the scenario IMEI pending confirmation. In that historical version, Call 2 had no media; the current version removes it as described below. Kosovo is unchanged.

call-media-v2/profile19 removes REC-SYR-CALL-002 from both locale datasets at the user's request. All other records, Call 1 media, locations, entities and Kosovo remain unchanged. The previous dataset is retained for rollback.

call-media-v3/profile20 adds side_a_sim and side_b_sim to Call 1, matched by endpoint IMEI to DEMO-SIM-SYR-001 and DEMO-SIM-SYR-002 in Cellular Geolocations. Timeline, viewer and map endpoint popups prefer SIMs over legacy demo numbers. IMEIs, locations and supplied media remain unchanged.
