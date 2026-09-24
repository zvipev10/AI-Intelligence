# Conventional ADINT record identification

User requests Record terminology and REC-prefixed identifiers like other layers. ADINT table and record-details identifier now use canonical event_id labeled Record ID, replacing the observation_id/OBS display. Existing canonical IDs and record navigation remain unchanged; source observation_id retained in data for traceability/search. No dataset/state migration required. Static UI update only.

Deployed e76f58f4 on the VM; app/bootstrap version216. JS syntax and isolated viewer checks pass. Live-served table uses event_id/Record ID and canonical links; source OBS identifiers are no longer the displayed column. Existing identifiers/data/state unchanged. Published in draft PR82, not merged.
