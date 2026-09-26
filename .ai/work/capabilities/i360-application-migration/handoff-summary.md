# Handoff: I360 application migration planning

## Completed

Created a capability brief, role reviews, decisions, status dashboard, and two-part implementation plan. Part 1 delivers the non-chat analyst application on I360. Part 2 adds chat-based investigation through an application-owned controller and I360 `llm/chat`.

## Scope decision

Workstream and scenario playback are excluded. The plan preserves the current frontend and investigation logic behind an I360 provider adapter.

## Next action

Architecture/security and product review the split, then Development runs P1.0 using an authenticated ordinary-user I360 test environment. Part 1 can proceed and ship without the agent work; Part 2 may start after the Part 1 domain services are stable.

## Key handoff inputs needed

- I360 environment and authentication mechanism;
- ordinary-user test identities and permission matrix;
- representative item/entity/media IDs;
- platform owner for data-ingestion and capability questions.
