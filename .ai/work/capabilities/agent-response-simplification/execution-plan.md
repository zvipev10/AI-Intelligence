# Execution Plan — Collapsed research steps

## Gate

User explicitly approved implementation and deployment on 2026-08-08.

## Slice 1

Wrap each activity item in a native disclosure. Keep the summary minimal and move current metadata/details/actions into the expanded body. Add focused tests and increment cache versions.

## Slice 2

Validate closed and expanded states in both locales, push the branch, back up the VM static UI, deploy changed assets, and verify the public page.

## API/data impact

None.

## Rollback

Restore the deployed static files from the timestamped VM backup and restart `serbia-poc-ui.service`.
