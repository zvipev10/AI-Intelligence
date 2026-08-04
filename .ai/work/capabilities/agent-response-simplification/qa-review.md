# QA review: agent response simplification

## Required fixture matrix

- Welcome and starter prompts.
- Retrieval: one result, many results, and zero results.
- Investigation: confident, uncertain, conflicting, and partial coverage.
- Clarification question.
- Moshe direct answer and target candidate outcome.
- Workstream creation and large workstream update.
- Playback progress, completion, and failure.
- Continuation with prior steps.
- Saved-answer replay.
- Agent, network, configuration, and malformed-response errors.

## Contract checks

- Known `kind`; non-empty headline.
- No more than three findings.
- Per-field character limits, rather than blind whole-answer truncation.
- Coverage is mandatory for partial or truncated queries.
- Error diagnostics are separated from user-facing content.
- Legacy free text still renders safely during migration.

## UI checks

- No horizontal overflow at the current chat width.
- Default response can be scanned without expanding details.
- Evidence and research controls remain keyboard accessible.
- Long lists show a count and a bounded preview.
- Continuation shows only new steps.
- Routine playback changes do not add permanent messages.
- RTL text, mixed IDs, and dates remain readable.

## Regression metrics

- Visible word count by response kind.
- Number of inline canonical IDs.
- Number of duplicated prior research steps.
- Raw JSON/internal tool-name leakage.
- Percentage of partial answers with explicit coverage.
- Time-to-locate the answer in moderated usability checks.

## Release gate

Run the full matrix against recorded fixtures and at least one real live-agent example per durable response kind. Do not deploy if uncertainty, scope, or evidence navigation is lost in simplification.

