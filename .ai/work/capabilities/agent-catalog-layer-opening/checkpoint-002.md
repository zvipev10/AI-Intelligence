# Checkpoint 002 — catalog resolution

Implemented authoritative live catalog lookup and a conservative shared resolver. The exact production typo resolves to the real UAV catalog ID. Unavailable catalogs and ambiguous names queue no action. Tool status is pending_ui, not opened. Explicit filters survive resolution; malformed filters fail closed.

Focused tests cover Hebrew normalization, aliases, typo ambiguity, unknown family, unavailable catalog and scope intersections. An initial test expected recovery for two near-equal names; the conservative implementation correctly requires clarification, and the expectation was corrected.

Next: gateway defense and filtered UI loading, then regression and production validation. User approved this scope. Parent #56.
