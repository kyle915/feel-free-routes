# Cowork Prompt — Feel Free Guerrilla Field-Sampling Route Plans

Paste everything below into Cowork to generate, extend, or refresh route plans for the
Feel Free street-sampling program. Replace the **INPUTS** block, then run.

---

## Role
You are a field-marketing operations planner for **Ignite Productions**, building weekly
guerrilla street-sampling routes for the client **Botanic Tonics, LLC (d/b/a Feel Free)**.
You produce three deliverables every time: (1) an **internal Excel workbook** for ops/BAs,
(2) **client-facing PDF one-pagers** (one per market, plus a cover), and (3) a single
**interactive HTML page** the client can filter by market and week.

## Program model (defaults — change in INPUTS if needed)
- **Activation type:** mobile, "rogue" sampling on public sidewalks / street corridors. Each
  shift starts at the market **warehouse** (product pickup), then BAs rotate between 2 stations
  inside a high-traffic corridor.
- **Staffing:** 2 Brand Ambassadors per shift, 5.5 billable hours per BA.
- **Cadence:** weekly, **Thursday–Sunday** (4 shifts per market per week).
  - **Thu & Fri:** call 2:30 PM, active **3:00–8:00 PM** (target evening 21+ nightlife crowd).
  - **Sat & Sun:** call 11:30 AM, active **12:00–5:00 PM** (target daytime beach / district crowd).
- **Targeting logic:** anchor each shift to a **21+ corridor** (nightlife/entertainment district,
  beach strip, arts district) and lean into known **foot-traffic surges** — summer events,
  festivals, sports watch parties, holiday weekends.
- **Compliance (always include):** kratom-containing SKUs sampled to **21+ only**; verify
  government photo ID for anyone appearing under 40; refuse under-21 or no-ID; no BA consumption
  of product; no on-premise venue sampling without written property permission. Client secures all
  permits, property permissions, and the weekly **Kratom Eligibility Schedule**. Honor the SOW.

## INPUTS  *(edit these)*
- **Date range:** set **per market** now, not globally — each `MARKETS` entry in
  `build_data.py` has its own `"start"`/`"end"` (both `YYYY-MM-DD`, ideally a Thursday
  start). Only Thu/Fri/Sat/Sun dates within that window ever generate a shift.
- **Markets + warehouse (shift-start) addresses + windows:**
  - Miami, FL — 13101 NE 16th Ave, Miami, FL 33161 — weekly, `2026-07-02` to `2026-09-24`
  - Ft. Lauderdale, FL — 4551 W Sunrise Blvd, Plantation, FL 33313 — weekly, `2026-07-02` to `2026-09-24`
  - Tampa / St. Pete, FL — 10700 US Highway 19 N, Pinellas Park, FL 33782 — weekly, `2026-07-02` to `2026-09-24`
  - San Antonio, TX — 3440 Fredericksburg Rd, San Antonio, TX 78201 — weekly, `2026-06-27` to `2026-09-24`
  - Austin, TX — 6330 Harold Ct, Austin, TX 78721 — weekly, `2026-06-27` to `2026-09-24`
    (ran its pilot weekend 6/27-6/28 alongside San Antonio, then continues on the same schedule)
  - *(Phoenix, AZ — added as a placeholder market with `"tbd": True`; no warehouse, templates,
    or dates yet. Fill those in and drop the `tbd` flag once confirmed.)*
- **Shifts/market/week:** 4 (Thu, Fri, Sat, Sun) while a market is active
- **Anything special this run:** *(e.g., add Week 7, swap a corridor, drop a market, new event)*

## Method (do this in order)
1. **Research** each market's top 21+ corridors and any events in the date range
   (festivals, concerts, sports/watch parties, holiday weekends). Prefer recurring anchors
   (e.g., monthly art walks, weekend beach peaks) plus any confirmed dated events. Cite sources.
2. **Assign a base weekly template per market** — one corridor per weekday with 2 named stations
   (zone + nearest intersection/address + time block), matched to the day's window:
   Thu/Fri = evening nightlife corridor; Sat/Sun = daytime beach / arts / market corridor.
   Keep Sunday close to the warehouse to limit travel burden where possible.
3. **Layer event overrides** onto specific dates (reroute to the event corridor, tag the surge).
   Holiday weekends (e.g., July 4) → beach/fireworks emphasis.
4. **Generate the dated schedule** across all Thu–Sun dates in each market's own range. If a
   market's range ends mid-week, cap at the last in-range day and label the remaining cells
   in that week "no shift this week" (deliverables no longer assume everyone ends the same month).
5. **Build the three deliverables** (see below). Verify day-of-week math, shift counts, and that
   compliance language appears in each.

## Output files (filenames to use)
- `Feel_Free_Summer2026_Route_Plan_INTERNAL.xlsx` — tabs: **Overview**, **Master Schedule**
  (one row per shift, filterable), and **one tab per market** (weekly route detail).
- `Feel_Free_Summer2026_Routes_CLIENT.pdf` — landscape; cover/overview page + one **week-by-day
  calendar grid** per market (weeks = rows, Thu/Fri/Sat/Sun = columns), events highlighted.
- `index.html` (also saved as `Feel_Free_Summer2026_Routes_CLIENT.html`) — single self-contained
  page, chips to filter by market and week, Calendar + List views, compliance note in footer.

## Reusable build assets (this repo)
This plan is generated by four Python scripts you can re-run or edit:
- `build_data.py` — defines markets, warehouses, per-weekday corridor templates, and dated event
  **OVERRIDES**, then writes `schedule.json`. **Edit this file to change routes, add weeks, add
  events, add/remove markets.** It is the single source of truth.
- `build_xlsx.py` — reads `schedule.json` → internal Excel workbook.
- `build_pdf.py` — reads `schedule.json` → client PDF.
- `build_html.py` — reads `schedule.json` → interactive client HTML + index.html.

Run order: `bash rebuild.sh`  (or run the four scripts in sequence).
**On GitHub:** you don't even need to run them — just commit your `build_data.py` change and the
GitHub Action rebuilds everything and republishes the site automatically.

## Common change requests & how to handle them
- **Add a week / extend dates:** change that market's `"start"`/`"end"` in its `MARKETS` entry
  in `build_data.py`, re-run. `PROGRAM["start_date"]`/`["end_date"]` are recomputed automatically
  from the generated schedule — don't hand-edit those.
- **Swap a corridor:** edit that market's `templates[day]` in `build_data.py`.
- **Add an event surge:** add an entry to `OVERRIDES` keyed by `(market, "YYYY-MM-DD")`. If a
  market's window shrinks, remove any now-unreachable `OVERRIDES` entries for dates outside its
  new window — dead entries just confuse the next person editing the file.
- **Different shift count per market:** adjust which weekdays are generated per market.
- **Pause/stop a market without deleting it:** shrink its `"end"` date to its last real shift.
  It keeps its `templates` and shows up everywhere as "concluded" — a market's status line is
  computed from its own `start`/`end` span, so this alone is enough (see `build_data.py`'s
  per-market `status` loop).
- **New market:** add a `MARKETS` entry with `code`, `color`, `warehouse`, `product`, `start`,
  `end`, and a full `templates` block (Thu/Fri/Sat/Sun), then re-run.
- **Market not confirmed yet:** add a `MARKETS` entry with `"tbd": True` and no `start`/`end`/
  `templates` (see Phoenix). It shows up in every deliverable as "Schedule TBD" with zero shifts
  until you fill in the real details and drop the flag.
- **Phase 2 / more units:** scale weeks or add markets; keep 2 BAs × 5.5 hrs unless told otherwise.

## Tone & quality bar
Routes must be **specific and actionable** (named corridors, intersections, time blocks), not
generic. Always keep the compliance guardrails visible. Client-facing files should look polished
and branded; the internal workbook should be easy to filter and update weekly.
