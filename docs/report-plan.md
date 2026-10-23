# Investigation report from memory: plan

Decided with Zvika, 2026-10-14. Full plan: https://claude.ai/code/artifact/36c3baaf-7bfd-4f2e-9502-aa668a259018
Mockups: `docs/report-mockups.html` (open in a browser). **Zvika picked layout A, "Document".**

## Decisions

- Shape: the Op Praha sample report (Multi-INT fusion assessment), not a generic summary.
- Facts come straight from the memory records and their i360 links. No model touches a fact.
- Analysis (interpretation only) is written by HL API `/api/v1/llm/chat`, one call per analysis block,
  JSON schema per block, citing only the record refs it was given. Not the i360 chat.
- Subject person: default = the person with the most linked memory records, changeable in the Create report dialog.
- Classification: one free-text line in the dialog, repeated in the footer.
- Storage: browser + PDF only (Export PDF = browser print with a print stylesheet). Nothing written to i360.

## Layout A: Document

The report renders as a white paper page (like the PDF it becomes) centred on the app's dark background.
A top bar holds the breadcrumb (Investigation › Memory › Report), per-section progress chips
(Facts ready, Summary, Findings n/6, Assessment…), Back to memory and Export PDF.

On the page:
- Header line: "Intelligence Report · <classification>" left, "<report id> · <date>" right.
- Title + one subtitle sentence built from the layers present ("Fusion of Satellite, ADINT, IPDR, ... records on one subject").
- Summary box (key/value rows): subject IMEI, reporting period (earliest-latest memory record), area (bounding box of located records; a place name, if any, is analysis and tagged).
- Each analysis block is a tinted panel tagged "Analysis · HL LLM · <time> · cites N records" with Edit and Regenerate, and record refs after each sentence. Fact values are plain text with a dotted underline that opens the record.
- Analysis blocks fill in as they arrive; fact sections render first.

## Sections, in order

| Section | Source | How |
|---|---|---|
| Header + summary box | Facts | title = investigation name; report id = short name + run number; period; area; subject IMEI |
| Executive summary | Analysis | 4-6 sentences over all memory records |
| Source correlation chain | Facts + 1 analysis line | steps from i360 links: Satellite=Detection, ADINT=Device set, IPDR=Attribution, person=Identification, Calls=Intercept, CCTV=Confirmation. ADINT-IPDR link is on the public IP (IPDR ip_public / ADINT ip). A step with no i360 link is dashed, tagged "no i360 link" |
| Findings by source, one block per layer in memory | Facts + analysis | fact line (count, time range, key fields under mapping names) then a short narrative per layer: Satellite (coordinates, detected objects, thumbnails), ADINT (devices, IPs, keyboard), IPDR (private IP, carrier, IMEI, matched value), Calls (verbatim translation quote printed by the app; the model only picks which line), Cellular Locations (route in time order, distance computed), CCTV (thumbnail, time) |
| Subject identification | Facts | person entity: name, IMEI, MSISDN and IMSI with status ("Recommended" shown as not yet approved) |
| Subject identifiers table | Facts | IMEI, MSISDN, IMSI, device, public IP (ADINT), private IP + carrier (IPDR), top B-party contacts |
| Assessment and confidence | Analysis | JSON list {claim, level HIGH/MODERATE/LOW, refs}; app draws the badges; then open questions |
| Attachments | Facts | memory records grouped by layer as annexes A, B, C |
| Footer | Facts | classification, report id, page numbers (print stylesheet) |
