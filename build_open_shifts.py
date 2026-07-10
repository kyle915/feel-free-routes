"""Build the standalone "Open Shifts" page (open-shifts.html).

BAs use this to submit availability to make up missing hours. Fields: Name,
Market, Date, and a start time that defines a fixed 5-hour window. Submissions
are emailed (via FormSubmit.co — a no-backend form-to-email relay, since this
is a static GitHub Pages site) to Kyle + Harris + Myriant.

"Available hours" per market are shown from OPEN_HOURS below — a static page
can't decrement a shared pool live, so this is a displayed number Kyle edits
(subtract as claims come in), OR upgrade later to a Google Apps Script + Sheet
backend for true auto-decrementing. See chat notes.
"""
import json

data = json.load(open("schedule.json"))
MK = data["markets"]

# Active markets only (skip TBD markets like Phoenix — nothing to claim yet).
MARKETS = [(name, m["color"]) for name, m in MK.items() if not m.get("tbd")]

# ---- Open make-up hours per market (EDIT THESE) ----
# Placeholder values until Kyle supplies the real pool. Subtract manually as
# claims arrive, or move to the Sheet-backed version for auto-decrement.
OPEN_HOURS = {
    "Miami, FL": 20,
    "Ft. Lauderdale, FL": 20,
    "Tampa / St. Pete, FL": 20,
    "Austin, TX": 20,
    "San Antonio, TX": 20,
}

# ---- Email delivery (FormSubmit.co) ----
FORM_TO = "kyle@igniteproductions.co"          # primary recipient (action URL)
FORM_CC = "harris@igniteproductions.co,myriant@igniteproductions.co"
SHIFT_HOURS = 5                                 # fixed shift-window length
NEXT_URL = "https://kyle915.github.io/feel-free-routes/open-shifts.html?submitted=1"

market_cards = "".join(
    f'<div class="mcard" style="border-top:3px solid {c}">'
    f'<div class="mname">{name}</div>'
    f'<div class="mhours"><b>{OPEN_HOURS.get(name, 0)}</b><span>hrs open</span></div>'
    f'</div>'
    for name, c in MARKETS
)
market_options = "".join(f'<option value="{name}">{name}</option>' for name, _ in MARKETS)

HTML = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Feel Free — Open Shifts (Make-Up Hours)</title>
<style>
:root{{--ink:#14202b;--mute:#5d6b78;--line:#e3e8ee;--bg:#f6f8fa;--card:#fff;--accent:#0f7d8c;}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.45}}
.wrap{{max-width:760px;margin:0 auto;padding:0 20px 80px}}
header{{background:linear-gradient(135deg,#0f2a36,#15455a);color:#fff;padding:42px 0 34px}}
header .wrap{{padding-bottom:0}}
.kicker{{letter-spacing:.18em;text-transform:uppercase;font-size:12px;opacity:.8;font-weight:600}}
h1{{font-size:32px;font-weight:800;margin:8px 0 6px;letter-spacing:-.5px}}
.sub{{opacity:.9;font-size:15px;max-width:560px}}
.back{{display:inline-block;margin-top:16px;font-size:13px;color:#bfe3e0;text-decoration:none;font-weight:600}}
.back:hover{{text-decoration:underline}}
.sectlbl{{font-size:12px;font-weight:800;color:var(--mute);text-transform:uppercase;letter-spacing:.1em;margin:30px 0 12px}}
.mgrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px}}
.mcard{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:13px 14px;box-shadow:0 1px 2px rgba(20,32,43,.04)}}
.mname{{font-weight:700;font-size:13.5px}}
.mhours{{margin-top:6px;display:flex;align-items:baseline;gap:6px}}
.mhours b{{font-size:26px;font-weight:800}}
.mhours span{{font-size:12px;color:var(--mute)}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px;margin-top:14px;box-shadow:0 1px 2px rgba(20,32,43,.04)}}
label{{display:block;font-size:13px;font-weight:700;margin:0 0 6px}}
.field{{margin-bottom:16px}}
input,select{{width:100%;font-size:15px;font-family:inherit;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:10px;padding:11px 12px}}
input:focus,select:focus{{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(15,125,140,.12)}}
.row2{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
@media(max-width:520px){{.row2{{grid-template-columns:1fr}}}}
.window{{background:#eef6f6;border:1px solid #cfe6e4;border-radius:10px;padding:10px 13px;font-size:14px;color:#0c5a63;font-weight:600;margin-bottom:16px}}
.window .muted{{color:var(--mute);font-weight:500}}
.hint{{font-size:12px;color:var(--mute);margin-top:5px}}
button{{width:100%;font-size:15px;font-weight:800;color:#fff;background:var(--accent);border:none;border-radius:10px;padding:14px;cursor:pointer;transition:.15s}}
button:hover{{background:#0c6975}}
button:active{{transform:scale(.99)}}
.thanks{{display:none;background:#e9f7ef;border:1px solid #b6e2c6;border-radius:14px;padding:22px;margin-top:14px}}
.thanks h2{{font-size:18px;margin-bottom:6px;color:#1c7a45}}
.thanks p{{font-size:14px;color:#2f6b48}}
.foot{{margin-top:28px;font-size:12px;color:var(--mute);border-top:1px solid var(--line);padding-top:16px}}
</style></head>
<body>
<header><div class="wrap">
  <div class="kicker">Ignite Productions × Feel Free</div>
  <h1>Open Shifts — Make-Up Hours</h1>
  <div class="sub">Missed some hours? Submit your availability below and we'll slot you into an open make-up shift. Each shift is a {SHIFT_HOURS}-hour window — pick your start time and we'll do the rest.</div>
  <a class="back" href="index.html">← Back to route schedule</a>
</div></header>
<div class="wrap">

  <div class="sectlbl">Hours currently open by market</div>
  <div class="mgrid">{market_cards}</div>

  <div class="sectlbl">Submit your availability</div>

  <div class="thanks" id="thanks">
    <h2>✓ Availability submitted</h2>
    <p>Thanks — your make-up hours request is in. The Ignite team will confirm your shift by email. You can close this page.</p>
  </div>

  <form class="card" id="shiftForm" action="https://formsubmit.co/{FORM_TO}" method="POST">
    <input type="hidden" name="_subject" value="Open Shift availability — make-up hours">
    <input type="hidden" name="_cc" value="{FORM_CC}">
    <input type="hidden" name="_template" value="table">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_next" value="{NEXT_URL}">
    <input type="text" name="_honey" style="display:none">

    <div class="field">
      <label for="ba_name">Your name</label>
      <input type="text" id="ba_name" name="Name" placeholder="First and last name" required>
    </div>

    <div class="field">
      <label for="market">Market</label>
      <select id="market" name="Market" required>
        <option value="" disabled selected>Select a market…</option>
        {market_options}
      </select>
    </div>

    <div class="row2">
      <div class="field">
        <label for="date">Date available</label>
        <input type="date" id="date" name="Date" required>
      </div>
      <div class="field">
        <label for="start">Start time</label>
        <input type="time" id="start" name="Start Time" required>
        <div class="hint">Shifts run {SHIFT_HOURS} hours from your start.</div>
      </div>
    </div>

    <div class="window" id="window">Pick a start time to see your <span class="muted">{SHIFT_HOURS}-hour</span> shift window.</div>
    <input type="hidden" name="Shift Window" id="window_field" value="">

    <button type="submit">Submit availability</button>
  </form>

  <div class="foot">
    Prepared by Ignite Productions for Botanic Tonics, LLC (d/b/a Feel Free).
    Submitted availability is emailed to the Ignite scheduling team; shift confirmation follows by email.
  </div>
</div>
<script>
const SHIFT_HOURS = {SHIFT_HOURS};
const startEl = document.getElementById('start');
const winEl = document.getElementById('window');
const winField = document.getElementById('window_field');
const dateEl = document.getElementById('date');

// Don't let BAs pick a past date.
dateEl.min = new Date().toISOString().split('T')[0];

function fmt(h, m){{
  const ap = h < 12 ? 'AM' : 'PM';
  let hr = h % 12; if(hr === 0) hr = 12;
  return hr + ':' + String(m).padStart(2,'0') + ' ' + ap;
}}
function updateWindow(){{
  const v = startEl.value;
  if(!v){{ winEl.innerHTML = 'Pick a start time to see your <span class="muted">' + SHIFT_HOURS + '-hour</span> shift window.'; winField.value = ''; return; }}
  const [h, m] = v.split(':').map(Number);
  const endH = (h + SHIFT_HOURS) % 24;
  const startStr = fmt(h, m), endStr = fmt(endH, m);
  const wrapNote = (h + SHIFT_HOURS) >= 24 ? ' (next day)' : '';
  winEl.innerHTML = 'Your shift: <b>' + startStr + ' – ' + endStr + wrapNote + '</b> &nbsp;·&nbsp; <span class="muted">' + SHIFT_HOURS + ' hours</span>';
  winField.value = startStr + ' – ' + endStr + wrapNote + ' (' + SHIFT_HOURS + ' hrs)';
}}
startEl.addEventListener('input', updateWindow);

// Thank-you state after FormSubmit redirects back with ?submitted=1
if(new URLSearchParams(location.search).get('submitted') === '1'){{
  document.getElementById('shiftForm').style.display = 'none';
  document.getElementById('thanks').style.display = 'block';
}}
</script>
</body></html>"""

with open("open-shifts.html", "w") as f:
    f.write(HTML)
print("Open Shifts page written:", len(HTML), "bytes -> open-shifts.html")
