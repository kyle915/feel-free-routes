"""
Feel Free Summer 2026 Guerrilla Sampling — master route dataset builder.
Generates schedule.json consumed by the Excel, PDF, and HTML deliverables.
EDIT THIS FILE to change routes, add weeks, add events, or add/remove markets.
"""
import json, datetime

# ---------------------------------------------------------------------------
# Program constants
# ---------------------------------------------------------------------------
PROGRAM = {
    "name": "Feel Free — Summer 2026 Guerrilla Field Sampling",
    "client": "Botanic Tonics, LLC (d/b/a Feel Free)",
    "agency": "Ignite Productions",
    "start_date": "2026-06-25",
    "end_date": "2026-07-31",
    "bas_per_shift": 2,
    "billable_hours_per_ba": 5.5,
    "cadence": "Weekly, Thursday–Sunday",
    "windows": {
        "Thu": {"call": "2:30 PM", "active": "3:00–8:00 PM", "release": "8:00 PM"},
        "Fri": {"call": "2:30 PM", "active": "3:00–8:00 PM", "release": "8:00 PM"},
        "Sat": {"call": "11:30 AM", "active": "12:00–5:00 PM", "release": "5:00 PM"},
        "Sun": {"call": "11:30 AM", "active": "12:00–5:00 PM", "release": "5:00 PM"},
    },
    "compliance": (
        "Kratom-containing SKUs are sampled to 21+ only. BAs verify government-issued photo ID "
        "for anyone appearing under 40 and refuse anyone under 21 or who declines ID. No BA "
        "consumption of sampled product. Sampling occurs on public sidewalks / street corridors; "
        "no on-premise venue sampling without written property permission. Per the SOW, Client "
        "secures all permits, property permissions, and the weekly Kratom Eligibility Schedule."
    ),
}

EVE_BLOCKS = ["3:00–5:30 PM", "5:30–8:00 PM"]
DAY_BLOCKS = ["12:00–2:30 PM", "2:30–5:00 PM"]

# ---------------------------------------------------------------------------
# Markets, warehouses, and base weekly route templates
# ---------------------------------------------------------------------------
MARKETS = {
    "Miami, FL": {
        "code": "MIA", "color": "#E5552E",
        "warehouse": "13101 NE 16th Ave, Miami, FL 33161 (North Miami)",
        "product": "Kratom-eligible (FL Kratom CPA) + non-kratom SKUs",
        "templates": {
            "Thu": {"corridor": "Wynwood", "vibe": "Arts district / breweries / World Cup watch parties",
                "why": "Young 21+ creative crowd; FIFA World Cup watch parties surge through 7/19.",
                "stops": [
                    {"zone": "Wynwood Walls & Marketplace", "address": "NW 2nd Ave & NW 26th St"},
                    {"zone": "Cervecería La Tropical (World Cup watch)", "address": "42 NE 25th St"}]},
            "Fri": {"corridor": "Brickell", "vibe": "Rooftop / happy-hour finance crowd",
                "why": "Peak 7pm–2am energy; dense walkable 21+ after-work corridor.",
                "stops": [
                    {"zone": "Mary Brickell Village", "address": "901 S Miami Ave"},
                    {"zone": "Brickell City Centre", "address": "701 S Miami Ave"}]},
            "Sat": {"corridor": "South Beach", "vibe": "Beach + Lincoln Road daytime",
                "why": "Highest weekend daytime foot traffic; beach-bar 21+ crowd.",
                "stops": [
                    {"zone": "Lincoln Road Mall", "address": "Lincoln Rd & Washington Ave"},
                    {"zone": "Ocean Drive beachfront", "address": "Ocean Dr & 8th St"}]},
            "Sun": {"corridor": "Coconut Grove", "vibe": "Waterfront / CocoWalk daytime",
                "why": "Relaxed daytime 21+ brunch + waterfront crowd.",
                "stops": [
                    {"zone": "CocoWalk", "address": "3015 Grand Ave"},
                    {"zone": "Regatta Park waterfront", "address": "3500 Pan American Dr"}]},
        },
    },
    "Ft. Lauderdale, FL": {
        "code": "FTL", "color": "#1F8FB2",
        "warehouse": "4551 W Sunrise Blvd, Plantation, FL 33313",
        "product": "Kratom-eligible (FL Kratom CPA) + non-kratom SKUs",
        "templates": {
            "Thu": {"corridor": "Himmarshee Village / Riverwalk", "vibe": "Downtown bars & clubs",
                "why": "Cobblestone bar district; early-weekend 21+ crowd builds Thursday.",
                "stops": [
                    {"zone": "Himmarshee St", "address": "SW 2nd St & SW 2nd Ave"},
                    {"zone": "Las Olas Riverfront", "address": "SW 2nd St & SW 5th Ave"}]},
            "Fri": {"corridor": "Las Olas Boulevard", "vibe": "Waterfront dining & craft bars",
                "why": "Marquee walkable strip; American Social / Elbo Room draw.",
                "stops": [
                    {"zone": "E Las Olas (American Social)", "address": "E Las Olas Blvd & SE 8th Ave"},
                    {"zone": "E Las Olas (gallery row)", "address": "E Las Olas Blvd & SE 11th Ave"}]},
            "Sat": {"corridor": "Fort Lauderdale Beach", "vibe": "Beachfront patios",
                "why": "Saturday beach peak; Elbo Room + Beach Place 21+ patio traffic.",
                "stops": [
                    {"zone": "Las Olas Beach (Elbo Room)", "address": "A1A & E Las Olas Blvd"},
                    {"zone": "Beach Place", "address": "17 S Fort Lauderdale Beach Blvd"}]},
            "Sun": {"corridor": "Beach / Oceanside Park", "vibe": "Sunday beach daytime",
                "why": "Sunday Funday beach crowd along A1A.",
                "stops": [
                    {"zone": "Las Olas Oceanside Park", "address": "3000 E Las Olas Blvd"},
                    {"zone": "North Beach strip", "address": "Fort Lauderdale Beach Blvd & Sunrise Blvd"}]},
        },
    },
    "Tampa / St. Pete, FL": {
        "code": "TPA", "color": "#C0392B",
        "warehouse": "10700 US Highway 19 N, Pinellas Park, FL 33782",
        "product": "Kratom-eligible (FL Kratom CPA) + non-kratom SKUs",
        "templates": {
            "Thu": {"corridor": "Ybor City", "vibe": "Historic 7th Ave bar district",
                "why": "Tampa's nightlife backbone; RITZ Ybor event nights draw crowds.",
                "stops": [
                    {"zone": "Centro Ybor", "address": "E 7th Ave & 17th St"},
                    {"zone": "RITZ Ybor frontage", "address": "E 7th Ave & 16th St"}]},
            "Fri": {"corridor": "SoHo / S Howard Ave (Hyde Park)", "vibe": "Young-professional cocktail strip",
                "why": "Trendy 21+ Friday happy-hour corridor.",
                "stops": [
                    {"zone": "S Howard & Azeele", "address": "S Howard Ave & W Azeele St"},
                    {"zone": "S Howard & Swann", "address": "S Howard Ave & W Swann Ave"}]},
            "Sat": {"corridor": "Downtown St. Pete", "vibe": "Central Ave & Beach Drive",
                "why": "Closest dense corridor to warehouse; strong Saturday daytime brunch crowd.",
                "stops": [
                    {"zone": "Central Ave (600 block)", "address": "Central Ave & 6th St N"},
                    {"zone": "Beach Drive NE", "address": "Beach Dr NE & 2nd Ave NE"}]},
            "Sun": {"corridor": "Clearwater / St. Pete Beach", "vibe": "Gulf beach daytime",
                "why": "Sunday Gulf-beach peak; Pier 60 + Corey Ave 21+ traffic.",
                "stops": [
                    {"zone": "Pier 60, Clearwater Beach", "address": "10 Pier 60 Dr, Clearwater"},
                    {"zone": "Corey Ave, St. Pete Beach", "address": "Corey Ave & Gulf Blvd"}]},
        },
    },
    "Austin, TX": {
        "code": "AUS", "color": "#6B4FA0",
        "warehouse": "6330 Harold Ct, Austin, TX 78721 (East Austin)",
        "product": "Kratom-eligible (TX Kratom CPA / HB 4127) + non-kratom SKUs",
        "templates": {
            "Thu": {"corridor": "Rainey Street", "vibe": "Bungalow bars / patios",
                "why": "Laid-back 21+ Thursday crowd; Long Center Drop-In free concerts nearby.",
                "stops": [
                    {"zone": "Rainey St & Davis", "address": "Rainey St & Davis St"},
                    {"zone": "Rainey St & River", "address": "Rainey St & River St"}]},
            "Fri": {"corridor": "6th Street + Red River", "vibe": "Pedestrian party district",
                "why": "E 6th closes to traffic Thu–Sat nights; thousands bar-hopping.",
                "stops": [
                    {"zone": "E 6th St (pedestrian)", "address": "E 6th St & Neches St"},
                    {"zone": "Red River (Stubb's)", "address": "Red River St & E 7th St"}]},
            "Sat": {"corridor": "South Congress (SoCo)", "vibe": "Daytime shopping + patios",
                "why": "Iconic Saturday daytime stroll corridor.",
                "stops": [
                    {"zone": "S Congress & Elizabeth", "address": "S Congress Ave & Elizabeth St"},
                    {"zone": "S Congress & Academy", "address": "S Congress Ave & Academy Dr"}]},
            "Sun": {"corridor": "East Austin", "vibe": "Patios near warehouse",
                "why": "Close-in Sunday daytime patio + brunch crowd; low travel burden.",
                "stops": [
                    {"zone": "E 6th St (East)", "address": "E 6th St & Medina St"},
                    {"zone": "E Cesar Chavez", "address": "E Cesar Chavez St & Robert T Martinez"}]},
        },
    },
    "San Antonio, TX": {
        "code": "SAT", "color": "#D68910",
        "warehouse": "3440 Fredericksburg Rd, San Antonio, TX 78201",
        "product": "Kratom-eligible (TX Kratom CPA / HB 4127) + non-kratom SKUs",
        "templates": {
            "Thu": {"corridor": "St. Mary's Strip", "vibe": "Local bar & live-music corridor",
                "why": "San Antonio's original entertainment district; heavy local 21+ traffic.",
                "stops": [
                    {"zone": "N St Mary's & Magnolia", "address": "N St Mary's St & E Magnolia Ave"},
                    {"zone": "N St Mary's & Mistletoe", "address": "N St Mary's St & E Mistletoe Ave"}]},
            "Fri": {"corridor": "Pearl District", "vibe": "Walkable brewery-complex nightlife",
                "why": "Walkable cocktail + restaurant hub active into the evening.",
                "stops": [
                    {"zone": "Pearl plaza", "address": "303 Pearl Pkwy"},
                    {"zone": "Pearl / Museum Reach", "address": "Pearl Pkwy & Grayson St"}]},
            "Sat": {"corridor": "River Walk (Downtown)", "vibe": "Tourist + local riverfront",
                "why": "Highest weekend daytime foot traffic in the city.",
                "stops": [
                    {"zone": "River Walk (Commerce)", "address": "Commerce St & Losoya St"},
                    {"zone": "Museum Reach", "address": "River Walk & Camden St"}]},
            "Sun": {"corridor": "Southtown / Blue Star", "vibe": "Arts district daytime",
                "why": "Sunday arts + brunch crowd; gallery foot traffic.",
                "stops": [
                    {"zone": "Blue Star Arts Complex", "address": "116 Blue Star"},
                    {"zone": "Southtown (S Alamo)", "address": "S Alamo St & S St Mary's St"}]},
        },
    },
}

# ---------------------------------------------------------------------------
# Week-specific overrides (market, isodate) -> partial template override + event tag
# ---------------------------------------------------------------------------
OVERRIDES = {
    ("Miami, FL", "2026-07-04"): {"event": "July 4th — beach + fireworks crowd peak"},
    ("Ft. Lauderdale, FL", "2026-07-04"): {"event": "July 4th — beach + fireworks crowd peak"},
    ("Tampa / St. Pete, FL", "2026-07-04"): {"event": "July 4th — Gulf beach + fireworks peak"},
    ("Austin, TX", "2026-07-04"): {"event": "July 4th — Lady Bird Lake / downtown fireworks"},
    ("San Antonio, TX", "2026-07-04"): {"event": "July 4th — River Walk + downtown fireworks"},
    ("Miami, FL", "2026-07-11"): {
        "corridor": "Wynwood Art Walk (2nd Sat)", "vibe": "Open-air arts + music night",
        "why": "2nd-Saturday Art Walk turns Wynwood into a high-traffic evening street scene.",
        "stops": [
            {"zone": "Wynwood Walls", "address": "NW 2nd Ave & NW 26th St"},
            {"zone": "Wynwood Marketplace", "address": "2250 NW 2nd Ave"}],
        "event": "Wynwood Art Walk (2nd Saturday)"},
    ("Austin, TX", "2026-07-16"): {
        "corridor": "Red River Cultural District", "vibe": "Hot Summer Nights free fest",
        "why": "Hot Summer Nights 7/16–18: 130+ artists, music from ~7pm; massive 21+ crowd.",
        "stops": [
            {"zone": "Stubb's / Red River", "address": "Red River St & E 8th St"},
            {"zone": "Mohawk / Empire", "address": "Red River St & E 7th St"}],
        "event": "Hot Summer Nights (Red River) 7/16–18"},
    ("Austin, TX", "2026-07-17"): {
        "corridor": "Red River Cultural District", "vibe": "Hot Summer Nights free fest",
        "why": "Hot Summer Nights night 2; pair with 6th St pedestrian closure spillover.",
        "stops": [
            {"zone": "Red River strip", "address": "Red River St & E 7th St"},
            {"zone": "E 6th pedestrian", "address": "E 6th St & Red River St"}],
        "event": "Hot Summer Nights (Red River) 7/16–18"},
    ("Austin, TX", "2026-07-18"): {
        "corridor": "Red River + Hot Summer Nights Market", "vibe": "Daytime market + evening fest",
        "why": "HSN Market at The Liberty 7/18 plus festival; all-day Red River traffic.",
        "stops": [
            {"zone": "The Liberty (HSN Market)", "address": "1618 E 6th St"},
            {"zone": "Red River strip", "address": "Red River St & E 7th St"}],
        "event": "Hot Summer Nights Market 7/18"},
    ("Tampa / St. Pete, FL", "2026-07-17"): {"event": "RITZ Ybor: Cat Power (7/17) — concert spillover"},
    ("Tampa / St. Pete, FL", "2026-07-24"): {"event": "RITZ Ybor: Qveen Herby (7/24) — concert spillover"},
}

# ---------------------------------------------------------------------------
# Build the dated schedule
# ---------------------------------------------------------------------------
def daterange_thu_sun(start, end):
    d, days = start, []
    while d <= end:
        if d.weekday() in (3, 4, 5, 6):
            days.append(d)
        d += datetime.timedelta(days=1)
    return days

start = datetime.date.fromisoformat(PROGRAM["start_date"])
end = datetime.date.fromisoformat(PROGRAM["end_date"])
dates = daterange_thu_sun(start, end)
WD = {3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}

def week_no(d):
    return (d - start).days // 7 + 1

schedule = []
for market, m in MARKETS.items():
    for d in dates:
        wd = WD[d.weekday()]; iso = d.isoformat()
        tpl = dict(m["templates"][wd])
        ov = dict(OVERRIDES.get((market, iso), {}))
        event = ov.pop("event", None)
        tpl.update(ov)
        blocks = EVE_BLOCKS if wd in ("Thu", "Fri") else DAY_BLOCKS
        win = PROGRAM["windows"][wd]
        stops = [{**s, "time": blocks[i] if i < len(blocks) else blocks[-1]}
                 for i, s in enumerate(tpl["stops"])]
        schedule.append({
            "market": market, "code": m["code"], "color": m["color"],
            "week": week_no(d), "date": iso, "date_pretty": d.strftime("%a %b %-d"),
            "day": wd, "call": win["call"], "active": win["active"], "release": win["release"],
            "warehouse": m["warehouse"], "corridor": tpl["corridor"], "vibe": tpl["vibe"],
            "why": tpl["why"], "stops": stops, "event": event,
            "bas": PROGRAM["bas_per_shift"], "hours": PROGRAM["billable_hours_per_ba"],
        })

with open("schedule.json", "w") as f:
    json.dump({"program": PROGRAM, "markets": MARKETS, "schedule": schedule}, f, indent=2)

from collections import Counter
c = Counter(s["market"] for s in schedule)
print("Total shifts:", len(schedule))
for k, v in c.items():
    print(f"  {k}: {v} shifts ({v*2} BA-slots, {v*5.5:.0f} BA-hrs)")
print("Span:", schedule[0]["date"], "->", schedule[-1]["date"], "| weeks:", sorted(set(s['week'] for s in schedule)))
