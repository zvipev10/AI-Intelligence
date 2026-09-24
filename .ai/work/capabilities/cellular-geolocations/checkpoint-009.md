# Call endpoint SIMs

User requested replacing demo numbers with SIMs. Added explicit side_a_sim/side_b_sim fields using the existing geolocation IMEI-to-SIM mapping. Display these in timeline, viewer (label SIM) and map popups; retain number fallback for older call datasets. Immutable Syria call-media-v3/profile20 has 443 records; rebuilt compatible Python search cache. Eight dataset tests and JavaScript syntax passed. No changes to IMEIs, media, locations or Kosovo data.
