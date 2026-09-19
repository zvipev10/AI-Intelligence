# Execution Plan

## Capability

Playback deployment recovery

## Plan status

Approved by the user's explicit end-to-end request.

## Prerequisite review gate

- Product intent: explicit user request to restore playback end to end.
- Developer and QA reviews: captured in this capability workspace.
- Architecture/security constraint: never delete server-owned runtime state during UI deployment.

## Approach

1. Correct the deployment payload and systemd environment.
2. Replace the root manifest with the validated dataset-start baseline.
3. Surface playback loading errors in the header.
4. Test locally, deploy, and run production smoke checks.

## Stop conditions

Stop if live state restoration requires choosing among backups or if the service does not pass the health check after deployment.

## Rollback

Restore the pre-deployment UI directory from a timestamped remote backup before retrying.
