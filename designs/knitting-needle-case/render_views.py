#!/usr/bin/env python3
"""
Presentation views of the needle case, generated from the same geometry as
the drawing set (generate_drawings.py).  Not photographs: styled vector
illustrations so the cover sheet shows the design as drawn, not the earlier
reference products.

Run:  python3 render_views.py      -> renders/*.svg, renders/*.png, renders/*.jpg
"""
import base64
import math
import os

import generate_drawings as G

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "renders")
os.makedirs(OUT, exist_ok=True)

FONT = G.FONT
LEATHER_CSS = """
.bg{fill:#f3efe8}
.lth{fill:url(#lth);stroke:#5a4634;stroke-width:0.35}
.lth2{fill:url(#lth2);stroke:#5a4634;stroke-width:0.35}
.lth3{fill:url(#lth3);stroke:#5a4634;stroke-width:0.35}
.edge{fill:none;stroke:#efe2c8;stroke-width:0.45;stroke-dasharray:1.1,0.7}
.strap{fill:url(#strap);stroke:#2a1a10;stroke-width:0.35}
.strapedge{fill:none;stroke:#c8905a;stroke-width:0.35;stroke-dasharray:1,0.7}
.brass{fill:url(#brass);stroke:#6b4f1f;stroke-width:0.3}
.needle{fill:url(#metal);stroke:#4a4a4a;stroke-width:0.15}
.elastic{fill:url(#elastic);stroke:#7a6a52;stroke-width:0.3}
.slit{stroke:#3a2d20;stroke-width:0.8}
.tack{stroke:#efe2c8;stroke-width:0.4;stroke-dasharray:0.6,0.5}
.shadow{fill:#000;opacity:0.18;filter:url(#blur)}
.lab{font-family:%s;font-size:2.2px;fill:#4a3b2c;text-anchor:middle}
.lab2{font-family:%s;font-size:1.7px;fill:#4a3b2c;text-anchor:middle}
.cap{font-family:%s;font-size:3.6px;fill:#3a3028;letter-spacing:0.5px;text-anchor:middle}
.hole{fill:#3a2415}
""" % (FONT, FONT, FONT)

DEFS = """
<defs>
 <linearGradient id="lth" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#dcc7a6"/><stop offset="0.55" stop-color="#cbb08a"/><stop offset="1" stop-color="#b8996f"/>
 </linearGradient>
 <linearGradient id="lth2" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#c9ad86"/><stop offset="1" stop-color="#ad8f68"/>
 </linearGradient>
 <linearGradient id="lth3" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#b3936a"/><stop offset="1" stop-color="#9c7d57"/>
 </linearGradient>
 <linearGradient id="strap" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#4a2e1c"/><stop offset="0.5" stop-color="#5e3b24"/><stop offset="1" stop-color="#3b2314"/>
 </linearGradient>
 <linearGradient id="brass" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#e3c77a"/><stop offset="0.5" stop-color="#b8923f"/><stop offset="1" stop-color="#d9b85d"/>
 </linearGradient>
 <linearGradient id="metal" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#7d8186"/><stop offset="0.35" stop-color="#eef0f2"/><stop offset="0.6" stop-color="#b9bec4"/><stop offset="1" stop-color="#676b70"/>
 </linearGradient>
 <linearGradient id="elastic" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#d9c7a8"/><stop offset="1" stop-color="#bfa988"/>
 </linearGradient>
 <pattern id="weave" patternUnits="userSpaceOnUse" width="0.6" height="0.6">
  <rect width="0.6" height="0.6" fill="none"/><line x1="0" y1="0.3" x2="0.6" y2="0.3" stroke="#a08d6e" stroke-width="0.12"/>
 </pattern>
 <filter id="blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2"/></filter>
</defs>
"""


def logo_data():
    with open(os.path.join(HERE, "reference", "logo.png"), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.p = []

    def add(self, s):
        self.p.append(s)

    def rect(self, x, y, w, h, cls, rx=0):
        self.add(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" rx="{rx}" class="{cls}"/>')

    def path(self, d, cls):
        self.add(f'<path d="{d}" class="{cls}"/>')

    def line(self, x1, y1, x2, y2, cls):
        self.add(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" class="{cls}"/>')

    def circle(self, x, y, r, cls):
        self.add(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" class="{cls}"/>')

    def text(self, x, y, s, cls):
        self.add(f'<text x="{x:.3f}" y="{y:.3f}" class="{cls}">{G.esc(s)}</text>')

    def logo(self, cx, cy, size, rot=0):
        tr = f' transform="rotate({rot} {cx:.2f} {cy:.2f})"' if rot else ""
        self.add(f'<image x="{cx - size / 2:.2f}" y="{cy - size / 2:.2f}" width="{size:.2f}" height="{size:.2f}" href="{logo_data()}"{tr}/>')

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}mm" height="{self.h}mm" viewBox="0 0 {self.w} {self.h}">'
                f'<style>{LEATHER_CSS}</style>{DEFS}<rect width="{self.w}" height="{self.h}" class="bg"/>'
                + "\n".join(self.p) + "</svg>")


def rr(X, Y, L, x, y, w, h, r, corners=(1, 1, 1, 1)):
    return G.rounded_rect_path(X, Y, L, x, y, w, h, r, corners)


# --------------------------------------------------------------------------
# 1. Closed front view
# --------------------------------------------------------------------------
def closed_front():
    c = Canvas(160, 110)
    s = 6.0
    v = G.View((160 - G.BASE_W * s) / 2, (110 - G.BASE_H * s) / 2 + 2, s)
    X, Y, L = v.X, v.Y, v.L
    c.rect(X(0.6), Y(0.9), L(G.BASE_W), L(G.BASE_H), "shadow", rx=6)
    c.path(rr(X, Y, L, 0, 0, G.BASE_W, G.BASE_H, G.R), "lth")
    c.path(rr(X, Y, L, 0.3, 0.3, G.BASE_W - 0.6, G.BASE_H - 0.6, G.R - 0.3), "edge")
    # flap edge with a soft shade below it
    c.path(rr(X, Y, L, 0, 0, G.BASE_W, G.REAR_FLAP, G.R, (1, 1, 0, 0)), "lth2")
    c.path(rr(X, Y, L, 0.3, 0.3, G.BASE_W - 0.6, G.REAR_FLAP - 0.6, G.R - 0.3, (1, 1, 0, 0)), "edge")
    cx = G.BASE_W / 2
    # strap down the front, buckle piece, keeper, tongue, snap
    c.rect(X(cx - G.STRAP_W / 2), Y(0), L(G.STRAP_W), L(G.STRAP_STUD_FROM_TOP + 0.5), "strap")
    c.path(f"M{X(cx - G.STRAP_W / 2):.2f},{Y(G.STRAP_STUD_FROM_TOP + 0.5):.2f} L{X(cx + G.STRAP_W / 2):.2f},{Y(G.STRAP_STUD_FROM_TOP + 0.5):.2f} L{X(cx):.2f},{Y(G.STRAP_STUD_FROM_TOP + 1.8):.2f} Z", "strap")
    c.line(X(cx - G.STRAP_W / 2 + 0.3), Y(0), X(cx - G.STRAP_W / 2 + 0.3), Y(G.STRAP_STUD_FROM_TOP + 0.6), "strapedge")
    c.line(X(cx + G.STRAP_W / 2 - 0.3), Y(0), X(cx + G.STRAP_W / 2 - 0.3), Y(G.STRAP_STUD_FROM_TOP + 0.6), "strapedge")
    c.rect(X(cx - G.STRAP_W / 2), Y(G.BUCKLE_ON_FLAP - 1.5), L(G.STRAP_W), L(4.5), "strap")
    bw, bh = L(G.STRAP_W + 0.6), L(1.4)
    c.rect(X(cx) - bw / 2, Y(G.BUCKLE_ON_FLAP) - bh / 2, bw, bh, "brass", rx=1.2)
    c.rect(X(cx) - bw / 2 + 1.3, Y(G.BUCKLE_ON_FLAP) - bh / 2 + 1.3, bw - 2.6, bh - 2.6, "strap")
    c.line(X(cx), Y(G.BUCKLE_ON_FLAP) - bh / 2, X(cx), Y(G.BUCKLE_ON_FLAP) + bh / 2 + 1.2, "brass")
    c.rect(X(cx - G.STRAP_W / 2 - 0.2), Y(G.KEEPER_ON_FLAP - 0.35), L(G.STRAP_W + 0.4), L(0.7), "strap")
    for i in (1.6, 2.8):
        c.circle(X(cx), Y(i), 0.9, "hole")
    c.circle(X(cx), Y(G.STRAP_STUD_FROM_TOP), 2.8, "brass")
    c.circle(X(cx), Y(G.STRAP_STUD_FROM_TOP), 1.1, "strap")
    c.logo(X(G.BASE_W - 3.0), Y(G.LOGO_FROM_TOP), L(2.5))
    c.text(80, 105, "CLOSED, FRONT  -  21 x 13 x 6 cm", "cap")
    return c


# --------------------------------------------------------------------------
# 2. Closed isometric
# --------------------------------------------------------------------------
def closed_iso():
    c = Canvas(160, 110)
    s = 3.2
    ox, oy = 60, 52
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))
    W, D, H = G.BASE_W, 6.0, G.BASE_H

    def P(x, y, z):
        return (ox + (x - y) * c30 * s, oy + (x + y) * s30 * s - z * s)

    def poly(pts, cls):
        c.path("M" + " L".join(f"{a:.2f},{b:.2f}" for a, b in pts) + " Z", cls)
    # shadow
    poly([P(-0.5, -0.5, -0.3), P(W + 1.5, -0.5, -0.3), P(W + 1.5, D + 1.0, -0.3), P(-0.5, D + 1.0, -0.3)], "shadow")
    poly([P(0, 0, H), P(W, 0, H), P(W, D, H), P(0, D, H)], "lth2")            # top
    poly([P(0, D, 0), P(W, D, 0), P(W, D, H), P(0, D, H)], "lth")             # front
    poly([P(0, D, H - G.REAR_FLAP), P(W, D, H - G.REAR_FLAP), P(W, D, H), P(0, D, H)], "lth2")   # flap over the front
    poly([P(W, 0, 0), P(W, D, 0), P(W, D, H), P(W, 0, H)], "lth3")            # right end
    # stitching lines near edges
    for a, b in [(P(0.3, 0.3, H), P(W - 0.3, 0.3, H)), (P(0.3, D - 0.3, H), P(W - 0.3, D - 0.3, H)),
                 (P(0.3, D, H - 0.3), P(W - 0.3, D, H - 0.3)), (P(0.3, D, 0.3), P(W - 0.3, D, 0.3)),
                 (P(W, 0.3, 0.3), P(W, D - 0.3, 0.3)), (P(W, 0.3, H - 0.3), P(W, D - 0.3, H - 0.3))]:
        c.line(a[0], a[1], b[0], b[1], "edge")
    # flap edge on the front face (10 cm below the top)
    a, b = P(0, D, H - G.REAR_FLAP), P(W, D, H - G.REAR_FLAP)
    c.line(a[0], a[1], b[0], b[1], "edge")
    c.add(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="#5a4634" stroke-width="0.4"/>')
    # strap: over the top (y from 0 to D) and down the front (z from H to H-11.5)
    cx = W / 2
    poly([P(cx - 1.5, 0, H), P(cx + 1.5, 0, H), P(cx + 1.5, D, H), P(cx - 1.5, D, H)], "strap")
    zt = H - G.STRAP_STUD_FROM_TOP - 0.5
    poly([P(cx - 1.5, D, H), P(cx + 1.5, D, H), P(cx + 1.5, D, zt), P(cx - 1.5, D, zt)], "strap")
    poly([P(cx - 1.5, D, zt), P(cx + 1.5, D, zt), P(cx, D, zt - 1.3)], "strap")
    # buckle piece / buckle / keeper on the front face
    zb = H - G.BUCKLE_ON_FLAP
    poly([P(cx - 1.5, D, zb + 1.5), P(cx + 1.5, D, zb + 1.5), P(cx + 1.5, D, zb - 3.0), P(cx - 1.5, D, zb - 3.0)], "strap")
    poly([P(cx - 1.8, D + 0.15, zb + 0.7), P(cx + 1.8, D + 0.15, zb + 0.7), P(cx + 1.8, D + 0.15, zb - 0.7), P(cx - 1.8, D + 0.15, zb - 0.7)], "brass")
    poly([P(cx - 1.3, D + 0.16, zb + 0.35), P(cx + 1.3, D + 0.16, zb + 0.35), P(cx + 1.3, D + 0.16, zb - 0.35), P(cx - 1.3, D + 0.16, zb - 0.35)], "strap")
    zk = H - G.KEEPER_ON_FLAP
    poly([P(cx - 1.7, D + 0.1, zk + 0.35), P(cx + 1.7, D + 0.1, zk + 0.35), P(cx + 1.7, D + 0.1, zk - 0.35), P(cx - 1.7, D + 0.1, zk - 0.35)], "strap")
    sp = P(cx, D + 0.15, H - G.STRAP_STUD_FROM_TOP)
    c.add(f'<ellipse cx="{sp[0]:.2f}" cy="{sp[1]:.2f}" rx="2.4" ry="2.4" class="brass"/>')
    # logo on the front face via an affine map of face coords (u along X, w down the face)
    a_, b_ = P(0, D, H)
    m = f"matrix({c30 * s:.4f},{s30 * s:.4f},0,{s:.4f},{a_:.3f},{b_:.3f})"
    lx, ly = W - 3.0, G.LOGO_FROM_TOP
    c.add(f'<g transform="{m}"><image x="{lx - 1.25:.2f}" y="{ly - 1.25:.2f}" width="2.5" height="2.5" href="{logo_data()}"/></g>')
    c.text(80, 105, "CLOSED  -  strap wraps the case", "cap")
    return c


# --------------------------------------------------------------------------
# Panel faces (shared)
# --------------------------------------------------------------------------
def panel_face(c, v, sizes, tip_len, tip_top, band_c, x_offset=0.0, zone_w=None, backwall=False,
               page_outline=True, labels=True):
    X, Y, L = v.X, v.Y, v.L
    Wd, Hd = (G.BASE_W, G.BASE_H) if backwall else (G.PAGE_W, G.PAGE_H)
    zone_w = Wd if zone_w is None else zone_w
    margin, slots = G.slot_layout(sizes, zone_w, margin=None)
    slots = [(lab, a + x_offset, b + x_offset) for lab, a, b in slots]
    if page_outline:
        c.rect(X(0.5), Y(0.7), L(Wd), L(Hd), "shadow", rx=4)
        c.path(rr(X, Y, L, 0, 0, Wd, Hd, G.R, (1, 1, 1, 1) if backwall else (1, 1, 0, 0)), "lth")
        c.path(rr(X, Y, L, 0.3, 0.3, Wd - 0.6, Hd - 0.6, G.R - 0.3, (1, 1, 1, 1) if backwall else (1, 1, 0, 0)), "edge")
    # needles
    for lab, a, b in slots:
        d = float(lab) / 10.0
        cxm = (a + b) / 2
        for side in (-1, 1):
            cc = cxm + side * (d / 2 + 0.03)
            xl, xr = X(cc - d / 2), X(cc + d / 2)
            yt, yb = Y(tip_top), Y(tip_top + tip_len)
            tip = Y(tip_top + min(1.6, tip_len * 0.3))
            c.path(f"M{X(cc):.2f},{yt:.2f} L{xr:.2f},{tip:.2f} L{xr:.2f},{yb:.2f} L{xl:.2f},{yb:.2f} L{xl:.2f},{tip:.2f} Z", "needle")
            # join line (interchangeable thread end) near the butt
            c.line(xl, Y(tip_top + tip_len - 0.9), xr, Y(tip_top + tip_len - 0.9), "slit")
    # elastic loops threaded through slits
    y0, y1 = band_c - G.ELASTIC / 2, band_c + G.ELASTIC / 2
    for lab, a, b in slots:
        c.rect(X(a), Y(y0), L(b - a), L(y1 - y0), "elastic", rx=0.3)
        c.add(f'<rect x="{X(a):.2f}" y="{Y(y0):.2f}" width="{L(b - a):.2f}" height="{L(y1 - y0):.2f}" fill="url(#weave)"/>')
        for xx in (a, b):
            c.line(X(xx), Y(band_c - G.SLIT / 2), X(xx), Y(band_c + G.SLIT / 2), "slit")
            c.line(X(xx), Y(band_c - G.SLIT / 2) - 1, X(xx), Y(band_c + G.SLIT / 2) + 1, "tack")
    # labels
    for lab, a, b in (slots if labels else []):
        cxm = (a + b) / 2
        c.text(X(cxm), Y(tip_top - 1.0), lab, "lab")
        c.text(X(cxm), Y(tip_top - 1.0) + 2.0, "mm", "lab2")
        c.add(f'<line x1="{X(cxm):.2f}" y1="{Y(tip_top - 1.0) + 2.6:.2f}" x2="{X(cxm):.2f}" y2="{Y(tip_top) - 0.6:.2f}" stroke="#6b5a48" stroke-width="0.2"/>')
    return slots


def pocket(c, v, x, y, w, h, flap, snap_r):
    X, Y, L = v.X, v.Y, v.L
    c.path(rr(X, Y, L, x, y + flap - 0.5, w, h + 0.5, 0.6, (0, 0, 1, 1)), "lth2")
    c.path(rr(X, Y, L, x + 0.3, y + flap - 0.2, w - 0.6, h - 0.1, 0.4, (0, 0, 1, 1)), "edge")
    c.path(rr(X, Y, L, x, y, w, flap + 0.8, 0.6, (1, 1, 1, 1)), "lth")
    c.path(rr(X, Y, L, x + 0.3, y + 0.3, w - 0.6, flap + 0.2, 0.4, (1, 1, 1, 1)), "edge")
    c.circle(X(x + w / 2), Y(y + flap - 0.3), snap_r, "brass")
    c.circle(X(x + w / 2), Y(y + flap - 0.3), snap_r * 0.4, "lth3")


def panel1():
    c = Canvas(160, 110)
    s = 6.4
    v = G.View((160 - G.PAGE_W * s) / 2, (110 - G.PAGE_H * s) / 2 - 2, s)
    panel_face(c, v, G.SIZES_SMALL, 10.0, 1.5, 6.5)
    c.text(80, 105, "PANEL 1  -  10 cm tips 2.0-5.0 mm", "cap")
    return c


def panel2():
    c = Canvas(160, 110)
    s = 6.4
    v = G.View((160 - G.PAGE_W * s) / 2, (110 - G.PAGE_H * s) / 2 - 2, s)
    panel_face(c, v, G.SIZES_LARGE10, 10.0, 1.5, 6.5, x_offset=5.0, zone_w=15.0)
    pocket(c, v, 0.5, 0.5, 3.9, 4.1, 1.6, 1.6)
    pocket(c, v, 0.5, 6.4, 3.9, 4.1, 1.6, 1.6)
    c.text(80, 105, "PANEL 2  -  10 cm tips 5.5-10 mm + pockets", "cap")
    return c


def backwall():
    c = Canvas(160, 110)
    s = 6.2
    v = G.View((160 - G.BASE_W * s) / 2, (110 - G.BASE_H * s) / 2 - 2, s)
    panel_face(c, v, G.SIZES_LARGE5, 5.0, 4.0, 6.5, x_offset=10.8, zone_w=10.2, backwall=True)
    pocket(c, v, 0.5, 0.5, 9.7, 9.0, 3.0, 2.2)
    c.text(80, 105, "PANEL 4, BACK WALL  -  5 cm tips 5.5-8 mm + cable pocket", "cap")
    return c


# --------------------------------------------------------------------------
# 3. Open case, flat, from above (pages stacked on the back wall)
# --------------------------------------------------------------------------
def open_flat():
    c = Canvas(160, 110)
    s = 2.05
    v = G.View((160 - G.PATTERN_W * s) / 2, 3, s)
    X, Y, L = v.X, v.Y, v.L
    xa, xb = G.END_FLAP, G.END_FLAP + G.SIDE_WALL
    xc, xd = xb + G.BASE_W, xb + G.BASE_W + G.SIDE_WALL
    ya, yb = G.REAR_FLAP, G.REAR_FLAP + G.REAR_WALL
    yc, yd = yb + G.BASE_H, yb + G.BASE_H + G.FRONT_WALL
    c.rect(X(0.4), Y(yb + 0.6), L(G.PATTERN_W), L(G.BASE_H), "shadow", rx=3)
    c.rect(X(xb + 0.4), Y(0.6), L(G.BASE_W), L(G.PATTERN_H), "shadow", rx=3)
    # inner face: lining colour (lth2) with edge stitching; gussets darker
    c.path(rr(X, Y, L, xb, 0, G.BASE_W, G.PATTERN_H, G.R), "lth2")
    c.path(rr(X, Y, L, 0, yb, G.PATTERN_W, G.BASE_H, G.R), "lth2")
    for (x0, y0, w, h) in [(xb, ya, G.BASE_W, G.REAR_WALL), (xb, yc, G.BASE_W, G.FRONT_WALL), (xa, yb, G.SIDE_WALL, G.BASE_H), (xc, yb, G.SIDE_WALL, G.BASE_H)]:
        c.rect(X(x0), Y(y0), L(w), L(h), "lth3")
    c.path(rr(X, Y, L, 0.3, yb + 0.3, G.PATTERN_W - 0.6, G.BASE_H - 0.6, G.R - 0.3), "edge")
    c.path(rr(X, Y, L, xb + 0.3, 0.3, G.BASE_W - 0.6, G.PATTERN_H - 0.6, G.R - 0.3), "edge")
    # back wall = panel 4 with cable pocket and 5 cm tips
    v4 = G.View(X(xb), Y(yb), s)
    panel_face(c, v4, G.SIZES_LARGE5, 5.0, 4.0, 6.5, x_offset=10.8, zone_w=10.2, backwall=True, page_outline=False, labels=False)
    pocket(c, v4, 0.5, 0.5, 9.7, 9.0, 3.0, 1.2)
    # three pages hinged at the bottom gusset, fanned slightly: P3 (back) to P1 (front)
    for i, (sizes, tl, tt, off) in enumerate([(G.SIZES_SMALL, 5.0, 3.75, 0.9), (G.SIZES_LARGE10, 10.0, 1.5, 0.45), (G.SIZES_SMALL, 10.0, 1.5, 0.0)]):
        vp = G.View(X(xb + 0.5), Y(yc - G.PAGE_H - off), s)
        kw = dict(x_offset=5.0, zone_w=15.0) if i == 1 else {}
        panel_face(c, vp, sizes, tl, tt, 6.5 if i else 6.25, labels=False, **kw)
        if i == 1:
            pocket(c, vp, 0.5, 0.5, 3.9, 4.1, 1.6, 0.9)
            pocket(c, vp, 0.5, 6.4, 3.9, 4.1, 1.6, 0.9)
    # strap tongue showing past the top flap, side-flap snap sockets on the front panel
    for sx in (xb + 5.0, xc - 5.0):
        c.circle(X(sx), Y(yd + 6.5), 1.3, "brass")
    c.text(80, 105, "OPEN  -  pages 1-3 over the back wall", "cap")
    return c


def main():
    views = [("closed-front", closed_front), ("closed-iso", closed_iso), ("open-flat", open_flat),
             ("panel1", panel1), ("panel2", panel2), ("backwall", backwall)]
    import cairosvg
    from PIL import Image
    for name, fn in views:
        svg = fn().svg()
        with open(os.path.join(OUT, name + ".svg"), "w") as f:
            f.write(svg)
        png = os.path.join(OUT, name + ".png")
        cairosvg.svg2png(bytestring=svg.encode(), write_to=png, output_width=1600)
        im = Image.open(png).convert("RGB")
        im.resize((900, int(im.size[1] * 900 / im.size[0])), Image.LANCZOS).save(os.path.join(OUT, name + ".jpg"), quality=86, optimize=True)
        print("rendered", name)


if __name__ == "__main__":
    main()
