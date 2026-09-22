# Developer and architecture review

Status: Draft recommendations; not human-approved. Inputs: inspected origin/main d475d2e and the read-only VM observations from 2026-09-22. Review issue #68.

## Findings and affected sources
- server.py selects Kosovo-specific paths using INTELLIGENCE_POC_DATASET_VERSION; STATE_SUFFIX scopes investigations, playback, recordings and catalogs mainly by version. Add scenario identity independently of version.
- app.js contains Kosovo map center/bounds, scenario text and serbia-prefixed browser-storage keys. Bootstrap profile before map creation/state reads.
- agent_routing.py indexes session bindings by conversation; prefix identity and cover Hermes and optional OpenAI routes.
- mcp_server/server.py loads EVENTS at import and uses dataset-specific environment paths plus a fixed UI catalog URL default. Switch via process lifecycle, not by mutating global environment in a running process.
- The inspected VM gateway truncates a shared audit file per run. Use run-scoped audit/live-step state.
- scenario_playback.py, workstream_artifacts.py, mcp_server/target_bank.py and evidence/index generation require storage/config inventory. Locate every background job admission path before introducing the queue.
- remote_deploy_ui.py is tied to a dataset/service/port. Parameterize package selection; retain incremental deployment and external persistent state. Preserve both restored documentation pages and their media.

## Recommendation
One active service set with operator-controlled activation; scenario/role state homes on disk; one agent execution slot initially. Avoid two deployments, an always-resident second MCP index, or prompt-only switching. Confirm installed Hermes support rather than applying assumptions from newer documentation. Profiles alone do not namespace our custom tools or external state.

## Risks and review gates
Storage migration and activation are architectural changes. Resolve the durable queue/restart behavior, external-action cancellation limits, compatibility/rollback contract and existing background services before coding. Do not claim memory sufficiency from idle measurements. No dependency selected in this proposal. See proposed-plan.md for slices and completion tests.

## Ready-for-planning status
The user asked for a proposal; the saved proposed sequence satisfies that request. Formal execution-plan.md and implementation authorization remain pending review of this draft, UX and QA recommendations. No approval inferred for unnamed Syria features.
