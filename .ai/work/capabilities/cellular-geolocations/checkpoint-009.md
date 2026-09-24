# Call endpoint SIMs

User requested replacing demo numbers with SIMs. Added explicit side_a_sim/side_b_sim fields using the existing geolocation IMEI-to-SIM mapping. Display these in timeline, viewer (label SIM) and map popups; retain number fallback for older call datasets. Immutable Syria call-media-v3/profile20 has 443 records; rebuilt compatible Python search cache. Eight dataset tests and JavaScript syntax passed. No changes to IMEIs, media, locations or Kosovo data.

User clarification: use the numbers themselves, not DEMO-SIM labels. call-media-v4/profile21 consistently replaces both labels with numeric demo strings 89000000000000000001/002 in calls and geolocations. Eight preservation/search tests pass and the search cache is rebuilt.
