# cararmour.sg — site statique

Refonte multi-pages SEO de Car Armour SG (car detailing, Singapour).
Contenu **en anglais (en-SG)**, prix en dollars de Singapour.

## État d'avancement

Le brief fixe quatre étapes, **aucune ne démarre sans validation explicite du
client**.

| Étape | Contenu | Statut |
|---|---|---|
| 1 | Design system en tokens | fait, visible sur `/styleguide/` |
| 2 | Accueil complet et abouti | fait, en relecture client |
| 3 | Gabarits : page service, page prix, article de guide, avis, contact | **non démarrée** |
| 4 | Pages restantes, `sitemap.xml`, `robots.txt`, schémas par page | non démarrée |

Pages réellement générées à ce jour : `/` et `/styleguide/` (noindex).
Les dix-neuf autres routes listées plus bas sont prévues, pas écrites.

## Lancer

```bash
python3 _src/build.py              # génère les pages
python3 -m http.server 8787        # http://127.0.0.1:8787/
```

Pour relire depuis un téléphone sur le même réseau :
`python3 -m http.server 8790 --bind 0.0.0.0`.

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
  sources/            PNG et JPEG d'origine, avant conversion — ne jamais purger
assets/css/main.css   design system — LA SOURCE, c'est ici qu'on édite
assets/css/main.min.css  GÉNÉRÉ par build.py, c'est ce que les pages chargent
assets/js/main.js     nav, accordéons, reveal — vanilla, zéro dépendance
assets/fonts/         Archivo + Inter (variables, sous-ensemble latin), auto-hébergées
assets/img/           WebP multi-largeurs + logos SVG + tuile de grain
<route>/index.html    SORTIE GÉNÉRÉE — ne jamais éditer à la main
```

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

Les composants partagés n'existent qu'une fois dans `_src/partials/`. Toute
modification du header ou du footer se fait là, puis `python3 _src/build.py`.

Options du générateur : `--base <préfixe>` réécrit toutes les URL absolues pour
un hébergement en sous-chemin, `--out <dossier>` écrit ailleurs qu'à la racine,
`--noindex` ajoute la balise robots sur toutes les pages.

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

La source d'origine du hero est perdue. `_src/sources/` contient
`car-detailing-singapore-hero-1800-avant-eclaircissement.png`, l'état antérieur
reconverti depuis le WebP : repartir de là plutôt que d'empiler une troisième
compression. Le fichier servi est éclairci de `-gamma 1.24 -level 2%,100%`, le
point noir restant à 0.

Le traitement n'est pas automatique. Les photos fournies par le client sont
souvent déjà étalonnées : la Ferrari de la section services est convertie
**sans aucun traitement**, recadrage 16:10 et WebP q86, parce que son rouge est
l'argument de l'image. Juger photo par photo, et vérifier le rendu final plutôt
que la commande.

**Conserver les sources** dans `_src/sources/`. Le traitement étant cuit dans
le WebP, le changer plus tard oblige sinon à l'inverser depuis un fichier déjà
compressé, ce qui ne rend jamais exactement l'original.

Toutes les URL servies portent une empreinte de contenu posée par `build.py`.
Un fichier remplacé change donc d'URL, sans quoi navigateurs et CDN continuent
de servir l'ancien, jusqu'à un an en production (`.htaccess`). L'empreinte
couvre CSS, JS, images, fontes et les `url()` à l'intérieur du CSS, pas
seulement les feuilles et les scripts.

### Fontes

Auto-hébergées : pas de round-trip vers Google Fonts, et les `.woff2` sont
préchargés dans le layout. Des `@font-face` de secours calées sur les métriques
réelles (hauteur de capitale et d'x) évitent que le swap décale la mise en page.
C'est ce qui a ramené le CLS de 0,26 à 0.

## Design system

Voir `/styleguide/` (noindex) : palette, échelle typographique, boutons,
cartes service, cartes prix, matrice tarifaire, déroulé, FAQ, avis, formulaire.

Règles non négociables :
- Jamais de blanc pur en fond. Fonds `--c-void` / `--c-charcoal` en alternance,
  sections claires en `--c-paper` `#F5F5F0`.
- **Un seul accent** : le doré champagne `--c-gold`. Pas d'autre couleur vive.
- Angles vifs (`--radius: 0`), filets 1 px, aucune ombre portée décorative.
- Titres Archivo sur l'axe de chasse 125 %, capitales. Corps en Inter 400.
- Un seul `<h1>` par page ; les paragraphes ne sont jamais des headings.
- **Prix : `$388`, jamais `S$388`.** Le client a tranché le 2026-10-06, les deux
  S à la suite accrochaient l'œil. La devise se dit une seule fois en toutes
  lettres, dans le chapo de la section tarifs.
- **Téléphone affiché avec l'indicatif** : `+65 8850 1200`. Source unique,
  `phoneDisplay` dans `site.json`.
- Mobile : composants repensés (matrice → cartes empilées, nav → overlay plein
  écran), pas de simple empilement.

### Sections claires : inversion de tokens

`.section--paper` ne change pas de couleurs une par une, elle **redéfinit les
tokens localement**. Conséquence à connaître : le doré n'est jamais une couleur
de texte sur fond clair. Assombri assez pour passer AA il vire au marron, ce que
le client a refusé. Il survit uniquement comme **marque graphique**
(`--c-gold-mark`, filet de 30 px au-dessus des sous-titres) ; le texte passe à
l'encre `#121216`.

La section pose aussi `color: var(--c-paper)` sur elle-même : sans cela la
couleur héritée du `body` reste résolue avec le token du `body`.

### Pièges CSS déjà rencontrés

Ils ont tous coûté une ou plusieurs itérations. Les relire avant d'éditer.

- Dans `clamp()`/`calc()`, **toujours des espaces autour de `+`**. Sans quoi la
  déclaration entière est invalide et silencieusement ignorée. Vingt règles
  d'espacement avaient disparu de cette façon.
- **Ordre des règles.** Une règle sans condition placée après une media query
  l'écrase à spécificité égale. Trois bugs de suite sont venus de là, dont la
  photo de l'équipe débordant de l'écran sur mobile. Écrire les règles de base
  **avant** les media queries, systématiquement.
- **Jamais de `background-size` qui dépende de la hauteur.** `cover` se
  recalcule quand le conteneur grandit : le fond de la FAQ sautait à l'ouverture
  d'un accordéon, le hero « zoomait » quand la barre d'URL mobile se rétractait.
  Dimensionner sur la largeur (`100% auto`), et pas de hauteur de hero en `svh`.
- `background-attachment: fixed` se dimensionne sur le viewport, pas sur
  l'élément. Retiré.
- `grid-row: 1 / -1` ne vise que la grille **explicite**. Avec des lignes
  implicites, utiliser `span N`.
- Un `::before` positionné recouvre un nœud de texte nu : `.btn > * { z-index }`
  ne suffit pas, le libellé n'est pas un élément. D'où `isolation: isolate` sur
  `.btn` et `z-index: -1` sur le voile.
- Le minificateur met les chaînes et les `url()` à l'abri avant ses passes de
  regex, et refuse de générer si une `url()` minifiée contient une espace.
  Sans cette protection, `fond-1800.webp` devenait `fond - 1800.webp`.
- Le texte courant illisible venait de la **graisse**, pas de la couleur :
  Inter s'amincit optiquement sur fond sombre. Corps en 400, jamais 330.
- Le reveal au scroll a un filet de sécurité (balayage sur `scroll`, `resize` et
  `load`) : l'IntersectionObserver seul laissait des blocs invisibles quand la
  hauteur de page changeait après coup.

### Simplicité

Retour client explicite après une section refaite quatre fois : quand un
composant résiste, c'est en général qu'une complication a été ajoutée en route.
Les photos du site utilisent toutes le même patron, `aspect-ratio` +
`overflow: hidden` + `object-fit: cover`. S'en écarter (positionnement absolu,
suppression de l'`aspect-ratio` sur mobile) a cassé à la fois la mise en page et
le lazy-load. Reprendre le patron existant avant d'inventer.

## Rédaction

Interdits absolus dans tout texte publié :

- **Tiret cadratin** (`—`) comme ponctuation d'incise. Marqueur d'IA immédiat.
- **Doubles négations rythmées** (« No workshop, no weekend lost waiting »), et
  plus largement les triplets trop équilibrés.
- **Paragraphes dans les zones de conversion**, même courts.

En haut de page : une phrase en gras, saut de ligne, une phrase non grasse,
quelques mots en gras à l'intérieur pour accrocher les mots-clés. Lignes de 6 à
12 mots. Les textes longs et les informations dures vont **plus bas**, dans les
sections explicatives.

Ton : on présente une entreprise premium. Pas de prénom de technicien, pas de
familiarité, et jamais de pique contre la concurrence. Trois versions de la
section équipe ont été refusées pour ces trois motifs.

## SEO

### Arbitrage retenu

**Tout se concentre sur l'accueil** plutôt que de se répartir en pages filles.
Site neuf, aucune autorité de domaine, tous les liens existants (GMB, Facebook,
annuaires) pointent sur la racine. `ceramic coating price` est traité comme une
déclinaison de `ceramic coating`, sur l'accueil. Ne pas reproposer de découper
les requêtes proches tant que le domaine n'a pas d'autorité mesurable.

Données mesurées (Google Trends SG + autocomplétion, 12 mois) :
- générique : `car detailing` 100 > `car coating` 71 >> `car grooming` 8
- localisé : `ceramic coating singapore` 100 > `car detailing singapore` 37
- `price` est le modificateur nº 1 sur tous les termes testés
- `review` et `reddit` sortent en tête sur `ceramic coating singapore`
- le cluster mobile/doorstep est à 0. **Le doorstep est un argument de vente,
  pas un levier SEO** : il se travaille en H2 et dans le corps du texte, jamais
  en H1 ni en title.

### Pages prévues

| Route | H1 |
|---|---|
| `/` | Car Detailing Singapore – Premium Coating & Grooming |
| `/ceramic-coating-singapore/` | Ceramic Coating Singapore – Done at Your Doorstep |
| `/graphene-coating-singapore/` | Graphene Coating Singapore – Artdeshine V3 Certified Installer |
| `/car-interior-detailing/` | Car Interior Detailing Singapore – We Come to You |
| `/car-polishing-paint-correction/` | Car Polishing & Paint Correction Singapore |
| `/coat-maintenance/` | Car Grooming & Coat Maintenance Singapore |
| `/mobile-car-detailing/` | Doorstep Car Detailing – Anywhere in Singapore (hors nav) |
| `/reviews/` | Car Armour SG Reviews – 200+ Verified Customers |
| `/contact/` | contact, horaires, réservation |
| `/guides/` | huit articles |

Sort de `/ceramic-coating-price-singapore/` **encore à trancher** : l'intention
prix a été rapatriée sur l'accueil, mais le bouton « What is ceramic coating ? »
de la section services pointe encore vers cette URL.

### Mise en œuvre

- `title`, `description`, `canonical`, OG uniques par page (bloc META).
- JSON-LD `AutoDetailing` global injecté par le layout ; les schémas `Service`,
  `FAQPage` et `AggregateRating` s'ajoutent par page via `headExtra`.
- Le `FAQPage` de l'accueil est **recopié depuis le HTML visible** à chaque
  modification des questions. Les deux ne doivent jamais diverger.
- `sitemap.xml` et `robots.txt` : à écrire en étape 4.

## Accueil : ordre des sections

```
hero → intro (void) → services (charcoal) → équipe (paper) → tarifs (charcoal)
→ doorstep (paper) → avis (charcoal) → FAQ (paper + fond travaillé) → CTA
```

Les sections claires et sombres alternent volontairement. La coupure entre deux
sections se marque par un filet doré avec un halo très discret au centre
(`.section--edge`), pas par un dégradé.

## Préproduction

<https://jorenzo24.github.io/cararmour.sg/> — sous-chemin, `noindex` sur toutes
les pages et `robots.txt` bloquant. Republier :

```bash
./_src/deploy-preview.sh "message de commit"
```

Le script reconstruit avec `--base /cararmour.sg --noindex`, puis pousse un
commit sur la branche `gh-pages`.

**Deux mécanismes coexistent**, et c'est à nettoyer : GitHub Pages est configuré
en `build_type: legacy` sur la branche `gh-pages`, donc c'est bien
`deploy-preview.sh` qui publie réellement. Le workflow
`.github/workflows/preview.yml` construit aussi le site à chaque push sur `main`
et appelle `deploy-pages`, sans effet tant que la configuration reste en legacy.

Leçon à ne pas répéter : le groupe de concurrence `pages` est **partagé avec le
pipeline intégré** de GitHub. Avec `cancel-in-progress: true`, chaque publication
tuait la précédente et aucune n'aboutissait. Quatre échecs d'affilée que j'avais
d'abord attribués à GitHub. Le groupe est désormais en `cancel-in-progress: false`.

Quand un run échoue, lire les annotations avant de conclure. Une panne réelle des
runners hébergés s'est produite ensuite, avec un message explicite
(`The job was not acquired by Runner of type hosted`), rien de configurable.

## Vérifier le rendu

`_src/shot.sh` capture une page en neutralisant le reveal au scroll et en
retirant `loading="lazy"`. Chrome headless ignore `--window-size` pour le
viewport de mise en page : pour tester une largeur mobile réelle, charger la page
dans une iframe de la largeur voulue. Les transitions CSS n'avancent pas sous
`--virtual-time-budget`.

Lighthouse local : A11y, bonnes pratiques et SEO à 100, CLS 0, LCP 0,7 s,
FCP 0,4 s. Le TBT reste bloqué entre 570 et 670 ms, y compris sur des variantes
dépouillées (sans CSS, sans JS, sans images, sans fontes) où il devrait
s'effondrer. Mesure locale non fiable. **À reprendre sur PageSpeed Insights une
fois le site en production.**

## À confirmer avec le client

- Grille tarifaire taille × durée : dérivée des tarifs de l'ancien site
  (Ceramic 1 couche S$388, Graphene V3 S$688, surcharge SUV/MPV S$50).
- Volume d'avis et note moyenne annoncés (`ratingValue` 4,9, `reviewCount` 213
  dans `site.json`). Seuls trente avis ont été récupérés, tous datés de 2021.
- Composition de l'équipe : le texte actuel reste volontairement large.
- « Trusted by car owners for over 20 years » et « 3,500+ customers ·
  5,000+ vehicles » viennent du client le 2026-10-06. Ces chiffres ne sont
  recoupés nulle part ailleurs, les garder cohérents si d'autres pages les
  reprennent.
- Adresse postale : aucune sur l'ancien site (service 100 % mobile).

## Fragments en attente

`_src/fragments/coating-comparison.html` : comparatif ceramic / graphene et
encart « ce que ça ne fait pas », retirés de l'accueil le 2026-10-05. À
replacer sur `/ceramic-coating-singapore/`. Les composants `.compare` et
`.caveat` sont restés dans le design system, il n'y a rien à réécrire.
