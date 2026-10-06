# cararmour.sg — site statique

Refonte multi-pages SEO de Car Armour SG (car detailing, Singapour).
Contenu **en anglais (en-SG)**, prix en **S$**.

## Lancer

```bash
python3 _src/build.py              # génère les pages
python3 -m http.server 8787        # http://127.0.0.1:8787/
```

## Architecture

```
_src/
  site.json           NAP, horaires, liens booking/WhatsApp, note globale  → source unique
  build.py            générateur (aucune dépendance)
  shot.sh             capture fiable d'une page (reveal et lazy-load neutralisés)
  deploy-preview.sh   republie la préproduction GitHub Pages
  partials/           layout, header, footer, wa-fab, logos inlinés
  pages/<nom>.html    une page = un bloc <!--META {...}--> + le corps
  fragments/          blocs retirés d'une page, en attente d'être replacés ailleurs
assets/css/main.css   design system — LA SOURCE, c'est ici qu'on édite
assets/css/main.min.css  GÉNÉRÉ par build.py, c'est ce que les pages chargent
assets/js/main.js     nav, accordéons, reveal — vanilla, zéro dépendance
assets/fonts/         Archivo + Inter (variables, sous-ensemble latin), auto-hébergées
assets/img/           WebP multi-largeurs + logos SVG + tuile de grain
<route>/index.html    SORTIE GÉNÉRÉE — ne jamais éditer à la main
```

### Images

Le traitement colorimétrique de la DA est **cuit dans les fichiers**, pas appliqué
en CSS : un `filter` sur une grande image se recalcule à chaque peinture.

```bash
magick source.jpg -modulate 86,72 -level 2.4%,97.6% traite.png
cwebp -q 80 -m 6 traite.png -o assets/img/<nom-avec-mots-cles>-<largeur>.webp
```

Largeurs : 1200 / 1000 / 700 / 460, **jamais au-delà de la largeur source**
(un agrandissement ne fait qu'alourdir). Nommer les fichiers avec le mot-clé de
la page qui les utilise. Les seuls `filter` restants sont des effets de survol.

**Conserver les sources** dans `_src/sources/`. Le traitement étant cuit dans
le WebP, le changer plus tard oblige sinon à l'inverser depuis un fichier déjà
compressé, ce qui ne rend jamais exactement l'original.

Toutes les URL servies portent une empreinte de contenu posée par `build.py`.
Un fichier remplacé change donc d'URL, sans quoi navigateurs et CDN continuent
de servir l'ancien, jusqu'à un an en production.

### Fontes

Auto-hébergées : pas de round-trip vers Google Fonts, et les `.woff2` sont
préchargés dans le layout. Des `@font-face` de secours calées sur les métriques
réelles (hauteur de capitale et d'x) évitent que le swap décale la mise en page —
c'est ce qui a ramené le CLS de 0,26 à 0.

Les composants partagés n'existent qu'une fois dans `_src/partials/`. Toute
modification du header ou du footer se fait là, puis `python3 _src/build.py`.

### Gabarit d'une page

```html
<!--META {
  "route": "/ceramic-coating-singapore/",
  "title": "…",  "description": "…",
  "ogType": "website", "ogImage": "/assets/img/og-default.jpg",
  "nav": "coating"
} -->
<section class="section section--void"> … </section>
```

Variables disponibles dans les gabarits : toutes les clés du bloc META, toutes
celles de `site.json`, plus `{{nav:clef}}` qui rend `is-current` si la page
déclare cette clef. `{{> nom}}` inclut un partial.

## Design system

Voir `/styleguide/` (noindex) : palette, échelle typographique, boutons,
cartes service, cartes prix, matrice tarifaire, déroulé, FAQ, avis, formulaire.

Règles non négociables :
- Jamais de blanc pur en fond. Fonds `--c-void` / `--c-charcoal` en alternance.
- **Un seul accent** : le doré champagne `--c-gold`. Pas d'autre couleur vive.
- Angles vifs (`--radius: 0`), filets 1 px, aucune ombre portée décorative.
- Titres Archivo sur l'axe de chasse 125 %, capitales. Corps en Inter 300/330.
- Un seul `<h1>` par page ; les paragraphes ne sont jamais des headings.
- Dans `clamp()`/`calc()`, **toujours des espaces autour de `+`** — sans quoi la
  déclaration entière est invalide et silencieusement ignorée.
- Le minificateur met les chaînes et les `url()` à l'abri avant ses passes de
  regex, et refuse de générer si une `url()` minifiée contient une espace.
  Sans cette protection, `fond-1800.webp` devenait `fond - 1800.webp`.
- Mobile : composants repensés (matrice → cartes empilées, nav → overlay plein
  écran), pas de simple empilement.

## SEO

- `title`, `description`, `canonical`, OG uniques par page (bloc META).
- JSON-LD `AutoDetailing` global injecté par le layout ; les schémas `Service`,
  `FAQPage` et `AggregateRating` s'ajoutent par page via `headExtra`.
- `sitemap.xml` et `robots.txt` statiques à la racine.

## À confirmer avec le client

- Grille tarifaire taille × durée : dérivée des tarifs de l'ancien site
  (Ceramic 1 couche S$388, Graphene V3 S$688, surcharge SUV/MPV S$50).
- Volume d'avis et note moyenne annoncés (`ratingValue`, `reviewCount`).
- Adresse postale : aucune sur l'ancien site (service 100 % mobile).

## Fragments en attente

`_src/fragments/coating-comparison.html` : comparatif ceramic / graphene et
encart « ce que ça ne fait pas », retirés de l'accueil le 2026-10-05. À
replacer sur `/ceramic-coating-singapore/`. Les composants `.compare` et
`.caveat` sont restés dans le design system, il n'y a rien à réécrire.
