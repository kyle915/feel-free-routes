"""Build the client-facing branded PDF: overview + one calendar one-pager per market."""
import json
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

data = json.load(open("schedule.json"))
P = data["program"]; MK = data["markets"]; SCH = data["schedule"]

PW, PH = landscape(letter)
INK = HexColor("#14202b"); MUTE = HexColor("#5d6b78"); LINE = HexColor("#dbe2e8")
BG = HexColor("#f6f8fa"); CREAM = HexColor("#fff4d6"); GOLD = HexColor("#f0d98a"); NAVY = HexColor("#15455a")
M = 40
DAYS = ["Thu", "Fri", "Sat", "Sun"]
c = canvas.Canvas("Feel_Free_Summer2026_Routes_CLIENT.pdf", pagesize=(PW, PH))

def wrap_text(cv, text, font, size, maxw):
    cv.setFont(font, size)
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if cv.stringWidth(t, font, size) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def cover():
    c.setFillColor(NAVY); c.rect(0, 0, PW, PH, fill=1, stroke=0); c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11); c.drawString(M, PH-58, "IGNITE PRODUCTIONS  ×  FEEL FREE")
    c.setFont("Helvetica-Bold", 30); c.drawString(M, PH-100, "Summer 2026 Guerrilla Field-Sampling Program")
    c.setFont("Helvetica", 14)
    c.drawString(M, PH-126, f'{P["client"]}   ·   {P["start_date"]} – {P["end_date"]}   ·   {P["cadence"]}')
    stats = [(str(len(MK)), "Markets"), (str(len(SCH)), "Total shifts"), (str(len(SCH)*2), "BA deployments"),
             (f'{len(SCH)*5.5:.0f}', "BA-hours"), ("4", "Shifts / active mkt / wk")]
    x = M; y = PH-220; cw = 138; ch = 78
    for big, lab in stats:
        c.setFillColor(HexColor("#1d5468")); c.roundRect(x, y, cw, ch, 10, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 30); c.drawString(x+14, y+34, big)
        c.setFont("Helvetica", 11); c.drawString(x+14, y+16, lab); x += cw + 12
    c.setFillColor(white); c.setFont("Helvetica-Bold", 13)
    c.drawString(M, y-34, "MARKETS & SIGNATURE 21+ CORRIDORS")
    yy = y-58
    for mk, m in MK.items():
        c.setFillColor(HexColor(m["color"])); c.roundRect(M, yy-10, 150, 22, 5, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 10.5); c.drawString(M+10, yy-3, f'{m["code"]} · {mk}')
        corrs = []
        for s in SCH:
            if s["market"] == mk and s["corridor"] not in corrs: corrs.append(s["corridor"])
        text = ("  •  ".join(corrs[:5]))[:120] if corrs else m.get("status", "Schedule TBD")
        c.setFillColor(HexColor("#cfe0e6")); c.setFont("Helvetica", 10)
        c.drawString(M+170, yy-3, text); yy -= 30
    c.setFillColor(HexColor("#0e2630")); c.rect(0, 0, PW, 92, fill=1, stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 11); c.drawString(M, 70, "COMPLIANCE GUARDRAILS")
    c.setFillColor(white)
    for i, line in enumerate(wrap_text(c, P["compliance"], "Helvetica", 9.5, PW-2*M)):
        c.drawString(M, 54-i*13, line)
    c.showPage()

def tbd_page(mk):
    m = MK[mk]; col = HexColor(m["color"])
    c.setFillColor(BG); c.rect(0, 0, PW, PH, fill=1, stroke=0)
    c.setFillColor(col); c.rect(0, PH-64, PW, 64, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 22); c.drawString(M, PH-40, f'{mk}')
    c.setFont("Helvetica-Bold", 11); c.drawRightString(PW-M, PH-26, f'{m["code"]}  ·  Feel Free Summer 2026')
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(PW/2, PH/2+14, "Schedule TBD")
    c.setFillColor(MUTE); c.setFont("Helvetica", 12)
    c.drawCentredString(PW/2, PH/2-10, "Warehouse, corridors, and launch dates to be announced.")
    c.showPage()

def market_page(mk):
    m = MK[mk]; col = HexColor(m["color"])
    if m.get("tbd"):
        tbd_page(mk); return
    rows = [s for s in SCH if s["market"] == mk]
    grid = {(s["week"], s["day"]): s for s in rows}
    mkt_weeks = sorted(set(s["week"] for s in rows))
    c.setFillColor(BG); c.rect(0, 0, PW, PH, fill=1, stroke=0)
    c.setFillColor(col); c.rect(0, PH-64, PW, 64, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 22); c.drawString(M, PH-40, f'{mk}')
    c.setFont("Helvetica-Bold", 11); c.drawRightString(PW-M, PH-26, f'{m["code"]}  ·  Feel Free Summer 2026')
    c.setFont("Helvetica", 10); c.drawRightString(PW-M, PH-42, m.get("status", "Weekly guerrilla sampling route"))
    c.setFont("Helvetica", 9.5)
    c.drawString(M, PH-57, f'⌂ Shift start (warehouse): {m["warehouse"]}   |   2 BAs/shift · 5.5 hrs/BA · {m["product"]}')
    top = PH-74; bottom = 64; label_w = 70; gx = M + label_w; gw = PW - M - gx; colw = gw/4
    head_h = 22; nrows = len(mkt_weeks); rowh = (top - bottom - head_h) / nrows
    c.setFillColor(INK)
    for i, d in enumerate(DAYS):
        x = gx + i*colw; c.rect(x, top-head_h, colw-2, head_h, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 11)
        wlabel = "12–5 PM" if d in ("Sat", "Sun") else "3–8 PM"
        c.drawString(x+8, top-head_h+7, f'{d}  ·  {wlabel}'); c.setFillColor(INK)
    for r, w in enumerate(mkt_weeks):
        ytop = top - head_h - r*rowh
        c.setFillColor(col); c.rect(M, ytop-rowh, label_w-2, rowh, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(M+(label_w-2)/2, ytop-rowh/2-4, f'Wk {w}')
        anchor = next((s["date_pretty"] for s in rows if s["week"] == w), "")
        c.setFont("Helvetica", 6.6); c.drawCentredString(M+(label_w-2)/2, ytop-rowh+8, anchor.replace("Thu ", ""))
        for i, d in enumerate(DAYS):
            x = gx + i*colw; s = grid.get((w, d))
            c.setFillColor(white); c.setStrokeColor(LINE); c.setLineWidth(0.8)
            c.rect(x, ytop-rowh, colw-2, rowh, fill=1, stroke=1)
            if not s:
                c.setFillColor(MUTE); c.setFont("Helvetica-Oblique", 8)
                c.drawString(x+8, ytop-rowh/2, "— (no shift this week)"); continue
            pad = 7; cy = ytop-12
            if s["event"]:
                c.setFillColor(CREAM); c.rect(x+1, ytop-rowh+1, colw-4, rowh-2, fill=1, stroke=0)
                c.setStrokeColor(GOLD); c.setLineWidth(1); c.rect(x, ytop-rowh, colw-2, rowh, fill=0, stroke=1)
            c.setFillColor(INK); c.setFont("Helvetica-Bold", 9.3)
            for ln in wrap_text(c, s["corridor"], "Helvetica-Bold", 9.3, colw-2*pad)[:2]:
                c.drawString(x+pad, cy, ln); cy -= 11
            c.setFillColor(MUTE); c.setFont("Helvetica", 7.4)
            for ln in wrap_text(c, s["vibe"], "Helvetica", 7.4, colw-2*pad)[:2]:
                c.drawString(x+pad, cy, ln); cy -= 9
            cy -= 2
            for t in s["stops"]:
                c.setFillColor(col); c.setFont("Helvetica-Bold", 7.2); c.drawString(x+pad, cy, "›")
                c.setFillColor(INK); c.setFont("Helvetica", 7.2)
                zone = wrap_text(c, t["zone"], "Helvetica", 7.2, colw-2*pad-10)[:1]
                c.drawString(x+pad+9, cy, zone[0] if zone else t["zone"]); cy -= 8.5
                c.setFillColor(MUTE); c.setFont("Helvetica", 6.6); c.drawString(x+pad+9, cy, t["time"]); cy -= 9
            if s["event"]:
                c.setFillColor(HexColor("#7a5b00")); c.setFont("Helvetica-Bold", 6.8)
                ev = wrap_text(c, "★ "+s["event"], "Helvetica-Bold", 6.8, colw-2*pad)[:1]
                c.drawString(x+pad, ytop-rowh+5, ev[0] if ev else "")
    c.setFillColor(MUTE); c.setFont("Helvetica", 8)
    c.drawString(M, 50, "Each shift starts at the warehouse for product pickup, then BAs rotate between the listed stations within the corridor.")
    c.drawString(M, 38, "Stations may shift within a corridor per BA safety assessment, weather, permits, and the weekly Kratom Eligibility Schedule. Kratom SKUs: 21+ only, ID-verified.")
    c.setFillColor(col); c.setFont("Helvetica-Bold", 8)
    c.drawRightString(PW-M, 38, "Ignite Productions  ·  Feel Free Summer 2026")
    c.showPage()

cover()
for mk in MK: market_page(mk)
c.save()
print("PDF saved (pages:", 1+len(MK), ")")
