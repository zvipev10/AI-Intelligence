# Capability decisions

## 2026-09-22 — Only one active demo
Decision: the user explicitly requires one demo scenario at a time.
Context: Syria will add a dataset/map and future features, while preserving Kosovo. The existing VM has about 1 GB RAM and two CPUs; a prior read-only idle sample showed about 221 MB available and 1 GB swap occupied. Those observations are not a load-capacity guarantee.
Rationale: avoid duplicate resident agents/indexes and cross-scenario state while sharing development.
Impact: propose stop/start activation of one runtime, isolated saved state, a bounded shared execution queue and versioned demo packages. No second always-running deployment.
Alternatives excluded by user: simultaneously active Kosovo and Syria runtimes.
Follow-up: review proposed operator switching, downtime and state-preservation assumptions in #68. Implementation details remain recommendations, not approved decisions.
