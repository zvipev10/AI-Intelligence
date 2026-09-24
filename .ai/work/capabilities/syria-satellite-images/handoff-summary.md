# Satellite image update handoff

Deployed Syria satellite-v1/profile10, runtime527915be. Dataset424 rows,88 locations,13 entities. Satellite record1 uses supplied WhatsApp17.14.49 image at LOC-SYR-SAT-001; record2 uses17.14.50 at LOC-SYR-SAT-002. Each new site is30m east of the previous ADINT reference point. CCTV/ADINT/IPDR unchanged. Each Satellite image_series contains exactly one own image and no pair/visit metadata. Source labels/location names/descriptions now say Satellite. Removed repeated-visit narrative and unsupported movement/confidence fields. Single-image heading fixed to Satellite image.

Both input images visibly contain SYNTHETIC DEMO and no EXIF metadata. Original JPEGs are preserved byte-for-byte, including watermark. Description reflects image content; authenticity is not invented. Existing scenario record timestamps are retained with explicit timestamp_basis; capture date is not supplied. Coordinates are assigned scenario positions, not verified image geolocation. This is the limit on the user request to make the information non-synthetic.

22 focused tests passed, JavaScript syntax passed, activation verified UI/gateway/role identity. Live API confirms two single-image records/new locations; downloaded JPEG bytes exactly equal both supplied files. Browser verified Satellite labels, new location names, single-image viewer and timestamp basis. Final static heading served correctly. Source/state backup /opt/demo-runtime/backups/syria-satellite-fd4c5e17; prior dataset/state retained.

Published with preceding ADINT/IPDR changes in draft PR82, not merged. Scenario/operations docs updated. Next: refresh application to see the latest assets. No full-suite or new LLM investigation claimed.
