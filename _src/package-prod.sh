#!/usr/bin/env bash
# Fabrique le paquet de production dans dist/ (et dist.zip) : exactement les
# fichiers a servir, rien des sources. Usage : ./_src/package-prod.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/dist"
cd "$ROOT"
rm -rf "$OUT" dist.zip
python3 _src/build.py --out "$OUT" >/dev/null
cp -R assets/fonts assets/img assets/js "$OUT/assets/"
cp favicon.ico .htaccess "$OUT/"
cp assets/css/styleguide.css "$OUT/assets/css/"
cp contact/send.php "$OUT/contact/"
rm -f "$OUT/assets/css/main.css"           # source non minifiee, inutile en ligne
# garde-fous : rien de la preprod ne doit partir en production
if grep -rl 'name="robots" content="noindex' "$OUT" --include=index.html | grep -v -e styleguide -e '/404/' ; then
  echo "ERREUR : noindex sur une page indexable" >&2; exit 1; fi
grep -q 'Allow: /' "$OUT/robots.txt" || { echo "ERREUR : robots.txt bloquant" >&2; exit 1; }
grep -rqE 'jorenzo24\.github\.io|="/cararmour\.sg/' "$OUT" && { echo "ERREUR : URL de preprod" >&2; exit 1; }
grep -q 'data-endpoint="/contact/send.php"' "$OUT/contact/index.html" || { echo "ERREUR : formulaire non branche" >&2; exit 1; }
(cd "$OUT" && zip -qr ../dist.zip . -x '.DS_Store')
echo "dist/ : $(find "$OUT" -type f | wc -l | tr -d ' ') fichiers, $(du -sh "$OUT" | cut -f1)  ->  dist.zip"
