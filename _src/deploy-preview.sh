#!/usr/bin/env bash
# Republie la préproduction sur https://jorenzo24.github.io/cararmour.sg/
# Usage : ./_src/deploy-preview.sh "message de commit"
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE=/cararmour.sg
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

cd "$ROOT"
python3 _src/build.py --base "$BASE" --noindex --out "$WORK"
cp -R assets/fonts assets/img assets/js "$WORK/assets/"
cp assets/css/styleguide.css "$WORK/assets/css/"
cp favicon.ico "$WORK/"
touch "$WORK/.nojekyll"
printf 'User-agent: *\nDisallow: /\n' > "$WORK/robots.txt"
cp _src/preview-readme.md "$WORK/README.md"

cd "$WORK"
git init -q -b gh-pages
git add -A
git -c user.name="Jorenzo24" -c user.email="josephlambert@live.fr" \
    commit -q -m "${1:-Préproduction : mise à jour}"
git remote add origin https://github.com/Jorenzo24/cararmour.sg.git
git push -q --force origin gh-pages
echo "→ https://jorenzo24.github.io/cararmour.sg/ (propagation ~1 min)"
