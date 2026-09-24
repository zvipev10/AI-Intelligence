# Calls timeline and adjacent viewer

User-requested change: default calls to Timeline even with geometry; open call details beside rather than over the timeline; keep timeline entries compact. Assumption pending optional clarification: a narrow vertical list with time, duration, endpoints and one-line summary.

Implementation slices: (1) calls-aware default for catalog/results and agent guidance; (2) compact keyboard-operable timeline buttons and nonmodal viewer docking, with cleanup on close/view change and stacked layout on small screens; (3) automated defaults/escaping tests, browser visual and interaction verification, VM deployment and handoff. Explicit Map/Table recommendations remain available. Mixed-source defaults remain unchanged. Reuse current viewer and media, with no dataset change.

Risks/checks: timeline must remain clickable; audio/map resources must release when switching records; source text must be escaped; no duplicate DOM ids; manual view changes must be honored. User request authorizes this UX implementation.
