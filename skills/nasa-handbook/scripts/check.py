"""Check a rendered handbook page PDF and cut zoomed tiles for a visual review.

    uv run --no-project --with pymupdf python check.py page.pdf [--pages N] [--out DIR] [--dpi 300]

Reports page count and size, every colour used, the fonts in the file, and
the paths of review tiles. Anything other than pure black or white is flagged,
because printers halftone tints and greys into dots.

It does not measure fit: render.sh does, and exits 3 when the page overflows.

Each page is cut into 8 overlapping tiles (left and right halves of four
horizontal bands) at --dpi, 300 by default, about 12 px per mm. Look at every
tile. Leaders touching text, labels touching boxes and clipped words are a
tenth of a millimetre wide and only show up at this size.
"""

import argparse
import sys
import tempfile
from pathlib import Path

import pymupdf

MM = 72 / 25.4
SIZES = {"A4": (210, 297), "US Letter": (215.9, 279.4)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--pages", type=int, default=1, help="expected page count")
    ap.add_argument("--out", help="folder for the tiles (default: a new temp folder)")
    ap.add_argument("--dpi", type=int, default=300, help="tile resolution")
    args = ap.parse_args()

    doc = pymupdf.open(args.pdf)
    problems = []

    print(f"pages: {doc.page_count}")
    if doc.page_count != args.pages:
        problems.append(f"expected {args.pages} page(s), got {doc.page_count}")

    out = Path(args.out) if args.out else Path(tempfile.mkdtemp(prefix="nasa-handbook-check-"))
    out.mkdir(parents=True, exist_ok=True)

    for i, page in enumerate(doc):
        w, h = page.rect.width / MM, page.rect.height / MM
        name = next((n for n, (sw, sh) in SIZES.items() if abs(sw - w) < 1 and abs(sh - h) < 1), "custom")
        print(f"page {i + 1}: {w:.1f} x {h:.1f} mm ({name})")

        colours = set()
        for d in page.get_drawings():
            for c in (d.get("fill"), d.get("color")):
                if c:
                    colours.add(tuple(round(v, 3) for v in c))
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    v = span["color"]
                    colours.add(tuple(round(x / 255, 3) for x in ((v >> 16) & 255, (v >> 8) & 255, v & 255)))
        tints = sorted(c for c in colours if c not in {(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)})
        print(f"  colours: {len(colours)} ({'black and white only' if not tints else 'TINTS: ' + str(tints)})")
        if tints:
            problems.append(f"page {i + 1} uses non-black/white colours {tints}; they print as dots")

        fonts = sorted({f[3].split("+")[-1] for f in page.get_fonts()})
        print(f"  fonts: {', '.join(fonts)}")

        page.get_pixmap(dpi=110).save(out / f"p{i + 1}-overview.png")
        step = (h - 20) / 4
        for j in range(4):
            top, bottom = j * step, min(h, (j + 1) * step + 20)
            for side, (left, right) in (("left", (0, w / 2 + 10)), ("right", (w / 2 - 10, w))):
                clip = pymupdf.Rect(left * MM, top * MM, right * MM, bottom * MM)
                page.get_pixmap(dpi=args.dpi, clip=clip).save(out / f"p{i + 1}-band{j + 1}-{side}-{top:.0f}-{bottom:.0f}mm.png")

    print(f"tiles: {out}")
    for p in sorted(out.iterdir()):
        print(f"  {p}")
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
