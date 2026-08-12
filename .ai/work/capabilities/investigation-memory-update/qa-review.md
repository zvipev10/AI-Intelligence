# QA Review

Status: Ready for execution planning; explicitly delegated by the user.

## Required coverage

- Empty chat summaries and layers: no job and no chat message.
- Non-empty summaries or layers: exactly one job per advanced revision.
- Replayed idempotency key: no duplicate agent execution or chat output.
- No active workstreams: general update still runs.
- Moshe failure or delay: general update completes independently.
- General update failure: Moshe and slice advance remain unaffected.
- Returned general-agent state contains memory and timeframe but no workstreams.
- Hebrew and English processing/status/result labels.
- Refresh during processing resumes polling without duplicating the completed chat result in one page session.
