# Interchangeable knitting needle case — design drawing set

Factory-ready drawing set for a premium leather trifold clutch holding a
full interchangeable needle set. Dimensions come from the cardboard
prototype (photos P1–P5); construction follows the client's written brief
and reference photos (R1–R6). Rev C, 2026-10-01.

## Files

| File | What it is |
| --- | --- |
| `knitting-needle-case-drawings.pdf` | The drawing set, 9 sheets, A3 landscape. Sheets 4–7 are full size (1:1) and can be printed at 100 % and used as slit-cutting templates. |
| `index.html` | Same nine sheets as a print-ready web page (File → Print, A3 landscape, no margins). |
| `sheets/sheet1.svg` … `sheet9.svg` | Each sheet as a vector SVG, editable in Inkscape / Illustrator. |
| `preview/sheet*.png` | Quick-look raster previews. |
| `reference/*.jpg` | Client reference photos, downscaled, as embedded on the cover sheet. |
| `generate_drawings.py` | Generator. Every dimension lives in this script; change a value, re-run, and all sheets update. |

## Sheet index

1. Cover — design brief, construction summary, reference photos, sheet index
2. Outer shell — flat pattern, outer face, with strap, buckle, logo and snap positions, 1:2
3. Assembly — front / back / end views closed, vertical section (front panel, pages 1–3, back wall), open layout, closing sequence, stack check, open questions
4. Panel 1 (page): 10 cm tips 2.0–5.0 mm, 11 pairs, 1:1
5. Panel 2 (page): 10 cm tips 5.5–10 mm, 6 pairs, plus two small snap pockets for accessories, 1:1
6. Panel 3 (page): 5 cm tips 2.0–5.0 mm, 11 pairs, 1:1
7. Panel 4 (back-wall lining): 5 cm tips 5.5–8 mm, 4 pairs, plus the large cable snap pocket, 1:1
8. Details — adjustable strap and buckle piece (1:2), page hinge section (2:1), pocket patterns (1:2), elastic threading section (2:1)
9. Contents checklist (64 tips / 32 pairs, 5 cables, accessories), bill of materials, construction sequence, tolerances, measurement record, hardware size assumptions

## What came from the prototype and what is proposed

Taken directly from the cardboard prototype:

- Outer shell cross pattern: top flap 5.0, top gusset 6.5, back panel 21.0 × 13.0, bottom gusset 6.0, front panel 12.7; side gussets 5.7, side flaps 8.0 with a snap each (photo 1).
- Slot widths: 0.6 cm for 2.0 mm rising 0.1 cm per size to 2.2 cm for 10 mm; 0.5 cm land between slots; 1.0 cm end margins; 1.5 cm clearance above the tip points (photos 2–5).

Taken from the client's brief and reference photos:

- Trifold clutch: side flaps fold in and tuck inside, front panel folds up, top flap folds over, adjustable 3 cm dark brown strap with 30 mm buckle and keeper; embossed logo on the flap; R 1.0 corners; contrast edge stitching.
- Storage order front to back: front panel, panel 1, panel 2, panel 3, back wall (panel 4). Panels 1–3 are pages sewn into the bottom gusset on three evenly spaced seams and are not removable; panel 4 is the back-wall lining itself.
- 15 mm elastic threaded in and out of each panel through die-cut slits, one visible loop per pair, size label above each pair.
- Large snap pocket for the cables on the back wall; two small snap pockets for caps, keys, connectors and the grip patch on panel 2.

Proposed to fit the full contents list:

- Page size 20.0 × 12.5 with a 1.5 hinge tab; hinge seams at 1.5 / 3.0 / 4.5 across the 6.0 gusset.
- Panel assignment: panel 1 = 10 cm 2.0–5.0, panel 2 = 10 cm 5.5–10, panel 3 = 5 cm 2.0–5.0, panel 4 = 5 cm 5.5–8.
- Leather grip patch 6.0 × 3.0 cm, veg-tan 1.8–2.0 mm, folded in half in pocket B.

Sheet 3 lists five open questions (gusset depths, top-flap depth, snap type, genuine vs faux leather, real hardware sizes) to confirm before cutting.

## Regenerating

```bash
cd designs/knitting-needle-case
python3 generate_drawings.py                      # writes sheets/*.svg and index.html
node pdf.js                                       # optional: print index.html to PDF with Chromium/Playwright
```

The PDF in this folder was produced with headless Chromium (Playwright) from `index.html`.
