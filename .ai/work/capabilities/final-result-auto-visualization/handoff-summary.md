# Handoff Summary

Final agent results are automatically presented on map or timeline through one shared client-side presenter. The agent's explicit `recommended_view` is honored; absent/unsupported values resolve from final-layer capabilities and then fall back to map. Supporting evidence-reference layers remain manual. The existing collapsed research-step behavior is preserved.

Published branch: `codex/final-result-auto-visualization`

Implementation commit: `9c463e7`

Deployment: active on `/opt/serbia-poc-ui`, cache key 143.

Rollback: `/opt/serbia-poc-ui.backup-final-auto-view-20260808T143521Z`
