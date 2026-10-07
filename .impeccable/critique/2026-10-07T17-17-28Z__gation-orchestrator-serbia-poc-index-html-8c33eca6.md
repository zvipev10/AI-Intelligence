---
target: app index
total_score: 20
max_score: 40
na_heuristics: 
p0_count: 0
p1_count: 3
target_identity: "file:/home/claude/ai-intelligence/llm_investigation_orchestrator_serbia_poc/index.html"
target_fingerprint: "sha256:c1ce2420bf28ee0d400b985397a3a5957d2b53eb61c54f0a5233876bf8bb0cc5"
target_path: /home/claude/ai-intelligence/llm_investigation_orchestrator_serbia_poc/index.html
timestamp: 2026-10-07T17-17-28Z
slug: gation-orchestrator-serbia-poc-index-html-8c33eca6
---
# AI Intelligence: Impeccable design critique (2026-10-07)

Method: dual-agent (A: design review in a real browser · B: Impeccable detector plus in-page overlay)
Branch: `feature/i360-only`, run locally against the fake HL API (signed in as analyst/analyst).
Limit: map basemap tiles and Google Fonts were blocked in the sandbox, so map styling was not judged and screenshots use fallback fonts.

## Verdict: generic
The **welcome page reads as an AI-made SaaS dashboard**, and the **workspace reads as a stock dark admin panel**. Rename "investigation" to "project" and it could be any collaboration tool.

The specific tells:
- **Welcome page layout.** A centred "Welcome back" hero sits over a radial blue glow, with a centred pill CTA under it. Below are rounded gradient cards with a coloured left stripe, centred text and a hover lift.
- **The "AI suggestion" marker.** The sparkle icon (`auto_awesome`) plus a lavender colour, the most recognisable LLM-era cliché.
- **Borrowed palette.** The colours are Google Material dark-theme values plus GitHub's blue. Nothing in them encodes source type, reliability or time.
- **Wide soft shadows.** Every modal, popover and the login panel has a 46–70px blur. The detector flagged this 16 times, its single strongest signal.
- **Tiny uppercase labels.** 10–11px all-caps labels ("PARTICIPANTS", "Activity level").
- **Fonts.** Roboto, with a Hebrew font leading the stack in an English-only app. Inter on the two guide pages. IDs, IPs and timestamps are in proportional type.
- **Kicker-over-heading pattern.** It repeats in all 8 sections of the user-flow guide page, under a tracked-caps eyebrow chip.

## Design health: 20/40 (Acceptable)
| # | Heuristic | Score | Key issue |
|---|---|---|---|
| 1 | System status | 2 | Data-source status is a tiny dot; no table loading state; joined investigation still listed under Invitations |
| 2 | Real-world match | 2 | "Memory", "draft", raw field name "Events by source_type"; no analyst-style reliability grading |
| 3 | User control | 3 | Escape closes viewers, modals and filters consistently |
| 4 | Consistency | 2 | Welcome page and workspace look like two products; login and help still half Hebrew |
| 5 | Error prevention | 2 | Empty state points to a "+" button that is hidden until you are in a draft |
| 6 | Recognition vs recall | 1 | Layers can only be added by typing names you must already know; empty search lists nothing |
| 7 | Efficiency | 2 | No keyboard shortcuts, multi-select or saved views |
| 8 | Minimalist design | 2 | Decorative welcome page; empty Map/Timeline/Table are black voids |
| 9 | Error recovery | 2 | Blank map gives no message when tiles fail |
| 10 | Help | 2 | Help is a static, partly Hebrew page in a new tab |

## What's working
- **The record viewer.** A plain-language summary sits above the raw fields, the ID is in monospace, and the panel docks beside the table. It is the most authored moment.
- **The dense IPDR table.** 300 rows with per-column sort and filter. It suits analysts.
- **MIL-STD markers and the teal/ochre call endpoints.** These are real seeds of a domain visual language.

## Priority issues
1. **[P1] The welcome page is a generic SaaS card template.**
   - *Fix:* replace the hero and cards with a compact, left-aligned investigation register: name, case ID, last activity (UTC), layers, members, access.
   - Remove the sparkle, the lavender colour, the glow, the 18px radius and the hover lift.
   - Show *why* an investigation is proposed ("shares 3 IMEIs with…") instead of "High overlap".
   - *Commands:* `/impeccable distill`, then `layout`.
2. **[P1] There is no domain visual language.**
   - *Fix:* one restrained colour per source family (SIGINT, VISINT, IPDR, CCTV, cellular), used consistently in tabs, timeline and map.
   - Show reliability and certainty as graded chips.
   - Set IDs, IPs, IMEIs and timestamps in monospace or tabular figures.
   - Use one English body font, self-hosted.
   - *Commands:* `typeset`, then `colorize`.
3. **[P1] The empty workspace and layer search are dead ends.**
   - *Fix:* show the source catalogue (with record counts) when the search is empty and in the empty views, as one-click "Add CCTV (2) / IPDR (300)".
   - Show "Basemap unavailable" when tiles fail.
   - *Commands:* `onboard`, then `harden`.
4. **[P2] Analyst concepts are plain grey text.**
   - *Fix:* show reliability and certainty as chips, not strings.
   - Make the timeline a horizontal time axis with lanes per source, linked to the map and table.
   - *Commands:* `shape`, then `bolder` (timeline only).
5. **[P2] The mobile layout breaks.**
   - The header grows to 197px, the Map tab scrolls off-screen, and the table clips on the left.
   - *Command:* `adapt`.

## Persona red flags
- **Power user:**
  - No shortcuts for switching views, adding layers or stepping through records.
  - Tab alternates ID and Save for all 300 rows.
  - The hero sits between them and their list on every visit.
- **Accessibility:**
  - Focus outlines are removed and replaced by a faint tint.
  - Layer-tab controls are icon-only.
  - Labels are 10–11px.
  - There is no reduced-motion rule.
  - The bilingual login labels confuse screen readers.
- **All-source analyst:**
  - Reliability is shown as prose with no grade.
  - There is no classification banner.
  - Timestamps use two formats (`…T08:00:00Z` vs `… 08:00:00`).
  - Unexplained sparkle "recommendations" invite distrust.
  - The "Welcome back" tone and stock-photo avatars feel wrong for the setting.

## Detector false positives
- The low-contrast hits on the guide pages are video elements and a gradient sampling error. The one real hit is white on amber at 2.6:1.
- Two of the "side stripes" are CSS triangles.
- The pulsing dot comes from the vendored MapLibre geolocate control.

## Questions to consider
1. What would be lost if analysts landed directly in their last investigation, with the register one keystroke away?
2. What if colour encoded source and reliability instead of "brand blue"?
3. Would an analyst join a proposed investigation without seeing the overlapping identifiers?

Screenshots in this folder: desktop-welcome, desktop-table-ipdr, desktop-workspace-map, desktop-record-viewer, mobile-table-ipdr.
