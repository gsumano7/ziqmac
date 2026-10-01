#!/usr/bin/env python3
"""
Technical drawing set for the interchangeable knitting-needle case.

Rev B: trifold clutch construction taken from the client's reference
photos (wrap-around strap with buckle and snap, interior pages sewn into
the bottom gusset, 1.5 cm elastic needle bands).  Every dimension comes
from the cardboard prototype (photos 1-5) unless a note on the sheet says
it is a proposal.  Units on the sheets are cm; page geometry is A3
landscape in mm.

Run:  python3 generate_drawings.py
Outputs sheets/*.svg and index.html (print-ready, A3 landscape).
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "sheets")
os.makedirs(OUT, exist_ok=True)

W, H = 420.0, 297.0          # A3 landscape, mm
M = 10.0                     # drawing border margin, mm
FONT = "Liberation Sans, Arial, Helvetica, sans-serif"
DATE = "2026-10-01"
REV = "B"
PROJECT = "INTERCHANGEABLE KNITTING NEEDLE CASE"
CLIENT = "gsumano7 / ziqmac"
TOTAL_SHEETS = 8

# --------------------------------------------------------------------------
# Design data (cm).  Slot widths are the prototype's values: 2.0 mm -> 0.6 cm
# rising 0.1 cm per size step to 10 mm -> 2.2 cm.
# --------------------------------------------------------------------------
SIZES_SMALL = [("2.0", 0.6), ("2.25", 0.7), ("2.5", 0.8), ("2.75", 0.9),
               ("3.0", 1.0), ("3.25", 1.1), ("3.5", 1.2), ("3.75", 1.3),
               ("4.0", 1.4), ("4.5", 1.5), ("5.0", 1.6)]
SIZES_LARGE10 = [("5.5", 1.7), ("6.0", 1.8), ("7.0", 1.9), ("8.0", 2.0),
                 ("9.0", 2.1), ("10.0", 2.2)]
SIZES_LARGE5 = SIZES_LARGE10[:4]
LAND = 0.5                   # stitch land between slots (prototype: "0.5 cm between typical")

# Outer shell (photo 1)
END_FLAP = 8.0
SIDE_WALL = 5.7
BASE_W, BASE_H = 21.0, 13.0
REAR_FLAP = 5.0
REAR_WALL = 6.5
FRONT_WALL = 6.0
LID_H = 12.7
SNAP_FROM_FOLD = 5.0         # end-flap snap, measured from the fold
SNAP_FROM_TOP = 6.5          # end-flap snap, measured along the 13 cm edge

PATTERN_W = END_FLAP + SIDE_WALL + BASE_W + SIDE_WALL + END_FLAP   # 48.4
PATTERN_H = REAR_FLAP + REAR_WALL + BASE_H + FRONT_WALL + LID_H    # 43.2

# Interior pages: 20.0 x 12.5 to clear the 21.0 x 13.0 back panel
PAGE_W, PAGE_H = 20.0, 12.5
HINGE_TAB = 1.5              # page hinge tab sewn into the bottom gusset
ELASTIC = 1.5                # client: 1.5 cm elastic sewn into the pages
STRAP_W = 3.0                # wrap-around strap (reference photos)
TONGUE = 10.5                # strap tongue beyond the top-flap edge
R = 1.0                      # corner radius on flaps and pages
SEAMS = (1.0, 2.2, 3.4, 4.6) # page hinge seams, from the back-panel fold, across the 6.0 gusset


def slot_layout(sizes, total_len, land=LAND, margin=None):
    """Return (margin, [(label, x0, x1), ...]) stacking slots along total_len."""
    body = sum(w for _, w in sizes) + land * (len(sizes) - 1)
    if margin is None:
        margin = (total_len - body) / 2.0
    x = margin
    out = []
    for lab, w in sizes:
        out.append((lab, x, x + w))
        x += w + land
    return margin, out


# --------------------------------------------------------------------------
# SVG sheet helper
# --------------------------------------------------------------------------
CSS = f"""
.cut{{stroke:#000;stroke-width:0.5;fill:none;stroke-linejoin:round}}
.fold{{stroke:#000;stroke-width:0.35;stroke-dasharray:3,1.5;fill:none}}
.stitch{{stroke:#000;stroke-width:0.3;stroke-dasharray:1.2,0.8;fill:none}}
.hid{{stroke:#000;stroke-width:0.3;stroke-dasharray:4,1,1,1;fill:none}}
.thin{{stroke:#000;stroke-width:0.25;fill:none}}
.dim{{stroke:#000;stroke-width:0.2;fill:none}}
.cl{{stroke:#000;stroke-width:0.2;stroke-dasharray:8,1.5,1.5,1.5;fill:none}}
.leather{{fill:#efe6d6;stroke:#000;stroke-width:0.5}}
.band{{fill:#d9c9a8;stroke:#000;stroke-width:0.35}}
.strap{{fill:#a9876a;stroke:#000;stroke-width:0.4}}
.brass{{fill:#c9a85c;stroke:#000;stroke-width:0.3}}
.elastic{{fill:#d8ccb4;stroke:#000;stroke-width:0.35}}
.mesh{{fill:#e4e9ee;stroke:#000;stroke-width:0.35}}
.needle{{fill:#9aa3ab;stroke:#000;stroke-width:0.15}}
.hatch{{fill:url(#h45)}}
.t{{font-family:{FONT};font-size:3px;fill:#000}}
.ts{{font-family:{FONT};font-size:2.4px;fill:#000}}
.tb{{font-family:{FONT};font-size:3px;font-weight:bold;fill:#000}}
.tt{{font-family:{FONT};font-size:5px;font-weight:bold;fill:#000}}
.tx{{font-family:{FONT};font-size:2.1px;fill:#000}}
.wh{{fill:#fff;stroke:none}}
"""

DEFS = """
<defs>
 <marker id="ar" viewBox="0 0 10 10" refX="10" refY="5" markerUnits="userSpaceOnUse"
   markerWidth="3" markerHeight="3" orient="auto-start-reverse">
   <path d="M0,1.5 L10,5 L0,8.5 z" fill="#000"/>
 </marker>
 <marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse"
   markerWidth="2" markerHeight="2"><circle cx="5" cy="5" r="4" fill="#000"/></marker>
 <pattern id="h45" patternUnits="userSpaceOnUse" width="2" height="2" patternTransform="rotate(45)">
   <line x1="0" y1="0" x2="0" y2="2" stroke="#000" stroke-width="0.15"/>
 </pattern>
</defs>
"""


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def fmt(v):
    """cm value -> short string."""
    s = f"{v:.2f}"
    if s.endswith("0"):
        s = s[:-1]
    return s


class Sheet:
    def __init__(self, n, title, scale):
        self.n, self.title, self.scale = n, title, scale
        self.p = []

    # primitives (page mm) ------------------------------------------------
    def add(self, s):
        self.p.append(s)

    def line(self, x1, y1, x2, y2, cls="cut", extra=""):
        self.add(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" class="{cls}" {extra}/>')

    def rect(self, x, y, w, h, cls="cut", rx=0):
        self.add(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" rx="{rx}" class="{cls}"/>')

    def circle(self, x, y, r, cls="thin"):
        self.add(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" class="{cls}"/>')

    def poly(self, pts, cls="cut", close=True):
        d = "M" + " L".join(f"{x:.3f},{y:.3f}" for x, y in pts) + (" Z" if close else "")
        self.add(f'<path d="{d}" class="{cls}"/>')

    def text(self, x, y, s, cls="t", anchor="start", rot=0):
        tr = f' transform="rotate({rot} {x:.3f} {y:.3f})"' if rot else ""
        self.add(f'<text x="{x:.3f}" y="{y:.3f}" class="{cls}" text-anchor="{anchor}"{tr}>{esc(s)}</text>')

    def lines(self, x, y, items, cls="t", lh=4.2):
        for i, s in enumerate(items):
            if s.startswith("**"):
                self.text(x, y + i * lh, s[2:], "tb")
            else:
                self.text(x, y + i * lh, s, cls)

    # dimensions ---------------------------------------------------------
    def dim_h(self, x1, x2, yf, yd, label, ext=True, textpos="above"):
        """Horizontal dimension between page x1,x2 of a feature at yf, line at yd."""
        if x1 > x2:
            x1, x2 = x2, x1
        if ext:
            o = 1.2 if yd > yf else -1.2
            g = 0.8 if yd > yf else -0.8
            self.line(x1, yf + g, x1, yd + o, "dim")
            self.line(x2, yf + g, x2, yd + o, "dim")
        L = x2 - x1
        if L >= 7:
            self.line(x1, yd, x2, yd, "dim", 'marker-start="url(#ar)" marker-end="url(#ar)"')
        else:  # arrows outside
            self.line(x1 - 5, yd, x1, yd, "dim", 'marker-end="url(#ar)"')
            self.line(x2, yd, x2 + 5, yd, "dim", 'marker-start="url(#ar)"')
        ty = yd - 0.9 if textpos == "above" else yd + 3.2
        self.text((x1 + x2) / 2, ty, label, "t", "middle")

    def dim_v(self, y1, y2, xf, xd, label, ext=True, textpos="left"):
        if y1 > y2:
            y1, y2 = y2, y1
        if ext:
            o = 1.2 if xd > xf else -1.2
            g = 0.8 if xd > xf else -0.8
            self.line(xf + g, y1, xd + o, y1, "dim")
            self.line(xf + g, y2, xd + o, y2, "dim")
        L = y2 - y1
        if L >= 7:
            self.line(xd, y1, xd, y2, "dim", 'marker-start="url(#ar)" marker-end="url(#ar)"')
        else:
            self.line(xd, y1 - 5, xd, y1, "dim", 'marker-end="url(#ar)"')
            self.line(xd, y2, xd, y2 + 5, "dim", 'marker-start="url(#ar)"')
        tx = xd - 0.9 if textpos == "left" else xd + 3.2
        self.text(tx, (y1 + y2) / 2, label, "t", "middle", rot=-90)

    def leader(self, x1, y1, x2, y2, label, cls="t", anchor="start"):
        self.line(x1, y1, x2, y2, "dim", 'marker-start="url(#dot)"')
        self.text(x2 + (0.8 if anchor == "start" else -0.8), y2 + 1, label, cls, anchor)

    def snap_cap(self, x, y, r=3.0, label=None):
        self.circle(x, y, r, "thin")
        self.circle(x, y, r * 0.55, "thin")
        self.line(x - r * 1.4, y, x + r * 1.4, y, "cl")
        self.line(x, y - r * 1.4, x, y + r * 1.4, "cl")
        if label:
            self.text(x + r + 1, y + 1, label, "ts")

    def snap_stud(self, x, y, r=3.0, label=None):
        self.circle(x, y, r, "hid")
        self.circle(x, y, r * 0.3, "thin")
        self.line(x - r * 1.4, y, x + r * 1.4, y, "cl")
        self.line(x, y - r * 1.4, x, y + r * 1.4, "cl")
        if label:
            self.text(x + r + 1, y + 1, label, "ts")

    def table(self, x, y, cols, rows, widths, rh=4.6, head_cls="tb", cls="ts"):
        """Simple ruled table.  cols: header strings, widths: mm."""
        tw = sum(widths)
        n = len(rows) + 1
        self.rect(x, y, tw, rh * n, "thin")
        self.line(x, y + rh, x + tw, y + rh, "thin")
        cx = x
        for i, w in enumerate(widths):
            if i:
                self.line(cx, y, cx, y + rh * n, "thin")
            self.text(cx + 1.2, y + rh * 0.72, cols[i], head_cls)
            cx += w
        for r, row in enumerate(rows):
            yy = y + rh * (r + 1)
            if r:
                self.line(x, yy, x + tw, yy, "dim")
            cx = x
            for i, w in enumerate(widths):
                self.text(cx + 1.2, yy + rh * 0.72, row[i], cls)
                cx += w
        return y + rh * n

    # frame --------------------------------------------------------------
    def frame(self):
        self.rect(M, M, W - 2 * M, H - 2 * M, "cut")
        # title block, bottom right
        tbw, tbh = 200.0, 30.0
        x0, y0 = W - M - tbw, H - M - tbh
        self.rect(x0, y0, tbw, tbh, "cut")
        self.line(x0, y0 + 10, x0 + tbw, y0 + 10, "thin")
        self.line(x0, y0 + 20, x0 + tbw, y0 + 20, "thin")
        self.line(x0 + 120, y0, x0 + 120, y0 + tbh, "thin")
        self.line(x0 + 160, y0 + 10, x0 + 160, y0 + tbh, "thin")
        self.text(x0 + 2, y0 + 3.2, "PROJECT", "tx")
        self.text(x0 + 2, y0 + 7.8, PROJECT, "tb")
        self.text(x0 + 122, y0 + 3.2, "CLIENT", "tx")
        self.text(x0 + 122, y0 + 7.8, CLIENT, "t")
        self.text(x0 + 2, y0 + 13.2, "SHEET TITLE", "tx")
        self.text(x0 + 2, y0 + 17.8, self.title, "tb")
        self.text(x0 + 122, y0 + 13.2, "SCALE", "tx")
        self.text(x0 + 122, y0 + 17.8, self.scale, "t")
        self.text(x0 + 162, y0 + 13.2, "UNITS", "tx")
        self.text(x0 + 162, y0 + 17.8, "cm (page A3)", "t")
        self.text(x0 + 2, y0 + 23.2, "SOURCE", "tx")
        self.text(x0 + 2, y0 + 27.8, "Cardboard prototype (photos 1-5) + client reference photos (Rev B)", "t")
        self.text(x0 + 122, y0 + 23.2, "DATE / REV", "tx")
        self.text(x0 + 122, y0 + 27.8, f"{DATE}   Rev {REV}", "t")
        self.text(x0 + 162, y0 + 23.2, "SHEET", "tx")
        self.text(x0 + 162, y0 + 27.8, f"{self.n} of {TOTAL_SHEETS}", "tb")
        # sheet heading, top left
        self.text(M + 3, M + 7, f"SHEET {self.n}  -  {self.title.upper()}", "tt")

    def svg(self):
        body = "\n".join(self.p)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" '
                f'viewBox="0 0 {W} {H}" font-family="{FONT}">\n<style>{CSS}</style>{DEFS}'
                f'<rect width="{W}" height="{H}" fill="#fff"/>\n{body}\n</svg>\n')


class View:
    """Maps model cm -> page mm."""

    def __init__(self, ox, oy, s):
        self.ox, self.oy, self.s = ox, oy, s

    def X(self, x):
        return self.ox + x * self.s

    def Y(self, y):
        return self.oy + y * self.s

    def L(self, v):
        return v * self.s


def draw_needle_pair(sh, v, x0, x1, ytop, length, dia, point_up=True):
    """Two tips side by side inside slot x0..x1 (model cm), lying along y."""
    cx = (x0 + x1) / 2
    for side in (-1, 1):
        c = cx + side * (dia / 2 + 0.03)
        xl, xr = v.X(c - dia / 2), v.X(c + dia / 2)
        if point_up:
            yt, yb = v.Y(ytop), v.Y(ytop + length)
            tip = v.Y(ytop + min(1.6, length * 0.3))
            pts = [(v.X(c), yt), (xr, tip), (xr, yb), (xl, yb), (xl, tip)]
        else:
            yt, yb = v.Y(ytop), v.Y(ytop + length)
            tip = v.Y(ytop + length - min(1.6, length * 0.3))
            pts = [(xl, yt), (xr, yt), (xr, tip), (v.X(c), yb), (xl, tip)]
        sh.poly(pts, "needle")


def draw_slot_strip(sh, v, slots, y0, y1, labels=True, label_y=None, band_cls="band"):
    """Band from y0..y1 (model) covering slots; stitch lines at each slot edge."""
    xa, xb = slots[0][1], slots[-1][2]
    sh.rect(v.X(xa) - 0.001, v.Y(y0), v.L(xb - xa), v.L(y1 - y0), band_cls)
    for lab, a, b in slots:
        for x in (a, b):
            sh.line(v.X(x), v.Y(y0) - 0.6, v.X(x), v.Y(y1) + 0.6, "stitch")
        if labels:
            ly = v.Y(label_y) if label_y is not None else v.Y((y0 + y1) / 2)
            sh.text(v.X((a + b) / 2) + 0.8, ly, lab, "tx", "middle", rot=-90)


def band_detail(sh, x, y, label="DETAIL A - slot band section, 2:1"):
    """Section through band with two needles side by side."""
    v = View(x, y, 20.0)   # 2:1 (20 mm per cm)
    X, Y, L = v.X, v.Y, v.L
    sh.text(X(0), Y(0) - 3, label, "tb")
    # panel (board + lining) 0.25 thick, band over it, two needles d=0.5 in a 1.6 slot
    sh.rect(X(0), Y(1.2), L(4.0), L(0.25), "hatch")
    sh.rect(X(0), Y(1.2), L(4.0), L(0.25), "thin")
    # neighbouring slot lands
    land = LAND
    slot = 1.6
    xa = 0.7
    d = 0.5
    # band path: flat on land, arcs over needles
    pts = [(X(0.2), Y(1.2))]
    pts.append((X(xa), Y(1.2)))
    # arch over two needles
    n = 24
    for i in range(n + 1):
        t = i / n
        xx = xa + t * slot
        yy = 1.2 - math.sin(t * math.pi) * (d + 0.05)
        pts.append((X(xx), Y(yy)))
    pts.append((X(xa + slot + land), Y(1.2)))
    pts.append((X(3.8), Y(1.2)))
    sh.poly(pts, "cut", close=False)
    # needles
    for cx in (xa + slot / 2 - d / 2 - 0.02, xa + slot / 2 + d / 2 + 0.02):
        sh.circle(X(cx), Y(1.2 - d / 2), L(d / 2), "needle")
    # stitch marks
    for xx in (xa, xa + slot, xa + slot + land, 0.2):
        sh.line(X(xx), Y(1.1), X(xx), Y(1.5), "stitch")
    sh.dim_h(X(xa), X(xa + slot), Y(1.45), Y(1.45) + 8, "slot width w (table)")
    sh.dim_h(X(xa + slot), X(xa + slot + land), Y(1.45), Y(1.45) + 8, "0.5", ext=False)
    sh.text(X(xa + slot + land / 2), Y(1.45) + 11.5, "land", "tx", "middle")
    sh.dim_v(Y(1.2 - d), Y(1.2), X(xa + slot + 0.1), X(xa + slot) + 14, "d")
    sh.leader(X(xa + slot / 2), Y(0.6), X(xa + slot / 2) + 10, Y(0.2), "2 tips side by side (1 pair), under 15 mm elastic")
    sh.leader(X(0.35), Y(1.33), X(0.35) - 1, Y(1.33) + 14, "page: 2 ply + 0.8 board", anchor="start")
    sh.leader(X(xa + slot + land / 2), Y(1.2), X(xa + slot + land / 2) + 6, Y(1.9) + 4, "double stitch line, 0.5 apart")


def slot_table(sh, x, y, slots, sizes, tips_len, extra_note=None):
    rows = []
    for i, ((lab, w), (_, a, b)) in enumerate(zip(sizes, slots)):
        rows.append([str(i + 1), f"{lab} mm", fmt(w), fmt(a), fmt(b), f"2 x {tips_len} cm"])
    end = sh.table(x, y, ["#", "Size", "Slot w", "From", "To", "Holds"], rows, [8, 18, 15, 15, 15, 24], rh=4.2)
    return end



# ==========================================================================
# Shared drawing pieces
# ==========================================================================
def rounded_rect_path(X, Y, L, x, y, w, h, r, corners=(1, 1, 1, 1)):
    """SVG path for a rect (model cm) with optional rounded corners (tl,tr,br,bl)."""
    tl, tr, br, bl = corners
    p = f"M{X(x + (r if tl else 0)):.3f},{Y(y):.3f} "
    p += f"L{X(x + w - (r if tr else 0)):.3f},{Y(y):.3f} "
    if tr:
        p += f"A{L(r):.3f},{L(r):.3f} 0 0 1 {X(x + w):.3f},{Y(y + r):.3f} "
    p += f"L{X(x + w):.3f},{Y(y + h - (r if br else 0)):.3f} "
    if br:
        p += f"A{L(r):.3f},{L(r):.3f} 0 0 1 {X(x + w - r):.3f},{Y(y + h):.3f} "
    p += f"L{X(x + (r if bl else 0)):.3f},{Y(y + h):.3f} "
    if bl:
        p += f"A{L(r):.3f},{L(r):.3f} 0 0 1 {X(x):.3f},{Y(y + h - r):.3f} "
    p += f"L{X(x):.3f},{Y(y + (r if tl else 0)):.3f} "
    if tl:
        p += f"A{L(r):.3f},{L(r):.3f} 0 0 1 {X(x + r):.3f},{Y(y):.3f} "
    return p + "Z"


def buckle(sh, cx, cy, w, cls_scale=1.0):
    """Simple buckle + prong symbol centred at page (cx, cy), frame width w mm."""
    hgt = w * 0.42
    sh.rect(cx - w / 2, cy - hgt / 2, w, hgt, "brass", rx=0.6)
    sh.rect(cx - w / 2 + 1.0, cy - hgt / 2 + 1.0, w - 2.0, hgt - 2.0, "thin")
    sh.line(cx, cy - hgt / 2, cx, cy + hgt / 2 + 1.5, "cut")       # prong


def size_labels(sh, v, slots, y_text, y_tip):
    """'2.0 / mm' label above each slot with a leader to the tip."""
    for lab, a, b in slots:
        cx = (a + b) / 2
        sh.text(v.X(cx), v.Y(y_text), lab, "tx", "middle")
        sh.text(v.X(cx), v.Y(y_text) + 2.4, "mm", "tx", "middle")
        sh.line(v.X(cx), v.Y(y_text) + 3.2, v.X(cx), v.Y(y_tip) - 0.8, "dim")


def draw_page(sh, v, sizes, tip_len, tip_top, band_c, margin=None, x_offset=0.0, zone_w=None):
    """Page outline + hinge tab + needles + 1.5 elastic.  Returns (margin, slots)."""
    X, Y, L = v.X, v.Y, v.L
    zone_w = PAGE_W if zone_w is None else zone_w
    margin, slots = slot_layout(sizes, zone_w, margin=margin)
    slots = [(lab, a + x_offset, b + x_offset) for lab, a, b in slots]
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, 0, 0, PAGE_W, PAGE_H, R, (1, 1, 0, 0))}" class="leather"/>')
    # hinge tab below the page
    sh.rect(X(1.0), Y(PAGE_H), L(PAGE_W - 2.0), L(HINGE_TAB), "hatch")
    sh.rect(X(1.0), Y(PAGE_H), L(PAGE_W - 2.0), L(HINGE_TAB), "thin")
    sh.line(X(0), Y(PAGE_H), X(PAGE_W), Y(PAGE_H), "fold")
    # edge stitch 0.3 in
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, 0.3, 0.3, PAGE_W - 0.6, PAGE_H - 0.6, R - 0.3, (1, 1, 0, 0))}" class="stitch"/>')
    for lab, a, b in slots:
        draw_needle_pair(sh, v, a, b, tip_top, tip_len, float(lab) / 10.0)
    y0, y1 = band_c - ELASTIC / 2, band_c + ELASTIC / 2
    draw_slot_strip(sh, v, slots, y0, y1, labels=False, band_cls="elastic")
    size_labels(sh, v, slots, tip_top - 1.0, tip_top)
    return margin, slots


def page_dims(sh, v, slots, margin, tip_len, tip_top, band_c, x_offset=0.0, zone_w=None, overall_off=8):
    X, Y, L = v.X, v.Y, v.L
    zone_w = PAGE_W if zone_w is None else zone_w
    y0, y1 = band_c - ELASTIC / 2, band_c + ELASTIC / 2
    xl = X(0) - 7
    sh.dim_v(Y(0), Y(tip_top), X(0), xl, fmt(tip_top))
    sh.dim_v(Y(tip_top), Y(tip_top + tip_len), X(0), xl, f"{fmt(tip_len)} tip")
    sh.dim_v(Y(tip_top + tip_len), Y(PAGE_H), X(0), xl, fmt(PAGE_H - tip_top - tip_len))
    sh.dim_v(Y(0), Y(PAGE_H), X(0), xl - overall_off, fmt(PAGE_H))
    sh.dim_v(Y(PAGE_H), Y(PAGE_H + HINGE_TAB), X(0), xl, fmt(HINGE_TAB))
    xr = X(PAGE_W) + 7
    sh.dim_v(Y(0), Y(y0), X(PAGE_W), xr, fmt(y0))
    sh.dim_v(Y(y0), Y(y1), X(PAGE_W), xr, f"{fmt(ELASTIC)} elastic")
    yb = Y(PAGE_H + HINGE_TAB) + 8
    sh.dim_h(X(x_offset), X(slots[0][1]), Y(PAGE_H + HINGE_TAB), yb, fmt(margin))
    sh.dim_h(X(slots[-1][2]), X(x_offset + zone_w), Y(PAGE_H + HINGE_TAB), yb, fmt(x_offset + zone_w - slots[-1][2]))
    sh.dim_h(X(slots[0][1]), X(slots[-1][2]), Y(PAGE_H + HINGE_TAB), yb, f"{fmt(slots[-1][2] - slots[0][1])} elastic strip")
    sh.dim_h(X(0), X(PAGE_W), Y(PAGE_H + HINGE_TAB), yb + 8, fmt(PAGE_W))
    # ordinate above the page
    yo = Y(0) - 8
    sh.line(X(0), yo, X(PAGE_W), yo, "dim")
    sh.text(X(0), yo - 11, "ORDINATE: elastic stitch-line positions from left page edge (cm)", "tx")
    sh.line(X(0), yo - 2.5, X(0), yo + 2.5, "dim")
    sh.text(X(0), yo - 1.2, "0", "tx", "middle")
    for lab, a, b in slots:
        for x in (a, b):
            sh.line(X(x), yo - 1.5, X(x), Y(0), "dim")
            sh.text(X(x) + 0.7, yo - 2.2, fmt(x), "tx", "start", rot=-90)
    sh.line(X(PAGE_W), yo - 2.5, X(PAGE_W), yo + 2.5, "dim")


def page_notes():
    return [
        "**PAGE CONSTRUCTION (all four pages)",
        "1. Page = 2 plies faux leather 1.0 mm over 0.8 mm board",
        "   stiffener, 20.0 x 12.5, R 1.0 top corners, edge-stitched",
        "   0.3 in contrast thread (as reference photos).",
        "2. Elastic: 15 mm knit elastic in matching colour, laid",
        "   flat and stitched on every line shown. Slot widths are",
        "   the prototype's: 0.6 for 2.0 mm, +0.1 per size step, to",
        "   2.2 for 10 mm. One slot holds one PAIR, side by side.",
        "3. Stitch lines in pairs 0.5 apart between slots (the",
        "   'land'); bar-tack both ends of each line.",
        "4. Size labels heat-stamped / printed above each slot",
        "   with a 0.5 leader line to the tip (reference photo).",
        "5. Hinge tab 1.5 below the page is sewn into the bottom",
        "   gusset - pages are not removable (sheet 7, detail C).",
        "6. Tip points up; 1.5 clear above the points (prototype).",
    ]


# ==========================================================================
# SHEET 1 - outer shell flat pattern (outer face up)
# ==========================================================================
def sheet1():
    sh = Sheet(1, "Outer shell - flat pattern, outer face (die line)", "1:2")
    sh.frame()
    s = 5.0
    v = View(28, 40, s)
    X, Y, L = v.X, v.Y, v.L
    xa = END_FLAP
    xb = END_FLAP + SIDE_WALL
    xc = xb + BASE_W
    xd = xc + SIDE_WALL
    ya = REAR_FLAP
    yb = ya + REAR_WALL
    yc = yb + BASE_H
    yd = yc + FRONT_WALL

    # fills
    sh.rect(X(xb), Y(0), L(BASE_W), L(PATTERN_H), "leather")
    sh.rect(X(0), Y(yb), L(PATTERN_W), L(BASE_H), "leather")
    # perimeter with rounded free corners
    r = R
    per = (f"M{X(xb):.3f},{Y(r):.3f} A{L(r)},{L(r)} 0 0 1 {X(xb + r):.3f},{Y(0):.3f} "
           f"L{X(xc - r):.3f},{Y(0):.3f} A{L(r)},{L(r)} 0 0 1 {X(xc):.3f},{Y(r):.3f} "
           f"L{X(xc):.3f},{Y(yb):.3f} L{X(PATTERN_W - r):.3f},{Y(yb):.3f} A{L(r)},{L(r)} 0 0 1 {X(PATTERN_W):.3f},{Y(yb + r):.3f} "
           f"L{X(PATTERN_W):.3f},{Y(yc - r):.3f} A{L(r)},{L(r)} 0 0 1 {X(PATTERN_W - r):.3f},{Y(yc):.3f} "
           f"L{X(xc):.3f},{Y(yc):.3f} L{X(xc):.3f},{Y(PATTERN_H - r):.3f} A{L(r)},{L(r)} 0 0 1 {X(xc - r):.3f},{Y(PATTERN_H):.3f} "
           f"L{X(xb + r):.3f},{Y(PATTERN_H):.3f} A{L(r)},{L(r)} 0 0 1 {X(xb):.3f},{Y(PATTERN_H - r):.3f} "
           f"L{X(xb):.3f},{Y(yc):.3f} L{X(r):.3f},{Y(yc):.3f} A{L(r)},{L(r)} 0 0 1 {X(0):.3f},{Y(yc - r):.3f} "
           f"L{X(0):.3f},{Y(yb + r):.3f} A{L(r)},{L(r)} 0 0 1 {X(r):.3f},{Y(yb):.3f} "
           f"L{X(xb):.3f},{Y(yb):.3f} Z")
    sh.add(f'<path d="{per}" class="cut"/>')
    for yy in (ya, yb, yc, yd):
        sh.line(X(xb), Y(yy), X(xc), Y(yy), "fold")
    for xx in (xa, xb, xc, xd):
        sh.line(X(xx), Y(yb), X(xx), Y(yc), "fold")

    # strap (stitched part): back panel + top gusset + top flap, centred
    cx = xb + BASE_W / 2
    sh.rect(X(cx - STRAP_W / 2), Y(0), L(STRAP_W), L(yc), "strap")
    sh.rect(X(cx - STRAP_W / 2 + 0.3), Y(0.3), L(STRAP_W - 0.6), L(yc - 0.6), "stitch")
    sh.text(X(cx) + 10, Y(yb + 9.0), "STRAP 3.0 wide, dark brown, stitched 0.3 from edges", "ts", "middle", rot=-90)
    buckle(sh, X(cx), Y(2.6), L(STRAP_W + 0.6))
    sh.rect(X(cx - STRAP_W / 2 - 0.2), Y(3.9), L(STRAP_W + 0.4), L(0.7), "strap")   # keeper
    sh.text(X(cx) + 11, Y(2.9), "buckle 30 mm", "tx")
    sh.text(X(cx) + 11, Y(4.6), "keeper", "tx")
    sh.text(X(cx), Y(0) - 1.5, "tongue continues 10.5 beyond this edge - sheet 7", "tx", "middle")
    # logo emboss on top flap
    lx, ly = xc - 3.0, 2.5
    sh.rect(X(lx - 1.25), Y(ly - 1.25), L(2.5), L(2.5), "thin")
    sh.text(X(lx), Y(ly) + 1, "LOGO", "tx", "middle")
    sh.text(X(lx), Y(ly) + 3.3, "emboss 2.5 sq", "tx", "middle")

    # labels
    def lab(x, y, a, b=None):
        sh.text(X(x), Y(y), a, "tb", "middle")
        if b:
            sh.text(X(x), Y(y) + 4, b, "ts", "middle")
    lab(xb + 4.5, REAR_FLAP / 2 + 0.3, "TOP FLAP", "21.0 x 5.0")
    lab(xb + 4.5, ya + REAR_WALL / 2 + 0.3, "TOP GUSSET", "21.0 x 6.5")
    lab(xb + 4.5, yb + BASE_H / 2 - 0.3, "BACK PANEL", "21.0 x 13.0 (pages inside)")
    lab(cx, yc + FRONT_WALL / 2 + 0.3, "BOTTOM GUSSET - page hinge seams inside", "21.0 x 6.0")
    lab(cx, yd + 3.0, "FRONT PANEL", "21.0 x 12.7")
    sh.text(X(xa + SIDE_WALL / 2) + 1.2, Y(yb + 1.2), "SIDE GUSSET 5.7 x 13.0", "ts", "end", rot=-90)
    sh.text(X(xc + SIDE_WALL / 2) + 1.2, Y(yb + 1.2), "SIDE GUSSET 5.7 x 13.0", "ts", "end", rot=-90)
    lab(END_FLAP / 2, yb + 2.2, "SIDE FLAP (L)", "8.0 x 13.0 - tucks inside")
    lab(xd + END_FLAP / 2, yb + 2.2, "SIDE FLAP (R)", "8.0 x 13.0 - tucks inside")

    # side-flap snap studs (outer face) + sockets on front panel inner face (hidden)
    sxl, sxr, sy = xa - SNAP_FROM_FOLD, xd + SNAP_FROM_FOLD, yb + SNAP_FROM_TOP
    sh.snap_cap(X(sxl), Y(sy), 3.0)
    sh.snap_cap(X(sxr), Y(sy), 3.0)
    sh.text(X(sxl), Y(sy) + 7.5, "SNAP STUD (outer face)", "tx", "middle")
    sh.text(X(sxr), Y(sy) + 7.5, "SNAP STUD (outer face)", "tx", "middle")
    sock_y = yd + SNAP_FROM_TOP
    for sx in (xb + SNAP_FROM_FOLD, xc - SNAP_FROM_FOLD):
        sh.snap_stud(X(sx), Y(sock_y), 3.0)
    sh.text(X(xb + SNAP_FROM_FOLD), Y(sock_y) + 7.5, "SOCKET x2, inner face (hidden)", "tx", "middle")
    sh.text(X(xc - SNAP_FROM_FOLD), Y(sock_y) + 7.5, "SOCKET x2, inner face (hidden)", "tx", "middle")
    # strap stud on front panel outer face
    st_y = PATTERN_H - 8.0
    sh.snap_cap(X(cx), Y(st_y), 3.0)
    sh.text(X(cx), Y(st_y) + 7.5, "STRAP STUD (outer face)", "tx", "middle")

    # dimensions
    yt = Y(0) - 9
    segs = [(0, xa, "8.0"), (xa, xb, "5.7"), (xb, xc, "21.0"), (xc, xd, "5.7"), (xd, PATTERN_W, "8.0")]
    for a, b, t in segs:
        sh.dim_h(X(a), X(b), Y(yb) if (a < xb or b > xc) else Y(0), yt, t)
    sh.dim_h(X(0), X(PATTERN_W), Y(yb), yt - 8, fmt(PATTERN_W) + "  OVERALL")
    xr = X(PATTERN_W) + 8
    vsegs = [(0, ya, "5.0"), (ya, yb, "6.5"), (yb, yc, "13.0"), (yc, yd, "6.0"), (yd, PATTERN_H, "12.7")]
    for a, b, t in vsegs:
        sh.dim_v(Y(a), Y(b), X(PATTERN_W) if (a >= yb and b <= yc) else X(xc), xr, t)
    sh.dim_v(Y(0), Y(PATTERN_H), X(PATTERN_W), xr + 8, fmt(PATTERN_H) + "  OVERALL")
    sh.dim_h(X(sxl), X(xa), Y(sy), Y(yc) + 5, "5.0")
    sh.dim_v(Y(yb), Y(sy), X(sxl), X(0) - 5, "6.5")
    sh.text(X(0), Y(yc) + 12, "(R) side flap: snap position symmetrical", "tx")
    sh.dim_h(X(xb), X(xb + SNAP_FROM_FOLD), Y(sock_y), Y(PATTERN_H) + 5, "5.0")
    sh.dim_h(X(xc - SNAP_FROM_FOLD), X(xc), Y(sock_y), Y(PATTERN_H) + 5, "5.0")
    sh.dim_v(Y(yd), Y(sock_y), X(xb), X(xb) - 5, "6.5")
    sh.dim_v(Y(st_y), Y(PATTERN_H), X(cx), X(xc) + 8, "8.0")
    sh.dim_h(X(cx - STRAP_W / 2), X(cx + STRAP_W / 2), Y(yb + 1), Y(yb) - 4, "3.0", ext=False)
    gx, gy = X(xb) - 14, Y(yd + 2)
    sh.line(gx, gy + 30, gx, gy, "thin", 'marker-end="url(#ar)"')
    sh.line(gx, gy, gx, gy + 30, "thin", 'marker-end="url(#ar)"')
    sh.text(gx - 1.5, gy + 15, "GRAIN / NAP", "tx", "middle", rot=-90)
    sh.text(X(xb + 1.0), Y(PATTERN_H) - 2, "all free corners R 1.0; edge-stitch 0.3 all round", "tx")

    nx, ny = 288, 22
    sh.text(nx, ny, "LEGEND", "tb")
    sh.line(nx, ny + 5, nx + 14, ny + 5, "cut"); sh.text(nx + 17, ny + 6, "Cut line (net finished size)", "ts")
    sh.line(nx, ny + 10, nx + 14, ny + 10, "fold"); sh.text(nx + 17, ny + 11, "Fold / score line", "ts")
    sh.line(nx, ny + 15, nx + 14, ny + 15, "hid"); sh.text(nx + 17, ny + 16, "Hidden (feature on far face)", "ts")
    sh.line(nx, ny + 20, nx + 14, ny + 20, "stitch"); sh.text(nx + 17, ny + 21, "Stitch line", "ts")
    sh.snap_cap(nx + 7, ny + 28, 2.2); sh.text(nx + 17, ny + 29, "Snap on this face", "ts")
    sh.snap_stud(nx + 7, ny + 36, 2.2); sh.text(nx + 17, ny + 37, "Snap on far face", "ts")
    sh.lines(nx, ny + 46, [
        "**NOTES",
        "1. All dimensions in cm, finished (net) sizes as measured",
        "   on the cardboard prototype. No seam allowance included:",
        "   add 0.8 for turned seams, 0 for bound / edge-painted",
        "   edges (reference shows edge-stitched, turned edges).",
        "2. Drawn with the OUTER face up (strap, buckle, logo side).",
        "   Pattern assumed symmetrical about its vertical centre",
        "   line; left side measured equal to the right (5.7 / 8.0).",
        "3. Construction: trifold clutch (reference photos). Side",
        "   flaps fold in and tuck inside, front panel folds up over",
        "   them, top flap folds down, strap tongue snaps to the",
        "   front panel. Pages are sewn into the bottom gusset.",
        "4. Gusset depths as measured: 5.7 (sides), 6.0 (bottom),",
        "   6.5 (top). Top 6.5 gives the flap room over the front",
        "   panel; keep as measured (Q1, sheet 2).",
        "5. Snaps: 12.5 mm (line 20) spring snaps: 2 on the side",
        "   flaps, 1 strap tongue, 1 accessory pocket. Set the",
        "   front-panel sockets and strap stud from a dry fold.",
        "6. Outer: faux leather (PU) 1.0-1.2 mm, tan; strap dark",
        "   brown. Stiffen back and front panels with 1.0 mm board.",
        "   Lining: faux leather 0.6 mm, same tan (reference).",
        "7. Reference photos show a deeper top flap (about 9-10) and",
        "   the buckle lower down; prototype gives 5.0 - confirm (Q2).",
        "",
        "**SHEET INDEX",
        "1  Outer shell - flat pattern (this sheet)",
        "2  Assembly - closed views, section, open layout, fold sequence",
        "3  Page 1: 10 cm tips 2.0-5.0 mm (11 pairs)",
        "4  Page 2: 10 cm tips 5.5-10 mm (6 pairs)",
        "5  Page 3: 5 cm tips 2.0-5.0 mm (11 pairs)",
        "6  Page 4: 5 cm tips 5.5-8 mm (4 pairs) + accessory pocket",
        "7  Details: strap, cable pocket, hinge section, elastic section",
        "8  Contents checklist, bill of materials, construction",
    ], "ts", 3.9)
    return sh


# ==========================================================================
# SHEET 2 - assembly
# ==========================================================================
def sheet2():
    sh = Sheet(2, "Assembly - closed views, section, open layout, fold sequence", "1:2 / 1:1 / 1:4 as noted")
    sh.frame()
    s = 5.0
    D = 6.0
    # ---- FRONT VIEW closed ----
    v = View(30, 40, s)
    X, Y, L = v.X, v.Y, v.L
    sh.text(X(0), Y(0) - 14, "FRONT VIEW - closed (1:2)", "tb")
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, 0, 0, BASE_W, BASE_H, R)}" class="leather"/>')
    sh.line(X(0), Y(REAR_FLAP), X(BASE_W), Y(REAR_FLAP), "cut")
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, 0.3, 0.3, BASE_W - 0.6, BASE_H - 0.6, R - 0.3)}" class="stitch"/>')
    cx = BASE_W / 2
    sh.rect(X(cx - STRAP_W / 2), Y(0), L(STRAP_W), L(REAR_FLAP + 6.0), "strap")
    sh.poly([(X(cx - STRAP_W / 2), Y(REAR_FLAP + 6.0)), (X(cx + STRAP_W / 2), Y(REAR_FLAP + 6.0)), (X(cx), Y(REAR_FLAP + 7.5))], "strap")
    buckle(sh, X(cx), Y(2.6), L(STRAP_W + 0.6))
    sh.rect(X(cx - STRAP_W / 2 - 0.2), Y(3.9), L(STRAP_W + 0.4), L(0.7), "strap")
    sh.circle(X(cx), Y(REAR_FLAP + 3.0), 2.2, "brass")
    sh.text(X(cx) + 4, Y(REAR_FLAP + 3.0) + 1, "snap", "tx")
    sh.rect(X(BASE_W - 4.25), Y(1.25), L(2.5), L(2.5), "thin")
    sh.text(X(BASE_W - 3.0), Y(2.5) + 1, "logo", "tx", "middle")
    sh.text(X(1.5), Y(2.8), "top flap 5.0", "tx")
    sh.text(X(1.5), Y(9.0), "front panel", "tx")
    sh.dim_h(X(0), X(BASE_W), Y(0), Y(0) - 6, "21.0")
    sh.dim_v(Y(0), Y(BASE_H), X(BASE_W), X(BASE_W) + 7, "13.0")
    sh.dim_v(Y(0), Y(REAR_FLAP), X(0), X(0) - 7, "5.0")
    sh.dim_v(Y(0), Y(REAR_FLAP + 3.0), X(0), X(0) - 14, "8.0 to snap")

    # ---- BACK VIEW ----
    v2 = View(155, 40, s)
    sh.text(v2.X(0), v2.Y(0) - 14, "BACK VIEW - closed (1:2)", "tb")
    sh.add(f'<path d="{rounded_rect_path(v2.X, v2.Y, v2.L, 0, 0, BASE_W, BASE_H, R)}" class="leather"/>')
    sh.rect(v2.X(cx - STRAP_W / 2), v2.Y(0), v2.L(STRAP_W), v2.L(BASE_H), "strap")
    sh.rect(v2.X(cx - STRAP_W / 2 + 0.3), v2.Y(0.3), v2.L(STRAP_W - 0.6), v2.L(BASE_H - 0.6), "stitch")
    sh.text(v2.X(cx) + 6, v2.Y(BASE_H - 0.8), "strap stitched full height of back", "tx", rot=-90)
    sh.dim_h(v2.X(cx - STRAP_W / 2), v2.X(cx + STRAP_W / 2), v2.Y(BASE_H), v2.Y(BASE_H) + 6, "3.0", ext=False)

    # ---- END VIEW ----
    v3 = View(272, 40, s)
    sh.text(v3.X(0), v3.Y(0) - 14, "END VIEW (1:2)", "tb")
    sh.add(f'<path d="{rounded_rect_path(v3.X, v3.Y, v3.L, 0, 0, D, BASE_H, 0.6)}" class="leather"/>')
    sh.line(v3.X(0), v3.Y(REAR_FLAP), v3.X(D), v3.Y(REAR_FLAP), "thin")
    sh.dim_h(v3.X(0), v3.X(D), v3.Y(BASE_H), v3.Y(BASE_H) + 6, "6.0")

    # ---- SECTION A-A 1:1 ----
    v4 = View(40, 126, 10.0)
    X4, Y4, L4 = v4.X, v4.Y, v4.L
    sh.text(X4(0) - 10, Y4(0) - 11, "SECTION A-A - vertical through the centre, closed (1:1)", "tb")
    sh.text(X4(0) - 10, Y4(0) - 7, "Pages fan from staggered hinge seams in the bottom gusset. P1 (back): 10 cm 2.0-5.0; P2: 10 cm 5.5-10; P3: 5 cm 2.0-5.0; P4 (front): 5 cm 5.5-8 + pocket.", "ts")
    t = 0.25
    sh.rect(X4(-t), Y4(0), L4(t), L4(BASE_H), "leather")                      # back
    sh.rect(X4(-t), Y4(BASE_H), L4(FRONT_WALL + t), L4(t), "leather")          # bottom gusset
    sh.rect(X4(FRONT_WALL - t), Y4(BASE_H - LID_H), L4(t), L4(LID_H), "leather")   # front panel
    sh.rect(X4(-t), Y4(-t), L4(REAR_WALL + t), L4(t), "leather")              # top gusset
    sh.rect(X4(REAR_WALL - t), Y4(-t), L4(t), L4(REAR_FLAP + t), "leather")   # top flap
    sh.rect(X4(REAR_WALL), Y4(REAR_FLAP - 1.0), L4(0.15), L4(TONGUE - 2.0 - 0.0), "strap")   # tongue over flap/front
    sh.rect(X4(-t - 0.15), Y4(0), L4(0.15), L4(BASE_H), "strap")               # strap on back
    sh.circle(X4(REAR_WALL - 0.05), Y4(8.0), 1.2, "brass")
    sh.text(X4(REAR_WALL) + 4, Y4(8.0) + 1, "strap snap", "tx")
    sh.text(X4(REAR_WALL) + 4, Y4(2.5), "top flap", "tx")
    sh.text(X4(FRONT_WALL) + 4, Y4(11.0), "front panel", "tx")
    sh.text(X4(-t) - 5, Y4(6.5), "back panel + strap", "tx", "middle", rot=-90)
    for i, sp in enumerate(SEAMS):
        xtop = sp + 0.12 * i - 0.1
        sh.line(X4(sp), Y4(BASE_H), X4(xtop), Y4(BASE_H - PAGE_H), "cut")
        sh.line(X4(sp) + 0.5, Y4(BASE_H) - 1.5, X4(sp) + 0.5, Y4(BASE_H) + 4, "stitch")
        sh.text(X4(xtop), Y4(BASE_H - PAGE_H) - 1.5, f"P{i + 1}", "tx", "middle")
        ln = 10 if i < 2 else 5
        top = BASE_H - PAGE_H + (1.5 if i < 2 else 3.75)
        sh.rect(X4(xtop) + 0.3, Y4(top), L4(0.5 if i in (0, 2) else (1.0 if i == 1 else 0.8)), L4(ln), "needle")
    sh.rect(X4(0), Y4(BASE_H - 9.0), L4(0.2), L4(9.0), "mesh")
    sh.text(X4(0) + 3, Y4(BASE_H - 7.0), "cable pocket", "tx", rot=-90)
    yd = Y4(BASE_H + t) + 7
    sh.dim_h(X4(0), X4(SEAMS[0]), Y4(BASE_H + t), yd, "1.0")
    for a, b in zip(SEAMS, SEAMS[1:]):
        sh.dim_h(X4(a), X4(b), Y4(BASE_H + t), yd, "1.2")
    sh.dim_h(X4(SEAMS[-1]), X4(FRONT_WALL), Y4(BASE_H + t), yd, "1.4")
    sh.dim_h(X4(0), X4(FRONT_WALL), Y4(BASE_H + t), yd + 8, "6.0 bottom gusset")
    sh.dim_v(Y4(BASE_H - PAGE_H), Y4(BASE_H), X4(REAR_WALL), X4(REAR_WALL) + 22, "12.5 page")
    sh.dim_v(Y4(0), Y4(BASE_H), X4(REAR_WALL), X4(REAR_WALL) + 30, "13.0")

    # ---- OPEN LAYOUT 1:4 ----
    s4 = 2.5
    vi = View(160, 134, s4)
    Xi, Yi, Li = vi.X, vi.Y, vi.L
    sh.text(Xi(0), Yi(0) - 8, "OPEN LAYOUT - inner face up, flaps flat (1:4)", "tb")
    xa, xb = END_FLAP, END_FLAP + SIDE_WALL
    xc, xd = xb + BASE_W, xb + BASE_W + SIDE_WALL
    ya, yb = REAR_FLAP, REAR_FLAP + REAR_WALL
    yc, yd2 = yb + BASE_H, yb + BASE_H + FRONT_WALL
    sh.rect(Xi(xb), Yi(0), Li(BASE_W), Li(PATTERN_H), "leather")
    sh.rect(Xi(0), Yi(yb), Li(PATTERN_W), Li(BASE_H), "leather")
    for yy in (ya, yb, yc, yd2):
        sh.line(Xi(xb), Yi(yy), Xi(xc), Yi(yy), "fold")
    for xx in (xa, xb, xc, xd):
        sh.line(Xi(xx), Yi(yb), Xi(xx), Yi(yc), "fold")
    for i in range(4):
        off = 0.35 * (3 - i)
        sh.rect(Xi(xb + 0.5), Yi(yc - PAGE_H - off), Li(PAGE_W), Li(PAGE_H), "band")
    sh.text(Xi(xb + BASE_W / 2), Yi(yc - 6.0), "P4 (front page) over P3, P2, P1", "ts", "middle")
    sh.text(Xi(xb + BASE_W / 2), Yi(yc - 3.0), "cable pocket on back panel behind P1", "tx", "middle")
    sh.text(Xi(xb + BASE_W / 2), Yi(yc + FRONT_WALL / 2) + 1, "page hinge seams in bottom gusset", "tx", "middle")
    sh.text(Xi(xb + BASE_W / 2), Yi(yd2 + 2.5), "FRONT PANEL (inner face)", "tx", "middle")
    sh.text(Xi(xb + BASE_W / 2), Yi(yd2 + 9.5), "sockets for side-flap snaps", "tx", "middle")
    sh.text(Xi(xb + BASE_W / 2), Yi(REAR_FLAP / 2) + 1, "TOP FLAP", "tx", "middle")
    sh.text(Xi(xb + BASE_W / 2), Yi(ya + REAR_WALL / 2) + 1, "TOP GUSSET", "tx", "middle")
    sh.text(Xi(END_FLAP / 2) + 1, Yi(yb + 6.5), "SIDE FLAP", "tx", "middle", rot=-90)
    sh.text(Xi(xd + END_FLAP / 2) + 1, Yi(yb + 6.5), "SIDE FLAP", "tx", "middle", rot=-90)
    for sx in (xb + SNAP_FROM_FOLD, xc - SNAP_FROM_FOLD):
        sh.circle(Xi(sx), Yi(yd2 + 6.5), 1.3, "thin")
    sh.circle(Xi(xa - 5.0), Yi(yb + 3.5), 1.3, "hid")
    sh.circle(Xi(xd + 5.0), Yi(yb + 3.5), 1.3, "hid")
    sh.text(Xi(xa - 5.0), Yi(yb + 2.2), "stud, far face", "tx", "middle")
    sh.text(Xi(xd + 5.0), Yi(yb + 2.2), "stud, far face", "tx", "middle")

    # ---- NOTES column ----
    fx, fy = 312, 22
    sh.lines(fx, fy, [
        "**FOLD / CLOSING SEQUENCE",
        "1. Pages stand up from the bottom gusset.",
        "2. Fold both side flaps in over the pages;",
        "   they tuck inside the front panel.",
        "3. Fold the front panel up; its inner-face",
        "   sockets snap onto the side-flap studs.",
        "4. Fold the top gusset + flap over the front.",
        "5. Pass the strap tongue through the buckle",
        "   and keeper; snap it to the front-panel stud.",
        "",
        "**STACK-HEIGHT CHECK (depth 6.0)",
        "P1  2 x 5 mm tips + page          0.7",
        "P2  2 x 10 mm tips + page         1.2",
        "P3  2 x 5 mm tips + page          0.7",
        "P4  2 x 8 mm tips + pocket        1.2",
        "cable pocket, 5 coils             1.2",
        "back + front panel                0.5",
        "TOTAL                             5.5  (OK)",
        "",
        "**OPEN QUESTIONS (confirm before cutting)",
        "Q1 Keep gussets 5.7 / 6.0 / 6.5 as measured?",
        "Q2 Top flap 5.0 (prototype) vs ~9 in the",
        "   reference photos?",
        "Q3 Strap: working buckle, or fixed buckle",
        "   with snap closure only (drawn)?",
        "Q4 Side-flap snaps: spring snaps (drawn) or",
        "   hidden magnetic snaps?",
        "Q5 Cables in the back-panel pocket (drawn)",
        "   or in page 4's accessory pocket?",
        "Q6 Confirm real cap / key / connector sizes",
        "   against the pocket on sheet 6.",
    ], "ts", 3.85)
    return sh


# ==========================================================================
# SHEETS 3-6 - pages
# ==========================================================================
def page_sheet(n, title, sizes, tip_len, tip_top, band_c, table_title):
    sh = Sheet(n, title, "1:1")
    sh.frame()
    v = View(32, 48, 10.0)
    margin, slots = draw_page(sh, v, sizes, tip_len, tip_top, band_c)
    page_dims(sh, v, slots, margin, tip_len, tip_top, band_c)
    sh.text(v.X(PAGE_W / 2), v.Y(PAGE_H + HINGE_TAB) + 27,
            f"{title.split(':')[0].upper()} - 20.0 x 12.5 + 1.5 hinge tab. Full size 1:1 - use as pattern.", "tb", "middle")
    tx = 258
    sh.text(tx, 22, table_title, "tb")
    end = slot_table(sh, tx, 25, slots, sizes, tip_len)
    sh.lines(tx, end + 6, page_notes(), "ts", 3.7)
    return sh, v, slots, end


def sheet3():
    sh, *_ = page_sheet(3, "Page 1: 10 cm tips 2.0-5.0 mm (11 pairs)", SIZES_SMALL, 10.0, 1.5, 6.5,
                        "SLOT TABLE - page 1 (positions from left page edge, cm)")
    band_detail(sh, 32, 232, "DETAIL A - elastic slot section, 2:1 (same on all pages)")
    return sh


def sheet4():
    sh, v, slots, end = page_sheet(4, "Page 2: 10 cm tips 5.5-10 mm (6 pairs)", SIZES_LARGE10, 10.0, 1.5, 6.5,
                                   "SLOT TABLE - page 2 (positions from left page edge, cm)")
    sh.lines(258, end + 6 + 15 * 3.7 + 4, [
        "**PAGE 2 NOTE",
        "- 6 slots use 14.2 of the 20.0 width; the strip is",
        "  centred (2.9 margins). The 10 mm pair is the thickest",
        "  item in the case (1.0) - see stack check, sheet 2.",
    ], "ts", 3.7)
    return sh


def sheet5():
    sh, v, slots, end = page_sheet(5, "Page 3: 5 cm tips 2.0-5.0 mm (11 pairs)", SIZES_SMALL, 5.0, 3.75, 6.25,
                                   "SLOT TABLE - page 3 (positions from left page edge, cm)")
    sh.lines(258, end + 6 + 15 * 3.7 + 4, [
        "**PAGE 3 NOTE",
        "- Same slot widths and stitch positions as page 1, so",
        "  the two pages share one stitching template.",
        "- 5 cm tips sit centred on the page (reference photo):",
        "  points 3.75 from the top, elastic centred at 6.25.",
    ], "ts", 3.7)
    return sh


def sheet6():
    sh = Sheet(6, "Page 4: 5 cm tips 5.5-8 mm (4 pairs) + accessory snap pocket", "1:1")
    sh.frame()
    v = View(32, 48, 10.0)
    X, Y, L = v.X, v.Y, v.L
    tip_len, tip_top, band_c = 5.0, 3.75, 6.25
    pw, ph, pf = 7.0, 9.0, 3.0          # pocket body, flap
    px, py = 1.0, 1.0                   # pocket position
    zone_x = px + pw + 1.0              # needle zone start (9.0)
    zone_w = PAGE_W - zone_x            # 11.0
    margin, slots = draw_page(sh, v, SIZES_LARGE5, tip_len, tip_top, band_c, x_offset=zone_x, zone_w=zone_w)
    # pocket: body + flap
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, px, py + pf - 0.5, pw, ph, 0.6, (0, 0, 1, 1))}" class="band"/>')
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, px + 0.3, py + pf - 0.2, pw - 0.6, ph - 0.6, 0.4, (0, 0, 1, 1))}" class="stitch"/>')
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, px, py, pw, pf + 1.0, 0.6, (1, 1, 1, 1))}" class="leather"/>')
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, px + 0.3, py + 0.3, pw - 0.6, pf + 0.4, 0.4, (1, 1, 1, 1))}" class="stitch"/>')
    sh.line(X(px), Y(py), X(px + pw), Y(py), "fold")
    sh.circle(X(px + pw / 2), Y(py + pf - 0.4), 3.0, "brass")
    sh.circle(X(px + pw / 2), Y(py + pf - 0.4), 1.4, "thin")
    sh.text(X(px + pw / 2), Y(py + pf + 3.5), "ACCESSORY POCKET", "ts", "middle")
    sh.text(X(px + pw / 2), Y(py + pf + 4.3), "6 end caps, 4 keys,", "tx", "middle")
    sh.text(X(px + pw / 2), Y(py + pf + 5.0), "3 connectors, grip patch", "tx", "middle")
    sh.text(X(px + pw / 2), Y(py + pf + 6.2), "patch pocket 7.0 x 9.0,", "tx", "middle")
    sh.text(X(px + pw / 2), Y(py + pf + 6.9), "flap 7.0 x 3.0, snap 12.5 mm", "tx", "middle")
    sh.text(X(px + pw / 2), Y(py + 0.8), "flap", "tx", "middle")
    # dims
    page_dims(sh, v, slots, margin, tip_len, tip_top, band_c, x_offset=zone_x, zone_w=zone_w, overall_off=8)
    yb = Y(PAGE_H + HINGE_TAB) + 8
    sh.dim_h(X(0), X(px), Y(PAGE_H + HINGE_TAB), yb, "1.0")
    sh.dim_h(X(px), X(px + pw), Y(PAGE_H + HINGE_TAB), yb, "7.0 pocket")
    sh.dim_h(X(px + pw), X(zone_x), Y(PAGE_H + HINGE_TAB), yb, "1.0")
    sh.dim_v(Y(0), Y(py), X(px + pw), X(px + pw) + 5, "1.0")
    sh.dim_v(Y(py), Y(py + pf), X(px + pw), X(px + pw) + 5, "3.0 flap")
    sh.dim_v(Y(py + pf), Y(py + pf - 0.5 + ph), X(px + pw), X(px + pw) + 5, "8.5")
    sh.dim_v(Y(py + pf - 0.5 + ph), Y(PAGE_H), X(px + pw), X(px + pw) + 5, "1.0")
    sh.text(X(PAGE_W / 2), Y(PAGE_H + HINGE_TAB) + 27, "PAGE 4 - 20.0 x 12.5 + 1.5 hinge tab. Full size 1:1 - use as pattern.", "tb", "middle")
    tx = 258
    sh.text(tx, 22, "SLOT TABLE - page 4 (positions from left page edge, cm)", "tb")
    end = slot_table(sh, tx, 25, slots, SIZES_LARGE5, 5)
    sh.lines(tx, end + 6, [
        "**PAGE 4 LAYOUT (reference photo 5)",
        "- Accessory pocket at left: patch pocket 7.0 x 9.0",
        "  with a 3.0 flap and 12.5 mm brass snap, edge-",
        "  stitched. Body cut 7.0 x 9.5 (0.5 under the flap).",
        "- Holds the 6 screw-on end caps, 4 cable keys,",
        "  3 connectors and the leather grip patch.",
        "- Needle zone 11.0 wide: 4 pairs 5.5 / 6 / 7 / 8 mm,",
        "  slot widths 1.7-2.0, strip centred (1.05 margins).",
        "",
        "**LEATHER GRIP PATCH (replaces the rubber grip disc)",
        "- Veg-tan leather 1.8-2.0 mm, 6.0 x 4.0, R 0.5 corners,",
        "  suede side out. Fold round the tip when tightening.",
        "",
    ] + page_notes(), "ts", 3.7)
    return sh


# ==========================================================================
# SHEET 7 - details
# ==========================================================================
def sheet7():
    sh = Sheet(7, "Details - strap, cable pocket, page hinge section, elastic section", "1:2 / 2:1 as noted")
    sh.frame()
    # ---- STRAP 1:2 ----
    v = View(22, 34, 5.0)
    X, Y, L = v.X, v.Y, v.L
    total = BASE_H + REAR_WALL + REAR_FLAP + TONGUE + 1.0
    sh.text(X(0), Y(0) - 5, "DETAIL B - STRAP, flat, 1:2 (dark brown faux leather, 2 ply, edge-stitched 0.3)", "tb")
    tip_len = 2.0
    body = total - tip_len
    pts = [(X(0), Y(0)), (X(body), Y(0)), (X(total), Y(STRAP_W / 2)), (X(body), Y(STRAP_W)), (X(0), Y(STRAP_W))]
    sh.poly(pts, "strap")
    sh.line(X(0.3), Y(0.3), X(body), Y(0.3), "stitch")
    sh.line(X(0.3), Y(STRAP_W - 0.3), X(body), Y(STRAP_W - 0.3), "stitch")
    # zones
    z = [(0, 1.0, "anchor"), (1.0, 1.0 + BASE_H, "back panel (stitched)"), (1.0 + BASE_H, 1.0 + BASE_H + REAR_WALL, "top gusset"),
         (1.0 + BASE_H + REAR_WALL, 1.0 + BASE_H + REAR_WALL + REAR_FLAP, "top flap"), (1.0 + BASE_H + REAR_WALL + REAR_FLAP, total, "free tongue")]
    for a, b, t in z:
        sh.line(X(a), Y(0) - 1, X(a), Y(STRAP_W) + 1, "fold")
        sh.text(X((a + b) / 2), Y(STRAP_W) + 4, t, "tx", "middle")
    # holes (decorative) + snap socket
    for i in range(3):
        sh.circle(X(total - 4.5 - i * 1.5), Y(STRAP_W / 2), L(0.2), "cut")
    sh.circle(X(total - 2.0), Y(STRAP_W / 2), 2.0, "brass")
    sh.circle(X(total - 2.0), Y(STRAP_W / 2), 0.9, "thin")
    sh.text(X(total - 2.0), Y(0) - 7, "snap socket (inner face)", "tx", "middle")
    sh.text(X(total - 7.5), Y(0) - 7, "3 holes 0.4, decorative", "tx", "middle")
    # dims
    yd = Y(STRAP_W) + 10
    for a, b, t in [(0, 1.0, "1.0"), (1.0, 14.0, "13.0"), (14.0, 20.5, "6.5"), (20.5, 25.5, "5.0"), (25.5, total, fmt(TONGUE))]:
        sh.dim_h(X(a), X(b), Y(STRAP_W), yd, t)
    sh.dim_h(X(0), X(total), Y(STRAP_W), yd + 8, f"{fmt(total)} overall")
    sh.dim_v(Y(0), Y(STRAP_W), X(0), X(0) - 6, "3.0")
    sh.dim_h(X(total - 2.0), X(total), Y(0), Y(0) - 3, "2.0", ext=False)
    # buckle piece
    bx = X(0)
    by = yd + 22
    sh.text(bx, by - 3, "BUCKLE PIECE - 3.0 x 8.0 loop round the 30 mm buckle bar, stitched to the top flap under the strap with the bar 2.6 below the flap edge; keeper 3.4 x 0.7 stitched 1.3 below the buckle", "ts")
    vb = View(bx, by, 5.0)
    sh.rect(vb.X(0), vb.Y(0), vb.L(8.0), vb.L(STRAP_W), "strap")
    buckle(sh, vb.X(4.0), vb.Y(STRAP_W / 2), vb.L(STRAP_W + 0.6))
    sh.rect(vb.X(4.0 + 1.3 + 1.6), vb.Y(-0.2), vb.L(0.7), vb.L(STRAP_W + 0.4), "strap")
    sh.dim_h(vb.X(0), vb.X(8.0), vb.Y(STRAP_W), vb.Y(STRAP_W) + 6, "8.0")
    sh.text(vb.X(10), vb.Y(1.0), "Buckle: 30 mm (1 1/4 in) antique brass, roller or plain; prong engages the strap holes.", "ts")
    sh.text(vb.X(10), vb.Y(2.3), "Closure is the snap: the buckle is decorative unless Q3 (sheet 2) says otherwise.", "ts")

    # ---- CABLE POCKET 1:2 ----
    vc = View(22, 128, 5.0)
    Xc, Yc, Lc = vc.X, vc.Y, vc.L
    sh.text(Xc(0), Yc(0) - 5, "DETAIL D - CABLE POCKET on the inner face of the back panel, behind page 1 (1:2)", "tb")
    sh.rect(Xc(0), Yc(0), Lc(BASE_W), Lc(BASE_H), "leather")
    sh.rect(Xc(0.5), Yc(BASE_H - 9.5), Lc(PAGE_W), Lc(9.0), "mesh")
    sh.rect(Xc(0.5), Yc(BASE_H - 9.5), Lc(PAGE_W), Lc(0.8), "elastic")
    sh.text(Xc(BASE_W / 2), Yc(BASE_H - 9.5) + 2.8, "15 mm elastic top edge", "tx", "middle")
    for i, d in enumerate([8.0, 7.0, 6.0, 5.0, 4.0]):
        sh.circle(Xc(BASE_W / 2), Yc(BASE_H - 5.0), Lc(d / 2), "thin")
    sh.text(Xc(BASE_W / 2), Yc(BASE_H - 5.0) + 1, "5 cables coiled", "tx", "middle")
    sh.text(Xc(BASE_W / 2), Yc(BASE_H - 5.0) + 3.4, "25 / 40 / 60 / 80 / 100 cm", "tx", "middle")
    sh.text(Xc(BASE_W / 2), Yc(1.8), "BACK PANEL inner face 21.0 x 13.0", "ts", "middle")
    sh.dim_h(Xc(0), Xc(0.5), Yc(BASE_H), Yc(BASE_H) + 6, "0.5", ext=False)
    sh.dim_h(Xc(0.5), Xc(0.5 + PAGE_W), Yc(BASE_H), Yc(BASE_H) + 6, "20.0 pocket")
    sh.dim_v(Yc(BASE_H - 9.5), Yc(BASE_H - 0.5), Xc(BASE_W), Xc(BASE_W) + 6, "9.0")
    sh.dim_v(Yc(BASE_H - 0.5), Yc(BASE_H), Xc(BASE_W), Xc(BASE_W) + 6, "0.5", ext=False)
    sh.lines(Xc(BASE_W) + 16, Yc(1.5), [
        "- Slip pocket, faux leather lining 0.6 mm, sides and",
        "  bottom stitched to the back-panel lining before",
        "  the shell is assembled; 15 mm elastic in the top hem",
        "  keeps the coils in.",
        "- Alternative (Q5): put the cables in page 4's pocket",
        "  and use this pocket for a pattern card.",
    ], "ts", 3.7)

    # ---- HINGE SECTION 2:1 ----
    vh = View(200, 128, 20.0)
    Xh, Yh, Lh = vh.X, vh.Y, vh.L
    sh.text(Xh(0) - 10, Yh(0) - 5, "DETAIL C - PAGE HINGE, section through the bottom gusset, 2:1", "tb")
    sh.rect(Xh(0), Yh(2.0), Lh(FRONT_WALL), Lh(0.25), "hatch")
    sh.rect(Xh(0), Yh(2.0), Lh(FRONT_WALL), Lh(0.25), "thin")
    sh.rect(Xh(-0.25), Yh(-0.8), Lh(0.25), Lh(3.05), "hatch")       # back panel
    sh.rect(Xh(-0.25), Yh(-0.8), Lh(0.25), Lh(3.05), "thin")
    sh.rect(Xh(FRONT_WALL), Yh(-0.8), Lh(0.25), Lh(3.05), "hatch")  # front panel
    sh.rect(Xh(FRONT_WALL), Yh(-0.8), Lh(0.25), Lh(3.05), "thin")
    for i, sp in enumerate(SEAMS):
        # tab folded: page comes down, tab lies flat on the gusset toward the front, stitched through
        sh.line(Xh(sp), Yh(-0.8), Xh(sp), Yh(2.0), "cut")
        sh.line(Xh(sp), Yh(2.0), Xh(sp + 0.9), Yh(2.0), "cut")
        sh.line(Xh(sp + 0.5), Yh(1.85), Xh(sp + 0.5), Yh(2.4), "stitch")
        sh.text(Xh(sp), Yh(-0.8) - 1.5, f"P{i + 1}", "tx", "middle")
    sh.text(Xh(FRONT_WALL / 2), Yh(2.25) + 4, "bottom gusset: outer 1.0 mm + 1.0 mm board + lining", "tx", "middle")
    sh.text(Xh(-0.1), Yh(0.6), "back", "tx", "end", rot=-90)
    sh.text(Xh(FRONT_WALL + 0.25) + 3, Yh(0.6), "front", "tx", "start", rot=-90)
    yd2 = Yh(2.4) + 10
    sh.dim_h(Xh(0), Xh(SEAMS[0]), Yh(2.25), yd2, "1.0")
    for a, b in zip(SEAMS, SEAMS[1:]):
        sh.dim_h(Xh(a), Xh(b), Yh(2.25), yd2, "1.2")
    sh.dim_h(Xh(SEAMS[-1]), Xh(FRONT_WALL), Yh(2.25), yd2, "1.4")
    sh.dim_h(Xh(0), Xh(FRONT_WALL), Yh(2.25), yd2 + 8, "6.0")
    sh.dim_h(Xh(SEAMS[0]), Xh(SEAMS[0] + 0.9), Yh(2.0), Yh(2.0) - 4, "1.5 tab, folded", ext=False)
    sh.lines(Xh(0) - 10, yd2 + 16, [
        "- Each page's 1.5 hinge tab folds toward the front and is",
        "  stitched through the gusset (lining + board + outer) on",
        "  one line, 0.5 from the fold. Seams staggered 1.2 apart",
        "  so the four pages fan open (reference photo).",
        "- Stitch pages P1 to P4 in order from the back; the front",
        "  panel seam is last. The gusset outer face shows four",
        "  parallel stitch lines - use the same contrast thread.",
    ], "ts", 3.7)

    band_detail(sh, 30, 226, "DETAIL A - elastic slot section, 2:1")
    return sh


# ==========================================================================
# SHEET 8 - contents, BOM, construction
# ==========================================================================
def sheet8():
    sh = Sheet(8, "Contents checklist, bill of materials, construction & cutting list", "-")
    sh.frame()
    x0, y0 = 14, 26
    sh.text(x0, y0, "CONTENTS CHECKLIST - 64 tips (32 pairs), 5 cables, 14 accessories: where each item lives", "tb")
    rows = []
    for i, (lab, w) in enumerate(SIZES_SMALL):
        rows.append([f"{lab} mm", "2 x 10 cm", "Page 1", str(i + 1), fmt(w), "2 x 5 cm", "Page 3", str(i + 1), fmt(w)])
    for i, (lab, w) in enumerate(SIZES_LARGE10):
        c = ("Page 4", str(i + 1), fmt(w)) if i < 4 else ("-", "-", "-")
        rows.append([f"{lab} mm", "2 x 10 cm", "Page 2", str(i + 1), fmt(w), "2 x 5 cm" if i < 4 else "-", *c])
    end = sh.table(x0, y0 + 3, ["Size", "10 cm tips", "Page", "Slot", "w", "5 cm tips", "Page", "Slot", "w"],
                   rows, [16, 18, 16, 10, 10, 18, 16, 10, 10], rh=4.0)
    sh.text(x0, end + 4, "Totals: 17 pairs x 10 cm (34 tips) on pages 1 + 2;  15 pairs x 5 cm (30 tips) on pages 3 + 4;  32 pairs / 64 tips.", "ts")
    sh.text(x0, end + 8, "Accessories: 6 end caps + 4 keys + 3 connectors + grip patch -> page 4 snap pocket;  5 cables -> back-panel cable pocket.", "ts")

    bx, by = 150, 26
    sh.text(bx, by, "BILL OF MATERIALS (per case)", "tb")
    bom = [
        ["1", "Outer shell, faux leather (PU) 1.0-1.2 mm, tan", "1", "48.4 x 43.2 net + allowance (sheet 1)"],
        ["2", "Lining, faux leather 0.6 mm, tan", "1", "48.4 x 43.2 net + allowance"],
        ["3", "Board 1.0 mm: back panel, front panel", "2", "21 x 13, 21 x 12.7"],
        ["4", "Board 0.8 mm: pages", "4", "20.0 x 12.5"],
        ["5", "Page faces, faux leather 1.0 mm", "8", "20.0 x 14.0 (incl. 1.5 hinge tab) + allowance"],
        ["6", "Knit elastic 15 mm, tan", "4", "17.1 / 14.2 / 17.1 / 8.9 cm"],
        ["7", "Strap, faux leather 1.2 mm, dark brown, 2 ply", "2", "3.0 x 36.0 (sheet 7)"],
        ["8", "Buckle piece + keeper, dark brown", "1+1", "3.0 x 8.0;  3.4 x 0.7"],
        ["9", "Buckle 30 mm, antique brass", "1", "roller or plain"],
        ["10", "Spring snaps 12.5 mm (line 20), antique brass", "4 sets", "2 side flaps, 1 strap, 1 pocket"],
        ["11", "Accessory pocket + flap, faux leather", "1+1", "7.0 x 9.5;  7.0 x 4.0"],
        ["12", "Cable pocket, lining faux leather", "1", "20.0 x 10.0 + 15 mm elastic 20 cm"],
        ["13", "Leather grip patch, veg-tan 1.8-2 mm", "1", "6.0 x 4.0, R 0.5"],
        ["14", "Thread, bonded polyester Tex 70, contrast", "-", "stitch length 3 mm"],
        ["15", "Logo emboss plate", "1", "2.5 x 2.5 (artwork by client)"],
    ]
    end2 = sh.table(bx, by + 3, ["#", "Item", "Qty", "Cut size (cm) / note"], bom, [8, 90, 14, 90], rh=4.0)
    sh.lines(150, end2 + 8, [
        "**CONSTRUCTION SEQUENCE",
        "1. Cut outer shell, lining and board (sheet 1). Emboss the logo on the top flap while flat.",
        "2. Stitch the strap to the outer shell (back panel + top gusset + top flap); add buckle piece and keeper.",
        "3. Make the four pages (sheets 3-6): stitch elastics and labels on the face plies, add the pocket to page 4,",
        "   then laminate face + board + back ply and edge-stitch, leaving the hinge tab single-ply.",
        "4. Stitch the cable pocket to the back-panel lining. Set the side-flap studs and front-panel sockets.",
        "5. Stitch the page hinge tabs through the bottom gusset in order P1-P4 (sheet 7, detail C).",
        "6. Laminate lining to shell with board in back and front panels; turn and edge-stitch 0.3 all round.",
        "7. Dry-fold; set the strap stud on the front panel and the socket in the tongue; check all snaps.",
        "8. Load the set per the contents checklist; check the closed case has no pressure on the 10 mm tips.",
        "",
        "**TOLERANCES",
        "Cut pieces +/- 0.1 cm; elastic stitch lines +/- 0.05 cm (the 0.6 slot must still take two 2 mm tips);",
        "snap centres +/- 0.15 cm; page hinge seams +/- 0.1 cm.",
    ], "ts", 3.8)

    mx, my = 14, 172
    sh.text(mx, my, "MEASUREMENT RECORD - what each prototype / reference photo contributed", "tb")
    mend = sh.table(mx, my + 3, ["Photo", "Feature", "Value used on drawings"], [
        ["P1", "Cardboard cross pattern", "Top flap 5.0, top gusset 6.5, back 21.0 x 13.0, bottom gusset 6.0, front 12.7; side gusset 5.7, side flap 8.0, snaps"],
        ["P2-P5", "Cardboard panels", "Slot widths 0.6-2.2 (= 6-22 mm), 0.5 lands, 1.0 end margins, 1.5 above the points"],
        ["R1, R3", "Closed clutch, front/back", "Trifold clutch, wrap strap 3.0 with buckle, keeper and snap; logo on flap; R 1.0 corners; edge stitch"],
        ["R2, R3", "Open case", "Pages sewn into the bottom gusset, not removable; side flaps tuck inside; cable pocket at the back"],
        ["R4, R5", "Page interiors", "1.5 elastic across the middle of each page; size labels above tips; snap accessory pocket on the 5.5-8 page"],
    ], [16, 54, 164], rh=4.2)
    sh.text(14, mend + 8, "HARDWARE SIZE ASSUMPTIONS (confirm against the real set - Q6)", "tb")
    sh.table(14, mend + 11, ["Item", "Qty", "Assumed size (cm)", "Where"], [
        ["Screw-on end cap", "6", "1.0 dia x 1.5", "page 4 pocket"],
        ["Cable key", "4", "1.2 x 3.5", "page 4 pocket"],
        ["Cable connector", "3", "1.0 dia x 3.0", "page 4 pocket"],
        ["Leather grip patch", "1", "6.0 x 4.0 x 0.2", "page 4 pocket"],
        ["Cables 25-100 cm", "5", "coil to 8.0 dia", "back-panel cable pocket"],
    ], [40, 12, 48, 60], rh=4.2)
    return sh


# ==========================================================================
def main():
    sheets = [sheet1(), sheet2(), sheet3(), sheet4(), sheet5(), sheet6(), sheet7(), sheet8()]
    names = []
    for sh in sheets:
        fn = f"sheet{sh.n}.svg"
        with open(os.path.join(OUT, fn), "w") as f:
            f.write(sh.svg())
        names.append((fn, sh.title))
    pages = []
    for fn, title in names:
        with open(os.path.join(OUT, fn)) as f:
            svg = f.read()
        pages.append(f'<section class="page" title="{esc(title)}">{svg}</section>')
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Knitting Needle Case - Drawing Set</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
 @page {{ size: A3 landscape; margin: 0; }}
 html,body {{ margin:0; background:#555; }}
 .page {{ width:420mm; height:297mm; background:#fff; margin:8mm auto; box-shadow:0 2px 12px rgba(0,0,0,.4); page-break-after:always; break-after:page; overflow:hidden; }}
 .page svg {{ width:420mm; height:297mm; display:block; }}
 @media print {{ html,body {{ background:#fff; }} .page {{ margin:0; box-shadow:none; }} }}
</style></head><body>
{''.join(pages)}
</body></html>
"""
    with open(os.path.join(HERE, "index.html"), "w") as f:
        f.write(html)
    print("wrote", len(sheets), "sheets")


if __name__ == "__main__":
    main()
