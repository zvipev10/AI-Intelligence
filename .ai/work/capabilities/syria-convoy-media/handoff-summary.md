# Syria paired-convoy handoff

Current deployment: Syria convoy-v2/profile 3, runtime `0ba309bee374f6fea8b76c2f71edc7c977c42314`. PR #72 / issue #71, stacked on #69; not merged to main.

Final user contract: one record per source/location, four total. CCTV has two five-second movies, one per site. Satellite has two records containing three paired recurring visits on September 20/21/22, 2026: Site 1 at 08:00 UTC then Site 2 at 08:15 UTC each day. Both viewers show each pair chronologically, with matching visit IDs, timestamps, locations, counterpart images and record IDs. The shared Convoy moves north between sites 5.004 km apart. CCTV represents the final visit. Return journeys are not depicted. All imagery/annotations are clearly synthetic.

Changed areas: immutable v2 dataset/media, Syria profile, media fixture generator, paired-image viewer, bootstrap versions, deployment list and tests. Kosovo profiles/data are unchanged. v1 data/media and state remain retained; source rollback backup `/opt/demo-runtime/backups/syria-convoy-v2-0ba309b`. Persistent Syria state was copied at a stopped transition; existing state was not deleted.

Verification: 15 focused scenario/data tests, paired-renderer chronology checks, JS syntax, representative image inspection, and public API/media checks passed. Public counts: 2 CCTV, 2 Satellite, 2 locations, 1 entity; 8 media assets match installed bytes; all three pairs have reciprocal links and exact 15-minute offsets. Full suite: 235 tests, same 8 baseline failures. Evidence `/opt/demo-runtime/control/syria-convoy-v2-qualification.json`. Real-browser layout/playback acceptance remains pending because no connected browser is available.

Next: refresh the application and open either Satellite record to inspect all three paired visits. Review PR #72 after platform #69. Focused operator documentation updated in `docs/demo-scenarios.md`; no further architecture change is needed. Fixed demo dates and fictional sites are retained assumptions; one record per source/location and synthetic media were user-confirmed.
