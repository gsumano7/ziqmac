# Interchangeable knitting needle case — design drawing set

Technical drawings for a faux-leather trifold clutch holding a full
interchangeable needle set. Dimensions come from the cardboard prototype
(photos 1–5); construction, strap, pages and elastic bands follow the
client's reference photos. Rev B, 2026-10-01.

## Files

| File | What it is |
| --- | --- |
| `knitting-needle-case-drawings.pdf` | The drawing set, 8 sheets, A3 landscape. Sheets 3–6 are full size (1:1) and can be printed at 100 % and used as pattern pieces. |
| `index.html` | Same seven sheets as a print-ready web page (File → Print, A3 landscape, no margins). |
| `sheets/sheet1.svg` … `sheet8.svg` | Each sheet as a vector SVG, editable in Inkscape / Illustrator. |
| `preview/sheet*.png` | Quick-look raster previews. |
| `generate_drawings.py` | Generator. Every dimension lives in this script; change a value, re-run, and all sheets update. |

## Sheet index

1. Outer shell — flat pattern, outer face (die line) with strap, buckle, logo and snap positions, 1:2
2. Assembly — front / back / end views closed, vertical section showing the fanned pages, open layout, closing sequence, stack-height check, open questions
3. Page 1: 10 cm tips 2.0–5.0 mm, 11 pairs, 1:1, with the elastic slot section detail
4. Page 2: 10 cm tips 5.5–10 mm, 6 pairs, 1:1
5. Page 3: 5 cm tips 2.0–5.0 mm, 11 pairs, 1:1
6. Page 4: 5 cm tips 5.5–8 mm, 4 pairs, plus the snap accessory pocket (caps, keys, connectors, grip patch), 1:1
7. Details — strap and buckle piece (1:2), cable pocket on the back panel (1:2), page hinge section through the bottom gusset (2:1), elastic slot section (2:1)
8. Contents checklist (64 tips / 32 pairs, 5 cables, accessories), bill of materials, construction sequence, tolerances, measurement record, hardware size assumptions

## What came from the prototype and what is proposed

Taken directly from the cardboard prototype:

- Outer shell cross pattern: top flap 5.0, top gusset 6.5, back panel 21.0 × 13.0, bottom gusset 6.0, front panel 12.7; side gussets 5.7, side flaps 8.0 with a snap each (photo 1).
- Slot widths: 0.6 cm for 2.0 mm rising 0.1 cm per size to 2.2 cm for 10 mm; 0.5 cm land between slots; 1.0 cm end margins; 1.5 cm clearance above the tip points (photos 2–5).

Taken from the reference photos:

- Trifold clutch: side flaps fold in and tuck inside, front panel folds up, top flap folds over, wrap-around strap (3.0 cm, dark brown) with 30 mm buckle, keeper and snap closure; embossed logo on the flap; R 1.0 corners; contrast edge stitching.
- Four interior pages sewn into the bottom gusset (not removable), each with a 1.5 cm elastic band across the middle and size labels above the tips.
- Snap accessory pocket on the large 5 cm page; cable pocket at the back.

Proposed to fit the full contents list:

- Page sizes 20.0 × 12.5 with a 1.5 hinge tab; hinge seams staggered 1.2 cm apart so the pages fan.
- Page order from the back: 10 cm 2.0–5.0, 10 cm 5.5–10, 5 cm 2.0–5.0, 5 cm 5.5–8 + pocket.
- Leather grip patch 6.0 × 4.0 cm, veg-tan 1.8–2.0 mm, in place of the rubber grip disc.

Sheet 2 lists six open questions (gusset depths, top-flap depth, working vs decorative buckle, snap type, cable location, real hardware sizes) to confirm before cutting.

## Regenerating

```bash
cd designs/knitting-needle-case
python3 generate_drawings.py                      # writes sheets/*.svg and index.html
node pdf.js                                       # optional: print index.html to PDF with Chromium/Playwright
```

The PDF in this folder was produced with headless Chromium (Playwright) from `index.html`.
