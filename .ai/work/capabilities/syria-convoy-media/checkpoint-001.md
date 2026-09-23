# Implementation checkpoint

Issue #71, parent #67; stacked on scenario platform PR #69. Implemented immutable Syria convoy-v1: 12 records, two sites 5.004 km apart, one Convoy entity. CCTV has six 5-second H.264 movies. Satellite has six records, each with three distinct timestamped PNG captures. All assets contain synthetic labels. Source annotations are deterministic fixture data, not an actual computer-vision extraction claim.

Generic record viewer supports safe timestamped image sequences; MCP preserves media fields and canonical entity/location enrichment. Syria gains CCTV/Satellite sources (18 total catalog layers), map focus and appropriate welcome copy. Kosovo profile and datasets remain unchanged. Readiness now respects the profile empty flag rather than hardcoding Syria as empty. Scenario media paths are fenced to the active scenario.

Checks: 15 scenario/dataset tests passed; media renderer harness passed; direct MCP enrichment passed. Full suite 235 tests, same 8 baseline failures. Media sample visually inspected; no browser available. Generator dependencies Pillow/imageio-ffmpeg are offline build-only, no VM runtime dependency.

Deployment next: private source/state backup, stopped copy of Syria empty-v1 state into convoy-v1 with updated state metadata, prebuilt index, release manifest and live readiness/media/count verification. Keep empty-v1 and backups for rollback. Do not copy Kosovo state.
