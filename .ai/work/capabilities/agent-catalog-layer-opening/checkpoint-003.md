# Checkpoint 003 — filters and UI

Scope implemented: gateway uses the shared resolver; canonicalization preserves validated location/entity/event/time filters. Raw-layer rows endpoint applies the scope. Browser distinguishes filtered/full layers, preserves scope on save/restore and playback refresh, and renders loading success/failure after the final summary so errors stay visible. Retained the production-only console error log. Asset version 185.

Validation: 14 catalog Python tests pass, including tool -> gateway -> real HTTP filtered loading and invalid-filter HTTP 400. Node execution tests pass for filtered/full coexistence, equivalent scopes, refresh, saved restore and successful/failed presentation. JS syntax passes. Full Python discovery initially ran 184 tests with six failures: five old version/manifest assertions reproduce unchanged on origin/main (0eaf3e7); the sixth was the current asset version check, updated to 185 and passing. Added one HTTP integration case afterward.

Known baseline failures: chat_autoscroll asset 178, production_v162 manifest and asset 178, welcome_page asset 178 and stylesheet 147. Baseline currently serves app 184/styles 149. No unrelated changes to these historical assertions.

Release: targeted backup/deploy only, not the general deployment scripts (which include data/config). Verify source hashes against inspected production before replacing. Deploy shared module to UI and MCP, restart services, verify live tool and HTTP result for LOC-V2-001/003, then browser verification. No data or credentials changed. Parent #56, child #57, draft PR #58.
