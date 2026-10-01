#!/usr/bin/env python3
"""
Technical drawing set for the interchangeable knitting-needle case.

Rev D: trifold clutch per the client's brief and reference photos: three
pages sewn into the bottom gusset plus the back wall as the fourth storage
panel, 15 mm elastic threaded in and out of each panel, snap pockets, a
wrap-around strap with decorative buckle and snap closure, client logo.  Every dimension comes
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
REV = "E"
PROJECT = "INTERCHANGEABLE KNITTING NEEDLE CASE"
CLIENT = "gsumano7 / ziqmac"
TOTAL_SHEETS = 9

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
REAR_FLAP = 10.0             # client 2026-10-01: longer flap per reference photo (prototype measured 5.0)
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
R = 1.0                      # corner radius on flaps and pages
SEAMS = (1.5, 3.0, 4.5)      # three page hinge seams, evenly spaced across the 6.0 gusset (from the back-wall fold)
SLIT = 1.6                   # slit length for the 15 mm elastic
BUCKLE_ON_FLAP = 4.7         # decorative buckle bar, below the top-flap top edge
KEEPER_ON_FLAP = 8.0         # keeper centre, below the top-flap top edge
TONGUE_FREE = 3.0            # strap tongue beyond the top-flap edge
SNAP_FROM_FLAP_EDGE = 1.0    # tongue snap socket, beyond the top-flap edge
STRAP_STUD_FROM_TOP = 11.0   # strap stud on the front panel, below the case top when closed
LOGO_FROM_TOP = 7.0          # logo centre below the top-flap top edge


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
.elastic{{fill:#cfd6dc;stroke:#000;stroke-width:0.35}}
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
        self.text(x0 + 2, y0 + 27.8, "Cardboard prototype P1-P5 + client brief, logo and reference photos R1-R6", "t")
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


def buckle(sh, cx, cy, w):
    hgt = w * 0.42
    sh.rect(cx - w / 2, cy - hgt / 2, w, hgt, "brass", rx=0.6)
    sh.rect(cx - w / 2 + 1.0, cy - hgt / 2 + 1.0, w - 2.0, hgt - 2.0, "thin")
    sh.line(cx, cy - hgt / 2, cx, cy + hgt / 2 + 1.5, "cut")


def size_labels(sh, v, slots, y_text, y_tip):
    for lab, a, b in slots:
        cx = (a + b) / 2
        sh.text(v.X(cx), v.Y(y_text), lab, "tx", "middle")
        sh.text(v.X(cx), v.Y(y_text) + 2.4, "mm", "tx", "middle")
        sh.line(v.X(cx), v.Y(y_text) + 3.2, v.X(cx), v.Y(y_tip) - 0.8, "dim")


def threaded_elastic(sh, v, slots, band_c):
    """Elastic threaded through slit pairs: visible loop per slot, hidden run between."""
    X, Y, L = v.X, v.Y, v.L
    y0, y1 = band_c - ELASTIC / 2, band_c + ELASTIC / 2
    sl0, sl1 = band_c - SLIT / 2, band_c + SLIT / 2
    # hidden run behind the face ply (dashed) from first slit to last
    sh.line(X(slots[0][1]), Y(band_c), X(slots[-1][2]), Y(band_c), "hid")
    for lab, a, b in slots:
        sh.rect(X(a), Y(y0), L(b - a), L(y1 - y0), "elastic")
        for x in (a, b):
            sh.line(X(x), Y(sl0), X(x), Y(sl1), "cut", 'stroke-width="0.9"')     # slit
            sh.line(X(x), Y(sl0) - 1.2, X(x), Y(sl1) + 1.2, "stitch")           # bar tack
    # anchor tacks at the two ends
    for x, d in ((slots[0][1], -1), (slots[-1][2], 1)):
        sh.rect(X(x) + (d * 1.0 if d < 0 else 0) - (1.0 if d < 0 else 0), Y(y0), 1.0, L(y1 - y0), "hatch")


def snap_pocket(sh, v, x, y, w, h, flap, lab1, lab2=None, r=0.6, snap_r=2.6):
    """Patch pocket with snap flap at model (x, y): flap height 'flap', body 'h' below the flap fold."""
    X, Y, L = v.X, v.Y, v.L
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, x, y + flap - 0.5, w, h + 0.5, r, (0, 0, 1, 1))}" class="band"/>')
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, x + 0.3, y + flap - 0.2, w - 0.6, h - 0.1, max(r - 0.3, 0.1), (0, 0, 1, 1))}" class="stitch"/>')
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, x, y, w, flap + 0.8, r, (1, 1, 1, 1))}" class="leather"/>')
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, x + 0.3, y + 0.3, w - 0.6, flap + 0.2, max(r - 0.3, 0.1), (1, 1, 1, 1))}" class="stitch"/>')
    sh.line(X(x), Y(y), X(x + w), Y(y), "fold")
    sh.circle(X(x + w / 2), Y(y + flap - 0.3), snap_r, "brass")
    sh.circle(X(x + w / 2), Y(y + flap - 0.3), snap_r * 0.45, "thin")
    sh.text(X(x + w / 2), Y(y + flap + h / 2) - 0.5, lab1, "ts", "middle")
    if lab2:
        sh.text(X(x + w / 2), Y(y + flap + h / 2) + 3.0, lab2, "tx", "middle")


def draw_panel(sh, v, sizes, tip_len, tip_top, band_c, margin=None, x_offset=0.0, zone_w=None,
               backwall=False):
    """Page (20 x 12.5 + hinge tab) or back wall (21 x 13) with needles, labels and threaded elastic."""
    X, Y, L = v.X, v.Y, v.L
    W, H = (BASE_W, BASE_H) if backwall else (PAGE_W, PAGE_H)
    zone_w = W if zone_w is None else zone_w
    margin, slots = slot_layout(sizes, zone_w, margin=margin)
    slots = [(lab, a + x_offset, b + x_offset) for lab, a, b in slots]
    if backwall:
        sh.rect(X(0), Y(0), L(W), L(H), "leather")
        sh.rect(X(0.3), Y(0.3), L(W - 0.6), L(H - 0.6), "stitch")
    else:
        sh.add(f'<path d="{rounded_rect_path(X, Y, L, 0, 0, W, H, R, (1, 1, 0, 0))}" class="leather"/>')
        sh.rect(X(1.0), Y(H), L(W - 2.0), L(HINGE_TAB), "hatch")
        sh.rect(X(1.0), Y(H), L(W - 2.0), L(HINGE_TAB), "thin")
        sh.line(X(0), Y(H), X(W), Y(H), "fold")
        sh.add(f'<path d="{rounded_rect_path(X, Y, L, 0.3, 0.3, W - 0.6, H - 0.6, R - 0.3, (1, 1, 0, 0))}" class="stitch"/>')
    for lab, a, b in slots:
        draw_needle_pair(sh, v, a, b, tip_top, tip_len, float(lab) / 10.0)
    threaded_elastic(sh, v, slots, band_c)
    size_labels(sh, v, slots, tip_top - 1.0, tip_top)
    return margin, slots


def panel_dims(sh, v, slots, margin, tip_len, tip_top, band_c, x_offset=0.0, zone_w=None,
               overall_off=8, backwall=False):
    X, Y, L = v.X, v.Y, v.L
    W, H = (BASE_W, BASE_H) if backwall else (PAGE_W, PAGE_H)
    zone_w = W if zone_w is None else zone_w
    y0, y1 = band_c - ELASTIC / 2, band_c + ELASTIC / 2
    tab = 0 if backwall else HINGE_TAB
    xl = X(0) - 7
    sh.dim_v(Y(0), Y(tip_top), X(0), xl, fmt(tip_top))
    sh.dim_v(Y(tip_top), Y(tip_top + tip_len), X(0), xl, f"{fmt(tip_len)} tip")
    sh.dim_v(Y(tip_top + tip_len), Y(H), X(0), xl, fmt(H - tip_top - tip_len))
    sh.dim_v(Y(0), Y(H), X(0), xl - overall_off, fmt(H))
    if not backwall:
        sh.dim_v(Y(H), Y(H + HINGE_TAB), X(0), xl, fmt(HINGE_TAB))
    xr = X(W) + 7
    sh.dim_v(Y(0), Y(y0), X(W), xr, fmt(y0))
    sh.dim_v(Y(y0), Y(y1), X(W), xr, f"{fmt(ELASTIC)} elastic")
    sh.dim_v(Y(band_c - SLIT / 2), Y(band_c + SLIT / 2), X(W), xr + 8, f"{fmt(SLIT)} slit")
    yb = Y(H + tab) + 8
    sh.dim_h(X(x_offset), X(slots[0][1]), Y(H + tab), yb, fmt(margin))
    sh.dim_h(X(slots[-1][2]), X(x_offset + zone_w), Y(H + tab), yb, fmt(x_offset + zone_w - slots[-1][2]))
    sh.dim_h(X(slots[0][1]), X(slots[-1][2]), Y(H + tab), yb, f"{fmt(slots[-1][2] - slots[0][1])} slit field")
    sh.dim_h(X(0), X(W), Y(H + tab), yb + 8, fmt(W))
    yo = Y(0) - 8
    sh.line(X(0), yo, X(W), yo, "dim")
    sh.text(X(0), yo - 11, "ORDINATE: slit positions from the left edge (cm) - one slit at each end of every loop", "tx")
    sh.line(X(0), yo - 2.5, X(0), yo + 2.5, "dim")
    sh.text(X(0), yo - 1.2, "0", "tx", "middle")
    for lab, a, b in slots:
        for x in (a, b):
            sh.line(X(x), yo - 1.5, X(x), Y(0), "dim")
            sh.text(X(x) + 0.7, yo - 2.2, fmt(x), "tx", "start", rot=-90)
    sh.line(X(W), yo - 2.5, X(W), yo + 2.5, "dim")


def panel_notes():
    return [
        "**PANEL CONSTRUCTION (all four storage surfaces)",
        "1. Face ply 1.0 mm leather with the slits die-cut, over",
        "   0.8 mm board and a 0.6 mm back ply; edge-stitched 0.3",
        "   in contrast thread. Pages: R 1.0 top corners.",
        "2. Elastic: 15 mm knit elastic, matching colour, threaded",
        "   IN and OUT of the face ply through 1.6 slits so each",
        "   pair sits in its own visible loop and the elastic runs",
        "   hidden behind the face between loops (reference photos).",
        "3. Loop (slot) widths are the prototype's: 0.6 for 2.0 mm,",
        "   +0.1 per size step, to 2.2 for 10 mm. 0.5 hidden run",
        "   between loops. One loop holds one PAIR, side by side.",
        "4. Thread the elastic before laminating the face to the",
        "   board. Bar-tack 1.5 at every slit; stitch the two ends",
        "   down under a 1.0 anchor. Elastic cut = slit field + 2.",
        "5. Size labels heat-stamped / printed above each loop",
        "   with a 0.5 leader line to the tip (reference photo).",
        "6. Tip points up; 1.5 clear above the points (prototype).",
    ]


# ==========================================================================
# SHEET 1 - cover: design brief, references, index
# ==========================================================================
def img_data(fn):
    import base64
    mime = "image/png" if fn.lower().endswith(".png") else "image/jpeg"
    with open(os.path.join(HERE, "reference", fn), "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def logo(sh, cx, cy, size):
    """Client logo centred at page (cx, cy), 'size' mm square."""
    sh.add(f'<image x="{cx - size / 2:.2f}" y="{cy - size / 2:.2f}" width="{size:.2f}" height="{size:.2f}" '
           f'href="{img_data("logo.png")}" preserveAspectRatio="xMidYMid meet"/>')


def sheet1():
    sh = Sheet(1, "Cover - design brief, construction summary, reference photos, sheet index", "-")
    sh.frame()
    x0, y0 = 14, 22
    sh.lines(x0, y0, [
        "**DESIGN BRIEF (client, 2026-10-01)",
        "Premium interchangeable knitting-needle case in genuine or faux leather:",
        "structured construction, finished edge stitching, folding side flaps, top flap,",
        "and a leather strap with metal hardware that wraps the whole case. Minimal",
        "and premium in appearance - not a fabric organiser. The case opens fully.",
        "- Snaps hold the front panel to the two folded side flaps.",
        "- The strap closes everything: buckle and keeper are visual, the strap tongue",
        "  snaps to a stud on the front panel. Client logo embossed on the top flap.",
        "",
        "**STORAGE SURFACES - front to back",
        "Front panel  >  Panel 1  >  Panel 2  >  Panel 3  >  Back wall (Panel 4)",
        "- Panels 1-3 are separate leather pages, permanently sewn into the bottom of",
        "  the case, evenly spaced, and able to flip individually like book pages.",
        "  They are NOT removable.",
        "- Panel 4 is the inside back wall of the case itself: the needle loops are",
        "  sewn / threaded directly into the back-wall lining. It also carries the",
        "  large snap pocket for the cables.",
        "- Panel 2 carries two small snap pockets for the accessories.",
        "- Every pair of tips has its own elastic loop, threaded in and out of the",
        "  panel, with the needle size marked above the pair.",
        "",
        "**CONTENTS TO BE HOUSED",
        "34 x 10 cm tips (17 pairs, 2.0-10 mm)   on panels 1 and 2",
        "30 x 5 cm tips (15 pairs, 2.0-8 mm)     on panels 3 and 4",
        "5 cables 25 / 40 / 60 / 80 / 100 cm      back-wall pocket (panel 4)",
        "6 end caps, 4 keys, 3 connectors,        panel 2 pockets",
        "1 leather grip patch (replaces the rubber grip disc)",
        "",
        "**CLOSED SIZE  21.0 x 13.0 x 6.0 cm  (W x H x D, from the cardboard prototype)",
        "",
        "**MATERIALS",
        "Outer: full-grain leather 1.2-1.4 mm, tan (or PU faux leather 1.0-1.2 mm).",
        "Strap: 1.4 mm, dark brown. Lining and pages: 0.6-1.0 mm matching leather.",
        "Hardware: antique brass - 30 mm buckle (decorative), 12.5 mm and 10 mm snaps.",
        "Elastic: 15 mm knit, colour-matched. Thread: bonded polyester, contrast.",
        "",
        "**LOGO (client artwork, right)  blind / heat emboss 2.5 x 2.5 on the top flap,",
        "centred 3.0 from the right edge and 7.0 from the flap top edge (sheet 2).",
        "Vector artwork to be supplied for the emboss die; raster shown for placement.",
        "",
        "**TOP FLAP 10.0 deep, as in the reference photos (client decision); the cardboard",
        "prototype measured 5.0. Pockets sized to the maximum that leaves the needle",
        "zones intact: cable pocket 9.7 x 9.0, accessory pockets 3.9 x 4.1 (sheets 5, 7).",
        "",
        "**SHEET INDEX",
        "1  Cover (this sheet)",
        "2  Outer shell - flat pattern, outer face",
        "3  Assembly - closed views, section, open layout, closing sequence",
        "4  Panel 1 (page): 10 cm tips 2.0-5.0 mm",
        "5  Panel 2 (page): 10 cm tips 5.5-10 mm + two accessory pockets",
        "6  Panel 3 (page): 5 cm tips 2.0-5.0 mm",
        "7  Panel 4 (back wall): 5 cm tips 5.5-8 mm + cable pocket",
        "8  Details: strap, elastic threading, page hinge, pockets",
        "9  Contents checklist, bill of materials, construction",
    ], "ts", 3.75)
    logo(sh, 178, 160, 26)
    sh.rect(163, 145, 30, 30, "thin")
    # reference photos, 2 x 3 grid
    gx, gy = 218, 22
    sh.text(gx, gy, "REFERENCE PHOTOS (client-supplied; construction and appearance target)", "tb")
    refs = [("R1-exterior-closed.jpg", "R1  Exterior closed - strap, buckle, keeper, snap, logo", 800, 533),
            ("R3-front-and-open.jpg", "R3  Closed front / open with pages", 800, 1362),
            ("R2-open-handheld.jpg", "R2  Pages fanned from the bottom gusset", 800, 1066),
            ("R4-panel1-2.0-5.0.jpg", "R4  Panel 1 - 2.0-5.0 mm, elastic loops, labels", 800, 666),
            ("R5-panel2-5.5-10-pockets.jpg", "R5  Panel 2 - 5.5-10 mm + two small snap pockets", 800, 533),
            ("R6-backwall-5.5-8-pocket.jpg", "R6  Back wall - 5.5-8 mm + large snap pocket", 800, 640)]
    cw, ch = 60.0, 60.0
    for i, (fn, cap, w, h) in enumerate(refs):
        col, row = i % 3, i // 3
        cx0, cy0 = gx + col * 64, gy + 4 + row * 72
        scale = min(cw / w, ch / h)
        iw, ih = w * scale, h * scale
        ix, iy = cx0 + (cw - iw) / 2, cy0 + (ch - ih) / 2
        sh.add(f'<image x="{ix:.2f}" y="{iy:.2f}" width="{iw:.2f}" height="{ih:.2f}" href="{img_data(fn)}" preserveAspectRatio="xMidYMid meet"/>')
        sh.rect(ix, iy, iw, ih, "thin")
        sh.text(cx0, cy0 + ch + 3.5, cap, "tx")
    sh.lines(gx, gy + 4 + 2 * 72 + 4, [
        "**HOW THE DRAWINGS RELATE TO THE BRIEF",
        "- Dimensions come from the client's cardboard prototype (21.0 x 13.0 base, 6.0",
        "  gussets, 8.0 side flaps, loop widths 0.6-2.2) - see the record on sheet 9.",
        "- Construction follows the reference photos R1-R6. Where the photos and the",
        "  prototype differed (top flap depth) the client chose the photo value, 10.0.",
        "- Sheets 4-7 are full size (1:1): print at 100 % for slit-cutting templates.",
        "- Open questions for the factory / client are listed on sheet 3.",
    ], "ts", 3.75)
    return sh


# ==========================================================================
# SHEET 2 - outer shell flat pattern (outer face up)
# ==========================================================================
def sheet2():
    sh = Sheet(2, "Outer shell - flat pattern, outer face (die line)", "1:2")
    sh.frame()
    s = 5.0
    v = View(28, 38, s)
    X, Y, L = v.X, v.Y, v.L
    xa = END_FLAP
    xb = END_FLAP + SIDE_WALL
    xc = xb + BASE_W
    xd = xc + SIDE_WALL
    ya = REAR_FLAP
    yb = ya + REAR_WALL
    yc = yb + BASE_H
    yd = yc + FRONT_WALL
    sh.rect(X(xb), Y(0), L(BASE_W), L(PATTERN_H), "leather")
    sh.rect(X(0), Y(yb), L(PATTERN_W), L(BASE_H), "leather")
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

    cx = xb + BASE_W / 2
    # strap stitched on back wall + top gusset + top flap; tongue continues beyond the flap edge
    sh.rect(X(cx - STRAP_W / 2), Y(0), L(STRAP_W), L(yc), "strap")
    sh.rect(X(cx - STRAP_W / 2 + 0.3), Y(0.3), L(STRAP_W - 0.6), L(yc - 0.6), "stitch")
    sh.text(X(cx) + 10, Y(yb + 10.5), "STRAP 3.0 wide, dark brown, stitched 0.3 from edges", "ts", "middle", rot=-90)
    # decorative buckle + keeper on the strap over the top flap
    sh.rect(X(cx - STRAP_W / 2), Y(BUCKLE_ON_FLAP - 1.5), L(STRAP_W), L(4.5), "strap")
    buckle(sh, X(cx), Y(BUCKLE_ON_FLAP), L(STRAP_W + 0.6))
    sh.rect(X(cx - STRAP_W / 2 - 0.2), Y(KEEPER_ON_FLAP - 0.35), L(STRAP_W + 0.4), L(0.7), "strap")
    sh.text(X(cx) - 11, Y(BUCKLE_ON_FLAP) + 1, "buckle 30 mm (decorative)", "tx", "end")
    sh.text(X(cx) - 11, Y(KEEPER_ON_FLAP) + 1, "keeper", "tx", "end")
    sh.text(X(cx), Y(0) - 1.5, "tongue continues 3.0 beyond this edge; snap socket 1.0 from the edge - sheet 8", "tx", "middle")
    # logo on the top flap
    logo(sh, X(xc - 3.0), Y(LOGO_FROM_TOP), L(2.5))
    sh.rect(X(xc - 3.0 - 1.25), Y(LOGO_FROM_TOP - 1.25), L(2.5), L(2.5), "thin")
    sh.text(X(xc - 3.0), Y(LOGO_FROM_TOP) + 10, "LOGO emboss 2.5 sq", "tx", "middle")
    sh.dim_v(Y(0), Y(LOGO_FROM_TOP), X(xc - 3.0), X(xc) + 15, fmt(LOGO_FROM_TOP) + " logo")
    sh.dim_h(X(xc - 3.0), X(xc), Y(LOGO_FROM_TOP), Y(LOGO_FROM_TOP) + 18, "3.0", ext=False)
    # strap stud on the front panel outer face
    st_y = PATTERN_H - STRAP_STUD_FROM_TOP
    sh.snap_cap(X(cx), Y(st_y), 3.0)
    sh.text(X(cx), Y(st_y) - 5, "STRAP STUD (outer face) - tongue snaps here", "tx", "middle")
    sh.line(X(xb), Y(PATTERN_H - REAR_FLAP), X(xc), Y(PATTERN_H - REAR_FLAP), "hid")
    sh.text(X(xc) - 2, Y(PATTERN_H - REAR_FLAP) - 1.2, "top-flap edge when closed", "tx", "end")

    def lab(x, y, a, b=None):
        sh.text(X(x), Y(y), a, "tb", "middle")
        if b:
            sh.text(X(x), Y(y) + 4, b, "ts", "middle")
    lab(xb + 4.5, REAR_FLAP - 2.2, "TOP FLAP", f"21.0 x {fmt(REAR_FLAP)}")
    lab(xb + 4.5, ya + REAR_WALL / 2 + 0.3, "TOP GUSSET", "21.0 x 6.5")
    lab(xb + 4.5, yb + BASE_H / 2 - 0.3, "BACK WALL", "21.0 x 13.0 (panel 4 inside)")
    lab(cx, yc + FRONT_WALL / 2 + 0.3, "BOTTOM GUSSET - page hinge seams inside", "21.0 x 6.0")
    lab(xb + 4.5, yd + 8.5, "FRONT PANEL", "21.0 x 12.7")
    sh.text(X(xa + SIDE_WALL / 2) + 1.2, Y(yb + 1.2), "SIDE GUSSET 5.7 x 13.0", "ts", "end", rot=-90)
    sh.text(X(xc + SIDE_WALL / 2) + 1.2, Y(yb + 1.2), "SIDE GUSSET 5.7 x 13.0", "ts", "end", rot=-90)
    lab(END_FLAP / 2, yb + 2.2, "SIDE FLAP (L)", "8.0 x 13.0 - tucks inside")
    lab(xd + END_FLAP / 2, yb + 2.2, "SIDE FLAP (R)", "8.0 x 13.0 - tucks inside")
    sxl, sxr, sy = xa - SNAP_FROM_FOLD, xd + SNAP_FROM_FOLD, yb + SNAP_FROM_TOP
    sh.snap_cap(X(sxl), Y(sy), 3.0)
    sh.snap_cap(X(sxr), Y(sy), 3.0)
    sh.text(X(sxl), Y(sy) + 7.5, "SNAP STUD (outer face)", "tx", "middle")
    sh.text(X(sxr), Y(sy) + 7.5, "SNAP STUD (outer face)", "tx", "middle")
    sock_y = yd + SNAP_FROM_TOP
    for sx in (xb + SNAP_FROM_FOLD, xc - SNAP_FROM_FOLD):
        sh.snap_stud(X(sx), Y(sock_y), 3.0)
    sh.text(X(xb + SNAP_FROM_FOLD), Y(sock_y) - 5, "SOCKET, inner face (hidden)", "tx", "middle")
    sh.text(X(xc - SNAP_FROM_FOLD), Y(sock_y) - 5, "SOCKET, inner face (hidden)", "tx", "middle")

    yt = Y(0) - 7
    for a, b, t in [(0, xa, "8.0"), (xa, xb, "5.7"), (xb, xc, "21.0"), (xc, xd, "5.7"), (xd, PATTERN_W, "8.0")]:
        sh.dim_h(X(a), X(b), Y(yb) if (a < xb or b > xc) else Y(0), yt, t)
    sh.dim_h(X(0), X(PATTERN_W), Y(yb), yt - 7, fmt(PATTERN_W) + "  OVERALL")
    xr = X(PATTERN_W) + 8
    for a, b, t in [(0, ya, fmt(REAR_FLAP)), (ya, yb, "6.5"), (yb, yc, "13.0"), (yc, yd, "6.0"), (yd, PATTERN_H, "12.7")]:
        sh.dim_v(Y(a), Y(b), X(PATTERN_W) if (a >= yb and b <= yc) else X(xc), xr, t)
    sh.dim_v(Y(0), Y(PATTERN_H), X(PATTERN_W), xr + 8, fmt(PATTERN_H) + "  OVERALL")
    sh.dim_h(X(sxl), X(xa), Y(sy), Y(yc) + 5, "5.0")
    sh.dim_v(Y(yb), Y(sy), X(sxl), X(0) - 5, "6.5")
    sh.text(X(0), Y(yc) + 12, "(R) side flap: snap position symmetrical", "tx")
    sh.dim_h(X(xb), X(xb + SNAP_FROM_FOLD), Y(sock_y), Y(PATTERN_H) + 5, "5.0")
    sh.dim_h(X(xc - SNAP_FROM_FOLD), X(xc), Y(sock_y), Y(PATTERN_H) + 5, "5.0")
    sh.dim_v(Y(yd), Y(sock_y), X(xb), X(xb) - 5, "6.5")
    sh.dim_v(Y(st_y), Y(PATTERN_H), X(cx), X(xc) + 3, fmt(STRAP_STUD_FROM_TOP) + " stud")
    sh.dim_v(Y(0), Y(BUCKLE_ON_FLAP), X(cx + STRAP_W / 2), X(xc) + 8, fmt(BUCKLE_ON_FLAP))
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
    sh.line(nx, ny + 15, nx + 14, ny + 15, "hid"); sh.text(nx + 17, ny + 16, "Hidden (far face / when closed)", "ts")
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
        "   them and snaps to the side flaps, top flap folds down,",
        "   strap tongue snaps to the front panel.",
        "   Pages 1-3 are sewn into the bottom gusset; the back",
        "   wall lining is storage panel 4 (sheet 7).",
        "4. Gusset depths as measured: 5.7 (sides), 6.0 (bottom),",
        "   6.5 (top). Keep as measured (Q1, sheet 3).",
        "5. Strap: stitched to the back wall, top gusset and top",
        "   flap; 30 mm buckle and keeper on the flap are visual",
        "   only. The tongue (3.0 beyond the flap) snaps to a stud",
        "   on the front panel 11.0 below the top. Side-flap snaps:",
        "   12.5 mm, studs outer face, sockets front-panel inner",
        "   face - they hold the front panel to the side flaps.",
        "6. Outer: full-grain leather 1.2-1.4 mm (or PU 1.0-1.2),",
        "   tan; strap dark brown. Board 1.0 mm in back wall and",
        "   front panel; lining 0.6 mm, same tan (reference).",
        "7. Top flap 10.0 as in the reference photos (client,",
        "   2026-10-01); the prototype measured 5.0 - superseded.",
    ], "ts", 3.9)
    return sh


# ==========================================================================
# SHEET 3 - assembly
# ==========================================================================
def sheet3():
    sh = Sheet(3, "Assembly - closed views, section, open layout, closing sequence", "1:2 / 1:1 / 1:4 as noted")
    sh.frame()
    s = 5.0
    D = 6.0
    v = View(30, 40, s)
    X, Y, L = v.X, v.Y, v.L
    sh.text(X(0), Y(0) - 14, "FRONT VIEW - closed (1:2)", "tb")
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, 0, 0, BASE_W, BASE_H, R)}" class="leather"/>')
    sh.line(X(0), Y(REAR_FLAP), X(BASE_W), Y(REAR_FLAP), "cut")
    sh.add(f'<path d="{rounded_rect_path(X, Y, L, 0.3, 0.3, BASE_W - 0.6, BASE_H - 0.6, R - 0.3)}" class="stitch"/>')
    cx = BASE_W / 2
    sh.rect(X(cx - STRAP_W / 2), Y(0), L(STRAP_W), L(STRAP_STUD_FROM_TOP + 0.5), "strap")
    sh.poly([(X(cx - STRAP_W / 2), Y(STRAP_STUD_FROM_TOP + 0.5)), (X(cx + STRAP_W / 2), Y(STRAP_STUD_FROM_TOP + 0.5)), (X(cx), Y(STRAP_STUD_FROM_TOP + 1.8))], "strap")
    sh.rect(X(cx - STRAP_W / 2), Y(BUCKLE_ON_FLAP - 1.5), L(STRAP_W), L(4.5), "strap")
    buckle(sh, X(cx), Y(BUCKLE_ON_FLAP), L(STRAP_W + 0.6))
    sh.rect(X(cx - STRAP_W / 2 - 0.2), Y(KEEPER_ON_FLAP - 0.35), L(STRAP_W + 0.4), L(0.7), "strap")
    sh.circle(X(cx), Y(STRAP_STUD_FROM_TOP), 2.2, "brass")
    sh.text(X(cx) + 4, Y(STRAP_STUD_FROM_TOP) + 1, "snap", "tx")
    sh.text(X(cx) - 11, Y(BUCKLE_ON_FLAP) + 1, "buckle + keeper (visual)", "tx", "end")
    logo(sh, X(BASE_W - 3.0), Y(LOGO_FROM_TOP), L(2.5))
    sh.text(X(1.5), Y(2.8), "top flap 10.0", "tx")
    sh.text(X(1.5), Y(11.8), "front panel", "tx")
    sh.dim_h(X(0), X(BASE_W), Y(0), Y(0) - 6, "21.0")
    sh.dim_v(Y(0), Y(BASE_H), X(BASE_W), X(BASE_W) + 7, "13.0")
    sh.dim_v(Y(0), Y(REAR_FLAP), X(0), X(0) - 7, fmt(REAR_FLAP))
    sh.dim_v(Y(0), Y(STRAP_STUD_FROM_TOP), X(0), X(0) - 14, f"{fmt(STRAP_STUD_FROM_TOP)} to snap")

    v2 = View(155, 40, s)
    sh.text(v2.X(0), v2.Y(0) - 14, "BACK VIEW - closed (1:2)", "tb")
    sh.add(f'<path d="{rounded_rect_path(v2.X, v2.Y, v2.L, 0, 0, BASE_W, BASE_H, R)}" class="leather"/>')
    sh.rect(v2.X(cx - STRAP_W / 2), v2.Y(0), v2.L(STRAP_W), v2.L(BASE_H), "strap")
    sh.rect(v2.X(cx - STRAP_W / 2 + 0.3), v2.Y(0.3), v2.L(STRAP_W - 0.6), v2.L(BASE_H - 0.6), "stitch")
    sh.text(v2.X(cx) + 6, v2.Y(BASE_H - 0.8), "strap stitched full height of back", "tx", rot=-90)
    sh.dim_h(v2.X(cx - STRAP_W / 2), v2.X(cx + STRAP_W / 2), v2.Y(BASE_H), v2.Y(BASE_H) + 6, "3.0", ext=False)

    v3 = View(272, 40, s)
    sh.text(v3.X(0), v3.Y(0) - 14, "END VIEW (1:2)", "tb")
    sh.add(f'<path d="{rounded_rect_path(v3.X, v3.Y, v3.L, 0, 0, D, BASE_H, 0.6)}" class="leather"/>')
    sh.line(v3.X(0), v3.Y(REAR_FLAP), v3.X(D), v3.Y(REAR_FLAP), "thin")
    sh.dim_h(v3.X(0), v3.X(D), v3.Y(BASE_H), v3.Y(BASE_H) + 6, "6.0")

    # ---- SECTION A-A 1:1 ----
    v4 = View(40, 126, 10.0)
    X4, Y4, L4 = v4.X, v4.Y, v4.L
    sh.text(X4(0) - 10, Y4(0) - 11, "SECTION A-A - vertical through the centre, closed (1:1)", "tb")
    sh.text(X4(0) - 10, Y4(0) - 7, "Front to back: front panel > P1 > P2 > P3 > back wall (P4). Pages hinge on evenly spaced seams in the bottom gusset.", "ts")
    t = 0.25
    sh.rect(X4(-t), Y4(0), L4(t), L4(BASE_H), "leather")
    sh.rect(X4(-t), Y4(BASE_H), L4(FRONT_WALL + t), L4(t), "leather")
    sh.rect(X4(FRONT_WALL - t), Y4(BASE_H - LID_H), L4(t), L4(LID_H), "leather")
    sh.rect(X4(-t), Y4(-t), L4(REAR_WALL + t), L4(t), "leather")
    sh.rect(X4(REAR_WALL - t), Y4(-t), L4(t), L4(REAR_FLAP + t), "leather")
    sh.rect(X4(REAR_WALL), Y4(-t), L4(0.15), L4(REAR_FLAP + TONGUE_FREE - 0.5), "strap")
    sh.rect(X4(-t - 0.15), Y4(0), L4(0.15), L4(BASE_H), "strap")
    sh.rect(X4(REAR_WALL - 0.1), Y4(BUCKLE_ON_FLAP - 0.6), L4(0.45), L4(1.2), "brass")
    sh.text(X4(REAR_WALL) + 6, Y4(BUCKLE_ON_FLAP + 0.2), "buckle (visual)", "tx")
    sh.circle(X4(REAR_WALL + 0.1), Y4(STRAP_STUD_FROM_TOP), 1.2, "brass")
    sh.text(X4(REAR_WALL) + 6, Y4(STRAP_STUD_FROM_TOP) + 1, "strap snap", "tx")
    sh.text(X4(REAR_WALL) + 4, Y4(2.5), "top flap", "tx")
    sh.text(X4(FRONT_WALL) + 4, Y4(11.5), "front panel", "tx")
    sh.text(X4(-t) - 5, Y4(6.5), "back wall = panel 4", "tx", "middle", rot=-90)
    # back wall storage: elastic loop + 5 cm tips + big pocket
    sh.rect(X4(0), Y4(BASE_H - 12.0), L4(0.15), L4(9.0), "band")
    sh.text(X4(0) + 3.2, Y4(BASE_H - 7.0), "pocket", "tx", rot=-90)
    sh.rect(X4(0.15), Y4(3.75), L4(0.8), L4(5.0), "needle")
    for i, sp in enumerate(SEAMS):
        xtop = sp + 0.12 * i - 0.1
        sh.line(X4(sp), Y4(BASE_H), X4(xtop), Y4(BASE_H - PAGE_H), "cut")
        sh.line(X4(sp) + 0.5, Y4(BASE_H) - 1.5, X4(sp) + 0.5, Y4(BASE_H) + 4, "stitch")
        sh.text(X4(xtop), Y4(BASE_H - PAGE_H) - 1.5, f"P{3 - i}", "tx", "middle")
        ln = 10 if i >= 1 else 5
        top = BASE_H - PAGE_H + (1.5 if i >= 1 else 3.75)
        dia = (0.5, 1.0, 0.5)[i]
        sh.rect(X4(xtop) + 0.3, Y4(top), L4(dia), L4(ln), "needle")
    yd = Y4(BASE_H + t) + 7
    sh.dim_h(X4(0), X4(SEAMS[0]), Y4(BASE_H + t), yd, fmt(SEAMS[0]))
    for a, b in zip(SEAMS, SEAMS[1:]):
        sh.dim_h(X4(a), X4(b), Y4(BASE_H + t), yd, fmt(b - a))
    sh.dim_h(X4(SEAMS[-1]), X4(FRONT_WALL), Y4(BASE_H + t), yd, fmt(FRONT_WALL - SEAMS[-1]))
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
    for i in range(3):
        off = 0.4 * (2 - i)
        sh.rect(Xi(xb + 0.5), Yi(yc - PAGE_H - off), Li(PAGE_W), Li(PAGE_H), "band")
    sh.text(Xi(xb + BASE_W / 2), Yi(yc - 6.0), "P1 (front page) over P2, P3", "ts", "middle")
    sh.text(Xi(xb + BASE_W / 2), Yi(yc - 3.0), "back wall (P4) with cable pocket behind P3", "tx", "middle")
    sh.text(Xi(xb + BASE_W / 2), Yi(yc + FRONT_WALL / 2) + 1, "3 page hinge seams in bottom gusset", "tx", "middle")
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

    fx, fy = 312, 22
    sh.lines(fx, fy, [
        "**OPENING / CLOSING",
        "Open: unsnap the strap tongue, lift the top",
        "flap, fold the front panel down (its snaps",
        "release from the side flaps), fold the side",
        "flaps out. The case lies flat and the three",
        "pages flip like a book; the back wall is the",
        "fourth storage surface.",
        "Close: side flaps in over the pages, front",
        "panel up and snap to the side flaps, top",
        "flap over, strap tongue snaps to the front.",
        "",
        "**STACK-HEIGHT CHECK (depth 6.0)",
        "P4 back wall: 8 mm tips / cable pocket  1.3",
        "P3  2 x 5 mm tips + page                0.7",
        "P2  2 x 10 mm tips + page + pockets     1.3",
        "P1  2 x 5 mm tips + page                0.7",
        "front + back walls, side flaps          0.9",
        "TOTAL                                   4.9  (OK)",
        "",
        "**OPEN QUESTIONS (confirm before cutting)",
        "Q1 Keep gussets 5.7 / 6.0 / 6.5 as measured?",
        "Q2 (closed) Top flap 10.0 per the reference",
        "   photos, agreed 2026-10-01.",
        "Q3 Side-flap snaps: spring snaps (drawn) or",
        "   hidden magnetic snaps?",
        "Q4 Genuine (full-grain 1.2-1.4) or PU faux",
        "   leather for the shell?",
        "Q5 Confirm real cap / key / connector / cable",
        "   sizes against the pockets on sheets 5, 7.",
    ], "ts", 3.85)
    return sh


# ==========================================================================
# SHEETS 4-7 - storage panels
# ==========================================================================
def page_sheet(n, title, sizes, tip_len, tip_top, band_c, table_title):
    sh = Sheet(n, title, "1:1")
    sh.frame()
    v = View(32, 48, 10.0)
    margin, slots = draw_panel(sh, v, sizes, tip_len, tip_top, band_c)
    panel_dims(sh, v, slots, margin, tip_len, tip_top, band_c)
    sh.text(v.X(PAGE_W / 2), v.Y(PAGE_H + HINGE_TAB) + 27,
            f"{title.split(':')[0].upper()} - page 20.0 x 12.5 + 1.5 hinge tab. Full size 1:1 - use as slit template.", "tb", "middle")
    tx = 258
    sh.text(tx, 22, table_title, "tb")
    end = slot_table(sh, tx, 25, slots, sizes, tip_len)
    sh.lines(tx, end + 6, panel_notes(), "ts", 3.7)
    return sh, v, slots, end


def sheet4():
    sh, *_ = page_sheet(4, "Panel 1 (page): 10 cm tips 2.0-5.0 mm (11 pairs)", SIZES_SMALL, 10.0, 1.5, 6.5,
                        "LOOP TABLE - panel 1 (slit positions from the left edge, cm)")
    return sh


def sheet5():
    sh = Sheet(5, "Panel 2 (page): 10 cm tips 5.5-10 mm (6 pairs) + two accessory snap pockets", "1:1")
    sh.frame()
    v = View(32, 48, 10.0)
    X, Y, L = v.X, v.Y, v.L
    tip_len, tip_top, band_c = 10.0, 1.5, 6.5
    pw, pf, ph = 3.9, 1.6, 4.1
    px = 0.5
    pa_y, pb_y = 0.5, 6.4
    zone_x = px + pw + 0.6          # 5.0
    zone_w = PAGE_W - zone_x        # 15.0
    margin, slots = draw_panel(sh, v, SIZES_LARGE10, tip_len, tip_top, band_c, x_offset=zone_x, zone_w=zone_w)
    snap_pocket(sh, v, px, pa_y, pw, ph, pf, "POCKET A", "caps + keys", r=0.5, snap_r=2.2)
    snap_pocket(sh, v, px, pb_y, pw, ph, pf, "POCKET B", "connectors + patch", r=0.5, snap_r=2.2)
    panel_dims(sh, v, slots, margin, tip_len, tip_top, band_c, x_offset=zone_x, zone_w=zone_w)
    yb = Y(PAGE_H + HINGE_TAB) + 8
    sh.dim_h(X(0), X(px), Y(PAGE_H + HINGE_TAB), yb, "0.5", ext=False)
    sh.dim_h(X(px), X(px + pw), Y(PAGE_H + HINGE_TAB), yb, "3.9")
    sh.dim_h(X(px + pw), X(zone_x), Y(PAGE_H + HINGE_TAB), yb, "0.6", ext=False)
    xp = X(px + pw) + 4
    sh.dim_v(Y(0), Y(pa_y), X(px + pw), xp, "0.5", ext=False)
    sh.dim_v(Y(pa_y), Y(pa_y + pf), X(px + pw), xp, "1.6")
    sh.dim_v(Y(pa_y + pf), Y(pa_y + pf + ph), X(px + pw), xp, "4.1")
    sh.dim_v(Y(pa_y + pf + ph), Y(pb_y), X(px + pw), xp, "0.2", ext=False)
    sh.dim_v(Y(pb_y), Y(pb_y + pf), X(px + pw), xp, "1.6")
    sh.dim_v(Y(pb_y + pf), Y(pb_y + pf + ph), X(px + pw), xp, "4.1")
    sh.dim_v(Y(pb_y + pf + ph), Y(PAGE_H), X(px + pw), xp, "0.4", ext=False)
    sh.text(X(PAGE_W / 2), Y(PAGE_H + HINGE_TAB) + 27, "PANEL 2 - page 20.0 x 12.5 + 1.5 hinge tab. Full size 1:1 - use as slit template.", "tb", "middle")
    tx = 258
    sh.text(tx, 22, "LOOP TABLE - panel 2 (slit positions from the left edge, cm)", "tb")
    end = slot_table(sh, tx, 25, slots, SIZES_LARGE10, 10)
    sh.lines(tx, end + 6, [
        "**PANEL 2 LAYOUT (reference photo R5)",
        "- Two small patch pockets at the left, stacked, as large",
        "  as the page allows beside the 15.0 needle zone: body",
        "  3.9 x 4.1, flap 3.9 x 1.6 with a 10 mm brass snap,",
        "  edge-stitched. Body cut 3.9 x 4.6 (0.5 under the flap).",
        "  Pocket A: 6 end caps + 4 keys. Pocket B: 3 connectors",
        "  + the folded leather grip patch (6.0 x 3.0, folds to 3.0).",
        "- Needle zone 15.0 wide: 6 pairs 5.5-10 mm, loop widths",
        "  1.7-2.2, slit field 14.2 centred (0.4 margins).",
        "- The 10 mm pair is the thickest item in the case (1.0).",
        "",
    ] + panel_notes(), "ts", 3.7)
    return sh


def sheet6():
    sh, v, slots, end = page_sheet(6, "Panel 3 (page): 5 cm tips 2.0-5.0 mm (11 pairs)", SIZES_SMALL, 5.0, 3.75, 6.25,
                                   "LOOP TABLE - panel 3 (slit positions from the left edge, cm)")
    sh.lines(258, end + 6 + 17 * 3.7 + 4, [
        "**PANEL 3 NOTE",
        "- Same loop widths and slit positions as panel 1, so",
        "  the two pages share one slit-cutting template.",
        "- 5 cm tips sit centred on the page (reference photo):",
        "  points 3.75 from the top, elastic centred at 6.25.",
    ], "ts", 3.7)
    return sh


def sheet7():
    sh = Sheet(7, "Panel 4 (back wall): 5 cm tips 5.5-8 mm (4 pairs) + large cable snap pocket", "1:1")
    sh.frame()
    v = View(30, 48, 10.0)
    X, Y, L = v.X, v.Y, v.L
    tip_len, tip_top, band_c = 5.0, 4.0, 6.5
    pw, pf, ph = 9.7, 3.0, 9.0
    px, py = 0.5, 0.5
    zone_x = px + pw + 0.6          # 10.8
    zone_w = BASE_W - zone_x        # 10.2
    margin, slots = draw_panel(sh, v, SIZES_LARGE5, tip_len, tip_top, band_c, x_offset=zone_x, zone_w=zone_w, backwall=True)
    snap_pocket(sh, v, px, py, pw, ph, pf, "CABLE POCKET", "5 cables coiled to <= 6.5 dia")
    sh.text(X(px + pw / 2), Y(py + pf + ph / 2) + 6.5, "body 9.7 x 9.0, flap 9.7 x 3.0", "tx", "middle")
    sh.text(X(px + pw / 2), Y(py + pf + ph / 2) + 9.5, "12.5 mm brass snap", "tx", "middle")
    panel_dims(sh, v, slots, margin, tip_len, tip_top, band_c, x_offset=zone_x, zone_w=zone_w, backwall=True)
    yb = Y(BASE_H) + 8
    sh.dim_h(X(0), X(px), Y(BASE_H), yb, "0.5", ext=False)
    sh.dim_h(X(px), X(px + pw), Y(BASE_H), yb, "9.7 pocket")
    sh.dim_h(X(px + pw), X(zone_x), Y(BASE_H), yb, "0.6", ext=False)
    xp = X(px + pw) + 5
    sh.dim_v(Y(0), Y(py), X(px + pw), xp, "0.5", ext=False)
    sh.dim_v(Y(py), Y(py + pf), X(px + pw), xp, "3.0 flap")
    sh.dim_v(Y(py + pf), Y(py + pf + ph), X(px + pw), xp, "9.0 body")
    sh.dim_v(Y(py + pf + ph), Y(BASE_H), X(px + pw), xp, "0.5", ext=False)
    sh.text(X(BASE_W / 2), Y(BASE_H) + 27, "PANEL 4 - BACK-WALL LINING 21.0 x 13.0 (inner face of the back wall; not a loose page). Full size 1:1 - use as slit template.", "tb", "middle")
    tx = 258
    sh.text(tx, 22, "LOOP TABLE - panel 4 (slit positions from the left edge, cm)", "tb")
    end = slot_table(sh, tx, 25, slots, SIZES_LARGE5, 5)
    sh.lines(tx, end + 6, [
        "**PANEL 4 - BACK WALL (reference photo R6)",
        "- This is the lining ply of the back wall, 21.0 x 13.0:",
        "  the loops and the pocket are made on it BEFORE it is",
        "  laminated to the board and outer shell, so the hidden",
        "  elastic runs lie between lining and board.",
        "- Cable pocket at the left, as large as the wall allows",
        "  beside the needle zone: patch pocket 9.7 x 9.0 with a",
        "  3.0 flap and 12.5 mm brass snap. Body cut 9.7 x 9.5.",
        "  Holds the 5 cables, each coiled to 6.5 cm or less.",
        "- Needle zone 10.2 wide: 4 pairs 5.5 / 6 / 7 / 8 mm, loop",
        "  widths 1.7-2.0, slit field 8.9 centred (0.65 margins).",
        "- 5 cm tips: points 4.0 from the top, elastic centred at",
        "  6.5 (level with panels 1-2).",
        "",
    ] + panel_notes(), "ts", 3.7)
    return sh


# ==========================================================================
# SHEET 8 - details
# ==========================================================================
def elastic_detail(sh, x, y, label="DETAIL A - elastic threaded through the face ply, section, 2:1"):
    v = View(x, y, 20.0)
    X, Y, L = v.X, v.Y, v.L
    sh.text(X(0), Y(0) - 3, label, "tb")
    face_y, face_t = 1.2, 0.1
    board_t, back_t = 0.08, 0.06
    # layers: face ply, board, back ply
    sh.rect(X(0), Y(face_y), L(5.2), L(face_t), "leather")
    sh.rect(X(0), Y(face_y + face_t), L(5.2), L(board_t), "hatch")
    sh.rect(X(0), Y(face_y + face_t), L(5.2), L(board_t), "thin")
    sh.rect(X(0), Y(face_y + face_t + board_t), L(5.2), L(back_t), "leather")
    # two loops: slot 1 (w=1.0) and slot 2 (w=1.3) with 0.5 hidden run
    d = 0.4
    loops = [(0.9, 1.0), (2.4, 1.3)]
    pts = [(X(0.4), Y(face_y + face_t))]
    for i, (xa, w) in enumerate(loops):
        pts.append((X(xa), Y(face_y + face_t)))      # under face up to slit
        n = 20
        for k in range(n + 1):
            tt = k / n
            pts.append((X(xa + tt * w), Y(face_y - math.sin(tt * math.pi) * (d + 0.05))))
        pts.append((X(xa + w), Y(face_y + face_t)))
    pts.append((X(4.6), Y(face_y + face_t)))
    sh.poly(pts, "cut", close=False)
    sh.add(f'<path d="M{X(0.4):.2f},{Y(face_y + face_t):.2f} L{X(4.6):.2f},{Y(face_y + face_t):.2f}" class="dim"/>')
    for xa, w in loops:
        for xx in (xa, xa + w):
            sh.line(X(xx), Y(face_y) - 0.5, X(xx), Y(face_y + face_t) + 0.5, "cut", 'stroke-width="1.2"')
        for cxn in (xa + w / 2 - d / 2 - 0.02, xa + w / 2 + d / 2 + 0.02):
            sh.circle(X(cxn), Y(face_y - d / 2), L(d / 2), "needle")
    sh.dim_h(X(loops[0][0]), X(loops[0][0] + loops[0][1]), Y(face_y + 0.3), Y(face_y + 0.3) + 8, "loop w (table)")
    sh.dim_h(X(loops[0][0] + loops[0][1]), X(loops[1][0]), Y(face_y + 0.3), Y(face_y + 0.3) + 8, "0.5", ext=False)
    sh.text(X(loops[0][0] + loops[0][1] + 0.25), Y(face_y + 0.3) + 11.5, "hidden run", "tx", "middle")
    sh.leader(X(loops[1][0] + loops[1][1] / 2), Y(face_y - d - 0.05), X(loops[1][0] + loops[1][1] / 2) + 10, Y(0.3), "visible loop over 1 pair")
    sh.leader(X(loops[0][0]), Y(face_y + face_t / 2), X(loops[0][0]) - 6, Y(0.5), "slit 1.6 through face ply only, bar-tacked", anchor="start")
    sh.leader(X(4.4), Y(face_y + face_t + board_t / 2), X(4.4) + 4, Y(face_y) + 12, "0.8 mm board", anchor="start")
    sh.leader(X(3.9), Y(face_y + face_t / 2), X(3.9) + 4, Y(face_y) + 17, "face ply 1.0 mm (elastic behind it between loops)", anchor="start")
    sh.leader(X(0.5), Y(face_y + face_t), X(0.5) - 2, Y(face_y) + 22, "elastic anchor: stitched 1.0 at each end", anchor="start")


def sheet8():
    sh = Sheet(8, "Details - strap, elastic threading, page hinge, pockets", "1:2 / 2:1 as noted")
    sh.frame()
    # ---- STRAP 1:2 ----
    v = View(22, 34, 5.0)
    X, Y, L = v.X, v.Y, v.L
    free = TONGUE_FREE
    total = 1.0 + BASE_H + REAR_WALL + REAR_FLAP + free
    sh.text(X(0), Y(0) - 11.5, "DETAIL B - STRAP, flat, 1:2 (dark brown leather 1.4 mm, 2 ply, edge-stitched 0.3)", "tb")
    tip_len = 1.5
    body = total - tip_len
    sh.poly([(X(0), Y(0)), (X(body), Y(0)), (X(total), Y(STRAP_W / 2)), (X(body), Y(STRAP_W)), (X(0), Y(STRAP_W))], "strap")
    sh.line(X(0.3), Y(0.3), X(body), Y(0.3), "stitch")
    sh.line(X(0.3), Y(STRAP_W - 0.3), X(body), Y(STRAP_W - 0.3), "stitch")
    z = [(0, 1.0, "anchor"), (1.0, 14.0, "back wall (stitched)"), (14.0, 20.5, "top gusset"), (20.5, 30.5, "top flap (buckle + keeper here)"), (30.5, total, "tongue")]
    for a, bb, t in z:
        sh.line(X(a), Y(0) - 1, X(a), Y(STRAP_W) + 1, "fold")
        sh.text(X((a + bb) / 2), Y(STRAP_W) + 4, t, "tx", "middle")
    sock = 30.5 + SNAP_FROM_FLAP_EDGE
    sh.circle(X(sock), Y(STRAP_W / 2), 2.0, "brass")
    sh.circle(X(sock), Y(STRAP_W / 2), 0.9, "thin")
    for hx in (sock - 4.0, sock - 5.2):
        sh.circle(X(hx), Y(STRAP_W / 2), L(0.2), "cut")
    sh.text(X(sock), Y(0) - 7, "snap socket, inner face", "tx", "middle")
    sh.text(X(sock - 4.6), Y(0) - 7, "2 holes 0.4, decorative", "tx", "middle")
    buckle(sh, X(20.5 + BUCKLE_ON_FLAP), Y(STRAP_W / 2), L(STRAP_W + 0.6))
    sh.rect(X(20.5 + KEEPER_ON_FLAP - 0.35), Y(-0.2), L(0.7), L(STRAP_W + 0.4), "strap")
    yd = Y(STRAP_W) + 10
    for a, bb, t in [(0, 1.0, "1.0"), (1.0, 14.0, "13.0"), (14.0, 20.5, "6.5"), (20.5, 30.5, "10.0"), (30.5, total, fmt(free))]:
        sh.dim_h(X(a), X(bb), Y(STRAP_W), yd, t)
    sh.dim_h(X(0), X(total), Y(STRAP_W), yd + 8, f"{fmt(total)} overall")
    sh.dim_v(Y(0), Y(STRAP_W), X(0), X(0) - 6, "3.0")
    sh.dim_h(X(30.5), X(sock), Y(0), Y(0) - 3, fmt(SNAP_FROM_FLAP_EDGE), ext=False)
    sh.dim_h(X(20.5), X(20.5 + BUCKLE_ON_FLAP), Y(0), Y(0) - 3, fmt(BUCKLE_ON_FLAP), ext=False)
    bx, by = X(0), yd + 22
    sh.text(bx, by - 3, "BUCKLE PIECE - 3.0 x 8.0 loop round the 30 mm buckle bar, stitched ON the strap over the top flap (bar 4.7 below the flap top edge); keeper 3.4 x 0.7 stitched at 8.0. Both decorative.", "ts")
    vb = View(bx, by, 5.0)
    sh.rect(vb.X(0), vb.Y(0), vb.L(8.0), vb.L(STRAP_W), "strap")
    buckle(sh, vb.X(2.0), vb.Y(STRAP_W / 2), vb.L(STRAP_W + 0.6))
    sh.rect(vb.X(5.3 - 0.35), vb.Y(-0.2), vb.L(0.7), vb.L(STRAP_W + 0.4), "strap")
    sh.dim_h(vb.X(0), vb.X(8.0), vb.Y(STRAP_W), vb.Y(STRAP_W) + 6, "8.0")
    sh.text(vb.X(10), vb.Y(1.0), "Buckle: 30 mm (1 1/4 in) antique brass, fixed; the tongue passes under the keeper and closes with the 12.5 mm snap.", "ts")
    sh.text(vb.X(10), vb.Y(2.3), "Stud on the front panel outer face, centred, 11.0 below the top edge (sheet 2). Set after a dry fold.", "ts")

    # ---- HINGE SECTION 2:1 ----
    vh = View(200, 128, 20.0)
    Xh, Yh, Lh = vh.X, vh.Y, vh.L
    sh.text(Xh(0) - 10, Yh(-0.8) - 7, "DETAIL C - PAGE HINGES, section through the bottom gusset, 2:1", "tb")
    sh.rect(Xh(0), Yh(2.0), Lh(FRONT_WALL), Lh(0.25), "hatch")
    sh.rect(Xh(0), Yh(2.0), Lh(FRONT_WALL), Lh(0.25), "thin")
    sh.rect(Xh(-0.25), Yh(-0.8), Lh(0.25), Lh(3.05), "hatch")
    sh.rect(Xh(-0.25), Yh(-0.8), Lh(0.25), Lh(3.05), "thin")
    sh.rect(Xh(FRONT_WALL), Yh(-0.8), Lh(0.25), Lh(3.05), "hatch")
    sh.rect(Xh(FRONT_WALL), Yh(-0.8), Lh(0.25), Lh(3.05), "thin")
    for i, sp in enumerate(SEAMS):
        sh.line(Xh(sp), Yh(-0.8), Xh(sp), Yh(2.0), "cut")
        sh.line(Xh(sp), Yh(2.0), Xh(sp + 0.9), Yh(2.0), "cut")
        sh.line(Xh(sp + 0.5), Yh(1.85), Xh(sp + 0.5), Yh(2.4), "stitch")
        sh.text(Xh(sp), Yh(-0.8) - 1.5, f"P{3 - i}", "tx", "middle")
    sh.text(Xh(FRONT_WALL / 2), Yh(2.25) + 4, "bottom gusset: outer + 1.0 mm board + lining", "tx", "middle")
    sh.text(Xh(-0.1), Yh(0.6), "back wall", "tx", "end", rot=-90)
    sh.text(Xh(FRONT_WALL + 0.25) + 3, Yh(0.6), "front", "tx", "start", rot=-90)
    yd2 = Yh(2.4) + 10
    sh.dim_h(Xh(0), Xh(SEAMS[0]), Yh(2.25), yd2, fmt(SEAMS[0]))
    for a, b in zip(SEAMS, SEAMS[1:]):
        sh.dim_h(Xh(a), Xh(b), Yh(2.25), yd2, fmt(b - a))
    sh.dim_h(Xh(SEAMS[-1]), Xh(FRONT_WALL), Yh(2.25), yd2, fmt(FRONT_WALL - SEAMS[-1]))
    sh.dim_h(Xh(0), Xh(FRONT_WALL), Yh(2.25), yd2 + 8, "6.0")
    sh.dim_h(Xh(SEAMS[0]), Xh(SEAMS[0] + 0.9), Yh(2.0), Yh(2.0) - 4, "1.5 tab, folded", ext=False)
    sh.lines(Xh(0) - 10, yd2 + 16, [
        "- Each page's 1.5 hinge tab folds toward the front and is",
        "  stitched through the gusset (lining + board + outer) on",
        "  one line, 0.5 from the fold. Three seams evenly spaced",
        "  at 1.5 so the pages fan open like a book (photo R2).",
        "- Stitch P3, then P2, then P1 from the back; the gusset",
        "  outer face shows three parallel stitch lines - use the",
        "  same contrast thread. Pages are not removable.",
    ], "ts", 3.7)

    # ---- POCKET PATTERNS 1:2 ----
    vp = View(22, 128, 5.0)
    Xp, Yp, Lp = vp.X, vp.Y, vp.L
    sh.text(Xp(0), Yp(0) - 5, "DETAIL D - POCKET PATTERNS, 1:2 (net; add 0.8 turn-under on the three stitched sides, top edge bound or skived)", "tb")
    # big pocket body + flap
    sh.rect(Xp(0), Yp(0), Lp(9.7), Lp(9.5), "band")
    sh.text(Xp(4.85), Yp(4.5), "cable pocket body", "ts", "middle")
    sh.text(Xp(4.85), Yp(5.5), "9.7 x 9.5", "tx", "middle")
    sh.add(f'<path d="{rounded_rect_path(Xp, Yp, Lp, 11.0, 0, 9.7, 3.8, 0.6, (0, 0, 1, 1))}" class="leather"/>')
    sh.text(Xp(15.85), Yp(1.4), "cable pocket flap", "ts", "middle")
    sh.text(Xp(15.85), Yp(2.3), "9.7 x 3.8 (0.8 stitched)", "tx", "middle")
    sh.circle(Xp(15.85), Yp(3.1), 2.0, "brass")
    # small pockets
    sh.rect(Xp(22.0), Yp(0), Lp(3.9), Lp(4.6), "band")
    sh.text(Xp(23.95), Yp(2.0), "A / B body", "tx", "middle")
    sh.text(Xp(23.95), Yp(2.8), "3.9 x 4.6 x2", "tx", "middle")
    sh.add(f'<path d="{rounded_rect_path(Xp, Yp, Lp, 27.0, 0, 3.9, 2.4, 0.5, (0, 0, 1, 1))}" class="leather"/>')
    sh.text(Xp(28.95), Yp(0.9), "A / B flap", "tx", "middle")
    sh.text(Xp(28.95), Yp(1.6), "3.9 x 2.4 x2", "tx", "middle")
    sh.circle(Xp(28.95), Yp(2.0), 1.3, "brass")
    sh.dim_h(Xp(0), Xp(9.7), Yp(9.5), Yp(9.5) + 6, "9.7")
    sh.dim_v(Yp(0), Yp(9.5), Xp(0), Xp(0) - 6, "9.5")
    sh.dim_v(Yp(0), Yp(3.8), Xp(11.0), Xp(11.0) - 5, "3.8")
    sh.dim_h(Xp(22.0), Xp(25.9), Yp(4.6), Yp(4.6) + 6, "3.9")
    sh.dim_v(Yp(0), Yp(4.6), Xp(22.0), Xp(22.0) - 5, "4.6")
    sh.dim_v(Yp(0), Yp(2.4), Xp(30.9), Xp(30.9) + 5, "2.4")
    sh.lines(Xp(0), Yp(9.5) + 12, [
        "- Pockets are patch pockets: body stitched to the panel face on three sides 0.3 from the edge, over a 0.8",
        "  turn-under; flap stitched along its top edge 0.5 in from the fold. Snaps: 12.5 mm (cable pocket), 10 mm (A, B).",
        "- Make the pockets on the face ply before the elastic is threaded and the ply laminated.",
    ], "ts", 3.7)

    elastic_detail(sh, 30, 222)
    return sh


# ==========================================================================
# SHEET 9 - contents, BOM, construction
# ==========================================================================
def sheet9():
    sh = Sheet(9, "Contents checklist, bill of materials, construction & cutting list", "-")
    sh.frame()
    x0, y0 = 14, 26
    sh.text(x0, y0, "CONTENTS CHECKLIST - 64 tips (32 pairs), 5 cables, 14 accessories: where each item lives", "tb")
    rows = []
    for i, (lab, w) in enumerate(SIZES_SMALL):
        rows.append([f"{lab} mm", "2 x 10 cm", "Panel 1", str(i + 1), fmt(w), "2 x 5 cm", "Panel 3", str(i + 1), fmt(w)])
    for i, (lab, w) in enumerate(SIZES_LARGE10):
        c = ("Panel 4", str(i + 1), fmt(w)) if i < 4 else ("-", "-", "-")
        rows.append([f"{lab} mm", "2 x 10 cm", "Panel 2", str(i + 1), fmt(w), "2 x 5 cm" if i < 4 else "-", *c])
    end = sh.table(x0, y0 + 3, ["Size", "10 cm tips", "Panel", "Loop", "w", "5 cm tips", "Panel", "Loop", "w"],
                   rows, [16, 18, 16, 10, 10, 18, 16, 10, 10], rh=4.0)
    sh.text(x0, end + 4, "Totals: 17 pairs x 10 cm (34 tips) on panels 1 + 2;  15 pairs x 5 cm (30 tips) on panels 3 + 4;  32 pairs / 64 tips.", "ts")
    sh.text(x0, end + 8, "Accessories: 6 caps + 4 keys -> panel 2 pocket A;  3 connectors + grip patch -> pocket B;  5 cables -> panel 4 (back wall) pocket.", "ts")

    bx, by = 150, 26
    sh.text(bx, by, "BILL OF MATERIALS (per case)", "tb")
    bom = [
        ["1", "Outer shell, full-grain leather 1.2-1.4 mm (or PU 1.0-1.2), tan", "1", "48.4 x 48.2 net + allowance (sheet 2)"],
        ["2", "Lining 0.6 mm, tan (back-wall lining = panel 4, sheet 7)", "1", "48.4 x 48.2 net + allowance"],
        ["3", "Board 1.0 mm: back wall, front panel", "2", "21 x 13, 21 x 12.7"],
        ["4", "Board 0.8 mm: pages", "3", "20.0 x 12.5"],
        ["5", "Page face plies 1.0 mm (slits die-cut) + back plies 0.6 mm", "3+3", "20.0 x 14.0 (incl. 1.5 hinge tab) + allowance"],
        ["6", "Knit elastic 15 mm, tan", "4", "19.1 / 16.2 / 19.1 / 10.9 cm (slit field + 2)"],
        ["7", "Strap, leather 1.4 mm, dark brown, 2 ply", "2", "3.0 x 33.5 (sheet 8)"],
        ["8", "Buckle piece + keeper, dark brown", "1+1", "3.0 x 8.0;  3.4 x 0.7"],
        ["9", "Buckle 30 mm, antique brass", "1", "decorative, fixed on the strap"],
        ["10", "Spring snaps 12.5 mm (line 20), antique brass", "4 sets", "2 side flaps, 1 strap tongue, 1 cable pocket"],
        ["11", "Spring snaps 10 mm, antique brass", "2 sets", "pockets A, B"],
        ["12", "Cable pocket body + flap, 0.8 mm leather", "1+1", "9.7 x 9.5;  9.7 x 3.8"],
        ["13", "Small pocket bodies + flaps, 0.8 mm leather", "2+2", "3.9 x 4.6;  3.9 x 2.4"],
        ["14", "Leather grip patch, veg-tan 1.8-2 mm", "1", "6.0 x 3.0, R 0.5, folds in half"],
        ["15", "Thread, bonded polyester Tex 70, contrast", "-", "stitch length 3 mm"],
        ["16", "Logo emboss die", "1", "2.5 x 2.5 (client artwork, sheet 1)"],
    ]
    end2 = sh.table(bx, by + 3, ["#", "Item", "Qty", "Cut size (cm) / note"], bom, [8, 100, 14, 86], rh=4.0)
    sh.lines(150, end2 + 8, [
        "**CONSTRUCTION SEQUENCE",
        "1. Cut shell, lining, board, pages and pockets (sheets 2, 4-8). Die-cut the elastic slits in the three page face plies and in the",
        "   back-wall lining (sheets 4-7 at 1:1). Emboss the logo on the top flap while flat.",
        "2. Make the pockets on the face plies (panel 2: A, B; back-wall lining: cable pocket). Set the pocket snaps.",
        "3. Thread the elastics in and out of the slits, loop by loop; bar-tack each slit, stitch the ends down. Print / stamp the size labels.",
        "4. Laminate each page: face ply + 0.8 board + back ply; edge-stitch 0.3, leaving the 1.5 hinge tab single-ply.",
        "5. Stitch the strap to the outer shell (back wall + top gusset + top flap) with the buckle piece and keeper on the flap section.",
        "6. Set the side-flap studs and the front-panel sockets. Laminate lining to shell with board in the back wall and front panel.",
        "7. Stitch the page hinge tabs through the bottom gusset in order P3, P2, P1 (sheet 8, detail C). Turn / bind all edges; edge-stitch 0.3.",
        "8. Dry-fold; set the strap stud on the front panel and the socket in the tongue; check all snaps. Load the set; the closed case must not press on the 10 mm tips.",
        "",
        "**TOLERANCES",
        "Cut pieces +/- 0.1 cm; slit positions +/- 0.05 cm (the 0.6 loop must still take two 2 mm tips); snap centres +/- 0.15 cm; hinge seams +/- 0.1 cm.",
    ], "ts", 3.8)

    mx, my = 14, 172
    sh.text(mx, my, "MEASUREMENT RECORD - what each prototype / reference photo contributed", "tb")
    mend = sh.table(mx, my + 3, ["Photo", "Feature", "Value used on drawings"], [
        ["P1", "Cardboard cross pattern", "Top gusset 6.5, back 21.0 x 13.0, bottom gusset 6.0, front 12.7; side gusset 5.7, side flap 8.0, snaps. Top flap 5.0 superseded by 10.0 (client, per R1/R3)"],
        ["P2-P5", "Cardboard panels", "Loop widths 0.6-2.2 (= 6-22 mm), 0.5 between loops, 1.0 end margins, 1.5 above the points"],
        ["R1, R3", "Closed clutch, front/back", "Trifold clutch, wrap strap 3.0 with buckle, keeper; logo on flap; R 1.0 corners; contrast edge stitch"],
        ["R2, R3", "Open case", "Pages sewn into the bottom gusset, not removable; side flaps tuck inside"],
        ["R4-R6", "Panel interiors", "1.5 elastic threaded in / out of the panel per pair; size labels above tips; snap pockets on panel 2 and the back wall"],
        ["Brief", "Client text 2026-10-01", "Front > P1 > P2 > P3 > back wall; back wall = panel 4 with cable pocket; 2 small pockets on panel 2; snaps hold the front panel to the side flaps; strap visual, snap-closed; logo"],
    ], [16, 54, 164], rh=4.2)
    sh.text(14, mend + 8, "HARDWARE SIZE ASSUMPTIONS (confirm against the real set - Q5)", "tb")
    sh.table(14, mend + 11, ["Item", "Qty", "Assumed size (cm)", "Where"], [
        ["Screw-on end cap", "6", "1.0 dia x 1.5", "panel 2 pocket A"],
        ["Cable key", "4", "1.2 x 3.5", "panel 2 pocket A"],
        ["Cable connector", "3", "1.0 dia x 3.0", "panel 2 pocket B"],
        ["Leather grip patch", "1", "6.0 x 3.0 x 0.2, folded", "panel 2 pocket B"],
        ["Cables 25-100 cm", "5", "coil to 6.5 dia", "panel 4 cable pocket"],
    ], [40, 12, 48, 60], rh=4.2)
    return sh


# ==========================================================================
def main():
    sheets = [sheet1(), sheet2(), sheet3(), sheet4(), sheet5(), sheet6(), sheet7(), sheet8(), sheet9()]
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
