#!/bin/bash
# Double-click this file in Finder to preview the portfolio.
# It starts a local web server and opens your browser.
# Close the Terminal window (or press Ctrl+C) when you're done.

cd "$(dirname "$0")" || exit 1

PORT=8787
# if 8787 is busy, walk up until we find a free port
while lsof -i ":$PORT" >/dev/null 2>&1; do
  PORT=$((PORT + 1))
done

echo ""
echo "  Maxine Zhou — portfolio preview"
echo "  ────────────────────────────────────────────"
echo "  Live site:      http://localhost:$PORT"
echo "  v2 prototype:   http://localhost:$PORT/_prototype/launchpad-v2.html"
echo ""
echo "  Leave this window open while you browse."
echo "  Press Ctrl+C (or just close this window) to stop."
echo "  ────────────────────────────────────────────"
echo ""

# give the server a moment, then open the browser
( sleep 1; open "http://localhost:$PORT/_prototype/launchpad-v2.html" ) &

python3 -m http.server "$PORT"
