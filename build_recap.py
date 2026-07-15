"""Build the client-facing "Sampling Recap" tab (sampling-recap.html).

A second page on the Feel Free routes site (linked as a tab alongside the
Route Schedule) that presents the program-to-date sampling RESULTS: total
samples, a market x week grid, and per-market SKU volume. Styled to match
index.html (same light theme / header) so it reads as a native tab, not a
foreign page.

NO photos on purpose — the client pulls field photos directly from Spark
(Kyle, 2026-07-15). This page is data only.

DATA SOURCE — all figures are real, reconciled-to-Spark pulls (Feel Free /
Botanic Tonics, tenant 4) for the program window Jun 27 - Jul 12, 2026:
  * WEEKLY = per-market samples split across the three activation weekends
    (Jun 27-28 pilot / Jul 2-5 / Jul 9-12). Row totals equal each market's
    program-to-date SKU total below.
  * VOLUME = per-market samples by SKU, the same numbers as build_html.py's
    RECAP[...]['ytd'] (recaps.field_sampling_report.sku_breakdown, "quantity"
    mode). Grand total 15,119.
To refresh: re-pull from Spark (see build_html.py's RECAP comment for the
recipe), update the two dicts below, rerun `python3 build_recap.py`, commit.
"""

import json

data = json.load(open("schedule.json"))
MK = data["markets"]

WINDOW = "Jun 27 – Jul 12, 2026"

# Column headers for the market x week grid; second item is an optional sub-label.
COLS = [("Jun 27–28", "pilot"), ("Jul 2–5", ""), ("Jul 9–12", "")]

# (display label, schedule.json market key, [wk1, wk2, wk3])  None = not active
ROWS = [
    ("Miami",            "Miami, FL",            [1144, 2304, 2142]),
    ("Ft. Lauderdale",   "Ft. Lauderdale, FL",   [None, 1795, 2355]),
    ("Tampa / St. Pete", "Tampa / St. Pete, FL", [None,  418, 1756]),
    ("Austin",           "Austin, TX",           [ 616, 1486, None]),
    ("San Antonio",      "San Antonio, TX",      [ 119,  984, None]),
]

# Per-market SKU volume (matches build_html.py RECAP ytd).
VOLUME = {
    "Miami":            [("Kava Mate", 5590)],
    "Ft. Lauderdale":   [("Classic Tonic", 2080), ("Kava Mate", 2070)],
    "Tampa / St. Pete": [("Classic Tonic", 1237), ("Kava Mate", 937)],
    "Austin":           [("Kava Mate", 1093), ("Classic Tonic", 1009)],
    "San Antonio":      [("Kava Mate", 672), ("Classic Tonic", 431)],
}

# Two SKUs, two consistent colors + a shared legend.
SKU_COLORS = {"Kava Mate": "#0f7d8c", "Classic Tonic": "#e0952a"}
SKU_ORDER = ["Kava Mate", "Classic Tonic"]

# ---- derived totals (computed, never hardcoded, so they can't drift) --------
n_weeks = len(COLS)
col_totals = [sum((r[2][i] or 0) for r in ROWS) for i in range(n_weeks)]
row_totals = {r[0]: sum(v or 0 for v in r[2]) for r in ROWS}
grand_total = sum(col_totals)
market_totals = {m: sum(q for _, q in skus) for m, skus in VOLUME.items()}
max_market = max(market_totals.values())


def fmt(n):
    return f"{n:,}"


def color_for(label):
    return MK.get(label + ", FL", MK.get(label + ", TX", {})).get("color", "#5d6b78")


# ---- market x week grid -----------------------------------------------------
head_cells = "".join(
    f'<th class="n">{c}{f"<span class=sub>{s}</span>" if s else ""}</th>'
    for c, s in COLS
)
grid_rows = ""
for label, _key, weeks in ROWS:
    cells = "".join(
        f'<td class="n">{fmt(v) if v is not None else "—"}</td>' for v in weeks
    )
    dot = color_for(label)
    grid_rows += (
        f'<tr><td class="mkt"><span class="mdot" style="background:{dot}"></span>'
        f"{label}</td>{cells}"
        f'<td class="n tot">{fmt(row_totals[label])}</td></tr>'
    )
foot_cells = "".join(f'<td class="n">{fmt(t)}</td>' for t in col_totals)
grid_rows += (
    f'<tr class="allrow"><td class="mkt">All markets</td>{foot_cells}'
    f'<td class="n tot">{fmt(grand_total)}</td></tr>'
)

# ---- per-market volume bars -------------------------------------------------
vol_rows = ""
for label, _key, _weeks in ROWS:
    skus = VOLUME[label]
    total = market_totals[label]
    bar_pct = total / max_market * 100
    segs = ""
    for sku, qty in skus:
        seg_pct = qty / total * 100
        segs += (
            f'<span class="seg" style="width:{seg_pct:.4f}%;'
            f'background:{SKU_COLORS.get(sku, "#5d6b78")}" '
            f'title="{sku}: {fmt(qty)}"></span>'
        )
    split = " · ".join(f"{sku} {fmt(qty)}" for sku, qty in skus)
    vol_rows += (
        f'<div class="vrow"><div class="vtop"><span class="vname">{label}</span>'
        f'<span class="vtot">{fmt(total)}</span></div>'
        f'<div class="vtrack"><div class="vbar" style="width:{bar_pct:.4f}%">{segs}</div></div>'
        f'<div class="vsplit">{split}</div></div>'
    )

legend = "".join(
    f'<span><span class="ldot" style="background:{SKU_COLORS[s]}"></span>{s}</span>'
    for s in SKU_ORDER
)

# ---- KPI cards --------------------------------------------------------------
kpis = [
    (fmt(grand_total), "Samples distributed"),
    (str(len(ROWS)), "Metro markets"),
    (str(n_weeks), "Activation weeks"),
    ("2", "SKUs · Kava Mate + Classic Tonic"),
]
kpi_html = "".join(
    f'<div class="stat"><b>{v}</b><span>{lbl}</span></div>' for v, lbl in kpis
)

HTML = (
    """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Feel Free — Summer 2026 Sampling Recap</title>
<style>
:root{--ink:#14202b;--mute:#5d6b78;--line:#e3e8ee;--bg:#f6f8fa;--card:#fff;--accent:#0f7d8c;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.45}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px 80px}
header{background:linear-gradient(135deg,#0f2a36,#15455a);color:#fff;padding:42px 0 34px}
header .wrap{padding-bottom:0}
.kicker{letter-spacing:.18em;text-transform:uppercase;font-size:12px;opacity:.8;font-weight:600}
h1{font-size:34px;font-weight:800;margin:8px 0 6px;letter-spacing:-.5px}
.sub{opacity:.9;font-size:15px;max-width:640px}
.pill{display:inline-flex;align-items:center;gap:7px;margin-top:16px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:6px 14px;font-size:12.5px;font-weight:600}
.pill b{color:#7fe0c9;font-weight:800}
.stats{display:flex;flex-wrap:wrap;gap:14px;margin-top:22px}
.stat{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:12px 16px;min-width:130px}
.stat b{display:block;font-size:26px;font-weight:800}
.stat span{font-size:12px;opacity:.85}
/* shared tab nav (also added to index.html) */
.tabsnav{background:var(--card);border-bottom:1px solid var(--line)}
.tabsnav .wrap{display:flex;gap:2px;padding-top:0;padding-bottom:0}
.tab{display:inline-flex;align-items:center;gap:7px;padding:14px 18px;font-size:13.5px;font-weight:700;color:var(--mute);text-decoration:none;border-bottom:3px solid transparent;transition:.15s}
.tab:hover{color:var(--ink)}
.tab.active{color:var(--accent);border-bottom-color:var(--accent)}
section.block{margin-top:34px}
.blocktitle{font-size:20px;font-weight:800;letter-spacing:-.2px}
.blocksub{color:var(--mute);font-size:13.5px;margin-top:3px}
.tablewrap{margin-top:16px;overflow-x:auto}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:12px;overflow:hidden;font-size:13.5px;border:1px solid var(--line);min-width:560px}
th,td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--line)}
th{background:var(--ink);color:#fff;font-size:11px;text-transform:uppercase;letter-spacing:.06em;font-weight:700}
th.n,td.n{text-align:right;font-variant-numeric:tabular-nums}
th .sub{display:block;font-size:9.5px;opacity:.7;font-weight:600;letter-spacing:.04em;margin-top:1px}
td.mkt{font-weight:700}
.mdot{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:8px;vertical-align:middle}
td.tot{font-weight:800;color:var(--accent)}
tr:hover td{background:#fafcfd}
tr.allrow td{background:#f0f5f6;font-weight:800;border-bottom:none}
tr.allrow td.tot{color:var(--ink)}
.vlegend{display:flex;gap:16px;margin-top:14px;font-size:12.5px;color:var(--mute)}
.vlegend span{display:inline-flex;align-items:center;gap:7px}
.ldot{width:12px;height:12px;border-radius:3px;display:inline-block}
.vlist{margin-top:16px;display:flex;flex-direction:column;gap:16px}
.vrow{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:13px 16px}
.vtop{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px}
.vname{font-weight:800;font-size:14.5px}
.vtot{font-weight:800;font-size:15px;color:var(--accent);font-variant-numeric:tabular-nums}
.vtrack{background:#eef2f4;border-radius:7px;height:16px;overflow:hidden}
.vbar{height:100%;display:flex;border-radius:7px;overflow:hidden;min-width:2px}
.seg{height:100%}
.vsplit{margin-top:7px;font-size:12px;color:var(--mute)}
.foot{margin-top:40px;font-size:12px;color:var(--mute);border-top:1px solid var(--line);padding-top:16px}
@media(max-width:560px){h1{font-size:26px}.stat b{font-size:22px}}
</style></head>
<body>
<header><div class="wrap">
  <div class="kicker">Ignite Productions × Feel Free</div>
  <h1>Summer 2026 Sampling Recap</h1>
  <div class="sub">Samples distributed to date across five metro markets, by week — pulled from filed brand-ambassador recaps in Spark.</div>
  <div class="pill">✓ Figures reconciled to Spark · window <b>"""
    + WINDOW
    + """</b></div>
  <div class="stats">"""
    + kpi_html
    + """</div>
</div></header>
<div class="tabsnav"><div class="wrap">
  <a class="tab" href="index.html">📅 Route Schedule</a>
  <a class="tab active" href="sampling-recap.html">📊 Sampling Recap</a>
</div></div>
<div class="wrap">
  <section class="block">
    <div class="blocktitle">Samples by market &amp; week</div>
    <div class="blocksub">Each market runs a Thursday–Sunday block per week. Miami samples Kava Mate only; the other markets split Kava Mate + Classic Tonic.</div>
    <div class="tablewrap"><table>
      <thead><tr><th>Market</th>"""
    + head_cells
    + """<th class="n">Total</th></tr></thead>
      <tbody>"""
    + grid_rows
    + """</tbody>
    </table></div>
  </section>
  <section class="block">
    <div class="blocktitle">Volume by market</div>
    <div class="blocksub">Program-to-date samples per market, split by SKU.</div>
    <div class="vlegend">"""
    + legend
    + """</div>
    <div class="vlist">"""
    + vol_rows
    + """</div>
  </section>
  <div class="foot">Prepared by Ignite Productions for Botanic Tonics, LLC (d/b/a Feel Free). All figures are reconciled to filed recaps in Spark for the Jun 27 – Jul 12, 2026 window. Field photos are available directly in Spark.</div>
</div>
</body></html>"""
)

with open("sampling-recap.html", "w") as f:
    f.write(HTML)
print("Sampling Recap page written:", len(HTML), "bytes -> sampling-recap.html")
print("  grand total:", grand_total, "| col totals:", col_totals)
print("  row totals:", row_totals)
# cross-check: weekly row totals must equal SKU volume totals per market
for label in row_totals:
    assert row_totals[label] == market_totals[label], (
        f"MISMATCH {label}: weekly={row_totals[label]} volume={market_totals[label]}"
    )
print("  ✓ weekly totals reconcile with SKU volume totals")
