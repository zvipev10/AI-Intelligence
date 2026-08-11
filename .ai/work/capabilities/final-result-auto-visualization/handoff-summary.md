# Handoff Summary

Final agent results are automatically presented on map or timeline through one shared client-side presenter. The agent's explicit `recommended_view` is honored; absent/unsupported values resolve from final-layer capabilities and then fall back to map. Supporting evidence-reference layers remain manual. The existing collapsed research-step behavior is preserved.

Follow-up fix: when a final result and its first requested layer disagree, the valid run-level `recommended_view` now has priority. This prevents a map-oriented layer hint from overriding a final timeline recommendation. The focused regression suite passes; this follow-up has not yet been deployed.

Published branch: `codex/final-result-auto-visualization`

Implementation commit: `9c463e7`

Deployment: active on `/opt/serbia-poc-ui`, cache key 143.

Rollback: `/opt/serbia-poc-ui.backup-final-auto-view-20260808T143521Z`
