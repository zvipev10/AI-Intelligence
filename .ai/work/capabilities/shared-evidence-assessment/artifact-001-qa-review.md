# QA / Security Review — Indication Artifact

## Status

AI-authored recommendation — pending human QA/Security approval.

## Highest-risk invariants

1. An indication always resolves to a stable item in the explicitly attached layer.
2. Artifact mutations cannot modify raw layer data, Investigation Memory, or the target bank.
3. Removed or contradictory indications remain attributable in revision history.
4. A stale client cannot overwrite a newer revision.
5. Only a distinct, attributable user chat turn can authorize persistence or mark the artifact ready for assessment.
6. Ready for assessment does not create an assessment or target.

## API and persistence tests

- Create the first supported artifact and reload it after server restart.
- Reject a second active artifact of the same type in one workstream.
- Enforce server-owned IDs, timestamps, and revisions.
- Validate bounded payloads, arrays, strings, enums, and participant attribution.
- Parse comma-, space-, and line-separated `REC-...` identifiers.
- Resolve an optional `TGT-...` subject through the read-only target catalog.
- Confirm that `TGT-...` is never counted as evidence and cannot satisfy the minimum-indication rule.
- Reject malformed, unknown, duplicate, and cross-layer record references.
- Add, remove, annotate, and classify indications with correct revision increments.
- Reject stale `expected_revision` with `409` and preserve the stored document.
- Reject mutation of archived workstreams.
- Confirm atomic write behavior and recovery from malformed stored JSON.
- Confirm status-transition allow-list.

## Authority and separation tests

- Reject `send_to_assessment` from an agent participant.
- Accept it only when Moshe supplies the attributable later user turn that confirmed the staged proposal and the current revision.
- Assert that artifact routes never open or mutate the target-bank SQLite database.
- Assert that raw layer files and Investigation Memory files remain byte-identical.
- Treat all client actor fields as untrusted demo attribution; document that this is not production authorization.

## Revision-history tests

- Every accepted action appends actor, action, timestamp, prior revision, and summary.
- Removed indications remain in history and cannot be silently reused with a new identity.
- Contradictions cannot disappear through a partial update.
- Reload produces the same current content and ordered history.
- A rejected artifact remains reviewable and cannot be silently reactivated without a new revision action.

## UX and regression tests

- Indicator behavior remains minimal and unchanged.
- Empty, proposed, active, conflict, read-only, unavailable-source, save-error, and ready states render.
- Manual ID entry, resolution preview, confirmation, cancellation, and retry work entirely in chat.
- Semantically equivalent confirmation and rejection phrasings behave consistently; ambiguous responses cause clarification rather than a write.
- Long record IDs and mixed RTL/LTR copy remain usable.
- Ordinary chat, Hermes routing, Investigation Memory, workstream creation/archive, map, timeline, and target-layer behavior do not regress.

## Manual demo acceptance

1. Create a workstream with one attached historical layer.
2. Address Moshe naturally in general chat with supporting and contradictory `REC-...` references and an optional `TGT-...`.
3. Verify Moshe resolves the references and proposes—but does not persist—the change.
4. Confirm in a later natural-language chat turn and refresh the page.
5. Verify both indications and their roles persist.
6. Remove one indication and verify history remains.
7. Trigger a deliberate stale-revision conflict in a second tab.
8. Send to assessment and verify no target or assessment is created.

## Security risks

- Source text displayed in chat must be escaped.
- Reference validation must not allow path traversal or arbitrary layer access.
- Payload limits must prevent oversized workstream files.
- Production authorization remains unresolved and blocks production release, but not the bounded single-user demo.

## Recommendation

Continue after architecture confirms reference resolution and the team accepts client-supplied actor attribution as a demo limitation.
