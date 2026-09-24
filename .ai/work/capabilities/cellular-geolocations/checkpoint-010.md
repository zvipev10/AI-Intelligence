# Realistic-format SIM and IMEI values

Applied one injective mapping to the two placeholder device/SIM pairs throughout both locale datasets, preserving equality relationships and blank values. Already-valid imported IMEI shared by IPDR/transcript is unchanged. Active dataset call-media-v5/profile22 remains 443 records. No actual hardware/carrier assignment is claimed.

Nine tests pass, including exact transformation comparison for all 443 records in both languages, identifier lengths/Luhn checks, call-to-geolocation SIM equality and preserved IPDR/transcript matches. Rebuilt Python semantic cache. No geometry, media, IP addresses or Kosovo changes. Mapping retained with the dataset for reproducibility.

Deployed a9d48797; backup /opt/demo-runtime/backups/syria-realistic-ids-a9d48797. Live status healthy, 443 records and maintenance disabled. All live SIM/IMEI fields in both language APIs exactly match the verified dataset. Published in PR86, not merged. Refresh application to load the new dataset generation.
