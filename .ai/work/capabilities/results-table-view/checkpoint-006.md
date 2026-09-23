# Checkpoint 006 — Remove persistent scenario footer

User requests removal of Syria label at application bottom. Bootstrap now hides the footer notice during normal operation and idle polling. Operational errors, scenario-change notices and queued-request cancellation remain visible when relevant, without a scenario label. Applies to normal footer for all scenarios; active Syria dataset remains unchanged. Cache bump bootstrap 208; app remains 207.

Validation: syntax and bootstrap DOM harness covering normal startup, idle polling, queue notice and return to idle; deploy static files and verify public source. No additional dependencies or data change.
