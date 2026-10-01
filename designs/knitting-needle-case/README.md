# Interchangeable knitting needle case — design drawing set

Technical drawings for a faux-leather case holding a full interchangeable
needle set, drawn from the measurements written on the cardboard prototype
(photos 1–5). Rev A, 2026-10-01.

## Files

| File | What it is |
| --- | --- |
| `knitting-needle-case-drawings.pdf` | The drawing set, 7 sheets, A3 landscape. Sheets 3–6 are full size (1:1) and can be printed at 100 % and used as pattern pieces. |
| `index.html` | Same seven sheets as a print-ready web page (File → Print, A3 landscape, no margins). |
| `sheets/sheet1.svg` … `sheet7.svg` | Each sheet as a vector SVG, editable in Inkscape / Illustrator. |
| `preview/sheet*.png` | Quick-look raster previews. |
| `generate_drawings.py` | Generator. Every dimension lives in this script; change a value, re-run, and all sheets update. |

## Sheet index

1. Outer shell — flat pattern (die line), 1:2
2. Assembly — closed views, isometric, fold sequence, interior layout, stack-height check, open questions
3. Needle panel A (base): 10 cm tips 2.0–5.0 mm, 11 pairs, 1:1
4. Needle panel B (lid): 10 cm tips 5.5–10 mm, 6 pairs, with 2-snap keeper flap, 1:1
5. Hinged page, face 1 — panel C: 5 cm tips 2.0–5.0 mm, 11 pairs, plus loops for 6 end caps and 4 cable keys, 1:1
6. Hinged page, face 2 — panel D: 5 cm tips 5.5–8 mm, 4 pairs, plus 3 connector loops, leather grip-patch pocket and zip cable pocket, 1:1
7. Contents checklist (64 tips / 32 pairs, 5 cables, accessories), bill of materials, construction sequence, tolerances, measurement record, hardware size assumptions

## What came from the prototype and what is proposed

Taken directly from the cardboard prototype:

- Outer shell cross pattern: rear flap 5.0, rear wall 6.5, base 21.0 × 13.0, front wall 6.0, lid 12.7; side walls 5.7, end flaps 8.0 with a snap each (photo 1).
- Slot widths: 0.6 cm for 2.0 mm rising 0.1 cm per size to 2.2 cm for 10 mm; 0.5 cm land between slots; 1.0 cm end margins; 1.5 cm clearance beyond the tip points (photos 3–5).
- Keeper flap on the large-size panel: 9.0 cm deep, two snaps (photos 2 and 4).

Proposed to fit the full contents list (marked "proposal" on the sheets):

- A double-sided hinged page carrying all 5 cm tips, caps, keys, connectors, grip patch and cables, hinged on the front wall.
- Interior panels sized 20.5 × 12.5 to drop into the 21.0 × 13.0 interior.
- 25 mm knit elastic for slot bands and accessory loops.
- Leather grip patch 6.0 × 4.0 cm, veg-tan 1.8–2.0 mm, in place of the rubber grip disc.

Sheet 2 lists six open questions (wall heights, rear-flap direction, soft vs board-stiffened, band material, cable pocket location, real hardware sizes) to confirm before cutting.

## Regenerating

```bash
cd designs/knitting-needle-case
python3 generate_drawings.py                      # writes sheets/*.svg and index.html
node pdf.js                                       # optional: print index.html to PDF with Chromium/Playwright
```

The PDF in this folder was produced with headless Chromium (Playwright) from `index.html`.
