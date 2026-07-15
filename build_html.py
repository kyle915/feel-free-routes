"""Build the interactive client-facing HTML page from schedule.json.
Writes both the named client file AND index.html (served by GitHub Pages)."""
import json

data = json.load(open("schedule.json"))
P = data["program"]; MK = data["markets"]; SCH = data["schedule"]

# Real field photos from the BA teams, kept separate from schedule.json
# (which build_data.py regenerates from scratch) so they survive reruns.
# Left empty for now — Kyle, to add photos: drop full-resolution originals in
# photos/<file>.jpg (never resized/recompressed here — that was the whole
# point of moving them off the slide deck), then add entries below as
# {"file": "<file>.jpg", "caption": "<short label>"} under the matching
# market key, rerun `python3 build_html.py`, and commit + push. The gallery
# and "Download all" button on each market's section only render when that
# market has at least one entry here.
PHOTOS = {}

# Field sampling recap — ACTUAL results pulled from Spark (Feel Free /
# Botanic Tonics, tenant 4), program-to-date through the Jul 9–12 weekend.
# Per-market SKU totals are real summed per-SKU sample quantities from filed
# recaps (recaps.field_sampling_report.sku_breakdown, "quantity" mode).
# Includes the Jun 27-28 pilot weekend: those 4 events were renamed in Spark
# to the standard "<Market> — <Corridor> · date" convention (2026-07-14,
# events 1258/1260/1527/1528), so sku_breakdown now folds them in
# AUTOMATICALLY — a fresh re-pull returns these same totals (15,119 grand),
# no manual overlay needed. The "Test Event" recap (136) stays excluded (its
# name has no market). The
# call-outs are real BA / consumer field notes (field_callouts), lightly
# trimmed for length and curated to consumer sentiment + actionable field
# insight (operational / expense notes dropped). All five markets are real
# filed-recap pulls now — refresh by re-pulling from Spark. Program-to-date
# snapshot, not week-filtered against the picked week chip.
RECAP = {'Miami, FL': {'real': True,
               'ytd': [['Kava Mate', 5590]],
               'callouts': [['Wynwood · Jul 2', 'Love the presentation and the bottle!!'],
                            ['Brickell · Jul 3',
                             'A positive, engaging atmosphere throughout the activation. Consumers '
                             'were curious about Feel Free Kava Maté and many stopped to ask '
                             'questions before sampling.'],
                            ['Brickell · Jul 10', 'Love the presentation of the bottle!!!'],
                            ['Coconut Grove · Jul 5', 'Love the taste of the kava!!!'],
                            ['Wynwood · Jul 9',
                             'A branded tent would give ambassadors much-needed shade in 99° heat '
                             'and would elevate the activation with a more premium look while '
                             'boosting visibility.'],
                            ['Brickell · Jul 10',
                             'Sampling times may need to be earlier to avoid the extreme midday '
                             'heat.']]},
 'Ft. Lauderdale, FL': {'real': True,
                        'ytd': [['Classic Tonic', 2080], ['Kava Mate', 2070]],
                        'callouts': [['Las Olas Boulevard · Jul 10',
                                      'Consumers were very receptive and asked thoughtful '
                                      'questions. Many commented positively on the quality after '
                                      'trying it, and several expressed intent to purchase.'],
                                     ['Fort Lauderdale Beach · Jul 11',
                                      'Most enjoyed the taste and were interested in the energy, '
                                      'focus, and mood-support benefits. Many said they would '
                                      'purchase after sampling.'],
                                     ['Beach / Oceanside Park · Jul 12',
                                      'Customers asked for coupons they can use in store.'],
                                     ['Las Olas Boulevard · Jul 3',
                                      "Many mentioned they'd like to see the product available at "
                                      'more retail locations.'],
                                     ['Himmarshee Village / Riverwalk · Jul 9',
                                      "The majority had positive reactions and several said they'd "
                                      'consider buying after learning more about the product.'],
                                     ['Beach / Oceanside Park · Jul 5',
                                      'Giveaways like shirts or keychains would make a good '
                                      'keepsake to prompt a later purchase.']]},
 'Tampa / St. Pete, FL': {'real': True,
                          'ytd': [['Classic Tonic', 1237], ['Kava Mate', 937]],
                          'callouts': [['Ybor City · Jul 2',
                                        'Most people we engaged were open to taking the Kava Mate '
                                        'and Classic Tonic with them to try later — a receptive '
                                        'audience.'],
                                       ['Downtown St. Pete · Jul 11',
                                        'A much better crowd here — this demographic was more open '
                                        'to trying the product, with constant foot traffic the '
                                        'whole time.'],
                                       ['Clearwater / St. Pete Beach · Jul 12',
                                        "A great night for sampling — a band at Ferg's across from "
                                        'Tropicana Field right after the Rays game drew a large '
                                        'crowd.'],
                                       ['Ybor City · Jul 2',
                                        'Most people were excited to take the sample to drink at '
                                        'home.'],
                                       ['Downtown St. Pete · Jul 11',
                                        'Would appreciate more branding signage or brand gear to '
                                        'help people notice the activation.']]},
 'Austin, TX': {'real': True,
                'ytd': [['Kava Mate', 1093], ['Classic Tonic', 1009]],
                'callouts': [['Rainey Street · Jul 2',
                              'Overall the demo was successful — customers engaged, asked '
                              'questions, and many expressed interest in purchasing.'],
                             ['East Austin · Jul 5',
                              'Most customers enjoyed the taste and appreciated learning about the '
                              "product's features."],
                             ['South Congress (SoCo) · Jul 4',
                              'A Fourth of July event with a good turnout — fewer people worried '
                              'about the kratom.'],
                             ['6th Street + Red River · Jul 3',
                              'A populated area — we got through a box and a half of each. Still '
                              'some pushback on the kratom ingredient.'],
                             ['Rainey Street · Jul 2',
                              'Good crowd; I focused on those with bags who could carry the '
                              'bottles home.']]},
 'San Antonio, TX': {'real': True,
                     'ytd': [['Kava Mate', 672], ['Classic Tonic', 431]],
                     'callouts': [['River Walk (Downtown) · Jul 4',
                                   'Consumers were familiar with the branding but not the product '
                                   'itself — a clear opportunity to educate.'],
                                  ["St. Mary's Strip · Jul 2",
                                   'The most active consumers were the ones intrigued to be '
                                   'educated on the product.'],
                                  ['Southtown / Blue Star · Jun 28',
                                   'A few consumers were already familiar with the product.'],
                                  ['Southtown / Blue Star · Jul 5',
                                   "A few consumers weren't thrilled with the product — useful "
                                   'early taste feedback.']]}}

payload = json.dumps({"program": P, "markets": MK, "schedule": SCH, "photos": PHOTOS, "recap": RECAP})

HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Feel Free — Summer 2026 Field Sampling Routes</title>
<style>
:root{--ink:#14202b;--mute:#5d6b78;--line:#e3e8ee;--bg:#f6f8fa;--card:#fff;--accent:#0f7d8c;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.45}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px 80px}
header{background:linear-gradient(135deg,#0f2a36,#15455a);color:#fff;padding:42px 0 34px}
header .wrap{padding-bottom:0}
.kicker{letter-spacing:.18em;text-transform:uppercase;font-size:12px;opacity:.8;font-weight:600}
h1{font-size:34px;font-weight:800;margin:8px 0 6px;letter-spacing:-.5px}
.sub{opacity:.9;font-size:15px}
.stats{display:flex;flex-wrap:wrap;gap:14px;margin-top:22px}
.stat{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:12px 16px;min-width:120px}
.stat b{display:block;font-size:22px;font-weight:800}
.stat span{font-size:12px;opacity:.85}
.tabsnav{background:var(--card);border-bottom:1px solid var(--line)}
.tabsnav .wrap{display:flex;gap:2px;padding-top:0;padding-bottom:0}
.tab{display:inline-flex;align-items:center;gap:7px;padding:14px 18px;font-size:13.5px;font-weight:700;color:var(--mute);text-decoration:none;border-bottom:3px solid transparent;transition:.15s}
.tab:hover{color:var(--ink)}
.tab.active{color:var(--accent);border-bottom-color:var(--accent)}
.toolbar{position:sticky;top:0;z-index:20;background:var(--bg);padding:18px 0 10px;border-bottom:1px solid var(--line)}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.label{font-size:12px;font-weight:700;color:var(--mute);text-transform:uppercase;letter-spacing:.08em;margin-right:4px}
.chip{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:7px 14px;font-size:13px;font-weight:600;cursor:pointer;transition:.15s;white-space:nowrap}
.chip:hover{border-color:var(--accent)}
.chip.active{background:var(--ink);color:#fff;border-color:var(--ink)}
.chip.mkt.active{color:#fff}
.viewtoggle{margin-left:auto}
.legend{display:flex;flex-wrap:wrap;gap:14px;margin:14px 0 4px;font-size:12px;color:var(--mute)}
.legend span{display:inline-flex;align-items:center;gap:6px}
.dot{width:11px;height:11px;border-radius:3px;display:inline-block}
section.market{margin-top:30px}
.mhead{display:flex;align-items:center;gap:12px;border-left:6px solid var(--accent);padding:6px 0 6px 14px;margin-bottom:6px}
.mhead h2{font-size:22px;font-weight:800}
.mhead .wh{font-size:12.5px;color:var(--mute)}
.mstatus{margin-left:auto;font-size:12px;font-weight:700;color:var(--accent);background:#e6f4f2;border:1px solid #c9e7e2;border-radius:999px;padding:5px 13px;white-space:nowrap}
.tbdnote{color:var(--mute);font-size:13px;margin:2px 0 0 20px}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.weeklbl{grid-column:1 / -1;font-size:12px;font-weight:800;color:var(--mute);text-transform:uppercase;letter-spacing:.1em;margin:14px 0 2px;display:flex;align-items:center;justify-content:space-between;gap:10px}
.xport{font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:none;color:var(--accent);background:#fff;border:1px solid var(--accent);border-radius:999px;padding:4px 12px;cursor:pointer;transition:.15s;white-space:nowrap}
.xport:hover{background:var(--accent);color:#fff}
.xport:active{transform:scale(.97)}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:13px 14px;display:flex;flex-direction:column;gap:7px;box-shadow:0 1px 2px rgba(20,32,43,.04)}
.card .d{display:flex;justify-content:space-between;align-items:baseline}
.card .day{font-weight:800;font-size:14px}
.card .date{font-size:12px;color:var(--mute)}
.card .corr{font-weight:700;font-size:14.5px;line-height:1.25}
.card .win{font-size:12px;color:var(--accent);font-weight:700}
.card .vibe{font-size:12px;color:var(--mute)}
.stops{border-top:1px dashed var(--line);padding-top:7px;display:flex;flex-direction:column;gap:6px}
.stop{font-size:12px}
.stop b{display:block;font-weight:700}
.stop .meta{color:var(--mute)}
.evt{background:#fff4d6;border:1px solid #f0d98a;color:#7a5b00;border-radius:8px;padding:5px 8px;font-size:11.5px;font-weight:700}
.listwrap{display:none}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:12px;overflow:hidden;font-size:13px;border:1px solid var(--line)}
th,td{text-align:left;padding:9px 11px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--ink);color:#fff;font-size:11px;text-transform:uppercase;letter-spacing:.06em;position:sticky;top:128px}
tr:hover td{background:#fafcfd}
.tagcode{font-weight:800;color:#fff;border-radius:6px;padding:2px 8px;font-size:11px}
.recapwrap{margin-top:16px;border-top:1px dashed var(--line);padding-top:14px}
.recapbtn{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:800;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:10px;padding:9px 15px;cursor:pointer;transition:.15s}
.recapbtn:hover{border-color:var(--accent)}
.recapbtn .caret{transition:transform .18s;font-size:11px;color:var(--mute)}
.recapbtn.open .caret{transform:rotate(180deg)}
.recapbody{display:none;margin-top:14px}
.recapbody.open{display:block}
.rnote{background:#fff;border:1px solid var(--line);border-radius:8px;padding:8px 12px;font-size:12px;color:var(--mute);font-style:italic;margin:0 0 12px}
.rgrid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:14px}
@media(max-width:700px){.rgrid{grid-template-columns:1fr}}
.rtable{width:100%;border-collapse:collapse;font-size:13px;background:transparent;border:none}
.rtable caption{text-align:left;font-weight:800;font-size:12.5px;margin-bottom:6px;caption-side:top;color:var(--mute);text-transform:uppercase;letter-spacing:.06em}
.rtable td{padding:6px 0;border-bottom:1px solid var(--line);background:transparent}
.rtable td.n{text-align:right;font-weight:700}
.rtable tr.total td{font-weight:800;border-bottom:none;padding-top:8px;color:var(--ink)}
.rqlabel{font-size:12px;font-weight:800;color:var(--mute);text-transform:uppercase;letter-spacing:.08em;margin:2px 0 8px}
.rquotes{display:flex;flex-direction:column;gap:8px}
.rquote{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.rquote .rtag{font-size:10.5px;font-weight:800;color:var(--mute);text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px}
.rquote .rtext{font-size:13px;line-height:1.45}
.photos{margin-top:16px;border-top:1px dashed var(--line);padding-top:14px}
.photos .phead{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px}
.photos .plabel{font-size:12px;font-weight:800;color:var(--mute);text-transform:uppercase;letter-spacing:.1em}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
.pcard{display:block;border-radius:10px;overflow:hidden;background:#eef1f4;border:1px solid var(--line)}
.pcard img{width:100%;height:160px;object-fit:cover;display:block}
.pcap{font-size:11px;color:var(--mute);padding:6px 8px}
@media(max-width:560px){.pgrid{grid-template-columns:repeat(auto-fill,minmax(120px,1fr))}.pcard img{height:120px}}
.foot{margin-top:30px;font-size:12px;color:var(--mute);border-top:1px solid var(--line);padding-top:16px}
.note{background:#fff;border:1px solid var(--line);border-left:4px solid #c0392b;border-radius:10px;padding:12px 14px;font-size:12.5px;color:var(--ink);margin-top:16px}
@media(max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}h1{font-size:26px}}
@media(max-width:560px){.grid{grid-template-columns:1fr}}
</style></head>
<body>
<header><div class="wrap">
  <div class="kicker">Ignite Productions × Feel Free</div>
  <h1>Summer 2026 Guerrilla Field-Sampling Routes</h1>
  <div class="sub" id="subline"></div>
  <div class="stats" id="stats"></div>
</div></header>
<div class="tabsnav"><div class="wrap">
  <a class="tab active" href="index.html">📅 Route Schedule</a>
  <a class="tab" href="sampling-recap.html">📊 Sampling Recap</a>
</div></div>
<div class="wrap">
  <div class="toolbar">
    <div class="row"><span class="label">Market</span><span id="mktchips"></span></div>
    <div class="row" style="margin-top:8px">
      <span class="label">Week</span><span id="wkchips"></span>
      <span class="viewtoggle row">
        <span class="chip view active" data-v="cal">Calendar</span>
        <span class="chip view" data-v="list">List</span>
      </span>
    </div>
    <div class="legend" id="legend"></div>
  </div>
  <div id="calwrap"></div>
  <div class="listwrap" id="listwrap"></div>
  <div class="note" id="compliance"></div>
  <div class="foot" id="foot"></div>
</div>
<script>
const DATA = __PAYLOAD__;
const S = DATA.schedule, MK = DATA.markets, P = DATA.program, PH = DATA.photos || {}, RC = DATA.recap || {};
const markets = Object.keys(MK);
const weeks = [...new Set(S.map(s=>s.week))].sort((a,b)=>a-b);
// Each week bucket's actual Thu–Sun date span (from real shift dates), so the
// UI labels weeks by DATE RANGE, not a global week number — the numbers don't
// map per market (Week 1 is only the Jun 27–28 pilot; the FL markets' first
// full week, Jul 2–5, shows as "Week 2"). Date ranges map correctly for every
// market. Same-month spans render "Jul 2–5"; cross-month "Jul 30 – Aug 2".
const weekSpan = {};
S.forEach(s=>{const c=weekSpan[s.week]; if(!c){weekSpan[s.week]={min:s.date,max:s.date};}else{if(s.date<c.min)c.min=s.date; if(s.date>c.max)c.max=s.date;}});
function fmtMD(iso){return new Date(iso+"T00:00:00").toLocaleDateString('en-US',{month:'short',day:'numeric'});}
function weekLabel(w){const s=weekSpan[w]; if(!s)return "Wk "+w; if(s.min===s.max)return fmtMD(s.min); const b=new Date(s.max+"T00:00:00"); return (new Date(s.min+"T00:00:00").getMonth()===b.getMonth()) ? fmtMD(s.min)+"–"+b.getDate() : fmtMD(s.min)+" – "+fmtMD(s.max);}
let fMkt = "ALL", fWk = "ALL", view = "cal";
document.getElementById('subline').textContent = P.client + "  ·  " + P.start_date + " – " + P.end_date + "  ·  " + P.cadence;
const totalShifts=S.length;
document.getElementById('stats').innerHTML = [
  [markets.length,"Markets"],[totalShifts,"Total shifts"],[totalShifts*2,"BA deployments"],
  [(totalShifts*5).toFixed(0),"BA-hours"],["4","Shifts / active market / week"]
].map(x=>`<div class="stat"><b>${x[0]}</b><span>${x[1]}</span></div>`).join("");
function chip(txt,active,cls){return `<span class="chip ${cls||''} ${active?'active':''}">${txt}</span>`}
function renderChips(){
  document.getElementById('mktchips').innerHTML =
    chip("All markets",fMkt==="ALL",'mkt') +
    markets.map(m=>{const c=MK[m].color;const a=fMkt===m;
      return `<span class="chip mkt ${a?'active':''}" data-m="${m}" style="${a?`background:${c};border-color:${c}`:`border-color:${c}`}">${m}</span>`}).join("");
  document.getElementById('wkchips').innerHTML =
    chip("All weeks",fWk==="ALL",'wk') +
    weeks.map(w=>`<span class="chip wk ${fWk==w?'active':''}" data-w="${w}">${weekLabel(w)}</span>`).join("");
  document.getElementById('legend').innerHTML = markets.map(m=>
    `<span><span class="dot" style="background:${MK[m].color}"></span>${m}</span>`).join("")
    + `<span><span class="dot" style="background:#f0d98a"></span>Event / surge anchor</span>`;
}
function filtered(){return S.filter(s=>(fMkt==="ALL"||s.market===fMkt)&&(fWk==="ALL"||s.week==fWk))}
function photosHTML(m){
  const pics = PH[m]; if(!pics||!pics.length) return "";
  const cards = pics.map(p=>`<a class="pcard" href="photos/${p.file}" target="_blank" rel="noopener">
    <img src="photos/${p.file}" alt="${p.caption}" loading="lazy"><div class="pcap">${p.caption}</div></a>`).join("");
  return `<div class="photos"><div class="phead">
    <span class="plabel">Field Photos</span>
    <button class="xport" data-pxm="${m}">⬇ Download all (${pics.length})</button>
  </div><div class="pgrid">${cards}</div></div>`;
}
function recapHTML(m){
  const r = RC[m]; if(!r) return "";
  const skuTable = (title, rows) => {
    const tot = rows.reduce((s,x)=>s+x[1],0);
    const body = rows.map(x=>`<tr><td>${x[0]}</td><td class="n">${x[1].toLocaleString()}</td></tr>`).join("");
    return `<table class="rtable"><caption>${title}</caption><tbody>${body}
      <tr class="total"><td>Total</td><td class="n">${tot.toLocaleString()}</td></tr></tbody></table>`;
  };
  const note = r.real ? "" : `<p class="rnote">Note: ${r.note}</p>`;
  const quotes = r.callouts.map(c=>`<div class="rquote"><div class="rtag">${c[0]}</div><div class="rtext">${c[1]}</div></div>`).join("");
  return `<div class="recapwrap">
    <button class="recapbtn" data-rxm="${m}">📋 Sampling Recap — Program to date (through Jul 12) <span class="caret">▾</span></button>
    <div class="recapbody" data-rbody="${m}">
      ${note}
      ${skuTable("Samples Distributed to Date · by SKU", r.ytd)}
      <div class="rqlabel">Field Call-Outs</div>
      <div class="rquotes">${quotes}</div>
    </div>
  </div>`;
}
function cardHTML(s){
  const stops = s.stops.map(t=>`<div class="stop"><b>${t.zone}</b><span class="meta">${t.time} · ${t.address}</span></div>`).join("");
  return `<div class="card" style="border-top:3px solid ${s.color}">
    <div class="d"><span class="day">${s.day}</span><span class="date">${s.date_pretty}</span></div>
    <div class="corr">${s.corridor}</div><div class="win">${s.active}</div>
    <div class="vibe">${s.vibe}</div><div class="stops">${stops}</div>
    ${s.event?`<div class="evt">★ ${s.event}</div>`:""}</div>`;
}
function renderCal(){
  const rows = filtered(); const byMkt = {};
  rows.forEach(s=>{(byMkt[s.market]=byMkt[s.market]||[]).push(s)});
  let html=""; const mlist = fMkt==="ALL"?markets:[fMkt];
  mlist.forEach(m=>{
    const items=(byMkt[m]||[]);
    if(!items.length){
      // TBD markets (or a market with zero shifts under the active filter)
      // still get a section instead of silently vanishing from the page.
      if(MK[m].tbd){
        html+=`<section class="market"><div class="mhead" style="border-color:${MK[m].color}">
          <h2>${m}</h2><span class="mstatus">${MK[m].status}</span></div>
          <p class="tbdnote">Warehouse, corridors, and launch dates will appear here once confirmed.</p></section>`;
      }
      return;
    }
    html+=`<section class="market"><div class="mhead" style="border-color:${MK[m].color}">
      <h2>${m}</h2><span class="wh">⌂ Start: ${MK[m].warehouse}</span><span class="mstatus">${MK[m].status}</span></div>`;
    const byWk={}; items.forEach(s=>{(byWk[s.week]=byWk[s.week]||[]).push(s)});
    Object.keys(byWk).sort((a,b)=>a-b).forEach(w=>{
      const ds=byWk[w];
      html+=`<div class="grid"><div class="weeklbl"><span>${weekLabel(w)} →</span>`+
        `<button class="xport" data-xm="${m}" data-xw="${w}">⬇ Export slide</button></div>`;
      ds.forEach(s=>html+=cardHTML(s)); html+=`</div>`;
    });
    html+=recapHTML(m);
    html+=photosHTML(m);
    html+=`</section>`;
  });
  document.getElementById('calwrap').innerHTML = html || "<p style='margin-top:30px;color:#5d6b78'>No shifts match.</p>";
}
function renderList(){
  const rows = filtered();
  let html=`<table style="margin-top:20px"><thead><tr>
    <th>Wk</th><th>Date</th><th>Day</th><th>Market</th><th>Corridor</th><th>Window</th>
    <th>Route stops</th><th>Event</th></tr></thead><tbody>`;
  if(!rows.length){
    const msg = (fMkt!=="ALL" && MK[fMkt] && MK[fMkt].tbd) ? MK[fMkt].status : "No shifts match.";
    html+=`<tr><td colspan="8" style="padding:20px;color:#5d6b78">${msg}</td></tr>`;
  }
  rows.forEach(s=>{
    const stops=s.stops.map(t=>`${t.zone} (${t.time})`).join("<br>");
    html+=`<tr><td>${s.week}</td><td>${s.date_pretty}</td><td>${s.day}</td>
      <td><span class="tagcode" style="background:${s.color}">${s.code}</span> ${s.market}</td>
      <td><b>${s.corridor}</b><br><span style="color:#5d6b78">${s.vibe}</span></td>
      <td>${s.active}</td><td>${stops}</td><td>${s.event||""}</td></tr>`;
  });
  html+="</tbody></table>"; document.getElementById('listwrap').innerHTML=html;
}
function render(){
  renderChips();
  document.getElementById('calwrap').style.display = view==="cal"?"block":"none";
  document.getElementById('listwrap').style.display = view==="list"?"block":"none";
  if(view==="cal") renderCal(); else renderList();
}
document.body.addEventListener('click',e=>{
  const rb=e.target.closest('.recapbtn');
  if(rb){
    const m=rb.dataset.rxm;
    const body=document.querySelector(`.recapbody[data-rbody="${m}"]`);
    rb.classList.toggle('open'); if(body) body.classList.toggle('open');
    return;
  }
  const x=e.target.closest('.xport');
  if(x){
    if(x.dataset.pxm!==undefined) downloadAllPhotos(x.dataset.pxm);
    else exportSlide(x.dataset.xm, x.dataset.xw);
    return;
  }
  const c=e.target.closest('.chip'); if(!c) return;
  if(c.dataset.m!==undefined) fMkt=c.dataset.m;
  else if(c.classList.contains('mkt')) fMkt="ALL";
  else if(c.dataset.w!==undefined) fWk=c.dataset.w;
  else if(c.classList.contains('wk')) fWk="ALL";
  else if(c.dataset.v) view=c.dataset.v;
  document.querySelectorAll('.chip.view').forEach(x=>x.classList.toggle('active',x.dataset.v===view));
  render();
});
document.getElementById('compliance').innerHTML = "<b>Compliance reminder.</b> "+P.compliance;
document.getElementById('foot').innerHTML =
  "Prepared by Ignite Productions for Botanic Tonics, LLC (d/b/a Feel Free). Routes anchor to public 21+ corridors and known summer foot-traffic surges; exact stations may rotate within each corridor per BA safety assessment, weather, permits, and the weekly Kratom Eligibility Schedule. Phoenix is a planned market with corridors and dates still TBD.";

// ---- "Export slide" — one branded, client-deck-ready PNG per market/week ----
// Drawn straight to a <canvas> (no library) so it stays a single self-
// contained file, matching this page's own build philosophy. Title-card
// layout mirrors the client's existing branded deck template; the right
// panel (blank in that template) is filled in here with the week's actual
// planned stops straight from the schedule data.
const SLIDE_EYEBROW = "DRIVING TRIAL";
const SLIDE_SUBTITLE = "250 & SUMMER SAMPLING PLAN";
const SLIDE_INK = "#1B2A54";
const SLIDE_MUTE = "#6B759A";
const SLIDE_PAPER = "#F7F6F2";
const SLIDE_PANEL = "#EFEDE6";

function slideWeekLabel(days){
  const toMD = iso => { const d=new Date(iso+"T00:00:00"); return (d.getMonth()+1)+"/"+d.getDate(); };
  const dates = days.map(d=>d.date).sort();
  const first = toMD(dates[0]), last = toMD(dates[dates.length-1]);
  return first===last ? first : (first+" – "+last);
}
function drawTracked(ctx, text, x, y, spacing){
  let cx = x;
  for(const ch of text){ ctx.fillText(ch, cx, y); cx += ctx.measureText(ch).width + spacing; }
  return cx;
}
function drawSlide(ctx, W, H, market, days, accent){
  ctx.fillStyle = SLIDE_PAPER; ctx.fillRect(0,0,W,H);
  const leftW = Math.round(W*0.46);
  ctx.fillStyle = SLIDE_PANEL; ctx.fillRect(0,0,leftW,H);
  ctx.fillStyle = "rgba(27,42,84,.06)";
  for(let yy=36; yy<H; yy+=34) for(let xx=36; xx<leftW; xx+=34){ ctx.beginPath(); ctx.arc(xx,yy,1.8,0,Math.PI*2); ctx.fill(); }

  const padX = Math.round(W*0.045);
  // Wordmark: measure each piece at its own font BEFORE laying out, then
  // stack left-to-right from a right-aligned start — fixed pixel offsets
  // here would silently overlap/gap depending on actual glyph widths.
  ctx.textBaseline = "alphabetic";
  const wmY = 92, FF_FONT = "italic 700 40px Georgia, 'Times New Roman', serif",
    X_FONT = "400 30px Arial, sans-serif", IGNITE_FONT = "800 34px Arial, sans-serif";
  ctx.font = FF_FONT; const ffW = ctx.measureText("feel free.").width;
  ctx.font = X_FONT; const xW = ctx.measureText("  ×  ").width;
  ctx.font = IGNITE_FONT; const igniteW = ctx.measureText("IGNITE").width;
  ctx.textAlign = "left";
  let wx = W - padX - ffW - xW - igniteW;
  ctx.fillStyle = SLIDE_INK; ctx.font = FF_FONT; ctx.fillText("feel free.", wx, wmY); wx += ffW;
  ctx.fillStyle = SLIDE_MUTE; ctx.font = X_FONT; ctx.fillText("  ×  ", wx, wmY); wx += xW;
  ctx.fillStyle = SLIDE_INK; ctx.font = IGNITE_FONT; ctx.fillText("IGNITE", wx, wmY);

  let ty = Math.round(H*0.17);
  ctx.fillStyle = SLIDE_INK; ctx.font = "800 46px Arial, sans-serif";
  drawTracked(ctx, SLIDE_EYEBROW, padX, ty, 5);

  ty += 50;
  ctx.fillStyle = SLIDE_MUTE; ctx.font = "700 24px Arial, sans-serif";
  drawTracked(ctx, SLIDE_SUBTITLE, padX, ty, 2);

  ty += 110;
  ctx.fillStyle = SLIDE_INK; ctx.font = "800 94px Arial, sans-serif";
  ctx.fillText(market.toUpperCase(), padX, ty);

  ty += 56;
  ctx.strokeStyle = accent; ctx.lineWidth = 5;
  ctx.beginPath(); ctx.moveTo(padX, ty); ctx.lineTo(leftW-padX, ty); ctx.stroke();

  ty += 54;
  ctx.fillStyle = accent; ctx.font = "800 34px Arial, sans-serif";
  drawTracked(ctx, "WEEK "+slideWeekLabel(days), padX, ty, 3);

  ctx.fillStyle = SLIDE_MUTE; ctx.font = "600 18px Arial, sans-serif";
  ctx.fillText("Prepared by Ignite Productions for Botanic Tonics, LLC (d/b/a Feel Free)", padX, H-44);

  const rx = leftW + Math.round(W*0.045);
  const rw = W - rx - padX;
  let ry = Math.round(H*0.13);
  ctx.fillStyle = SLIDE_INK; ctx.font = "800 24px Arial, sans-serif";
  drawTracked(ctx, "PLANNED LOCATIONS THIS WEEK", rx, ry, 2);
  ry += 30;
  ctx.strokeStyle = "rgba(27,42,84,.18)"; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(rx, ry); ctx.lineTo(rx+rw, ry); ctx.stroke();
  ry += 52;

  const rowH = Math.floor((H - ry - 50) / days.length);
  days.forEach(d=>{
    const dt = new Date(d.date+"T00:00:00");
    const label = d.day.toUpperCase()+" · "+dt.toLocaleDateString('en-US',{month:'short',day:'numeric'}).toUpperCase();
    ctx.fillStyle = accent; ctx.font = "800 26px Arial, sans-serif";
    ctx.fillText(label, rx, ry);
    ctx.fillStyle = SLIDE_INK; ctx.font = "700 26px Arial, sans-serif";
    ctx.fillText(d.corridor, rx+270, ry);
    let sy = ry + 34;
    if(d.event){
      ctx.fillStyle = "#8A6D00"; ctx.font = "700 17px Arial, sans-serif";
      ctx.fillText("★ "+d.event, rx, sy);
      sy += 28;
    }
    ctx.font = "600 19px Arial, sans-serif";
    d.stops.forEach(st=>{
      ctx.fillStyle = SLIDE_MUTE; ctx.fillText(st.time, rx, sy);
      ctx.fillStyle = SLIDE_INK; ctx.fillText(st.zone+" — "+st.address, rx+175, sy);
      sy += 27;
    });
    ry += rowH;
  });
}
function exportSlide(market, week){
  const days = S.filter(s=>s.market===market && String(s.week)===String(week)).sort((a,b)=>a.date.localeCompare(b.date));
  if(!days.length) return;
  const W=2400, H=1350;
  const canvas = document.createElement('canvas');
  canvas.width=W; canvas.height=H;
  drawSlide(canvas.getContext('2d'), W, H, market, days, MK[market].color);
  const a = document.createElement('a');
  const safeMarket = market.replace(/[^A-Za-z0-9]+/g,'');
  const safeWeek = slideWeekLabel(days).replace(/[^0-9]+/g,'-').replace(/^-+|-+$/g,'');
  a.download = "FeelFree_"+safeMarket+"_Week"+week+"_"+safeWeek+".png";
  a.href = canvas.toDataURL('image/png');
  document.body.appendChild(a); a.click(); a.remove();
}

// ---- Field photo downloads — full-resolution originals, never resized/
// recompressed server-side. Fetched as blobs (not bare <a download> hrefs)
// and staggered ~350ms apart so browsers don't treat a tight burst of
// programmatic downloads as blocked pop-ups.
async function downloadAllPhotos(market){
  const pics = PH[market]; if(!pics||!pics.length) return;
  for(let i=0;i<pics.length;i++){
    const p = pics[i];
    try{
      const res = await fetch("photos/"+p.file);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = p.file;
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(()=>URL.revokeObjectURL(url), 4000);
    }catch(err){ console.error('Download failed for', p.file, err); }
    if(i < pics.length-1) await new Promise(r=>setTimeout(r, 350));
  }
}

render();
</script>
</body></html>"""

html = HTML.replace("__PAYLOAD__", payload)
for fn in ("Feel_Free_Summer2026_Routes_CLIENT.html", "index.html"):
    with open(fn, "w") as f:
        f.write(html)
print("HTML written:", len(html), "bytes -> Feel_Free_Summer2026_Routes_CLIENT.html + index.html")
