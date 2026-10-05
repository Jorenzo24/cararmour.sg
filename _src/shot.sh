#!/usr/bin/env bash
# Capture fiable : copie de la page avec le reveal neutralisé.
# Les transitions CSS n'avancent pas sous --virtual-time-budget en headless.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${1:-index.html}"; OUT="${2:-/tmp/shot.png}"; W="${3:-1440}"; H="${4:-3600}"
mkdir -p "$ROOT/_shot"
python3 - "$ROOT/$SRC" "$ROOT/_shot/index.html" <<'PY'
import sys
src,dst=sys.argv[1],sys.argv[2]
h=open(src,encoding="utf8").read()
h=h.replace("</head>","<style>.js [data-reveal]{opacity:1!important;transform:none!important;transition:none!important}</style></head>",1)
open(dst,"w",encoding="utf8").write(h)
PY
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars \
  --window-size="$W,$H" --virtual-time-budget=20000 --screenshot="$OUT" \
  "http://127.0.0.1:8787/_shot/" 2>/dev/null
rm -rf "$ROOT/_shot"
echo "→ $OUT"
