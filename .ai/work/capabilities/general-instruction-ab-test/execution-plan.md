# General instruction A/B test execution plan

1. Preserve inline mode as the default and add an explicit, allowlisted `persistent` mode for General requests only.
2. Provision `generalpersistent` as an isolated Hermes profile on port 8644 with a separate audit path and the same General MCP capabilities.
3. Store the stable investigation, safety, evidence, and presentation contract in the profile `SOUL.md`; continue sending locale, classification/continuation contract, catalog IDs, and investigation state per run.
4. Record instruction mode, instruction characters/bytes/hash, serialized request bytes, Hermes timings, tool timings, and provider token usage.
5. Run 12 sequential paired repetitions of one frozen, read-only question, alternating A/B and B/A order. Report cold observations separately from warm medians and P90.
6. Review anonymized answer correctness, evidence IDs, tool sequence, coverage, uncertainty language, and presentation actions before deciding whether persistent mode may become the default.

Adoption gate: at least 20% lower warm median end-to-end latency, no P90 regression, no additional failures/timeouts, and no material quality or safety regression.
