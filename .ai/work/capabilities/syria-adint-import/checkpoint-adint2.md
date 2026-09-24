# ADINT2 replacement

Replace all 120 ADINT records from user-supplied ADINT2. Validated schema and unique IDs. Source differs only in all 120 IP values; 12 devices, 84 distinct coordinate pairs, 36 records without geometry and 76 missing keyboard languages are unchanged. No missing IPs; 10 records use 203.0.113.107. Copy exact source bytes into ADINT.json. Preserve location IDs/coordinates and all 304 non-ADINT records, including exchanged Satellite images. New immutable adint-v3/profile13; rebuild cache and deploy with state backup. Issue81 / draft PR82.
