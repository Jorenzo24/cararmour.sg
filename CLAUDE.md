# cararmour.sg — site statique

Refonte multi-pages SEO de Car Armour SG (car detailing, Singapour).
Contenu **en anglais (en-SG)**, prix en dollars de Singapour.

## État d'avancement

Le brief fixe quatre étapes, **aucune ne démarre sans validation explicite du
client**.

| Étape | Contenu | Statut |
|---|---|---|
| 1 | Design system en tokens | fait, visible sur `/styleguide/` |
| 2 | Accueil complet et abouti | fait, premier retour client intégré |
| 3 | Gabarits : page service informationnelle, avis, contact (réduit le 2026-10-14) | **en cours** : page service faite sur `/what-is-ceramic-coating/` |
| 4 | Pages restantes, `sitemap.xml`, `robots.txt`, schémas par page | non démarrée |

Pages réellement générées à ce jour : `/`, `/what-is-ceramic-coating/` et
`/styleguide/` (noindex). Les six autres routes internes listées plus bas sont
prévues, pas écrites.

### Retour client du 2026-10-06

Appliqué : hero éclairci, `S$` remplacé par `$`, indicatif `+65` sur les
numéros, accroche d'introduction devenue « Premium doorstep service at your
convenience » et portée par un `h2`, section avis retitrée « Trusted by car
owners for over 20 years » avec le sous-titre « Our care: 3,500+ customers ·
5,000+ vehicles » et la mention « Facebook and Google reviews ».

Signalé au client, sans réponse à ce jour :

- **Deux `h2` doorstep** cohabitent maintenant sur l'accueil, le nouveau en
  haut et « Doorstep service available island-wide » plus bas. Sans pénalité,
  mais redondant. Retitrer celui du bas si le client valide.
- « **Our care:** » sonne bancal en anglais. « Our track record: » dirait la
  même chose plus naturellement.
- Les « 20 ans » et les « 3 500+ clients » ne sont recoupés nulle part
  ailleurs, et l'`AggregateRating` annonce toujours 213 avis.

Le logo Lamborghini du hero devait être retiré. Le client a dit de laisser.

### Retour client du 2026-10-13

Appliqué : prix en `SGD 388` (retour sur la décision du 6), téléphone affiché
`+(65) 8850 1200`, accroches du hero et de l'intro inversées, « paint
correction » supprimé partout au profit de « polishing » (extra tarifaire
retiré, il n'en reste que deux), carte Graphene renommée « ARTDESHINE Nano
Graphene Coating+ », textes de l'équipe et de la FAQ repris, colonne « Learn »
du footer renommée « For Your Information (FYI) ».

La garantie n'a été retirée **que** là où le client l'a demandé (intro et
dernière FAQ). Ne pas l'enlever ailleurs sans demande explicite.

En attente :

- **Grille tarifaire réglée le 2026-10-14** : trois gabarits partout (Small,
  Large SUV/MPV, Extra Large / Exotic). Polish & Wax Coating 238 / 288 / 338
  (remplace le Nano Coating, qui n'existe plus), Ceramic 488 / 538 / 588, Nano
  Graphene Coating 688 / 738 / 788. Le sur-titre « Polish · Wax », la
  description et la durée « About two hours » de la première carte sont des
  propositions, à faire valider.
- **Le site dénigre la cire alors que le client en vend** : carte services
  Ceramic (« not a wax that washes off in a month ») et FAQ « Is a coating worth
  it over a good wax? » (« Singapore rain takes it off in weeks »). Signalé, à
  trancher avec le client.
- **Nom du graphène** : « V3 » subsiste dans la nav, la description de la carte
  tarifaire et la FAQ, alors que la carte services dit désormais « Coating+ ».
  Le titre de la carte tarifaire est passé à « Graphene Coating » (mot-clé
  transactionnel, à l'endroit le plus « prix » de la page).
- Maintenance « tous les trois mois » appliquée aussi à la FAQ durée, pour ne
  pas contredire la FAQ entretien.
- L'étape 2 du doorstep promet encore de prévenir « before you book », ce que la
  FAQ ne dit plus.

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
  "route": "/what-is-ceramic-coating/",
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
- **Prix : `SGD 388`**, espace insécable dans le HTML. Le client est passé de
  `S$` à `$` le 2026-10-06, puis de `$` à `SGD` le 2026-10-13. La mention « in
  Singapore dollars » du chapo tarifs a été retirée à sa demande.
- **Téléphone affiché** : `+(65) 8850 1200`, à la demande du client. Source
  unique, `phoneDisplay` dans `site.json`. Le lien `tel:` reste `+6588501200`.
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

**L'accueil porte toutes les requêtes transactionnelles** (car detailing,
ceramic et graphene coating, leurs déclinaisons `price`, interior detailing,
polishing). **Les pages internes sont informationnelles** : elles répondent à
une question et ne reprennent jamais la requête de l'accueil dans leur H1,
leur title ou leur URL, sans quoi elles le concurrencent. D'où des routes sans
`singapore` ni `price`, et des H1 en forme de question ou d'explication.

| Route | H1 | Requêtes visées |
|---|---|---|
| `/` | Car Detailing Singapore | toutes les transactionnelles |
| `/what-is-ceramic-coating/` | What Is Ceramic Coating? How It Bonds and How Long It Lasts | what is, durée de vie, worth it, vs wax, vs PPF |
| `/what-is-graphene-coating/` | What Is Graphene Coating? Artdeshine Nano Graphene Coating+ Explained | what is, ceramic vs graphene, nom du produit |
| `/car-polishing/` | Car Polishing Explained: Swirl Marks, Water Spots and Light Scratches | car polishing, swirl marks, polish avant coating |
| `/car-interior-detailing/` | What a Car Interior Detailing Session Includes | interior detailing, steam clean, cuir |
| `/coat-maintenance/` | How to Maintain a Coated Car in Singapore's Climate | coating maintenance, aftercare, car grooming |
| `/reviews/` | Car Armour SG Reviews | car armour review |
| `/contact/` | Contact & Booking | navigationnel |

**Validé le 2026-10-14** : la distinction page service / article de guide
disparaît, puisque toutes les pages internes sont informationnelles. Une page
explique un service en profondeur puis rappelle son prix. `/mobile-car-detailing/`
(doorstep à zéro volume, déjà argumenté sur l'accueil) et `/guides/` (huit
articles qui doublonneraient ces pages) sont abandonnés. Un guide ne se rouvre
que pour une question restée sans réponse une fois ces pages en ligne. Les
gabarits de l'étape 3 passent de cinq à trois : page service informationnelle,
avis, contact. **Changement de brief à faire valider par le client.**

**Appels à l'action dans les pages internes** : nombreux, et ils mènent
**directement à la réservation** (`{{booking}}`, qui affiche les prix et prend
le rendez-vous), jamais vers l'accueil. Une page informationnelle convertit sur
place.

**Menu** : sept entrées à plat, sans menu déroulant ni « Home » (le logo y
mène) : Ceramic Coating, Graphene Coating, Polishing, Interior, Maintenance,
Reviews, Contact, puis le bouton Book Now. Pas d'ancres vers les sections de
l'accueil, refusées par l'agence le 2026-10-14. Clefs `nav` des pages :
`ceramic`, `graphene`, `polishing`, `interior`, `maintenance`, `reviews`,
`contact`. Le menu bascule en burger sous 1220 px : en dessous, Book Now
débordait.

**Prix : source unique** dans `_src/partials/price-grid.html`, inclus par
l'accueil. Un changement de prix s'y fait, puis se reporte dans les textes de
l'accueil qui citent un chiffre (carte services, FAQ tarifs) : `grep SGD`.

### Gabarit de page service (étape 3)

`/what-is-ceramic-coating/` sert de modèle aux quatre autres pages de service.

**Contenu universel, jamais propre à Car Armour** (retour du 2026-10-14) : ni
prix, ni garantie, ni durée d'intervention maison, ni « we », ni « at your
residence ». La page explique le sujet comme une référence neutre ; Car Armour
n'y apparaît que par les boutons de réservation, qui mènent tous à
`{{booking}}`. Les prix et la garantie vivent sur l'accueil.

**Pas de petit titre au-dessus des titres** (`.eyebrow`, « 01 · The
chemistry », « Coating guide ») et **pas de rangée de chiffres clés** sous
l'en-tête : refusés le 2026-10-14.

**Structure éditoriale** (retours du 2026-10-14) : la page se lit comme un
article de site média. Une **colonne centrale** (`.sheet`, 62rem, fond
charbon) se détache des côtés plus sombres. Le texte (`.prose-col`, 44rem), les
photos et les figures y ont **la même largeur** ; seuls le tableau et la frise
prennent toute la colonne (`.sheet-wide`). Les données se racontent
dans le fil du texte, avec un visuel propre à chacune : coupe de peinture à
l'échelle, 365 cases dont 171 jours de pluie (`.days`), échelle UV de la NEA
(`.uv`), graphique de durées (`.range`), comparateur avant/après à
curseur (`.ba`).

**Maillage interne** : chaque page lie dans le texte les pages voisines
(polishing, coat maintenance, graphène) et renvoie à l'accueil avec l'ancre
de sa requête transactionnelle (« ceramic coating in Singapore »). Liens
contextuels dans des phrases, jamais une liste « related pages ».

**Mises en page refusées, à ne plus proposer sur aucun site** : l'en-tête
titre à gauche + petit paragraphe à droite (`.section-head--split`), et la
rangée de quatre chiffres clés séparés par des filets. L'utilisateur les voit
revenir d'un site à l'autre.

Fil de la page ceramic : en-tête → ce qu'est un coating → le climat de
Singapour → alternatives (tableau) → application (diptyque
photo, étapes) → durée de vie (facteurs, graphique) → entretien (photo, frise)
→ FAQ propre à la page → CTA. Un bouton de réservation clôt chaque partie.

**Pas d'encadré à filet gauche** (`.caveat`), jugé « standard IA ». Le bloc
« ce que ça ne fait pas » a été retiré entièrement le 2026-10-14 : jugé inutile,
et il dénigrait le service vendu.

**Faits** : uniquement des chiffres vérifiés et sourcés sur la page (climat :
Meteorological Service Singapore, normales 1991–2020, 2 113 mm, 171 jours de
pluie, 82 % d'humidité ; UV : échelle NEA). Les pratiques décrites sont celles du
métier en général, pas celles de l'entreprise.

La page graphène est l'endroit où le **nom commercial du produit** a toute sa
place : le terme générique travaille sur l'accueil, la marque sur la page qui
l'explique. Nom exact à confirmer (V3 ou Coating+).

`/ceramic-coating-price-singapore/` est **abandonnée** : l'intention prix vit
sur l'accueil. Le bouton « What is ceramic coating? » des services mène à
`/what-is-ceramic-coating/`.

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

Les `h2` de la page, dans l'ordre : Doorstep Service at Your Convenience (hero),
Premium coating & grooming, Our car detailing services, Meet our
expert team, Our car detailing prices, Doorstep service available island-wide,
Trusted by car owners for over 20 years, Questions we get every week.

`.intro__title` est un `h2` pour la structure, pas pour le style : il garde la
fonte de labeur et la casse normale. En Archivo capitales juste sous le hero il
concurrencerait le `h1`.

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
  (Ceramic 1 couche $388, Graphene V3 $688, surcharge SUV/MPV $50).
- Volume d'avis et note moyenne annoncés (`ratingValue` 4,9, `reviewCount` 213
  dans `site.json`). Seuls trente avis ont été récupérés, tous datés de 2021.
- Composition de l'équipe : le texte actuel reste volontairement large.
- « Trusted by car owners for over 20 years » et « 3,500+ customers ·
  5,000+ vehicles » viennent du client le 2026-10-06. Ces chiffres ne sont
  recoupés nulle part ailleurs, les garder cohérents si d'autres pages les
  reprennent.
- Adresse postale : aucune sur l'ancien site (service 100 % mobile).

## Photos à demander au client

- **Avant / après** pour `/what-is-ceramic-coating/` (« What you notice
  afterwards ») : même panneau, même lumière, même cadrage, avant polissage et
  après coating. Le comparateur `.ba` attend avec deux placeholders ; un
  commentaire dans le source dit quoi remplacer.
- Des photos propres à chaque page de service : les quatre de la page ceramic
  sont déjà utilisées sur l'accueil.

## Fragments en attente

`_src/fragments/coating-comparison.html` : comparatif ceramic / graphene et
encart « ce que ça ne fait pas », retirés de l'accueil le 2026-10-05. À
replacer sur `/what-is-ceramic-coating/`. Les composants `.compare` et
`.caveat` sont restés dans le design system, il n'y a rien à réécrire.
