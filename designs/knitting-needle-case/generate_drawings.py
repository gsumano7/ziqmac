#!/usr/bin/env python3
"""
Technical drawing set for the interchangeable knitting-needle case.

Every dimension comes from the cardboard prototype (photos 1-5) unless a
note on the sheet says it is a proposal.  Units on the sheets are cm;
page geometry is A3 landscape in mm.

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
REV = "A"
PROJECT = "INTERCHANGEABLE KNITTING NEEDLE CASE"
CLIENT = "gsumano7 / ziqmac"
TOTAL_SHEETS = 7

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

# Interior panels: 20.5 x 12.5 to clear the 21.0 x 13.0 interior
PANEL_W, PANEL_H = 20.5, 12.5
KEEPER_FLAP = 9.0            # photo 2: "9 cm"


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
        self.text(x0 + 2, y0 + 27.8, "Cardboard prototype, hand-measured (photos 1-5)", "t")
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


# ==========================================================================
# SHEET 1 - outer shell flat pattern
# ==========================================================================
def sheet1():
    sh = Sheet(1, "Outer shell - flat pattern (die line)", "1:2")
    sh.frame()
    s = 5.0
    v = View(28, 38, s)
    X, Y, L = v.X, v.Y, v.L
    xa = END_FLAP                       # left side wall
    xb = END_FLAP + SIDE_WALL           # base left edge
    xc = xb + BASE_W                    # base right edge
    xd = xc + SIDE_WALL                 # right flap start
    ya = REAR_FLAP
    yb = ya + REAR_WALL                 # base top
    yc = yb + BASE_H                    # base bottom
    yd = yc + FRONT_WALL                # lid top

    # fills
    sh.rect(X(xb), Y(0), L(BASE_W), L(PATTERN_H), "leather")
    sh.rect(X(0), Y(yb), L(PATTERN_W), L(BASE_H), "leather")
    # perimeter (cut)
    per = [(xb, 0), (xc, 0), (xc, yb), (PATTERN_W, yb), (PATTERN_W, yc), (xc, yc),
           (xc, PATTERN_H), (xb, PATTERN_H), (xb, yc), (0, yc), (0, yb), (xb, yb)]
    sh.poly([(X(x), Y(y)) for x, y in per], "cut")
    # fold lines
    for yy in (ya, yb, yc, yd):
        sh.line(X(xb), Y(yy), X(xc), Y(yy), "fold")
    for xx in (xa, xb, xc, xd):
        sh.line(X(xx), Y(yb), X(xx), Y(yc), "fold")

    # labels
    def lab(x, y, a, b=None):
        sh.text(X(x), Y(y), a, "tb", "middle")
        if b:
            sh.text(X(x), Y(y) + 4, b, "ts", "middle")
    cx = xb + BASE_W / 2
    lab(cx, REAR_FLAP / 2 + 0.3, "REAR FLAP", "21.0 x 5.0  (tuck / keeper flap)")
    lab(cx, ya + REAR_WALL / 2 + 0.3, "REAR WALL", "21.0 x 6.5")
    lab(cx, yb + BASE_H / 2 - 0.3, "BASE (inside: needle panel A)", "21.0 x 13.0")
    lab(cx, yc + FRONT_WALL / 2 + 0.3, "FRONT WALL - lid hinge", "21.0 x 6.0")
    lab(cx, yd + LID_H / 2 - 1.2, "LID (inside: needle panel B)", "21.0 x 12.7")
    sh.text(X(xa + SIDE_WALL / 2) + 1.2, Y(yb + 1.2), "SIDE WALL 5.7 x 13.0", "ts", "end", rot=-90)
    sh.text(X(xc + SIDE_WALL / 2) + 1.2, Y(yb + 1.2), "SIDE WALL 5.7 x 13.0", "ts", "end", rot=-90)
    lab(END_FLAP / 2, yb + 2.2, "END FLAP (L)", "8.0 x 13.0 - snap cap")
    lab(xd + END_FLAP / 2, yb + 2.2, "END FLAP (R)", "8.0 x 13.0 - snap cap")

    # snaps on end flaps
    sxl = xa - SNAP_FROM_FOLD
    sxr = xd + SNAP_FROM_FOLD
    sy = yb + SNAP_FROM_TOP
    sh.snap_cap(X(sxl), Y(sy), 3.2)
    sh.snap_cap(X(sxr), Y(sy), 3.2)
    sh.text(X(sxl), Y(sy) + 7.5, "SNAP CAP+SOCKET", "tx", "middle")
    sh.text(X(sxr), Y(sy) + 7.5, "SNAP CAP+SOCKET", "tx", "middle")
    # mating studs on lid (outer face) - shown hidden
    stud_y = PATTERN_H - SNAP_FROM_TOP
    for sx in (xb + SNAP_FROM_FOLD, xc - SNAP_FROM_FOLD):
        sh.snap_stud(X(sx), Y(stud_y), 3.2)
    sh.text(X(cx), Y(stud_y) + 7.5, "SNAP STUD+POST x2 on OUTER face of lid (hidden) - mates with end-flap caps", "tx", "middle")

    # dimensions: horizontal chain at top
    yt = Y(0) - 7
    segs = [(0, xa, "8.0"), (xa, xb, "5.7"), (xb, xc, "21.0"), (xc, xd, "5.7"), (xd, PATTERN_W, "8.0")]
    for a, b, t in segs:
        sh.dim_h(X(a), X(b), Y(yb) if (a < xb or b > xc) else Y(0), yt, t)
    sh.dim_h(X(0), X(PATTERN_W), Y(yb), yt - 8, fmt(PATTERN_W) + "  OVERALL")
    # vertical chain at right
    xr = X(PATTERN_W) + 8
    vsegs = [(0, ya, "5.0"), (ya, yb, "6.5"), (yb, yc, "13.0"), (yc, yd, "6.0"), (yd, PATTERN_H, "12.7")]
    for a, b, t in vsegs:
        sh.dim_v(Y(a), Y(b), X(PATTERN_W) if (a >= yb and b <= yc) else X(xc), xr, t)
    sh.dim_v(Y(0), Y(PATTERN_H), X(PATTERN_W), xr + 8, fmt(PATTERN_H) + "  OVERALL")
    # snap position dims (left flap)
    sh.dim_h(X(sxl), X(xa), Y(sy), Y(yc) + 5, "5.0")
    sh.dim_v(Y(yb), Y(sy), X(sxl), X(0) - 5, "6.5")
    sh.text(X(0), Y(yc) + 12, "(R) end flap: snap position symmetrical", "tx")
    # stud dims on lid
    sh.dim_h(X(xb), X(xb + SNAP_FROM_FOLD), Y(stud_y), Y(PATTERN_H) + 5, "5.0")
    sh.dim_h(X(xc - SNAP_FROM_FOLD), X(xc), Y(stud_y), Y(PATTERN_H) + 5, "5.0")
    sh.dim_v(Y(stud_y), Y(PATTERN_H), X(xb), X(xb) - 5, "6.5")
    # grain arrow
    gx, gy = X(xb) - 14, Y(yd + 2)
    sh.line(gx, gy + 30, gx, gy, "thin", 'marker-end="url(#ar)"')
    sh.line(gx, gy, gx, gy + 30, "thin", 'marker-end="url(#ar)"')
    sh.text(gx - 1.5, gy + 15, "GRAIN / NAP", "tx", "middle", rot=-90)

    # legend + notes
    nx, ny = 288, 22
    sh.text(nx, ny, "LEGEND", "tb")
    sh.line(nx, ny + 5, nx + 14, ny + 5, "cut"); sh.text(nx + 17, ny + 6, "Cut line (net finished size)", "ts")
    sh.line(nx, ny + 10, nx + 14, ny + 10, "fold"); sh.text(nx + 17, ny + 11, "Fold / score line", "ts")
    sh.line(nx, ny + 15, nx + 14, ny + 15, "hid"); sh.text(nx + 17, ny + 16, "Hidden (feature on far face)", "ts")
    sh.line(nx, ny + 20, nx + 14, ny + 20, "stitch"); sh.text(nx + 17, ny + 21, "Stitch line", "ts")
    sh.snap_cap(nx + 7, ny + 28, 2.2); sh.text(nx + 17, ny + 29, "Snap cap + socket (this face)", "ts")
    sh.snap_stud(nx + 7, ny + 36, 2.2); sh.text(nx + 17, ny + 37, "Snap stud + post (far face)", "ts")

    notes = [
        "**NOTES",
        "1. All dimensions in cm, finished (net) sizes as measured",
        "   on the cardboard prototype. No seam allowance included:",
        "   add 0.8 cm for turned seams, 0 for bound / edge-painted",
        "   edges, or 1.0 cm wrap allowance if covering board.",
        "2. Pattern assumed symmetrical about its vertical centre",
        "   line. Left side wall / end flap not dimensioned on the",
        "   prototype; drawn equal to the right side (5.7 / 8.0).",
        "3. Wall heights are as measured: 5.7 (sides), 6.0 (front),",
        "   6.5 (rear). For a square-cornered box equalise all four",
        "   to 6.0 before cutting - see sheet 2, open question Q1.",
        "4. Base 13.0 vs lid 12.7: the 0.3 cm difference lets the",
        "   lid clear the rear flap when closed. Keep as measured.",
        "5. Snaps: 12.5 mm (line 20) spring snaps, 2 sets on the",
        "   end flaps + 2 sets on panel B keeper flap (sheet 4).",
        "   Set snap studs on the lid after a dry fold of the first",
        "   sample; the fold radius shifts them ~1 material thickness.",
        "6. Outer: faux leather (PU) 1.0-1.2 mm. Stiffen base, lid",
        "   and walls with 1.5 mm greyboard (optional for flaps).",
        "   Lining and interior panels: sheets 3-6. BOM: sheet 7.",
        "7. Rear flap (5.0) folds inward over the contents before the",
        "   lid closes; end flaps fold over the lid and snap.",
        "",
        "**SHEET INDEX",
        "1  Outer shell - flat pattern (this sheet)",
        "2  Assembly - closed views, fold sequence, interior layout",
        "3  Needle panel A (base): 10 cm tips 2.0-5.0 mm",
        "4  Needle panel B (lid): 10 cm tips 5.5-10 mm + keeper flap",
        "5  Hinged page face 1 - panel C: 5 cm tips 2.0-5.0 mm, caps, keys",
        "6  Hinged page face 2 - panel D: 5 cm tips 5.5-8 mm, accessories",
        "7  Contents checklist, bill of materials, construction",
    ]
    sh.lines(nx, ny + 46, notes, "ts", 3.9)
    return sh


# ==========================================================================
# SHEET 2 - assembly / views / interior layout
# ==========================================================================
def sheet2():
    sh = Sheet(2, "Assembly - closed views, fold sequence, interior layout", "1:2 (views)  1:4 (interior)")
    sh.frame()
    s = 5.0
    D = 6.0   # nominal closed depth
    # --- TOP VIEW (closed) ---
    v = View(30, 40, s)
    X, Y, L = v.X, v.Y, v.L
    sh.text(X(0), Y(0) - 12, "TOP VIEW - closed (end flaps folded over lid)", "tb")
    sh.rect(X(0), Y(0), L(BASE_W), L(BASE_H), "leather")
    sh.rect(X(0), Y(0), L(END_FLAP), L(BASE_H), "hatch")
    sh.rect(X(BASE_W - END_FLAP), Y(0), L(END_FLAP), L(BASE_H), "hatch")
    sh.line(X(END_FLAP), Y(0), X(END_FLAP), Y(BASE_H), "cut")
    sh.line(X(BASE_W - END_FLAP), Y(0), X(BASE_W - END_FLAP), Y(BASE_H), "cut")
    sh.line(X(0), Y(BASE_H), X(BASE_W), Y(BASE_H), "fold")
    sh.text(X(BASE_W / 2), Y(BASE_H) + 3.5, "lid hinge (front wall)", "tx", "middle")
    sh.text(X(BASE_W / 2), Y(0) - 1.5, "rear", "tx", "middle")
    sh.snap_cap(X(SNAP_FROM_FOLD), Y(SNAP_FROM_TOP), 3.0)
    sh.snap_cap(X(BASE_W - SNAP_FROM_FOLD), Y(SNAP_FROM_TOP), 3.0)
    sh.text(X(END_FLAP / 2), Y(BASE_H - 1.5), "END FLAP", "ts", "middle")
    sh.text(X(BASE_W - END_FLAP / 2), Y(BASE_H - 1.5), "END FLAP", "ts", "middle")
    sh.text(X(BASE_W / 2), Y(BASE_H / 2) + 1, "LID", "tb", "middle")
    sh.dim_h(X(0), X(BASE_W), Y(0), Y(0) - 6, "21.0")
    sh.dim_v(Y(0), Y(BASE_H), X(BASE_W), X(BASE_W) + 7, "13.0")
    sh.dim_h(X(0), X(END_FLAP), Y(BASE_H), Y(BASE_H) + 8, "8.0")
    sh.dim_h(X(BASE_W - SNAP_FROM_FOLD), X(BASE_W), Y(BASE_H), Y(BASE_H) + 8, "5.0")
    sh.dim_v(Y(0), Y(SNAP_FROM_TOP), X(0), X(0) - 7, "6.5")
    # --- FRONT VIEW ---
    v2 = View(30, Y(BASE_H) + 26, s)
    sh.text(v2.X(0), v2.Y(0) - 4, "FRONT VIEW - closed", "tb")
    sh.rect(v2.X(0), v2.Y(0), v2.L(BASE_W), v2.L(D), "leather")
    sh.line(v2.X(0), v2.Y(0.12), v2.X(BASE_W), v2.Y(0.12), "thin")
    sh.dim_v(v2.Y(0), v2.Y(D), v2.X(BASE_W), v2.X(BASE_W) + 7, "6.0 nom.")
    sh.text(v2.X(BASE_W / 2), v2.Y(D / 2) + 1, "front wall 6.0 (lid hinge along top edge)", "tx", "middle")
    # --- END VIEW ---
    v3 = View(185, v2.oy, s)
    sh.text(v3.X(0), v3.Y(0) - 4, "END VIEW", "tb")
    sh.rect(v3.X(0), v3.Y(0), v3.L(BASE_H), v3.L(D), "leather")
    sh.line(v3.X(0), v3.Y(0.12), v3.X(BASE_H), v3.Y(0.12), "thin")
    sh.text(v3.X(BASE_H / 2), v3.Y(D / 2) + 1, "side wall 5.7 + end flap over lid", "tx", "middle")
    sh.dim_h(v3.X(0), v3.X(BASE_H), v3.Y(D), v3.Y(D) + 7, "13.0")

    # --- ISOMETRIC closed ---
    ox, oy = 325, 98
    si = 3.5
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))

    def P(x, y, z):
        return (ox + (x - y) * c30 * si, oy + (x + y) * s30 * si - z * si)
    Wb, Db, Hb = BASE_W, BASE_H, D
    sh.text(ox - 42, oy - 32, "ISOMETRIC - closed", "tb")
    sh.poly([P(0, 0, Hb), P(Wb, 0, Hb), P(Wb, Db, Hb), P(0, Db, Hb)], "leather")
    sh.poly([P(0, Db, 0), P(Wb, Db, 0), P(Wb, Db, Hb), P(0, Db, Hb)], "leather")
    sh.poly([P(Wb, 0, 0), P(Wb, Db, 0), P(Wb, Db, Hb), P(Wb, 0, Hb)], "leather")
    for x0 in (0, Wb - END_FLAP):
        sh.poly([P(x0, 0, Hb), P(x0 + END_FLAP, 0, Hb), P(x0 + END_FLAP, Db, Hb), P(x0, Db, Hb)], "hatch")
        sh.poly([P(x0, 0, Hb), P(x0 + END_FLAP, 0, Hb), P(x0 + END_FLAP, Db, Hb), P(x0, Db, Hb)], "thin")
    sh.line(*P(0, Db, Hb), *P(Wb, Db, Hb), "fold")
    for sx in (SNAP_FROM_FOLD, Wb - SNAP_FROM_FOLD):
        px, py = P(sx, SNAP_FROM_TOP, Hb)
        sh.add(f'<ellipse cx="{px:.2f}" cy="{py:.2f}" rx="2.4" ry="1.4" class="thin"/>')
        sh.add(f'<ellipse cx="{px:.2f}" cy="{py:.2f}" rx="1.2" ry="0.7" class="thin"/>')
    a = P(Wb - END_FLAP / 2, Db * 0.5, Hb)
    sh.leader(a[0], a[1], a[0] + 16, a[1] - 12, "end flap, snapped")
    b = P(Wb * 0.5, Db, Hb)
    sh.leader(b[0], b[1], b[0] - 24, b[1] + 34, "lid hinge (front wall fold)", anchor="end")
    c = P(Wb * 0.5, 0, Hb)
    sh.leader(c[0], c[1], c[0] + 6, c[1] - 14, "rear flap tucked inside")
    sh.text(ox - 42, oy + 66, "Closed size 21.0 x 13.0 x 6.0 cm (W x D x H, nominal)", "t")

    # --- FOLD SEQUENCE (between front view and isometric) ---
    fx, fy = 185, 22
    sh.lines(fx, fy, [
        "**FOLD / ASSEMBLY SEQUENCE",
        "1. Fold the four walls up 90 deg from the base",
        "   (rear 6.5, front 6.0, sides 5.7).",
        "2. Glue / stitch the corner tabs (not shown; add",
        "   1.5 cm tabs on the side walls if a rigid box).",
        "3. Fit interior: panel A to base (sheet 3), page",
        "   hinge to front wall inner face (sheets 5-6),",
        "   panel B to lid inner face (sheet 4).",
        "4. Fold rear flap (5.0) inward over the contents.",
        "5. Close lid over the front-wall hinge.",
        "6. Fold both end flaps over the lid; snap.",
    ], "ts", 3.9)

    # --- INTERIOR LAYOUT (open) 1:4 ---
    s4 = 2.5
    vi = View(30, 178, s4)
    sh.text(vi.X(0), vi.Y(0) - 5, "INTERIOR LAYOUT - open, lid folded flat, viewed from above (1:4)", "tb")
    yl = 0
    yf = LID_H
    yb = LID_H + FRONT_WALL
    sh.rect(vi.X(0), vi.Y(yl), vi.L(BASE_W), vi.L(LID_H), "leather")
    sh.rect(vi.X(0), vi.Y(yf), vi.L(BASE_W), vi.L(FRONT_WALL), "leather")
    sh.rect(vi.X(0), vi.Y(yb), vi.L(BASE_W), vi.L(BASE_H), "leather")
    pm = (BASE_W - PANEL_W) / 2
    sh.rect(vi.X(pm), vi.Y(yl + (LID_H - PANEL_H) / 2), vi.L(PANEL_W), vi.L(PANEL_H), "band")
    sh.text(vi.X(BASE_W / 2), vi.Y(yl + LID_H / 2) + 1, "PANEL B", "ts", "middle")
    sh.rect(vi.X(pm), vi.Y(yb + (BASE_H - PANEL_H) / 2), vi.L(PANEL_W), vi.L(PANEL_H), "band")
    sh.text(vi.X(BASE_W / 2), vi.Y(yb + BASE_H / 2) + 1, "PANEL A  +  PAGE (dashed)", "ts", "middle")
    sh.rect(vi.X(pm), vi.Y(yb + 0.25), vi.L(PANEL_W), vi.L(PANEL_H), "hid")
    sh.line(vi.X(pm), vi.Y(yf + FRONT_WALL / 2), vi.X(pm + PANEL_W), vi.Y(yf + FRONT_WALL / 2), "fold")
    sh.text(vi.X(BASE_W / 2), vi.Y(yf + FRONT_WALL / 2) - 1.2, "page hinge", "tx", "middle")
    sh.dim_v(vi.Y(yl), vi.Y(yf), vi.X(BASE_W), vi.X(BASE_W) + 6, "12.7")
    sh.dim_v(vi.Y(yf), vi.Y(yb), vi.X(BASE_W), vi.X(BASE_W) + 6, "6.0")
    sh.dim_v(vi.Y(yb), vi.Y(yb + BASE_H), vi.X(BASE_W), vi.X(BASE_W) + 6, "13.0")
    tx = vi.X(BASE_W) + 16
    sh.lines(tx, vi.Y(2), [
        "**LID - panel B (sheet 4)",
        "10 cm tips 5.5-10 mm, 6 slots, keeper flap with 2 snaps.",
    ], "ts", 3.8)
    sh.lines(tx, vi.Y(yf + 1.5), [
        "**FRONT WALL - page hinge",
        "1.5 cm strip; the page flips from base to lid.",
    ], "ts", 3.8)
    sh.lines(tx, vi.Y(yb + 2), [
        "**BASE - panel A (sheet 3) under the hinged page",
        "Panel A: 10 cm tips 2.0-5.0 mm, 11 slots.",
        "Page face 1 (sheet 5): 5 cm tips 2.0-5.0 mm, caps, keys.",
        "Page face 2 (sheet 6): 5 cm tips 5.5-8 mm, connectors,",
        "grip patch, zip cable pocket.",
    ], "ts", 3.8)

    # --- STACK HEIGHT CHECK ---
    sx0, sy0 = 215, 178
    sh.text(sx0, sy0 - 5, "STACK-HEIGHT CHECK (box depth 6.0 nominal)", "tb")
    sh.table(sx0, sy0, ["Layer (bottom to top)", "Thickest item", "Height"], [
        ["Panel A on base", "2 x 5.0 mm tips side by side + band", "0.8"],
        ["Page face 1 (C)", "2 x 5.0 mm tips + elastic", "0.8"],
        ["Page core", "1.5 mm board + 2 lining", "0.4"],
        ["Page face 2 (D)", "2 x 8.0 mm tips / 5 coiled cables", "1.6"],
        ["Panel B in lid", "2 x 10 mm tips + keeper flap", "1.4"],
        ["Rear flap + clearance", "", "1.0"],
        ["TOTAL", "", "6.0  (= depth, OK)"],
    ], [42, 58, 30], rh=4.2)
    sh.lines(sx0, sy0 + 38, [
        "**OPEN QUESTIONS (confirm before cutting)",
        "Q1  Keep measured wall heights 5.7 / 6.0 / 6.5 or equalise to 6.0?",
        "Q2  Rear flap 5.0: tuck inside (drawn) or fold over the lid outside?",
        "Q3  Soft case (faux leather + interfacing only) or board-stiffened box?",
        "Q4  Slot bands: 25 mm knit elastic (drawn) or self faux-leather strips?",
        "Q5  Cable pocket on the page (drawn) or a separate pouch?",
        "Q6  Check real hardware sizes (caps, keys, connectors) against sheet 5-6 loops.",
    ], "ts", 3.8)
    return sh


# ==========================================================================
# Needle panel sheets (shared drawing routine)
# ==========================================================================
def draw_panel(sh, v, sizes, needle_len, tip_margin, butt_margin, band_y0, band_y1,
               title, label_y=None):
    """Panel PANEL_W x PANEL_H with a slot strip. Returns slots."""
    X, Y, L = v.X, v.Y, v.L
    margin, slots = slot_layout(sizes, PANEL_W)
    sh.rect(X(0), Y(0), L(PANEL_W), L(PANEL_H), "leather")
    # needles (drawn under band)
    for lab, a, b in slots:
        draw_needle_pair(sh, v, a, b, tip_margin, needle_len, float(lab) / 10.0)
    draw_slot_strip(sh, v, slots, band_y0, band_y1, label_y=label_y)
    if title:
        sh.text(X(PANEL_W / 2), Y(PANEL_H) + 27, title, "tb", "middle")
    return margin, slots


def panel_dims(sh, v, slots, margin, needle_len, tip_margin, butt_margin, band_y0, band_y1, ydim_off=10):
    X, Y, L = v.X, v.Y, v.L
    # vertical dims (left of panel)
    xl = X(0) - 7
    sh.dim_v(Y(0), Y(tip_margin), X(0), xl, fmt(tip_margin))
    sh.dim_v(Y(tip_margin), Y(tip_margin + needle_len), X(0), xl, f"{fmt(needle_len)} tip")
    sh.dim_v(Y(tip_margin + needle_len), Y(PANEL_H), X(0), xl, fmt(butt_margin))
    sh.dim_v(Y(0), Y(PANEL_H), X(0), xl - 8, fmt(PANEL_H))
    # band position (right side)
    xr = X(PANEL_W) + 7
    sh.dim_v(Y(0), Y(band_y0), X(PANEL_W), xr, fmt(band_y0))
    sh.dim_v(Y(band_y0), Y(band_y1), X(PANEL_W), xr, f"{fmt(band_y1 - band_y0)} band")
    # horizontal: margins + overall + ordinate ticks at every stitch line
    yb = Y(PANEL_H) + ydim_off
    sh.dim_h(X(0), X(slots[0][1]), Y(PANEL_H), yb, fmt(margin))
    sh.dim_h(X(slots[-1][2]), X(PANEL_W), Y(PANEL_H), yb, fmt(PANEL_W - slots[-1][2]))
    sh.dim_h(X(slots[0][1]), X(slots[-1][2]), Y(PANEL_H), yb, f"{fmt(slots[-1][2] - slots[0][1])} slot strip")
    sh.dim_h(X(0), X(PANEL_W), Y(PANEL_H), yb + 8, fmt(PANEL_W))
    # ordinate (running) dimensions from left edge, above the panel
    yo = Y(0) - 8
    sh.line(X(0), yo, X(PANEL_W), yo, "dim")
    sh.text(X(0), yo - 11, "ORDINATE: stitch-line positions from left edge (cm)", "tx")
    sh.line(X(0), yo - 2.5, X(0), yo + 2.5, "dim")
    sh.text(X(0), yo - 1.2, "0", "tx", "middle")
    for lab, a, b in slots:
        for x in (a, b):
            sh.line(X(x), yo - 1.5, X(x), Y(0), "dim")
            sh.text(X(x) + 0.7, yo - 2.2, fmt(x), "tx", "start", rot=-90)
    sh.line(X(PANEL_W), yo - 2.5, X(PANEL_W), yo + 2.5, "dim")


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
    sh.leader(X(xa + slot / 2), Y(0.6), X(xa + slot / 2) + 10, Y(0.2), "2 tips side by side (1 pair)")
    sh.leader(X(0.35), Y(1.33), X(0.35) - 1, Y(1.33) + 14, "panel: 1.5 mm board + lining", anchor="start")
    sh.leader(X(xa + slot + land / 2), Y(1.2), X(xa + slot + land / 2) + 6, Y(1.9) + 4, "double stitch line, 0.5 apart")


def slot_table(sh, x, y, slots, sizes, tips_len, extra_note=None):
    rows = []
    for i, ((lab, w), (_, a, b)) in enumerate(zip(sizes, slots)):
        rows.append([str(i + 1), f"{lab} mm", fmt(w), fmt(a), fmt(b), f"2 x {tips_len} cm"])
    end = sh.table(x, y, ["#", "Size", "Slot w", "From", "To", "Holds"], rows, [8, 18, 15, 15, 15, 24], rh=4.2)
    return end


def panel_notes():
    return [
        "**CONSTRUCTION NOTES",
        "1. Slot widths (w) are finished inside widths, taken",
        "   straight from the prototype: 0.6 cm for 2.0 mm,",
        "   +0.1 cm per size step, to 2.2 cm for 10 mm. Each",
        "   slot holds one PAIR, the two tips side by side.",
        "2. Band: 25 mm knit elastic (drawn) stitched flat to",
        "   the panel on every stitch line; no ease needed.",
        "   If a faux-leather strip is used instead, add ease",
        "   of 2 x tip diameter to the strip length per slot.",
        "3. Stitch lines in pairs 0.5 cm apart (the 'land');",
        "   single line at the strip ends. Stitch 3 mm, 2 passes.",
        "4. Panel = 1.5 mm greyboard wrapped in lining faux",
        "   leather; finished 20.5 x 12.5 to drop into the",
        "   21.0 x 13.0 interior. Glue + edge-stitch in place.",
        "5. Size labels heat-stamped / printed on the band",
        "   at each slot (shown on drawing). Order: smallest",
        "   size nearest the edge shown, as on the prototype.",
        "6. Tip points toward the top edge of the drawing;",
        "   1.5 cm clear above the points (prototype).",
    ]


# ==========================================================================
# SHEET 3 - panel A
# ==========================================================================
def sheet3():
    sh = Sheet(3, "Needle panel A - base: 10 cm tips 2.0-5.0 mm (11 pairs)", "1:1  (detail 2:1)")
    sh.frame()
    v = View(32, 48, 10.0)
    tip_m, nl = 1.5, 10.0
    butt_m = PANEL_H - tip_m - nl
    b0, b1 = 5.0, 8.0
    margin, slots = draw_panel(sh, v, SIZES_SMALL, nl, tip_m, butt_m, b0, b1,
                               "PANEL A - 20.5 x 12.5, fits BASE interior. Full size 1:1 - use as pattern.")
    panel_dims(sh, v, slots, margin, nl, tip_m, butt_m, b0, b1)
    # table + notes + detail
    tx = 258
    sh.text(tx, 22, "SLOT TABLE - panel A (positions from left edge, cm)", "tb")
    end = slot_table(sh, tx, 25, slots, SIZES_SMALL, 10)
    sh.lines(tx, end + 6, panel_notes(), "ts", 3.7)
    band_detail(sh, 32, 215)
    return sh


# ==========================================================================
# SHEET 4 - panel B with keeper flap
# ==========================================================================
def sheet4():
    sh = Sheet(4, "Needle panel B - lid: 10 cm tips 5.5-10 mm (6 pairs) + keeper flap", "1:1  (flap 1:2)")
    sh.frame()
    v = View(32, 48, 10.0)
    X, Y, L = v.X, v.Y, v.L
    tip_m, nl = 1.5, 10.0
    butt_m = PANEL_H - tip_m - nl
    b0, b1 = 5.0, 8.0
    margin, slots = draw_panel(sh, v, SIZES_LARGE10, nl, tip_m, butt_m, b0, b1,
                               "PANEL B - 20.5 x 12.5, fits LID interior. Full size 1:1 - use as pattern. "
                               "Keeper flap shown folded closed (dashed) and open at 1:2, right.")
    snap_from_hinge = 8.0
    snap_x = (1.6, PANEL_W - 1.6)
    # keeper flap folded closed: dashed outline over the panel, hinge on the top edge
    r = 1.0
    sh.add(f'<path d="M{X(0):.3f},{Y(0):.3f} L{X(0):.3f},{Y(KEEPER_FLAP - r):.3f} '
           f'A{L(r):.3f},{L(r):.3f} 0 0 0 {X(r):.3f},{Y(KEEPER_FLAP):.3f} L{X(PANEL_W - r):.3f},{Y(KEEPER_FLAP):.3f} '
           f'A{L(r):.3f},{L(r):.3f} 0 0 0 {X(PANEL_W):.3f},{Y(KEEPER_FLAP - r):.3f} L{X(PANEL_W):.3f},{Y(0):.3f}" class="hid"/>')
    sh.line(X(0), Y(0), X(PANEL_W), Y(0), "fold")
    sh.text(X(PANEL_W / 2), Y(KEEPER_FLAP) + 3.2, "free edge of keeper flap when closed (9.0 from hinge)", "tx", "middle")
    sh.text(X(PANEL_W / 2), Y(0) - 1.5, "keeper-flap hinge = top (tip) edge of panel B", "tx", "middle")
    for sx in snap_x:
        sh.snap_stud(X(sx), Y(snap_from_hinge), 3.0)
    sh.text(X(snap_x[0]), Y(snap_from_hinge) + 6, "stud+post", "tx", "middle")
    sh.text(X(snap_x[1]), Y(snap_from_hinge) + 6, "stud+post", "tx", "middle")
    panel_dims(sh, v, slots, margin, nl, tip_m, butt_m, b0, b1)
    sh.dim_v(Y(0), Y(snap_from_hinge), X(PANEL_W), X(PANEL_W) + 15, "8.0 snap")
    sh.dim_h(X(0), X(snap_x[0]), Y(snap_from_hinge), Y(snap_from_hinge) + 17, "1.6", ext=False)
    sh.dim_h(X(snap_x[1]), X(PANEL_W), Y(snap_from_hinge), Y(snap_from_hinge) + 17, "1.6", ext=False)

    # keeper flap, open, 1:2
    vf = View(276, 76, 5.0)
    fx, fy = vf.X, vf.Y
    sh.text(fx(0) - 12, fy(0) - 11, "KEEPER FLAP - open, 1:2 (20.5 x 9.0, R 1.0 free corners)", "tb")
    sh.add(f'<path d="M{fx(0):.3f},{fy(KEEPER_FLAP):.3f} L{fx(0):.3f},{fy(r):.3f} '
           f'A{vf.L(r):.3f},{vf.L(r):.3f} 0 0 1 {fx(r):.3f},{fy(0):.3f} L{fx(PANEL_W - r):.3f},{fy(0):.3f} '
           f'A{vf.L(r):.3f},{vf.L(r):.3f} 0 0 1 {fx(PANEL_W):.3f},{fy(r):.3f} L{fx(PANEL_W):.3f},{fy(KEEPER_FLAP):.3f} Z" class="leather"/>')
    sh.line(fx(0), fy(KEEPER_FLAP), fx(PANEL_W), fy(KEEPER_FLAP), "fold")
    sh.text(fx(PANEL_W / 2), fy(KEEPER_FLAP) + 3.2, "hinge: stitched to tip edge of panel B", "tx", "middle")
    sh.text(fx(PANEL_W / 2), fy(KEEPER_FLAP / 2) - 2, "inner face shown", "ts", "middle")
    sh.text(fx(PANEL_W / 2), fy(KEEPER_FLAP / 2) + 2, "2 ply faux leather + interfacing, edge-stitched 0.3", "tx", "middle")
    for sx in snap_x:
        sh.snap_cap(fx(sx), fy(KEEPER_FLAP - snap_from_hinge), 2.2)
    sh.text(fx(snap_x[0]) + 4, fy(KEEPER_FLAP - snap_from_hinge) - 3, "cap+socket x2", "tx")
    sh.dim_h(fx(0), fx(PANEL_W), fy(0), fy(0) - 6, "20.5")
    sh.dim_h(fx(0), fx(snap_x[0]), fy(KEEPER_FLAP), fy(KEEPER_FLAP) + 8, "1.6")
    sh.dim_h(fx(snap_x[1]), fx(PANEL_W), fy(KEEPER_FLAP), fy(KEEPER_FLAP) + 8, "1.6")
    sh.dim_v(fy(0), fy(KEEPER_FLAP), fx(PANEL_W), fx(PANEL_W) + 7, "9.0")
    sh.dim_v(fy(KEEPER_FLAP - snap_from_hinge), fy(KEEPER_FLAP), fx(0), fx(0) - 7, "8.0")

    # table + notes
    tx = 258
    sh.text(tx, 22, "SLOT TABLE - panel B (positions from left edge, cm)", "tb")
    slot_table(sh, tx, 25, slots, SIZES_LARGE10, 10)
    sh.lines(tx, 130, [
        "**KEEPER FLAP (from prototype photos 2 and 4)",
        "- The lid hangs open when the case is used, so the",
        "  large tips need a flap: 9.0 deep (photo 2), two",
        "  snaps (photo 4), hinged on the tip edge of panel B.",
        "- Snaps sit in the 3.15 margins either side of the slot",
        "  strip, 8.0 from the hinge and 1.6 from the side",
        "  edges, so the studs on the panel clear the needles.",
        "  Studs go through panel board + lining; back each",
        "  with a 2 x 2 cm leather patch.",
        "- Flap covers 9.0 of the 12.5 panel: the tip points",
        "  (1.5-6.5 from the hinge) are fully covered.",
        "- Check snap engagement after a dry fold; move the",
        "  caps 0.1-0.2 toward the hinge if the flap pulls tight.",
        "",
    ] + panel_notes()[:10], "ts", 3.7)
    return sh


# ==========================================================================
# SHEET 5 - hinged page face 1 (panel C) + end caps / keys
# ==========================================================================
def acc_loops(sh, v, x_start, y0, y1, items, land=0.4):
    """items: list of (label, width). Returns end x."""
    X, Y, L = v.X, v.Y, v.L
    x = x_start
    total = sum(w for _, w in items) + land * (len(items) - 1)
    sh.rect(X(x_start), Y(y0), L(total), L(y1 - y0), "elastic")
    for lab, w in items:
        for xx in (x, x + w):
            sh.line(X(xx), Y(y0) - 0.6, X(xx), Y(y1) + 0.6, "stitch")
        sh.text(X(x + w / 2) + 0.8, Y((y0 + y1) / 2), lab, "tx", "middle", rot=-90)
        x += w + land
    return x - land


def sheet5():
    sh = Sheet(5, "Hinged page, face 1 - panel C: 5 cm tips 2.0-5.0 mm (11 pairs) + caps & keys", "1:1")
    sh.frame()
    v = View(32, 48, 10.0)
    X, Y, L = v.X, v.Y, v.L
    tip_m, nl, butt_m = 1.5, 5.0, 1.5
    b0, b1 = 3.0, 5.0
    margin, slots = slot_layout(SIZES_SMALL, PANEL_W)
    sh.rect(X(0), Y(0), L(PANEL_W), L(PANEL_H), "leather")
    for lab, a, b in slots:
        draw_needle_pair(sh, v, a, b, tip_m, nl, float(lab) / 10.0)
    draw_slot_strip(sh, v, slots, b0, b1)
    sh.text(X(PANEL_W / 2), Y(PANEL_H + 1.5) + 35, "PAGE FACE 1 - 20.5 x 12.5 (page hinge along the BOTTOM edge, 1.5 cm strip to front wall). Full size 1:1 - use as pattern.", "tb", "middle")
    # needle zone dims
    xl = X(0) - 7
    sh.dim_v(Y(0), Y(tip_m), X(0), xl, "1.5")
    sh.dim_v(Y(tip_m), Y(tip_m + nl), X(0), xl, "5.0 tip")
    sh.dim_v(Y(tip_m + nl), Y(8.0), X(0), xl, "1.5")
    sh.dim_v(Y(8.0), Y(PANEL_H), X(0), xl, "4.5 accessories")
    sh.dim_v(Y(0), Y(PANEL_H), X(0), xl - 8, "12.5")
    xr = X(PANEL_W) + 7
    sh.dim_v(Y(0), Y(b0), X(PANEL_W), xr, "3.0")
    sh.dim_v(Y(b0), Y(b1), X(PANEL_W), xr, "2.0 band")
    # divider line between zones
    sh.line(X(0), Y(8.0), X(PANEL_W), Y(8.0), "thin")
    # accessory loops: 6 end caps (1.6) + 4 keys (1.4)
    items = [(f"CAP {i + 1}", 1.6) for i in range(6)] + [(f"KEY {i + 1}", 1.4) for i in range(4)]
    body = sum(w for _, w in items) + 0.4 * (len(items) - 1)
    ax = (PANEL_W - body) / 2
    ay0, ay1 = 9.0, 11.5
    aend = acc_loops(sh, v, ax, ay0, ay1, items)
    sh.dim_v(Y(8.0), Y(ay0), X(PANEL_W), xr, "1.0")
    sh.dim_v(Y(ay0), Y(ay1), X(PANEL_W), xr, "2.5 elastic")
    yb = Y(PANEL_H + 1.5) + 10
    sh.dim_h(X(0), X(ax), Y(PANEL_H), yb, fmt(ax))
    sh.dim_h(X(ax), X(ax + 1.6), Y(PANEL_H), yb, "1.6")
    sh.dim_h(X(ax + 1.6), X(ax + 2.0), Y(PANEL_H), yb, "0.4", ext=False, textpos="below")
    sh.dim_h(X(aend - 1.4), X(aend), Y(PANEL_H), yb, "1.4")
    sh.dim_h(X(aend), X(PANEL_W), Y(PANEL_H), yb, fmt(PANEL_W - aend))
    sh.dim_h(X(ax), X(aend), Y(PANEL_H), yb + 8, f"{fmt(body)} elastic loop strip: 6 cap loops 1.6 + 4 key loops 1.4, 0.4 lands")
    sh.dim_h(X(0), X(PANEL_W), Y(PANEL_H), yb + 16, "20.5")
    # ordinate for slots (above)
    yo = Y(0) - 8
    sh.line(X(0), yo, X(PANEL_W), yo, "dim")
    sh.text(X(0), yo - 11, "ORDINATE: slot stitch-line positions from left edge (cm) - identical to panel A", "tx")
    for lab, a, b in slots:
        for x in (a, b):
            sh.line(X(x), yo - 1.5, X(x), Y(0), "dim")
            sh.text(X(x) + 0.7, yo - 2.2, fmt(x), "tx", "start", rot=-90)
    sh.line(X(0), yo - 2.5, X(0), yo + 2.5, "dim")
    sh.text(X(0), yo - 1.2, "0", "tx", "middle")
    # hinge strip at the bottom
    sh.rect(X(0), Y(PANEL_H), L(PANEL_W), L(1.5), "hatch")
    sh.rect(X(0), Y(PANEL_H), L(PANEL_W), L(1.5), "thin")
    sh.text(X(PANEL_W / 2), Y(PANEL_H + 0.75) + 1, "HINGE STRIP 20.5 x 1.5 - faux leather, stitched to page edge and to front-wall inner face", "tx", "middle")
    sh.dim_v(Y(PANEL_H), Y(PANEL_H + 1.5), X(PANEL_W), xr, "1.5")

    tx = 258
    sh.text(tx, 22, "SLOT TABLE - panel C (positions from left edge, cm)", "tb")
    end = slot_table(sh, tx, 25, slots, SIZES_SMALL, 5)
    sh.lines(tx, end + 6, [
        "**PAGE (both faces) - proposal, not in prototype",
        "- One double-sided page carries all 5 cm tips plus the",
        "  small hardware, so the 10 cm panels stay uncluttered.",
        "  Core 1.5 mm board, lined both faces, 20.5 x 12.5.",
        "- Hinge: 1.5 cm faux-leather strip along the bottom",
        "  edge, stitched to the front-wall inner face. The page",
        "  lies on panel A when closed and flips onto the lid",
        "  when the case is opened (sheet 2).",
        "- Face 1 (this sheet): 5 cm tips 2.0-5.0 mm in the same",
        "  slot widths and positions as panel A, band 2.0 wide",
        "  (narrower for the short tips). Below: 2.5 cm elastic",
        "  with 6 loops for the screw-on end caps (1.6 wide)",
        "  and 4 loops for the cable keys (1.4 wide).",
        "- Loop sizes assume caps <= 1.0 dia x 1.5 long and keys",
        "  <= 1.2 x 3.5. Measure the real hardware (Q6, sheet 2).",
        "",
    ] + panel_notes()[:9], "ts", 3.7)
    return sh


# ==========================================================================
# SHEET 6 - hinged page face 2 (panel D) + connectors, grip patch, cable pocket
# ==========================================================================
def sheet6():
    sh = Sheet(6, "Hinged page, face 2 - panel D: 5 cm tips 5.5-8 mm (4 pairs) + accessories", "1:1")
    sh.frame()
    v = View(32, 48, 10.0)
    X, Y, L = v.X, v.Y, v.L
    tip_m, nl, butt_m = 1.5, 5.0, 1.5
    b0, b1 = 3.0, 5.0
    sh.rect(X(0), Y(0), L(PANEL_W), L(PANEL_H), "leather")
    # Panel D strip in the left zone: margins 1.0
    _, slots = slot_layout(SIZES_LARGE5, 0, margin=1.0)
    for lab, a, b in slots:
        draw_needle_pair(sh, v, a, b, tip_m, nl, float(lab) / 10.0)
    draw_slot_strip(sh, v, slots, b0, b1)
    zone_w = slots[-1][2] + 1.0          # 10.9
    sh.line(X(zone_w), Y(0), X(zone_w), Y(PANEL_H), "thin")
    sh.text(X(PANEL_W / 2), Y(PANEL_H) + 35, "PAGE FACE 2 - 20.5 x 12.5 (reverse of face 1; hinge along the BOTTOM edge). Full size 1:1 - use as pattern.", "tb", "middle")
    # connector loops + patch pocket below
    sh.line(X(0), Y(8.0), X(zone_w), Y(8.0), "thin")
    items = [(f"CONN {i + 1}", 1.4) for i in range(3)]
    cend = acc_loops(sh, v, 1.0, 9.0, 11.5, items)
    # grip patch slip pocket
    px0, px1 = cend + 0.6, zone_w - 0.6
    sh.rect(X(px0), Y(8.5), L(px1 - px0), L(3.5), "band")
    sh.line(X(px0), Y(8.5), X(px1), Y(8.5), "cut")
    sh.text(X((px0 + px1) / 2), Y(10.3), "GRIP PATCH", "tx", "middle")
    sh.text(X((px0 + px1) / 2), Y(11.1), "slip pocket", "tx", "middle")
    # cable pocket in right zone
    cx0 = zone_w + 0.6
    cw = PANEL_W - cx0 - 0.6
    sh.rect(X(cx0), Y(0.6), L(cw), L(PANEL_H - 1.2), "mesh")
    # zip along the top
    sh.rect(X(cx0), Y(0.6), L(cw), L(0.8), "thin")
    for i in range(int(L(cw) / 2)):
        sh.line(X(cx0) + i * 2 + 1, Y(0.6) + 1, X(cx0) + i * 2 + 1, Y(0.6) + 7, "thin")
    sh.text(X(cx0 + cw / 2), Y(1.0) + 0.9, "zip (8 cm)", "tx", "middle")
    # coiled cables suggestion
    ccx, ccy = X(cx0 + cw / 2), Y(6.8)
    for i, lab in enumerate(["100", "80", "60", "40", "25"]):
        sh.circle(ccx, ccy, 36 - i * 6, "thin")
    sh.text(ccx, Y(2.55), "5 cables (25 / 40 / 60 / 80 / 100 cm) coiled to <= 8 cm dia", "tx", "middle")
    sh.text(X(cx0 + cw / 2), Y(PANEL_H - 1.3), "CABLE POCKET - mesh front, zip top, grip-patch slip pocket behind", "tx", "middle")
    # dims
    xl = X(0) - 7
    sh.dim_v(Y(0), Y(tip_m), X(0), xl, "1.5")
    sh.dim_v(Y(tip_m), Y(tip_m + nl), X(0), xl, "5.0 tip")
    sh.dim_v(Y(tip_m + nl), Y(8.0), X(0), xl, "1.5")
    sh.dim_v(Y(8.0), Y(9.0), X(0), xl, "1.0")
    sh.dim_v(Y(9.0), Y(11.5), X(0), xl, "2.5")
    sh.dim_v(Y(11.5), Y(PANEL_H), X(0), xl, "1.0")
    sh.dim_v(Y(0), Y(b0), X(0), xl - 8, "3.0")
    sh.dim_v(Y(b0), Y(b1), X(0), xl - 8, "2.0 band")
    sh.dim_v(Y(0), Y(PANEL_H), X(0), xl - 16, "12.5")
    xr = X(PANEL_W) + 7
    sh.dim_v(Y(0), Y(0.6), X(PANEL_W), xr, "0.6")
    sh.dim_v(Y(0.6), Y(PANEL_H - 0.6), X(PANEL_W), xr, f"{fmt(PANEL_H - 1.2)} pocket")
    sh.dim_v(Y(PANEL_H - 0.6), Y(PANEL_H), X(PANEL_W), xr, "0.6")
    yb = Y(PANEL_H) + 10
    sh.dim_h(X(0), X(1.0), Y(PANEL_H), yb, "1.0")
    x = 1.0
    for lab, a, b in slots:
        sh.dim_h(X(a), X(b), Y(PANEL_H), yb, fmt(b - a))
        if b < slots[-1][2]:
            sh.dim_h(X(b), X(b + LAND), Y(PANEL_H), yb, "0.5", ext=False, textpos="below")
    sh.dim_h(X(slots[-1][2]), X(zone_w), Y(PANEL_H), yb, "1.0")
    sh.dim_h(X(zone_w), X(cx0), Y(PANEL_H), yb, "0.6", ext=False, textpos="below")
    sh.dim_h(X(cx0), X(cx0 + cw), Y(PANEL_H), yb, f"{fmt(cw)} cable pocket")
    sh.dim_h(X(cx0 + cw), X(PANEL_W), Y(PANEL_H), yb, "0.6", ext=False, textpos="below")
    sh.dim_h(X(0), X(zone_w), Y(PANEL_H), yb + 8, f"{fmt(zone_w)} panel D zone")
    sh.dim_h(X(0), X(PANEL_W), Y(PANEL_H), yb + 16, "20.5")
    sh.dim_h(X(1.0), X(cend), Y(8.0), Y(8.0) - 6, f"{fmt(cend - 1.0)} = 3 loops x 1.4 + 2 lands x 0.4", textpos="above")
    sh.dim_h(X(px0), X(px1), Y(8.0), Y(8.0) - 6, f"{fmt(px1 - px0)} pocket")
    # ordinate for slot stitch lines
    yo = Y(0) - 8
    sh.line(X(0), yo, X(zone_w), yo, "dim")
    sh.text(X(0), yo - 11, "ORDINATE: slot stitch-line positions from left edge (cm)", "tx")
    for lab, a, b in slots:
        for xx in (a, b):
            sh.line(X(xx), yo - 1.5, X(xx), Y(0), "dim")
            sh.text(X(xx) + 0.7, yo - 2.2, fmt(xx), "tx", "start", rot=-90)
    sh.line(X(0), yo - 2.5, X(0), yo + 2.5, "dim")
    sh.text(X(0), yo - 1.2, "0", "tx", "middle")

    tx = 258
    sh.text(tx, 22, "SLOT TABLE - panel D (positions from left edge, cm)", "tb")
    end = slot_table(sh, tx, 25, slots, SIZES_LARGE5, 5)
    sh.lines(tx, end + 6, [
        "**FACE 2 LAYOUT - proposal, not in prototype",
        "- Panel D: 5 cm tips 5.5 / 6 / 7 / 8 mm, slot widths",
        "  1.7-2.0 as on the prototype (photo 4), 1.0 margins,",
        "  band 2.0 wide. Zone width 10.9.",
        "- Below panel D: 3 connector loops (1.4 wide, 2.5 cm",
        "  elastic) and a slip pocket 4.3 x 3.5 for the leather",
        "  grip patch (see spec, right).",
        "- Cable pocket 8.5 x 11.3: mesh front, 8 cm zip along the",
        "  top, 0.6 cm bound edges. Holds the 5 cables coiled",
        "  to <= 8 cm dia. A second slip pocket behind the mesh",
        "  can take a pattern card.",
        "",
        "**LEATHER GRIP PATCH (replaces the rubber grip disc)",
        "- Vegetable-tanned leather 1.8-2.0 mm, 6.0 x 4.0 cm,",
        "  R 0.5 corners, suede side out for grip. Burnish edges.",
        "- Optional: 0.6 cm punched hole in one corner so it can",
        "  be looped onto a cable key.",
        "- Fold it round the tip when tightening / loosening.",
        "",
        "**ELASTIC LOOP SPEC (caps, keys, connectors)",
        "- 25 mm knit elastic stitched flat on every line; the",
        "  loop widths are flat widths. Elastic stretches to",
        "  take hardware up to ~1.5x the loop width.",
    ], "ts", 3.7)
    return sh


# ==========================================================================
# SHEET 7 - contents, BOM, construction
# ==========================================================================
def sheet7():
    sh = Sheet(7, "Contents checklist, bill of materials, construction & cutting list", "-")
    sh.frame()
    x0, y0 = 14, 26
    sh.text(x0, y0, "CONTENTS CHECKLIST - 64 tips (32 pairs), 5 cables, 14 accessories: where each item lives", "tb")
    rows = []
    for i, (lab, w) in enumerate(SIZES_SMALL):
        rows.append([f"{lab} mm", "2 x 10 cm", "A (base)", str(i + 1), fmt(w), "2 x 5 cm", "C (page f.1)", str(i + 1), fmt(w)])
    for i, (lab, w) in enumerate(SIZES_LARGE10):
        c = ("D (page f.2)", str(i + 1), fmt(w)) if i < 4 else ("-", "-", "-")
        rows.append([f"{lab} mm", "2 x 10 cm", "B (lid)", str(i + 1), fmt(w), "2 x 5 cm" if i < 4 else "-", *c])
    end = sh.table(x0, y0 + 3, ["Size", "10 cm tips", "Panel", "Slot", "w", "5 cm tips", "Panel", "Slot", "w"],
                   rows, [16, 18, 18, 10, 10, 18, 22, 10, 10], rh=4.0)
    sh.text(x0, end + 4, "Totals: 17 pairs x 10 cm (34 tips) on panels A + B;  15 pairs x 5 cm (30 tips) on panels C + D;  32 pairs / 64 tips.", "ts")
    sh.text(x0, end + 8, "Accessories: 6 end caps + 4 keys -> face 1 loops;  3 connectors + grip patch -> face 2;  5 cables -> face 2 pocket.", "ts")

    # BOM
    bx, by = 150, 26
    sh.text(bx, by, "BILL OF MATERIALS (per case)", "tb")
    bom = [
        ["1", "Outer shell, faux leather (PU) 1.0-1.2 mm", "1", "48.4 x 43.2 net + allowance (sheet 1)"],
        ["2", "Lining, faux leather 0.6-0.8 mm or cotton", "1", "48.4 x 43.2 net + allowance"],
        ["3", "Greyboard 1.5 mm: base, lid, 4 walls", "6", "21x13, 21x12.7, 21x6.5, 21x6, 2 of 5.7x13"],
        ["4", "Greyboard 1.5 mm: panels A, B, page", "3", "20.5 x 12.5"],
        ["5", "Panel lining faux leather (wrap)", "3", "24.5 x 16.5 (2.0 wrap)"],
        ["6", "Knit elastic 25 mm, slot bands", "4", "17.1 / 14.2 / 17.1 / 8.9 cm"],
        ["7", "Knit elastic 25 mm, accessory loops", "2", "18.8 / 5.0 cm"],
        ["8", "Keeper flap faux leather (2 ply)", "2", "20.5 x 9.0 + allowance"],
        ["9", "Hinge strip faux leather", "1", "20.5 x 3.0 (folded to 1.5)"],
        ["10", "Mesh, cable pocket front", "1", "8.5 x 11.3 + allowance"],
        ["11", "Zip, #3 nylon coil", "1", "8 cm"],
        ["12", "Spring snaps 12.5 mm (line 20), 4-part", "4 sets", "2 end flaps + 2 keeper flap"],
        ["13", "Snap backing patches, leather 2 x 2 cm", "4", "behind lid studs / panel B studs"],
        ["14", "Leather grip patch, veg-tan 1.8-2 mm", "1", "6.0 x 4.0, R 0.5"],
        ["15", "Thread, bonded nylon / polyester Tex 70", "-", "stitch length 3 mm"],
        ["16", "Interfacing (if soft case, no board)", "1", "48.4 x 43.2"],
    ]
    end2 = sh.table(bx, by + 3, ["#", "Item", "Qty", "Cut size (cm) / note"], bom, [8, 90, 14, 90], rh=4.0)

    # construction notes
    cx, cy = 150, end2 + 8
    sh.lines(cx, cy, [
        "**CONSTRUCTION SEQUENCE",
        "1. Cut outer shell and lining from sheet 1 (net + allowance). Score fold lines on the board side.",
        "2. Make the three interior panels first (sheets 3-6): wrap board in lining, stitch bands / loops / pockets",
        "   through the lining BEFORE wrapping so no stitching shows on the back. Set panel B studs.",
        "3. Set end-flap snap caps on the outer shell while flat. Studs on the lid outer face: mark from a dry fold.",
        "4. Laminate board to the outer shell (base, lid, walls); turn / bind all edges; top-stitch at 0.3 cm.",
        "5. Form the box: fold the walls, glue corner tabs or stitch the corners (box-stitch) outside-in.",
        "6. Glue + edge-stitch panel A into the base, panel B into the lid; stitch the page hinge to the front wall.",
        "7. Stitch the keeper flap to the tip edge of panel B. Check all 4 snaps engage cleanly.",
        "8. Load the set in the order of the contents checklist and check the stack height closes without pressure.",
        "",
        "**TOLERANCES",
        "Cut pieces +/- 0.1 cm; slot stitch lines +/- 0.05 cm (the 0.6 slot must still take two 2 mm tips); snap centres +/- 0.15 cm.",
        "Interior panels are 0.5 cm smaller than the box interior in both directions to allow for lining thickness.",
    ], "ts", 3.8)

    # measurement record
    mx, my = 14, 172
    sh.text(mx, my, "PROTOTYPE MEASUREMENT RECORD - what each photo contributed", "tb")
    mend = sh.table(mx, my + 3, ["Photo", "Feature", "Value used on drawings"], [
        ["1", "Outer shell cross pattern", "Rear flap 5.0, rear wall 6.5, base 21.0 x 13.0, front wall 6.0, lid 12.7; side wall 5.7, end flap 8.0, snaps"],
        ["2", "Panel with 9 cm flap, large sizes (early draft)", "Keeper flap depth 9.0; 20.5 panel length. Row widths superseded by photo 4"],
        ["3", "Panel 2.0-5.0 mm, 11 rows", "Slot widths 0.6-1.6 (= 6-16 mm), 0.5 lands, 1.0 end margins, 1.5 side margin"],
        ["4", "Panel 5.5-10 mm, 6 rows + 2-snap flap", "Slot widths 1.7-2.2, 0.5 lands, 0.5 top / 1.0 bottom margin, two snap tabs"],
        ["5", "Panel 2.0-5.0 mm, clean copy", "Confirms photo 3 widths and 0.5 'between typical'; used for the 5 cm tip panel C"],
    ], [14, 70, 150], rh=4.2)
    hx = 14
    sh.text(hx, mend + 8, "HARDWARE SIZE ASSUMPTIONS (loops sized to these; measure the real parts - Q6)", "tb")
    sh.table(hx, mend + 11, ["Item", "Qty", "Assumed size (cm)", "Loop / pocket on drawing"], [
        ["Screw-on end cap", "6", "1.0 dia x 1.5", "1.6 wide loop, face 1"],
        ["Cable key", "4", "1.2 x 3.5", "1.4 wide loop, face 1"],
        ["Cable connector", "3", "1.0 dia x 3.0", "1.4 wide loop, face 2"],
        ["Leather grip patch", "1", "6.0 x 4.0 x 0.2", "4.3 x 3.5 slip pocket, face 2 (patch folds in half)"],
        ["Cables 25-100 cm", "5", "coil to 8.0 dia", "8.4 x 11.3 zip pocket, face 2"],
    ], [40, 12, 48, 120], rh=4.2)
    return sh


# ==========================================================================
def main():
    sheets = [sheet1(), sheet2(), sheet3(), sheet4(), sheet5(), sheet6(), sheet7()]
    names = []
    for sh in sheets:
        fn = f"sheet{sh.n}.svg"
        with open(os.path.join(OUT, fn), "w") as f:
            f.write(sh.svg())
        names.append((fn, sh.title))
    # print-ready HTML (A3 landscape pages)
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
