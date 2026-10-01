# -*- coding: utf-8 -*-
"""
Ebook generator - Automation Skills Portfolio series
Electrical Engineering Technology: Industrial Microgrid Controller (BESS Dispatch)
Author: Sipho Lucky Sibanda
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Sans", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Oblique", FD + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("Cond-Bold", FD + "DejaVuSansCondensed-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Cond", FD + "DejaVuSansCondensed.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FD + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("Mono-Bold", FD + "DejaVuSansMono-Bold.ttf"))

# ---------------------------------------------------------------------------
# Palette - electric blue primary, amber (solar) / green (battery) secondary
# ---------------------------------------------------------------------------
BASE      = colors.HexColor("#0D1218")
BASE2     = colors.HexColor("#141B23")
BASE_LINE = colors.HexColor("#26313D")
BLUEACC   = colors.HexColor("#7FA8D4")
BLUEACC_LT= colors.HexColor("#D6E4F5")
DEEPBLUE  = colors.HexColor("#1B4B8F")
TEAL      = colors.HexColor("#2ECC71")
AMBER     = colors.HexColor("#F5A623")
RED       = colors.HexColor("#E0503E")
SOLAR     = colors.HexColor("#D98F1E")
INK       = colors.HexColor("#151C24")
MUTED     = colors.HexColor("#5C6E80")
MUTED_LT  = colors.HexColor("#C3D3E3")
PANEL     = colors.HexColor("#EBF1F8")
ROWBAND   = colors.HexColor("#F5F9FC")
GRIDLINE  = colors.HexColor("#D6E1EC")

PAGE_W, PAGE_H = A4
MARGIN_L, MARGIN_R = 22 * mm, 20 * mm
MARGIN_TOP, MARGIN_BOT = 26 * mm, 24 * mm
AVAIL_W = PAGE_W - MARGIN_L - MARGIN_R

DOC_TITLE = "INDUSTRIAL MICROGRID CONTROLLER"
AUTHOR = "Sipho Lucky Sibanda"
OUTFILE = "/home/claude/microgrid-bess-dispatch/ebook/Microgrid_Technical_Manual.pdf"

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
body = ParagraphStyle("body", fontName="Sans", fontSize=10.2, leading=15,
                       textColor=INK, spaceAfter=8, alignment=TA_JUSTIFY)
body_l = ParagraphStyle("body_l", parent=body, alignment=TA_LEFT)
lead = ParagraphStyle("lead", parent=body, fontSize=12.5, leading=18, textColor=DEEPBLUE,
                       spaceAfter=10)
kicker = ParagraphStyle("kicker", fontName="Mono", fontSize=8.5, leading=11,
                         textColor=DEEPBLUE, spaceAfter=2)
h1 = ParagraphStyle("h1", fontName="Cond-Bold", fontSize=19, leading=22,
                     textColor=colors.HexColor("#12335E"), spaceAfter=2)
h2 = ParagraphStyle("h2", fontName="Cond-Bold", fontSize=13.5, leading=16,
                     textColor=colors.HexColor("#12335E"), spaceBefore=14, spaceAfter=6)
h3 = ParagraphStyle("h3", fontName="Sans-Bold", fontSize=10.6, leading=13,
                     textColor=colors.HexColor("#12335E"), spaceBefore=8, spaceAfter=4)
caption = ParagraphStyle("caption", fontName="Sans-Oblique", fontSize=8.3, leading=11,
                          textColor=MUTED, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)
bullet = ParagraphStyle("bullet", parent=body, alignment=TA_LEFT, leftIndent=12,
                         bulletIndent=0, spaceAfter=5)
chip_num = ParagraphStyle("chip_num", fontName="Cond-Bold", fontSize=17, leading=20,
                           textColor=colors.white, alignment=TA_CENTER)
toc_entry = ParagraphStyle("toc_entry", fontName="Sans", fontSize=10.5, leading=16,
                            textColor=INK)
toc_num = ParagraphStyle("toc_num", fontName="Mono-Bold", fontSize=10.5, leading=16,
                          textColor=DEEPBLUE)
cell_hdr = ParagraphStyle("cell_hdr", fontName="Sans-Bold", fontSize=8.6, leading=11,
                           textColor=colors.white)
cell_txt = ParagraphStyle("cell_txt", fontName="Sans", fontSize=8.6, leading=12,
                           textColor=INK)
code_style = ParagraphStyle("code", fontName="Mono", fontSize=7.5, leading=11.0,
                             textColor=BLUEACC_LT)
callout_title = lambda c: ParagraphStyle("ct", fontName="Sans-Bold", fontSize=9.6,
                                          leading=12, textColor=c, spaceAfter=3)
callout_body = ParagraphStyle("cb", fontName="Sans", fontSize=9.4, leading=13.4,
                               textColor=INK)

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def P(text, style=body):
    return Paragraph(text, style)

def chapter_head(num, title, kicker_text="MICROGRID BESS DISPATCH"):
    chip = Table([[Paragraph(str(num).zfill(2), chip_num)]],
                 colWidths=[17 * mm], rowHeights=[17 * mm])
    chip.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DEEPBLUE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    title_block = [P(kicker_text, kicker), P(title, h1)]
    row = Table([[chip, title_block]], colWidths=[22 * mm, AVAIL_W - 22 * mm])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    rule = HRFlowable(width="100%", thickness=1.3, color=BLUEACC, spaceBefore=8, spaceAfter=16)
    return [row, rule]

def subhead(text):
    return P(text, h2)

def bullets(items):
    out = []
    for it in items:
        out.append(P("&#8226;&nbsp;&nbsp;" + it, bullet))
    return out

def code_block(code_text, cap=None):
    lines = code_text.strip("\n").split("\n")
    esc_lines = []
    for ln in lines:
        stripped = ln.lstrip(" ")
        n = len(ln) - len(stripped)
        esc_lines.append("&nbsp;" * n + esc(stripped) if stripped else "&nbsp;")
    para = Paragraph("<br/>".join(esc_lines), code_style)
    cell = Table([[para]], colWidths=[AVAIL_W])
    cell.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BASE2),
        ("BOX", (0, 0), (-1, -1), 0.75, BASE_LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    out = [cell]
    if cap:
        out.append(P(cap, caption))
    else:
        out.append(Spacer(1, 10))
    return out

def data_table(headers, rows, col_widths=None):
    data = [[Paragraph(h, cell_hdr) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), cell_txt) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12335E")),
        ("GRID", (0, 0), (-1, -1), 0.5, GRIDLINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROWBAND))
    t.setStyle(TableStyle(style))
    return t

def callout(title, text, kind="info"):
    color = {"info": BLUEACC, "warning": AMBER, "critical": RED, "ok": TEAL}[kind]
    label = {"info": "NOTE", "warning": "ENGINEERING NOTE", "critical": "HONEST LIMITATION",
             "ok": "VERIFIED / DESIGN NOTE"}[kind]
    content = [P("%s &mdash; %s" % (label, title), callout_title(color)), P(text, callout_body)]
    inner = Table([[content]], colWidths=[AVAIL_W - 16])
    inner.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))
    outer = Table([["", inner]], colWidths=[5, AVAIL_W - 5])
    outer.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), color),
        ("BACKGROUND", (1, 0), (1, 0), PANEL),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
        ("RIGHTPADDING", (1, 0), (1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return [outer, Spacer(1, 10)]

def full_image(path, cap, max_h_mm=95):
    from PIL import Image as PILImage
    iw, ih = PILImage.open(path).size
    ratio = ih / float(iw)
    w = AVAIL_W
    h = w * ratio
    max_h = max_h_mm * mm
    if h > max_h:
        h = max_h
        w = h / ratio
    img = Image(path, width=w, height=h)
    img.hAlign = "CENTER"
    return [img, P(cap, caption)]


# ---------------------------------------------------------------------------
# Page backgrounds
# ---------------------------------------------------------------------------
def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(BASE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setStrokeColor(BASE_LINE)
    c.setLineWidth(0.4)
    step = 12 * mm
    x = 0
    while x < PAGE_W:
        c.line(x, 0, x, PAGE_H); x += step
    y = 0
    while y < PAGE_H:
        c.line(0, y, PAGE_W, y); y += step

    c.setStrokeColor(BLUEACC)
    c.setLineWidth(1.1)
    c.rect(10 * mm, 10 * mm, PAGE_W - 20 * mm, PAGE_H - 20 * mm, fill=0, stroke=1)

    # Decorative tri-node energy glyph, bottom right
    cx, cy = PAGE_W - 52 * mm, 42 * mm
    nodes = [(0, 18, SOLAR), (-16, -6, TEAL), (16, -6, BLUEACC)]
    c.setStrokeColor(colors.HexColor("#3a4652"))
    c.setLineWidth(0.8)
    for nx, ny in [(0,18),(-16,-6),(16,-6)]:
        c.line(cx, cy, cx+nx*mm, cy+ny*mm)
    for nx, ny, col in nodes:
        c.setFillColor(col)
        c.circle(cx+nx*mm, cy+ny*mm, 2.2*mm, fill=1, stroke=0)
    c.setFillColor(BLUEACC)
    c.setFont("Mono-Bold", 7)
    c.drawCentredString(cx, cy - 18*mm, "PCC")

    c.setFillColor(BLUEACC)
    c.setFont("Mono", 10.5)
    c.drawString(24 * mm, PAGE_H - 42 * mm, "AUTOMATION SKILLS PORTFOLIO   ·   ELECTRICAL ENG.")

    c.setFillColor(colors.white)
    c.setFont("Cond-Bold", 23)
    for i, line in enumerate(["INDUSTRIAL MICROGRID", "CONTROLLER"]):
        c.drawString(24 * mm, PAGE_H - 62 * mm - i * 11.5 * mm, line)

    c.setFont("Cond", 13.5)
    c.setFillColor(MUTED_LT)
    c.drawString(24 * mm, PAGE_H - 90 * mm, "Intelligent Battery Energy Storage System (BESS) Dispatch")

    c.setStrokeColor(BASE_LINE)
    c.setLineWidth(0.8)
    c.line(24 * mm, 46 * mm, PAGE_W - 24 * mm, 46 * mm)

    c.setFont("Mono", 9.5)
    c.setFillColor(AMBER)
    c.drawString(24 * mm, 38 * mm, "TECHNICAL PROJECT MANUAL  ·  REV. A")
    c.setFont("Sans-Bold", 13)
    c.setFillColor(colors.white)
    c.drawString(24 * mm, 31 * mm, "By " + AUTHOR)
    c.setFont("Sans", 8.6)
    c.setFillColor(MUTED_LT)
    c.drawString(24 * mm, 25.5 * mm, "Platform: Siemens S7-1500 (SCL) / CODESYS-portable Structured Text")
    c.drawString(24 * mm, 21 * mm, "Simulation & Portfolio Engineering Build  ·  Not for Utility Interconnection Use")
    c.restoreState()

def draw_body(c, doc):
    c.saveState()
    c.setFillColor(BASE)
    c.rect(0, PAGE_H - 15 * mm, PAGE_W, 15 * mm, fill=1, stroke=0)
    c.setFillColor(BLUEACC)
    c.setFont("Mono", 7.6)
    c.drawString(MARGIN_L, PAGE_H - 9.5 * mm, DOC_TITLE)
    c.setFillColor(colors.white)
    c.setFont("Sans", 7.4)
    c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 9.5 * mm, "By " + AUTHOR)
    c.setStrokeColor(BLUEACC)
    c.setLineWidth(0.8)
    c.line(0, PAGE_H - 15 * mm, PAGE_W, PAGE_H - 15 * mm)

    c.setFillColor(MUTED)
    c.setFont("Mono", 7.8)
    c.drawString(MARGIN_L, 13 * mm, "MICROGRID-BESS-DISPATCH")
    c.drawCentredString(PAGE_W / 2, 13 * mm, "Page %d" % c.getPageNumber())
    c.drawRightString(PAGE_W - MARGIN_R, 13 * mm, "Simulation / Portfolio Build")
    c.setStrokeColor(BLUEACC)
    c.setLineWidth(1)
    c.line(PAGE_W - MARGIN_R, 17 * mm, PAGE_W - MARGIN_R, 21 * mm)
    c.line(PAGE_W - MARGIN_R - 4 * mm, 17 * mm, PAGE_W - MARGIN_R, 17 * mm)
    c.restoreState()


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------
story = [PageBreak()]

# ---- Document control / disclaimer ------------------------------------------------
story += chapter_head("i", "Document Control &amp; Disclaimer", "FRONT MATTER")
story.append(P(
    "This document is a self-authored technical project manual produced as part of a "
    "personal engineering portfolio. It describes the design, control philosophy, and "
    "simulated validation of an industrial microgrid controller dispatching a behind-the-"
    "meter battery energy storage system, built to demonstrate demand-charge economics, "
    "time-of-use energy arbitrage, and power-quality control for automation, controls, "
    "and electrical/power systems engineering roles.", body))
story.append(P(
    "The system described here was developed and tested in simulation only (PLCSIM-style "
    "forcing of inputs and desktop review). No part of this project has been installed, "
    "commissioned, or verified on physical power systems hardware, and it must not be "
    "treated as a certified utility interconnection or protection system.", body))

story += callout(
    "Portfolio project, not a certified interconnection system",
    "A real behind-the-meter BESS installation requires a utility interconnection study, "
    "protection coordination, and compliance with grid codes such as IEEE 1547. Figures, "
    "thresholds, and I/O in this manual are engineering-realistic but illustrative.", "critical")

data = [
    ["Document Title", "Industrial Microgrid Controller \u2014 Technical Manual"],
    ["Author", AUTHOR],
    ["Revision", "A"],
    ["Document Type", "Portfolio Technical Manual (Simulation)"],
    ["Target Platform", "Siemens S7-1500 (TIA Portal / SCL) \u2014 CODESYS-portable"],
    ["Related Repository", "microgrid-bess-dispatch"],
    ["Series", "Automation Skills Portfolio \u2014 Electrical Engineering Technology"],
]
t = Table(data, colWidths=[45 * mm, AVAIL_W - 45 * mm])
t.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Sans-Bold"), ("FONTNAME", (1, 0), (1, -1), "Sans"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.4), ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#12335E")),
    ("TEXTCOLOR", (1, 0), (1, -1), INK),
    ("GRID", (0, 0), (-1, -1), 0.4, GRIDLINE),
    ("BACKGROUND", (0, 0), (0, -1), PANEL),
    ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(t)
story.append(PageBreak())

# ---- Contents ------------------------------------------------------------
story += chapter_head("ii", "Contents", "FRONT MATTER")
toc = [
    ("01", "Industry Context: Demand Charges &amp; Behind-the-Meter Storage"),
    ("02", "System Architecture &amp; Energy Flow Overview"),
    ("03", "Hardware &amp; Instrumentation Specification"),
    ("04", "I/O List &amp; Configuration Parameters"),
    ("05", "Control Philosophy: Dispatch Priority &amp; the Capability Curve"),
    ("06", "PLC Logic Walkthrough"),
    ("07", "HMI Design &amp; the Energy Flow Dashboard"),
    ("08", "Alarm Philosophy &amp; Fail-Safe Design"),
    ("09", "Testing, Commissioning &amp; FAT Procedures"),
    ("10", "Limitations, Real-World Deltas &amp; Future Work"),
    ("A", "Appendix A &mdash; I/O Quick Reference"),
    ("B", "Appendix B &mdash; Full Structured Text Listing"),
    ("C", "Appendix C &mdash; Glossary"),
    ("&mdash;", "About the Author"),
]
rows = []
for num, title in toc:
    rows.append([P(num, toc_num), P(title, toc_entry)])
tt = Table(rows, colWidths=[14 * mm, AVAIL_W - 14 * mm])
tt.setStyle(TableStyle([
    ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LINEBELOW", (0, 0), (-1, -2), 0.4, GRIDLINE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(tt)
story.append(PageBreak())

# ---- Executive Summary ----------------------------------------------------
story += chapter_head("iii", "Executive Summary", "FRONT MATTER")
story.append(P(
    "This is the fifth deliberate discipline shift in the wider automation portfolio, "
    "moving from validated process/safety control toward behind-the-meter power systems "
    "economics - a field where the control logic's job is as much about minimising a "
    "utility bill as it is about keeping a process running. Industrial utility tariffs "
    "are frequently dominated by demand charges: a single number, the highest 15 or "
    "30-minute average kW demand in the billing period, that can dwarf the cost of the "
    "energy actually consumed.", lead))
story.append(P(
    "<b>FB_Microgrid_BESS_Dispatch</b> gives a behind-the-meter battery three jobs, in a "
    "fixed and deliberate priority order: protect itself (SOC limits), shave demand peaks "
    "(the single biggest lever on the bill), and only after that, arbitrage cheap "
    "off-peak energy against expensive on-peak energy. A separate, largely independent "
    "control loop corrects the site's power factor using the same battery inverter's "
    "reactive power capability - genuinely respecting the shared apparent-power ceiling "
    "a real four-quadrant inverter operates under.", body))
story.append(P(
    "The design is explicit about honesty under stress: when a demand peak exceeds what "
    "the battery can actually cover, the function block discharges everything it safely "
    "can and <b>flags the shortfall</b> rather than silently under-shaving and letting "
    "the bill exceed expectations unflagged. Solar is curtailed only as a genuine last "
    "resort, after the battery is full and the utility interconnection agreement doesn't "
    "permit export.", body))
story.append(P(
    "What follows documents the tariff and interconnection context, architecture, "
    "hardware assumptions, full I/O list and configuration structure, control "
    "philosophy, complete annotated code, HMI design, alarm philosophy, and the "
    "functional test procedure used to validate the logic in simulation.", body))
story.append(PageBreak())

# ---- Chapter 1: Industry Context -------------------------------------------
story += chapter_head(1, "Industry Context: Demand Charges &amp; Behind-the-Meter Storage")
story.append(P(
    "Most industrial and commercial electricity tariffs bill on two separate components: "
    "energy consumed (kWh) and peak demand (kW). The <b>demand charge</b> is calculated "
    "from the single highest average demand recorded during a short window - typically "
    "15 or 30 minutes - anywhere in the entire billing period. A factory that runs "
    "efficiently all month but has one 20-minute spike from starting a large motor can "
    "see that single spike drive a meaningful fraction of its entire electricity bill.", body))
story.append(subhead("Why this makes a battery genuinely valuable, not just green"))
story.append(P(
    "A behind-the-meter battery sized correctly can \"shave\" that peak by discharging "
    "exactly when the factory's net demand would otherwise exceed a target ceiling - "
    "reducing the billed demand without the factory changing its actual operations at "
    "all. This is frequently the single largest economic driver for installing a BESS at "
    "an industrial site, ahead of energy arbitrage or renewable integration on their own.", body))
story.append(subhead("Time-of-use tariffs and arbitrage"))
story.append(P(
    "Many utilities also charge different energy rates depending on the time of day - "
    "cheaper overnight/off-peak rates, and expensive afternoon/evening on-peak rates that "
    "coincide with system-wide demand. A battery charged during off-peak hours and "
    "discharged during on-peak hours captures that price difference directly - "
    "<b>energy arbitrage</b> - though, as this project's dispatch priority makes explicit "
    "(Chapter 5), that opportunity is worth less than avoiding a demand charge peak.", body))
story += callout(
    "Interconnection agreements matter as much as the tariff",
    "Whether a site can export excess solar back to the grid at all is governed by its "
    "utility interconnection agreement, not just technical capability. Many industrial "
    "agreements simply don't allow export - which is why this project treats grid export "
    "as conditional (`DI_NetMeteringAllowed`) rather than assumed, with battery charging "
    "and, as a last resort, solar curtailment as the fallback.", "info")
story.append(PageBreak())

# ---- Chapter 2: Architecture ----------------------------------------------
story += chapter_head(2, "System Architecture &amp; Energy Flow Overview")
story.append(P(
    "Solar PV, a battery energy storage system, and the utility grid all connect at a "
    "common point - the Point of Common Coupling (PCC) - feeding the factory's load. The "
    "microgrid controller measures active and reactive power at the PCC and dispatches "
    "the battery's active and reactive power to manage both the bill and the site's power "
    "quality.", body))
story += full_image("../images/architecture_diagram.png",
    "Figure 2.1 &mdash; Energy flow and control architecture. Dashed lines represent PLC "
    "signal and configuration paths; the PCC is where solar, battery, grid, and factory "
    "load all meet electrically.", max_h_mm=100)
story.append(subhead("Control hierarchy"))
story += bullets([
    "<b>Field layer</b> &mdash; solar PV inverter, battery energy storage system with its "
    "own BMS, main utility meter, and PCC power quality metering.",
    "<b>Control layer</b> &mdash; a single PLC function block, "
    "<b>FB_Microgrid_BESS_Dispatch</b>, hosted on a Siemens S7-1500 (or CODESYS-based "
    "substation/microgrid controller), running the full dispatch priority chain.",
    "<b>Supervisory layer</b> &mdash; SCADA (tariff schedule and demand threshold "
    "configuration) and the energy HMI (live flow visualisation for site operators).",
])
story.append(KeepTogether([
    subhead("Why net load, not gross load, drives the dispatch decision"),
    P(
        "The function block computes <code>NetLoad_kW = FactoryLoad - SolarGeneration</code> "
        "as its very first step, and every dispatch decision downstream operates on that net "
        "figure. Solar generation is, in effect, treated as a form of demand reduction the "
        "battery doesn't need to duplicate - the battery only needs to cover whatever the "
        "site's own generation isn't already covering.", body)
]))
story.append(PageBreak())

# ---- Chapter 3: Hardware ----------------------------------------------------
story += chapter_head(3, "Hardware &amp; Instrumentation Specification")
story.append(P(
    "As with the rest of this portfolio, the logic here is platform-portable but written "
    "against a concrete reference platform so thresholds are grounded rather than "
    "arbitrary.", body))
story.append(data_table(
    ["Component", "Representative Spec", "Role"],
    [
        ["Microgrid Controller CPU", "Siemens SIMATIC S7-1500", "Executes FB_Microgrid_BESS_Dispatch"],
        ["Battery Inverter", "500 kW / 550 kVA, four-quadrant", "Active + reactive power dispatch"],
        ["Battery Management System (BMS)", "CAN/Modbus link to the controller", "SOC feedback and protection"],
        ["Main Utility Meter", "Revenue-grade, 4-20mA or Modbus", "Factory load and PCC power quality"],
        ["Solar PV Inverter", "Grid-tied string or central inverter", "Solar generation feedback"],
        ["Real-Time Clock", "Controller-resident RTC", "Time-of-use schedule reference"],
    ],
    col_widths=[52 * mm, 60 * mm, AVAIL_W - 52 * mm - 60 * mm]))
story.append(Spacer(1, 8))
story += callout(
    "Why the inverter's apparent power rating matters as much as its kW rating",
    "A battery inverter rated 500 kW active power might carry a 550 kVA apparent power "
    "rating - the extra headroom exists specifically so some reactive power capability "
    "remains even while dispatching significant active power. Sizing an inverter on "
    "active power alone, without considering how much reactive power support it will "
    "also be expected to provide, is a common and costly real-world design mistake.", "ok")
story.append(PageBreak())

# ---- Chapter 4: I/O List ----------------------------------------------------
story += chapter_head(4, "I/O List &amp; Configuration Parameters")
story.append(P(
    "The table below is the working I/O list for FB_Microgrid_BESS_Dispatch (see also "
    "<b>docs/IO_List.md</b> in the repository, and Appendix A of this manual).", body))
story.append(subhead("Configuration parameters (downloaded from SCADA)"))
story.append(data_table(
    ["Field", "Typical Value"],
    [
        ["DemandThreshold_kW", "800 kW"],
        ["OnPeak_Start_hr / OnPeak_End_hr", "14.0 / 20.0"],
        ["OffPeak_Start_hr / OffPeak_End_hr", "22.0 / 6.0"],
        ["Target_PF", "0.95"],
        ["Min_SOC_Pct / Max_SOC_Pct", "20.0 / 95.0"],
        ["Battery_Rated_kW", "500 kW"],
        ["Battery_Rated_kVA", "550 kVA"],
        ["Arbitrage_Charge_SOC_Target_Pct", "90.0 %"],
    ],
    col_widths=[70 * mm, AVAIL_W - 70 * mm]))
story.append(Spacer(1, 10))
story.append(subhead("Key inputs and outputs"))
story.append(data_table(
    ["Tag", "Description", "Signal"],
    [
        ["AI_FactoryLoad_kW / AI_SolarGeneration_kW", "Site metering", "4-20mA x2"],
        ["AI_BatterySOC_Pct / AI_ReactivePower_kVAR", "Battery + PCC feedback", "Mixed x2"],
        ["AI_HourOfDay_Decimal", "TOU schedule reference", "From RTC"],
        ["DI_NetMeteringAllowed / DI_System_Enable", "Interconnection + enable", "Digital x2"],
        ["AO_Battery_ActivePower_kW / ReactivePower_kVAR", "Battery dispatch commands", "4-20mA x2"],
        ["AO_SolarCurtailment_Pct", "Last-resort curtailment command", "4-20mA"],
        ["BESS_Mode / RatePeriod / Calculated_PF / SystemStatus", "State &amp; power quality data", "Mixed"],
    ],
    col_widths=[70 * mm, 62 * mm, AVAIL_W - 70 * mm - 62 * mm]))
story.append(PageBreak())


# ---- Chapter 5: Control Philosophy -----------------------------------------
story += chapter_head(5, "Control Philosophy: Dispatch Priority &amp; the Capability Curve")
story.append(P(
    "Two ideas define this project's control philosophy: a fixed economic priority order "
    "for active power, and a physically-grounded sharing rule between active and reactive "
    "power on the one inverter that has to deliver both.", body))
story.append(subhead("5.1 &nbsp; The dispatch priority order, and why it's this order"))
story.append(data_table(
    ["Priority", "Action", "Why it outranks what's below it"],
    [
        ["1", "Battery protection (SOC limits)", "A damaged battery has no economic value at all - this is non-negotiable"],
        ["2", "Peak shaving", "Demand charges are billed on a single peak - often the single largest bill line item"],
        ["3", "TOU arbitrage discharge (on-peak)", "Expensive energy avoided, but smaller and more gradual value than a demand spike"],
        ["4", "TOU arbitrage charge (off-peak)", "Prepares capacity for tomorrow's opportunities 2 and 3"],
        ["5", "Solar self-consumption / idle", "Lowest-priority use of remaining capacity"],
    ],
    col_widths=[18 * mm, 60 * mm, AVAIL_W - 18 * mm - 60 * mm]))
story.append(Spacer(1, 8))
story.append(P(
    "This is not an arbitrary preference ordering - it's a rough ranking of financial "
    "impact per kWh of battery capacity spent, for a typical industrial tariff structure. "
    "A dispatch algorithm that let arbitrage compete on equal footing with peak shaving "
    "risks a battery that's mid-arbitrage-discharge exactly when a demand spike arrives "
    "with nothing left to cover it.", body))
story.append(subhead("5.2 &nbsp; Honest shortfall reporting"))
story.append(P(
    "If a demand peak exceeds what the battery can actually deliver - either because SOC "
    "is too low or the peak simply exceeds the inverter's rated power - the function block "
    "discharges everything it safely can and raises <code>Alarm_DemandExceeded</code> "
    "rather than pretending the peak was fully covered. A facilities manager relying on "
    "this system needs to know when a shave attempt fell short, not discover it as a "
    "surprise on next month's bill.", body))
story.append(subhead("5.3 &nbsp; The shared inverter capability curve"))
story.append(P(
    "A real four-quadrant battery inverter has one apparent power rating, "
    "S<sub>rated</sub>, shared between active power (P) and reactive power (Q):", body))
story.append(P(
    "&radic;(P&sup2; + Q&sup2;) &le; S<sub>rated</sub>",
    ParagraphStyle("eq", parent=body, fontName="Mono", alignment=TA_CENTER, fontSize=11,
                   textColor=DEEPBLUE, spaceAfter=10)))
story.append(P(
    "This project computes the reactive power headroom that remains <i>after</i> active "
    "power is already committed to peak shaving or arbitrage, rather than treating P and "
    "Q as two independent, unlimited outputs. During a large peak-shaving event, there may "
    "be very little reactive headroom left - and the power factor correction logic "
    "explicitly accepts that limit rather than exceeding the inverter's real rating.", body))
story += callout(
    "Why PF correction still runs during a peak-shave event, just with less to give",
    "It would be simpler to disable power factor correction entirely whenever active power "
    "dispatch is high. This project deliberately doesn't do that - it computes whatever "
    "reactive headroom genuinely remains and uses all of it, flagging "
    "<code>Alarm_PF_OutOfSpec</code> only if that's insufficient to fully correct PF. "
    "Partial correction is still better than none.", "ok")
story.append(PageBreak())

# ---- Chapter 6: PLC Logic Walkthrough --------------------------------------
story += chapter_head(6, "PLC Logic Walkthrough")
story.append(P(
    "This chapter walks through <b>FB_Microgrid_BESS_Dispatch</b> section by section. The "
    "full listing is reproduced in Appendix B.", body))

story.append(subhead("6.1 &nbsp; Net load and battery headroom"))
story += code_block(
"""NetLoad_kW := AI_FactoryLoad_kW - AI_SolarGeneration_kW;

IF AI_BatterySOC_Pct > Config.Min_SOC_Pct THEN
    Available_Discharge_kW := Config.Battery_Rated_kW;
ELSE
    Available_Discharge_kW := 0.0;
END_IF

IF AI_BatterySOC_Pct < Config.Max_SOC_Pct THEN
    Available_Charge_kW := Config.Battery_Rated_kW;
ELSE
    Available_Charge_kW := 0.0;
END_IF""", "Listing 6.1 &mdash; Protection limits computed before any economic decision is made.")

story.append(subhead("6.2 &nbsp; Peak shaving, with honest shortfall reporting"))
story += code_block(
"""ELSIF NetLoad_kW > Config.DemandThreshold_kW THEN
    RequiredShave_kW := NetLoad_kW - Config.DemandThreshold_kW;
    IF RequiredShave_kW <= Available_Discharge_kW THEN
        AO_Battery_ActivePower_kW := RequiredShave_kW;
        Alarm_DemandExceeded := FALSE;
    ELSE
        AO_Battery_ActivePower_kW := Available_Discharge_kW;
        Alarm_DemandExceeded := TRUE;
    END_IF
    BESS_Mode := MODE_PEAK_SHAVE;""",
    "Listing 6.2 &mdash; The battery discharges everything it safely can; a shortfall is flagged, not hidden.")

story.append(subhead("6.3 &nbsp; TOU arbitrage - the literal \"battery vs. grid\" decision"))
story += code_block(
"""ELSIF (RatePeriod = PERIOD_ONPEAK) AND (Available_Discharge_kW > 0.0) THEN
    AO_Battery_ActivePower_kW := MIN(NetLoad_kW, Available_Discharge_kW);
    BESS_Mode := MODE_ARBITRAGE_DISCHARGE;

ELSIF (RatePeriod = PERIOD_OFFPEAK) AND (AI_BatterySOC_Pct < Config.Arbitrage_Charge_SOC_Target_Pct)
      AND (Available_Charge_kW > 0.0) THEN
    AO_Battery_ActivePower_kW := -Available_Charge_kW;
    BESS_Mode := MODE_ARBITRAGE_CHARGE;""",
    "Listing 6.3 &mdash; This is the code the recruiter brief was built around: exactly when to draw from the battery versus buy from the grid.")

story.append(subhead("6.4 &nbsp; Reactive power, sharing the inverter's rating"))
story += code_block(
"""ActivePowerMagnitude_kW := ABS(AO_Battery_ActivePower_kW);
Available_S_kVA := SQRT(MAX(0.0, (Config.Battery_Rated_kVA * Config.Battery_Rated_kVA)
                                   - (ActivePowerMagnitude_kW * ActivePowerMagnitude_kW)));

IF Calculated_PF < Config.Target_PF THEN
    RequiredQ_kVAR := AI_ReactivePower_kVAR * (1.0 - (Calculated_PF / Config.Target_PF));
    IF RequiredQ_kVAR > Available_S_kVA THEN
        AO_Battery_ReactivePower_kVAR := Available_S_kVA;
    ELSE
        AO_Battery_ReactivePower_kVAR := RequiredQ_kVAR;
    END_IF
    Alarm_PF_OutOfSpec := (AO_Battery_ReactivePower_kVAR < RequiredQ_kVAR);
END_IF""", "Listing 6.4 &mdash; Reactive headroom is derived FROM the active power already committed, not assumed unlimited.")
story.append(PageBreak())


# ---- Chapter 7: HMI ---------------------------------------------------------
story += chapter_head(7, "HMI Design &amp; the Energy Flow Dashboard")
story.append(P(
    "The HMI mockup (<b>hmi/index.html</b> in the repository) is built around a live "
    "energy flow diagram - solar, battery, grid, and factory load meeting at a central "
    "PCC node - paired with a time-of-use schedule strip and live power-quality metrics, "
    "matching the \"power flowing into a factory\" dashboard this project was scoped "
    "against.", body))
story += full_image("../images/hmi-dashboard.png",
    "Figure 7.1 &mdash; Mid-afternoon on-peak arbitrage discharge: battery covering "
    "500kW of the 683kW net load, animated flow lines showing direction, and the TOU "
    "strip's time marker sitting inside the on-peak (red) band.", max_h_mm=115)
story.append(subhead("Design decisions"))
story += bullets([
    "<b>A tri-colour energy palette, not a single accent</b> &mdash; amber for solar, "
    "green for battery, blue for grid - a sixth distinct visual identity in this "
    "portfolio, and the only one that genuinely needs three colours rather than one to "
    "represent its subject honestly.",
    "<b>Animated, directional flow lines</b> &mdash; each connection's arrowhead flips to "
    "show the actual direction of power flow (e.g. battery charging vs. discharging), "
    "tied directly to the sign convention the PLC logic itself uses.",
    "<b>The TOU schedule is always visible</b> &mdash; with a live time marker, so an "
    "operator can see at a glance not just what the system is doing now, but why, given "
    "where the site sits in its tariff cycle.",
    "<b>Numbers that are internally consistent</b> &mdash; the HMI's own dispatch "
    "simulation mirrors the same priority logic as the PLC, so battery kW + grid kW "
    "always sums to the displayed net load, the same arithmetic discipline the real "
    "function block enforces.",
])
story.append(PageBreak())

# ---- Chapter 8: Alarm Philosophy -------------------------------------------
story += chapter_head(8, "Alarm Philosophy &amp; Fail-Safe Design")
story.append(P(
    "Every alarm in this system maps to a specific financial or power-quality consequence, "
    "consistent with the rest of this portfolio.", body))
story.append(data_table(
    ["Condition", "Meaning", "Expected Response"],
    [
        ["Alarm_SOC_Low / Alarm_SOC_High", "Battery at a protective SOC limit", "Informational - the battery is managing itself correctly"],
        ["Alarm_DemandExceeded", "Battery could not fully cover a demand peak", "Review whether battery sizing or the demand threshold needs revisiting"],
        ["Alarm_PF_OutOfSpec", "Inverter reactive headroom insufficient for target PF", "Expected during large peak-shave events; investigate if persistent outside them"],
    ],
    col_widths=[52 * mm, 56 * mm, AVAIL_W - 52 * mm - 56 * mm]))
story.append(Spacer(1, 10))
story.append(subhead("Fail-safe defaults, summarised"))
story += bullets([
    "System disabled &rarr; battery active power commands to zero immediately, no stale "
    "dispatch commands held over.",
    "SOC at a protective limit &rarr; that direction (charge or discharge) is unavailable "
    "to every priority tier above idle, without exception.",
    "A demand peak the battery can't fully cover is reported honestly, not masked by "
    "reporting only what was achieved as if it were the whole target.",
])
story.append(PageBreak())

# ---- Chapter 9: Testing -----------------------------------------------------
story += chapter_head(9, "Testing, Commissioning &amp; FAT Procedures")
story.append(P(
    "The function block was validated against twelve functional test cases, anchored by "
    "a pair of tests proving the inverter capability-curve constraint is genuinely "
    "enforced rather than assumed. The full procedure is in "
    "<b>docs/Testing_Procedures.md</b>; the matrix is reproduced below.", body))
story.append(data_table(
    ["#", "Test Case", "Expected Result"],
    [
        ["1-3", "Peak shaving: engage, SOC floor, shortfall reporting", "Correct discharge, correct alarm behaviour in every case"],
        ["4-6", "Solar excess: charge battery, curtail, export", "Correct priority between charging, curtailment, and export"],
        ["7-8", "TOU arbitrage: on-peak discharge, off-peak charge", "Battery favoured over grid on-peak; charges toward target off-peak"],
        ["9", "Shoulder period idle", "No unnecessary cycling when there's no economic case to act"],
        ["10-11", "PF correction: ample headroom, constrained headroom", "Full correction when possible; honest clamping and alarm when not"],
        ["12", "System disable", "Immediate safe idle, no stale commands"],
    ],
    col_widths=[12 * mm, 66 * mm, AVAIL_W - 12 * mm - 66 * mm]))
story.append(Spacer(1, 10))
story += callout(
    "Why Test 11 is the one that actually proves something",
    "Any dispatch logic can look correct when reactive power has unlimited headroom to "
    "work with. Test 11 specifically forces a large simultaneous active power dispatch and "
    "confirms the reactive dispatch is clamped to what's genuinely left on the shared "
    "inverter rating - the difference between a plausible simulation and one that would "
    "actually respect real inverter hardware.", "warning")
story.append(PageBreak())

# ---- Chapter 10: Limitations -------------------------------------------------
story += chapter_head(10, "Limitations, Real-World Deltas &amp; Future Work")
story.append(P(
    "Naming the gap between a strong simulation and a certifiable interconnected power "
    "system is part of the engineering, consistent with every other project in this "
    "portfolio.", body))
story.append(subhead("What a real installation would add"))
story += bullets([
    "<b>Grid code compliance (e.g. IEEE 1547)</b> &mdash; anti-islanding protection, "
    "voltage/frequency ride-through, and formal utility interconnection approval this "
    "project makes no claim to.",
    "<b>Load and solar forecasting</b> &mdash; this project reacts to current conditions; "
    "a production system would forecast the coming peak to pre-position SOC ahead of it.",
    "<b>Protection coordination</b> &mdash; real breaker and relay coordination between "
    "the BESS, solar, and utility connection, well beyond this project's dispatch-only "
    "scope.",
    "<b>Multi-asset dispatch</b> &mdash; a real site may have multiple battery units or "
    "multiple solar arrays requiring their own internal load-sharing, not modelled here.",
])
story.append(subhead("10.1 &nbsp; Hazard &amp; safeguard register (HAZOP-style)"))
story.append(data_table(
    ["Hazard", "Cause", "Safeguard in This Design"],
    [
        ["Battery degradation from deep cycling", "Dispatch logic ignoring SOC limits under pressure",
         "SOC protection is priority 1, unconditionally, before any economic decision"],
        ["Inverter overload from P+Q dispatch", "Active and reactive power treated as independent",
         "Explicit shared capability-curve calculation (Chapter 5.3, 6.4)"],
        ["Uncontrolled export during an outage", "No anti-islanding logic modelled",
         "Named gap - a real system requires IEEE 1547 compliant anti-islanding protection"],
        ["Silent under-performance against demand charge target", "A shortfall reported as if fully corrected",
         "Alarm_DemandExceeded raised honestly whenever the battery can't fully cover a peak"],
    ],
    col_widths=[46 * mm, 52 * mm, AVAIL_W - 46 * mm - 52 * mm]))
story.append(Spacer(1, 8))
story.append(subhead("Where this project could go next"))
story += bullets([
    "Add a simple load-forecasting model to pre-position SOC ahead of an expected peak, "
    "rather than reacting only once the peak has already begun.",
    "Model anti-islanding protection and a formal IEEE 1547 compliance checklist.",
    "Extend to a second battery asset, demonstrating fleet-level dispatch coordination.",
])
story.append(PageBreak())


# ---- Appendix A: I/O Quick Reference ---------------------------------------
story += chapter_head("A", "Appendix A &mdash; I/O Quick Reference", "APPENDIX")
story.append(data_table(
    ["Tag", "Dir.", "Type", "Notes"],
    [
        ["Config", "IN", "ST_MicrogridConfig", "From SCADA"],
        ["AI_FactoryLoad_kW / SolarGeneration_kW", "IN", "REAL x2", "Site metering"],
        ["AI_BatterySOC_Pct", "IN", "REAL", "20-95% limits"],
        ["AI_ReactivePower_kVAR", "IN", "REAL", "PCC measurement"],
        ["AI_HourOfDay_Decimal", "IN", "REAL", "TOU schedule ref"],
        ["DI_NetMeteringAllowed", "IN", "BOOL", "Interconnection agreement"],
        ["DI_System_Enable", "IN", "BOOL", "Master enable"],
        ["AO_Battery_ActivePower_kW", "OUT", "REAL", "+discharge / -charge"],
        ["AO_Battery_ReactivePower_kVAR", "OUT", "REAL", "Shares S_rated with above"],
        ["AO_SolarCurtailment_Pct", "OUT", "REAL", "Last resort only"],
        ["BESS_Mode", "OUT", "ENUM", "6-mode dispatch state"],
        ["RatePeriod", "OUT", "ENUM", "TOU period"],
        ["Calculated_PF", "OUT", "REAL", "Site power factor"],
        ["Alarm_SOC_Low/High/DemandExceeded/PF_OutOfSpec", "OUT", "BOOL x4", "Process alarms"],
        ["SystemStatus", "OUT", "STRING", "HMI display"],
    ],
    col_widths=[68 * mm, 14 * mm, 34 * mm, AVAIL_W - 68 * mm - 14 * mm - 34 * mm]))
story.append(PageBreak())

# ---- Appendix B: Full ST Listing -------------------------------------------
story += chapter_head("B", "Appendix B &mdash; Full Structured Text Listing", "APPENDIX")
story.append(P("Complete, unedited listing of <b>src/Microgrid_BESS_Dispatch.st</b>.", body))

story += code_block(
"""(*
====================================================================================
  PROJECT   : Industrial Microgrid Controller
              Intelligent Battery Energy Storage System (BESS) Dispatch
  MODULE    : FB_Microgrid_BESS_Dispatch
  PLATFORM  : IEC 61131-3 Structured Text (Siemens SCL / CODESYS-portable)
  AUTHOR    : Sipho Lucky Sibanda
  See Chapter 5 for the dispatch priority and capability-curve discussion.
====================================================================================
*)

TYPE E_RatePeriod : (PERIOD_OFFPEAK, PERIOD_SHOULDER, PERIOD_ONPEAK); END_TYPE

TYPE E_BESS_Mode :
(
    MODE_IDLE, MODE_PEAK_SHAVE, MODE_ARBITRAGE_DISCHARGE,
    MODE_ARBITRAGE_CHARGE, MODE_SOLAR_CHARGE, MODE_PROTECT
);
END_TYPE

TYPE ST_MicrogridConfig :
STRUCT
    DemandThreshold_kW : REAL;
    OnPeak_Start_hr : REAL;         OnPeak_End_hr : REAL;
    OffPeak_Start_hr : REAL;          OffPeak_End_hr : REAL;
    Target_PF : REAL;
    Min_SOC_Pct : REAL;                 Max_SOC_Pct : REAL;
    Battery_Rated_kW : REAL;              Battery_Rated_kVA : REAL;
    Arbitrage_Charge_SOC_Target_Pct : REAL;
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_Microgrid_BESS_Dispatch
VAR_INPUT
    Config : ST_MicrogridConfig;
    AI_FactoryLoad_kW : REAL;         AI_SolarGeneration_kW : REAL;
    AI_BatterySOC_Pct : REAL;           AI_ReactivePower_kVAR : REAL;
    AI_HourOfDay_Decimal : REAL;
    DI_NetMeteringAllowed : BOOL;         DI_System_Enable : BOOL;
END_VAR""")

story += code_block(
"""VAR_OUTPUT
    AO_Battery_ActivePower_kW : REAL := 0.0;
    AO_Battery_ReactivePower_kVAR : REAL := 0.0;
    AO_SolarCurtailment_Pct : REAL := 0.0;
    BESS_Mode : E_BESS_Mode := MODE_IDLE;
    RatePeriod : E_RatePeriod := PERIOD_OFFPEAK;
    Calculated_PF : REAL := 1.0;
    Alarm_SOC_Low : BOOL := FALSE;              Alarm_SOC_High : BOOL := FALSE;
    Alarm_DemandExceeded : BOOL := FALSE;         Alarm_PF_OutOfSpec : BOOL := FALSE;
    SystemStatus : STRING[28] := 'STANDBY';
END_VAR

VAR
    NetLoad_kW : REAL;
    Available_Discharge_kW : REAL;      Available_Charge_kW : REAL;
    RequiredShave_kW : REAL;              GridImport_kW : REAL;
    Available_S_kVA : REAL;                 RequiredQ_kVAR : REAL;
    ActivePowerMagnitude_kW : REAL;
END_VAR

// 1. RATE PERIOD FROM TOU SCHEDULE
IF (AI_HourOfDay_Decimal >= Config.OnPeak_Start_hr) AND (AI_HourOfDay_Decimal < Config.OnPeak_End_hr) THEN
    RatePeriod := PERIOD_ONPEAK;
ELSIF (AI_HourOfDay_Decimal >= Config.OffPeak_Start_hr) OR (AI_HourOfDay_Decimal < Config.OffPeak_End_hr) THEN
    RatePeriod := PERIOD_OFFPEAK;
ELSE
    RatePeriod := PERIOD_SHOULDER;
END_IF

// 2. NET LOAD AND BATTERY HEADROOM
NetLoad_kW := AI_FactoryLoad_kW - AI_SolarGeneration_kW;
IF AI_BatterySOC_Pct > Config.Min_SOC_Pct THEN Available_Discharge_kW := Config.Battery_Rated_kW;
ELSE Available_Discharge_kW := 0.0; END_IF
IF AI_BatterySOC_Pct < Config.Max_SOC_Pct THEN Available_Charge_kW := Config.Battery_Rated_kW;
ELSE Available_Charge_kW := 0.0; END_IF
Alarm_SOC_Low  := AI_BatterySOC_Pct <= Config.Min_SOC_Pct;
Alarm_SOC_High := AI_BatterySOC_Pct >= Config.Max_SOC_Pct;""")

story += code_block(
"""// 3. ACTIVE POWER DISPATCH - FIXED PRIORITY ORDER
IF NOT DI_System_Enable THEN
    AO_Battery_ActivePower_kW := 0.0; BESS_Mode := MODE_IDLE;
ELSIF NetLoad_kW > Config.DemandThreshold_kW THEN
    RequiredShave_kW := NetLoad_kW - Config.DemandThreshold_kW;
    IF RequiredShave_kW <= Available_Discharge_kW THEN
        AO_Battery_ActivePower_kW := RequiredShave_kW; Alarm_DemandExceeded := FALSE;
    ELSE
        AO_Battery_ActivePower_kW := Available_Discharge_kW; Alarm_DemandExceeded := TRUE;
    END_IF
    BESS_Mode := MODE_PEAK_SHAVE;
ELSIF NetLoad_kW < 0.0 THEN
    Alarm_DemandExceeded := FALSE;
    IF Available_Charge_kW > 0.0 THEN
        AO_Battery_ActivePower_kW := MAX(NetLoad_kW, -Available_Charge_kW);
        BESS_Mode := MODE_SOLAR_CHARGE; AO_SolarCurtailment_Pct := 0.0;
    ELSIF NOT DI_NetMeteringAllowed THEN
        AO_Battery_ActivePower_kW := 0.0; BESS_Mode := MODE_PROTECT;
        AO_SolarCurtailment_Pct := 100.0 * (ABS(NetLoad_kW) / MAX(AI_SolarGeneration_kW, 0.1));
    ELSE
        AO_Battery_ActivePower_kW := 0.0; BESS_Mode := MODE_IDLE; AO_SolarCurtailment_Pct := 0.0;
    END_IF
ELSIF (RatePeriod = PERIOD_ONPEAK) AND (Available_Discharge_kW > 0.0) THEN
    AO_Battery_ActivePower_kW := MIN(NetLoad_kW, Available_Discharge_kW);
    BESS_Mode := MODE_ARBITRAGE_DISCHARGE; Alarm_DemandExceeded := FALSE;
ELSIF (RatePeriod = PERIOD_OFFPEAK) AND (AI_BatterySOC_Pct < Config.Arbitrage_Charge_SOC_Target_Pct)
      AND (Available_Charge_kW > 0.0) THEN
    AO_Battery_ActivePower_kW := -Available_Charge_kW;
    BESS_Mode := MODE_ARBITRAGE_CHARGE; Alarm_DemandExceeded := FALSE;
ELSE
    AO_Battery_ActivePower_kW := 0.0; BESS_Mode := MODE_IDLE; Alarm_DemandExceeded := FALSE;
END_IF
GridImport_kW := NetLoad_kW - AO_Battery_ActivePower_kW;""")

story += code_block(
"""// 4. REACTIVE POWER / POWER FACTOR CORRECTION
ActivePowerMagnitude_kW := ABS(AO_Battery_ActivePower_kW);
Available_S_kVA := SQRT(MAX(0.0, (Config.Battery_Rated_kVA * Config.Battery_Rated_kVA)
                                   - (ActivePowerMagnitude_kW * ActivePowerMagnitude_kW)));

IF ABS(AI_FactoryLoad_kW) > 0.01 THEN
    Calculated_PF := AI_FactoryLoad_kW
        / SQRT((AI_FactoryLoad_kW * AI_FactoryLoad_kW) + (AI_ReactivePower_kVAR * AI_ReactivePower_kVAR));
ELSE
    Calculated_PF := 1.0;
END_IF

IF Calculated_PF < Config.Target_PF THEN
    RequiredQ_kVAR := AI_ReactivePower_kVAR * (1.0 - (Calculated_PF / Config.Target_PF));
    IF RequiredQ_kVAR > Available_S_kVA THEN
        AO_Battery_ReactivePower_kVAR := Available_S_kVA;
    ELSE
        AO_Battery_ReactivePower_kVAR := RequiredQ_kVAR;
    END_IF
    Alarm_PF_OutOfSpec := (AO_Battery_ReactivePower_kVAR < RequiredQ_kVAR);
ELSE
    AO_Battery_ReactivePower_kVAR := 0.0; Alarm_PF_OutOfSpec := FALSE;
END_IF

// 5. STATUS TEXT
IF NOT DI_System_Enable THEN SystemStatus := 'STANDBY';
ELSIF Alarm_DemandExceeded THEN SystemStatus := 'PEAK SHAVE - CAPACITY LIMIT';
ELSE
    CASE BESS_Mode OF
        MODE_PEAK_SHAVE: SystemStatus := 'PEAK SHAVING ACTIVE';
        MODE_ARBITRAGE_DISCHARGE: SystemStatus := 'TOU ARBITRAGE - DISCHARGING';
        MODE_ARBITRAGE_CHARGE: SystemStatus := 'TOU ARBITRAGE - CHARGING';
        MODE_SOLAR_CHARGE: SystemStatus := 'CHARGING FROM EXCESS SOLAR';
        MODE_PROTECT: SystemStatus := 'SOLAR CURTAILED - BATTERY FULL';
        ELSE SystemStatus := 'IDLE';
    END_CASE
END_IF

END_FUNCTION_BLOCK""", "Listing B.1 &mdash; Complete FB_Microgrid_BESS_Dispatch source.")
story.append(PageBreak())

# ---- Appendix C: Glossary --------------------------------------------------
story += chapter_head("C", "Appendix C &mdash; Glossary", "APPENDIX")
story.append(data_table(
    ["Term", "Meaning"],
    [
        ["BESS", "Battery Energy Storage System"],
        ["Demand charge", "A utility bill component based on peak kW demand, not kWh consumed"],
        ["Peak shaving", "Using stored energy to reduce a billed demand peak"],
        ["TOU / arbitrage", "Time-of-Use tariff; charging cheap and discharging expensive periods"],
        ["PCC", "Point of Common Coupling &mdash; where generation, storage, and the grid meet the load"],
        ["Power factor (PF)", "P / sqrt(P^2 + Q^2) &mdash; a measure of how efficiently power is delivered"],
        ["Reactive power (kVAR)", "Non-working power associated with inductive/capacitive loads"],
        ["Four-quadrant inverter", "An inverter able to source/sink both active and reactive power"],
        ["SOC", "State of Charge &mdash; a battery's remaining energy as a percentage of capacity"],
        ["Net metering", "A utility arrangement allowing excess generation to be exported/credited"],
        ["IEEE 1547", "The standard governing grid interconnection of distributed energy resources"],
    ],
    col_widths=[38 * mm, AVAIL_W - 38 * mm]))
story.append(PageBreak())

# ---- About the Author -------------------------------------------------------
story += chapter_head("&mdash;", "About the Author", "CLOSING")
story.append(P(
    "<b>Sipho Lucky Sibanda</b> is an automation and controls engineer building a "
    "multi-disciplinary portfolio spanning marine systems, avionics, architectural "
    "technology, applied AI, biotechnology, electrical power systems, and industrial "
    "automation. This manual documents the fifth deliberate discipline shift in that "
    "portfolio, following the same documentation standard as every other project in the "
    "series: full logic, I/O documentation, a live HMI, functional test procedures, and "
    "an honest account of what separates a strong simulation from a certifiable "
    "production system.", lead))
story.append(P("Repository: <b>microgrid-bess-dispatch</b>", body))
story.append(Spacer(1, 20))
story.append(HRFlowable(width="40%", thickness=1, color=BLUEACC))
story.append(Spacer(1, 6))
story.append(P("End of document.", caption))

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
doc = SimpleDocTemplate(
    OUTFILE, pagesize=A4,
    leftMargin=MARGIN_L, rightMargin=MARGIN_R,
    topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOT,
    title="Industrial Microgrid Controller - Technical Manual",
    author=AUTHOR,
)
doc.build(story, onFirstPage=draw_cover, onLaterPages=draw_body)
print("Built:", OUTFILE)
