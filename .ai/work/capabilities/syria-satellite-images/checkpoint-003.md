# Satellite image exchange

User requested exchanging the images between the two records. Satellite record 1 now uses satellite-2.jpeg; record 2 uses satellite-1.jpeg. Matching visual descriptions and estimated counts move with the images. Record identities, timestamps, exact coordinates and all other sources remain unchanged. Immutable satellite-v3/profile12 retains rollback data and requires a rebuilt semantic cache.

Validation: 22 focused tests passed; semantic cache rebuilt for 424 records. Deployed fc2ddfb5, with service health and identity verified. Public API confirms record 1 references satellite-2.jpeg and record 2 references satellite-1.jpeg with matching descriptions and original site IDs; maintenance false. Backup: /opt/demo-runtime/backups/syria-satellite-image-swap-fc2ddfb5. Published in draft PR82, not merged. Scenario and operations guides updated; no architecture change.
