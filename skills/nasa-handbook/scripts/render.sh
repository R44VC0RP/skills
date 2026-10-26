#!/bin/sh
# Render a handbook page with headless Chrome.
#   render.sh path/to/page.html
# Writes page.pdf (vector, for print) and page.png (2x screen preview) next to
# the HTML, then prints the template's fit check (room left above the footer).
set -e
[ -n "$1" ] || { echo "usage: render.sh page.html" >&2; exit 2; }
DIR=$(cd "$(dirname "$1")" && pwd)
HTML="$DIR/$(basename "$1")"
BASE="${HTML%.html}"
URL="file://$HTML"

CHROME=${CHROME:-"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"}
if [ ! -x "$CHROME" ]; then
  CHROME=$(command -v google-chrome || command -v google-chrome-stable || command -v chromium || command -v chromium-browser || true)
fi
[ -n "$CHROME" ] || { echo "Chrome or Chromium not found; set CHROME=/path/to/chrome" >&2; exit 1; }

# Page size in CSS px at 96 dpi: A4 210x297 mm, US Letter 8.5x11 in.
if grep -q "size: *letter" "$HTML"; then W=816; H=1056; else W=794; H=1123; fi

# --allow-file-access-from-files lets the page load ./fonts; the time budget lets
# web fonts and the fit script settle before capture.
FLAGS="--headless=new --disable-gpu --allow-file-access-from-files --virtual-time-budget=4000 --window-size=$W,$H"

"$CHROME" $FLAGS --no-pdf-header-footer --print-to-pdf="$BASE.pdf" "$URL" 2>/dev/null
"$CHROME" $FLAGS --hide-scrollbars --force-device-scale-factor=2 --screenshot="$BASE.png" "$URL" 2>/dev/null
FIT=$("$CHROME" $FLAGS --dump-dom "$URL" 2>/dev/null | grep -o 'data-fit="[^"]*"' | head -1 | sed 's/data-fit="//; s/"$//')

echo "pdf: $BASE.pdf"
echo "png: $BASE.png"
echo "fit: ${FIT:-unknown (page has no fit script)}"
# An overfull page is clipped silently by .page { overflow: hidden }: fail loudly.
case "$FIT" in OVERFLOW*) echo "page overflows: cut words or a table row, don't shrink type" >&2; exit 3;; esac
