# Ziq Mac — photography site

A static site. The homepage is a single full-bleed picture; the navigation is
clickable regions of that picture. Interior pages use a conventional text nav.

```
index.html        the picture homepage + hotspot nav
work.html         portfolio grid
about.html
contact.html
assets/home.svg   the homepage picture (placeholder — swap for a real photo)
assets/site.css   shared styles for the interior pages
```

No build step and no dependencies. Open `index.html`, or serve the folder with
`python3 -m http.server`.

## How the hotspots work

The picture sits in a `.frame` whose aspect ratio is fixed to the image's, and
which is sized to cover the viewport. Each nav link is an `<li>` positioned in
percentages of that frame:

```html
<li style="--x:42%; --y:38%; --w:13.8%; --h:26.5%">
  <a href="work.html">…</a>
</li>
```

Because the hotspots share the frame's coordinate space, they stay glued to the
same features of the photo at every window size — which an `<img>` with
`object-fit: cover` alone would not do.

The links are one ordinary `<ul>`, styled two ways. Over about a 1.24 viewport
ratio they are hotspots; narrower than that the cover crop would carry them off
the edges of the screen, so the same list becomes a bar along the bottom. That
is one set of links in the markup, so keyboard and screen-reader users get the
real navigation rather than a duplicate copy of it.

## Swapping in your own photo

1. Drop the file in `assets/` and update the `<img src>` and its
   `width`/`height` in `index.html`.
2. Set `--ar` in the `:root` block to the image's width ÷ height.
3. Re-place the hotspots (below).

## Placing hotspots

Load the homepage with `?edit` on the URL — `index.html?edit`. Existing
hotspots get outlined, and clicking anywhere on the picture prints the
coordinates of that point and copies them to the clipboard, ready to paste into
a `<li>`'s `--x` / `--y`. The helper does nothing on the normal URL.

Keep hotspots away from the edges of the frame: anything closer to the left or
right edge than about 11% starts getting cropped on narrower screens before the
bar layout takes over. If you place one nearer the edge than that, raise the
`max-aspect-ratio` breakpoint in the nav media query to match, so the bar kicks
in before the hotspot disappears.

## Notes

- `alt` on the homepage image describes the picture; the nav links carry their
  own text, so the image is not doing navigational work for screen readers.
- The falling camera on `work.html` is decorative, uses scroll-driven CSS
  animation where available with a rAF fallback, and is dropped entirely under
  `prefers-reduced-motion` and on phones.
- Contact details and copy are placeholders — search for `example.com`.
