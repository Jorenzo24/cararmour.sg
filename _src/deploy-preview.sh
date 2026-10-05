#!/usr/bin/env bash
# Republie la préproduction sur https://jorenzo24.github.io/cararmour.sg/
# Usage : ./_src/deploy-preview.sh "message de commit"
#
# Publication incrémentale : on repart de la branche existante et on pousse
# un commit par-dessus. La version précédente forçait un historique neuf à
# chaque fois, ce que le pipeline GitHub Pages a fini par refuser.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE="https://github.com/Jorenzo24/cararmour.sg.git"
BASE=/cararmour.sg
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

SITE="$TMP/site"; REPO="$TMP/repo"
cd "$ROOT"
python3 _src/build.py --base "$BASE" --noindex --out "$SITE" >/dev/null
cp -R assets/fonts assets/img assets/js "$SITE/assets/"
cp assets/css/styleguide.css "$SITE/assets/css/"
cp favicon.ico "$SITE/"
touch "$SITE/.nojekyll"
printf 'User-agent: *\nDisallow: /\n' > "$SITE/robots.txt"
cp _src/preview-readme.md "$SITE/README.md"

if git clone -q --depth 1 --branch gh-pages "$REMOTE" "$REPO" 2>/dev/null; then
  find "$REPO" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
else
  git clone -q --depth 1 "$REMOTE" "$REPO"
  git -C "$REPO" checkout -q --orphan gh-pages
  git -C "$REPO" rm -rq --cached . 2>/dev/null || true
  find "$REPO" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
fi
cp -R "$SITE/." "$REPO/"

cd "$REPO"
git add -A
if git diff --cached --quiet; then
  echo "rien à publier, la préproduction est déjà à jour"
  exit 0
fi
git -c user.name="Jorenzo24" -c user.email="josephlambert@live.fr" \
    commit -q -m "${1:-Préproduction : mise à jour}"
git push -q origin gh-pages
echo "→ https://jorenzo24.github.io/cararmour.sg/ (propagation ~1 min)"
