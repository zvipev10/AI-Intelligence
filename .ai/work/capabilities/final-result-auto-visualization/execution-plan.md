# Execution Plan

Review gate: capability, developer, UX, and QA decisions are approved through explicit user delegation.

1. Add a shared final-result view resolver and presentation helper.
2. Route normal and restore-only completions through the helper.
3. Add focused regression coverage and bump the JavaScript cache key.
4. Validate, commit, push, deploy with rollback backup, and smoke-test the VM.

