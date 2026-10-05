#!/usr/bin/env python3
"""
Car Armour SG — générateur statique minimal (aucune dépendance).

    python3 _src/build.py

Assemble _src/pages/*.html + _src/partials/*.html -> /<route>/index.html
à la racine du dépôt. Les composants partagés (head, header, footer, CTA
WhatsApp) n'existent qu'une fois : la cohérence inter-pages est garantie.

Syntaxe des gabarits
  {{> nom }}        inclut _src/partials/nom.html (récursif)
  {{ cle }}         variable : méta de la page, puis _src/site.json
  {{ nav:clef }}    -> "is-current" si la page déclare "nav": "clef"
  Un bloc JSON en tête de page (dans un commentaire HTML) porte les métas.
"""
import argparse, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, PAGES, PARTIALS = ROOT / "_src", ROOT / "_src/pages", ROOT / "_src/partials"
SITE = json.loads((SRC / "site.json").read_text(encoding="utf-8"))

META_RE = re.compile(r"\A\s*<!--META\s*(\{.*?\})\s*-->\s*", re.S)
INC_RE = re.compile(r"\{\{>\s*([\w./-]+)\s*\}\}")
VAR_RE = re.compile(r"\{\{\s*([\w:.-]+)\s*\}\}")


def load_partial(name, seen=()):
    if name in seen:
        sys.exit(f"Inclusion circulaire : {name}")
    path = PARTIALS / f"{name}.html"
    if not path.exists():
        sys.exit(f"Partial introuvable : {path}")
    return expand(path.read_text(encoding="utf-8"), seen + (name,))


def expand(text, seen=()):
    return INC_RE.sub(lambda m: load_partial(m.group(1), seen), text)


def resolve(text, meta):
    def one(m):
        key = m.group(1)
        if key.startswith("nav:"):
            return "is-current" if meta.get("nav") == key[4:] else ""
        if key in meta:
            return str(meta[key])
        if key in SITE:
            return str(SITE[key])
        return ""  # variable optionnelle -> chaîne vide
    # deux passes : une variable peut en contenir une autre (ex. {{origin}})
    for _ in range(2):
        text = VAR_RE.sub(one, text)
    return text


# ── Déploiement sur un sous-chemin (GitHub Pages) ────────────────────────────
# Les pages référencent tout en absolu depuis la racine (/assets/…, /contact/).
# Servi sous https://user.github.io/<repo>/, il faut préfixer ces URL.

ATTR_RE = re.compile(r'\b(href|src)="(/(?!/)[^"]*)"')
SRCSET_RE = re.compile(r'\bsrcset="([^"]*)"', re.S)
CSS_URL_RE = re.compile(r"""url\((['"]?)(/(?!/)[^'")]*)\1\)""")
NOINDEX = '<meta name="robots" content="noindex, nofollow">'


def rebase_html(html, base):
    html = ATTR_RE.sub(lambda m: f'{m.group(1)}="{base}{m.group(2)}"', html)

    def srcset(m):
        parts = []
        for cand in m.group(1).split(","):
            cand = cand.strip()
            if cand.startswith("/") and not cand.startswith("//"):
                cand = base + cand
            parts.append(cand)
        return 'srcset="' + ", ".join(parts) + '"'

    return SRCSET_RE.sub(srcset, html)


def rebase_css(css, base):
    return CSS_URL_RE.sub(lambda m: f"url({m.group(1)}{base}{m.group(2)}{m.group(1)})", css)


def add_noindex(html):
    if "noindex" in html:
        return html
    return html.replace("</title>", "</title>\n" + NOINDEX, 1)


def route_to_path(route, out_root):
    route = route.strip("/")
    return out_root / (f"{route}/index.html" if route else "index.html")


CSS_COMMENT = re.compile(r"/\*(?!!).*?\*/", re.S)


def minify_css(css):
    """Minification prudente : commentaires, espaces et points-virgules superflus.

    Les chaines et les url() sont extraites avant les passes de regex puis
    restaurees telles quelles. Sans cette mise a l'abri, la regle qui retablit
    les espaces autour de + et - dans calc()/clamp() mordait sur les noms de
    fichiers : url(.../fond-1800.webp) devenait url(.../fond - 1800.webp).
    """
    vault = []

    def stash(text):
        vault.append(text)
        return f"\x00{len(vault) - 1}\x00"

    out, i, n = [], 0, len(css)
    while i < n:
        ch = css[i]
        if ch in "\"'":                       # chaine : mise a l'abri
            j = i + 1
            while j < n and css[j] != ch:
                j += 2 if css[j] == "\\" else 1
            out.append(stash(css[i:j + 1])); i = j + 1; continue
        if css.startswith("/*", i):           # commentaire : supprime
            j = css.find("*/", i + 2)
            i = n if j == -1 else j + 2; continue
        if css[i:i + 4].lower() == "url(":    # url() non quotee : mise a l'abri
            j = css.find(")", i)
            if j != -1 and '"' not in css[i:j] and "'" not in css[i:j]:
                out.append(stash(css[i:j + 1])); i = j + 1; continue
        out.append(ch); i += 1
    css = "".join(out)

    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    # espace obligatoire autour de + et - dans calc()/clamp()
    css = re.sub(r"(?<=[\d%a-z\)])([+\-])(?=[\.\d])", r" \1 ", css)
    css = re.sub(r"\x00(\d+)\x00", lambda m: vault[int(m.group(1))], css)
    return css.strip()


def fingerprint(path):
    """Empreinte courte du contenu, pour invalider le cache navigateur.
    Sans elle, le cache d'un an pose par .htaccess empecherait toute mise a
    jour d'atteindre un visiteur deja venu : le nom du fichier ne change pas."""
    return hashlib.md5(path.read_bytes()).hexdigest()[:10]


ASSET_URL_RE = re.compile(r"/assets/[A-Za-z0-9._\-/]+\.[A-Za-z0-9]{2,5}")


def asset_versions(out_root):
    """Empreinte de chaque fichier servi. Sans elle, un visuel remplace garde
    son URL : navigateurs et CDN continuent de servir l'ancien, parfois des
    mois. C'est arrive sur les photos de la section services."""
    versions = {}
    for base in (out_root, ROOT):
        root = base / "assets"
        if not root.exists():
            continue
        for f in root.rglob("*"):
            if not f.is_file():
                continue
            url = "/" + f.relative_to(base).as_posix()
            versions.setdefault(url, fingerprint(f))
    return versions


def stamp_assets(text, versions):
    return ASSET_URL_RE.sub(
        lambda m: m.group(0) + (f"?v={versions[m.group(0)]}" if m.group(0) in versions else ""),
        text)


def build_css(out_root, base="", versions=None):
    src = ROOT / "assets/css/main.css"
    out = out_root / "assets/css/main.min.css"
    out.parent.mkdir(parents=True, exist_ok=True)
    mini = minify_css(src.read_text(encoding="utf-8"))
    broken = re.findall(r"url\([^)]*\s[^)]*\)", mini)
    if broken:
        sys.exit("Minification : url() contenant un espace -> " + broken[0])
    if versions:
        mini = stamp_assets(mini, versions)
    if base:
        mini = rebase_css(mini, base)
    out.write_text(mini, encoding="utf-8")
    before, after = len(src.read_text(encoding="utf-8")), len(mini)
    print(f"  main.css {before // 1024} Ko  ->  main.min.css {after // 1024} Ko "
          f"(-{round((1 - after / before) * 100)} %)\n")


def build(out_root=ROOT, base="", noindex=False):
    if not PAGES.exists():
        sys.exit("Aucune page dans _src/pages/")
    build_css(out_root, base)                 # premiere passe, sans empreintes
    versions = asset_versions(out_root)
    build_css(out_root, base, versions)       # seconde passe, url() versionnees
    versions["/assets/css/main.min.css"] = fingerprint(out_root / "assets/css/main.min.css")
    written = []
    for page in sorted(PAGES.rglob("*.html")):
        raw = page.read_text(encoding="utf-8")
        m = META_RE.match(raw)
        if not m:
            sys.exit(f"{page.name} : bloc <!--META {{...}}--> manquant")
        meta = json.loads(m.group(1))
        body = raw[m.end():]
        layout = meta.get("layout", "layout")
        html = load_partial(layout).replace("{{content}}", body)
        html = resolve(expand(html), meta)
        html = re.sub(r"\n{3,}", "\n\n", html)
        html = stamp_assets(html, versions)
        if noindex:
            html = add_noindex(html)
        if base:
            html = rebase_html(html, base)
        out = route_to_path(meta["route"], out_root)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        written.append((meta["route"], out.relative_to(out_root), len(html)))
    width = max(len(r) for r, _, _ in written)
    for route, rel, size in written:
        print(f"  {route:<{width}}  ->  {rel}  ({size//1024} Ko)")
    print(f"  {len(versions)} fichiers servis, empreintes posees sur chaque URL")
    print(f"\n{len(written)} page(s) générée(s).")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Génère le site statique.")
    ap.add_argument("--base", default="",
                    help="Préfixe d'URL pour un déploiement en sous-chemin, ex. /cararmour.sg")
    ap.add_argument("--out", default=None,
                    help="Répertoire de sortie (défaut : racine du dépôt)")
    ap.add_argument("--noindex", action="store_true",
                    help="Ajoute noindex,nofollow sur toutes les pages (préproduction)")
    a = ap.parse_args()
    base = a.base.rstrip("/")
    if base and not base.startswith("/"):
        base = "/" + base
    out = Path(a.out).resolve() if a.out else ROOT
    build(out, base, a.noindex)
