# Data Dictionary

## `data/events.csv`

Contains 2,044 synthetic raw intelligence events.

| Field | Type | Meaning |
|---|---|---|
| `event_id` | string | Stable source-based identifier, for example `FIN-0001` or `PORT-0090`. The prefix describes source type, not analytical status. |
| `timestamp_utc` | ISO 8601 string | UTC time of the observation. |
| `source_type` | Hebrew string | Human-readable source category such as financial alert, port record, customs record, movement sensor, camera, or signal intercept. |
| `source_reliability` | Hebrew enum-like string | Reliability assessment such as high, medium, or low. |
| `entity_or_actor` | Hebrew string | Organization, person, vehicle/operator, or unknown actor related to the observation. |
| `location_id` | string | Foreign key into `locations.csv`. Every event has a location. |
| `event_summary` | Hebrew string | Raw-event description. This may contain ambiguous, benign, distracting, or suspicious information. |

## `data/locations.csv`

Contains nine synthetic benchmark locations based on real places in northern Israel.

| Field | Type | Meaning |
|---|---|---|
| `location_id` | string | Stable identifier from `L-201` through `L-209`. |
| `location_name` | Hebrew string | Display name. |
| `latitude` | decimal | Geographic latitude. |
| `longitude` | decimal | Geographic longitude. |
| `type` | Hebrew string | Port, industrial area, border crossing, road junction, urban center, side road, office, or fuel terminal. |
| `notes` | Hebrew string | Context about normal activity and the role of the location. |

## Relationships

- `events.location_id -> locations.location_id`
- One location may contain many events.
- A filtered event set is grouped by `location_id` to produce map count labels.
- Occurrences reference ordered collections of raw-event IDs and ordered route location IDs.

## Source-based ID examples

- `PORT-*`: port record
- `CUST-*`: customs record
- `FIN-*`: financial alert
- `TEL-*`: telephone metadata
- `MOVE-*`: movement sensor
- `CAM-*`: road camera
- `SIG-*`: signal intercept
- `OBS-*`: observation report
- `ACOU-*`: acoustic sensor
- `BORD-*`: border sensor
- `DRONE-*`: drone observation
- `MAINT-*`: maintenance log
- `SOC-*`: social media
- `OPS-*`: operations record

## Encoding and parsing

- Files are UTF-8 CSV.
- Parse with a proper CSV parser; summaries and notes may contain commas.
- Do not parse rows using string splitting.
- Preserve Hebrew strings exactly.
