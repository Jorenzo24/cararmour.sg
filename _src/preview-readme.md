# Préproduction — cararmour.sg

Branche **générée**, ne pas éditer à la main : elle est écrasée à chaque
publication. Les sources vivent sur `main`.

Sortie du générateur recompilée pour le sous-chemin GitHub Pages, avec `noindex`
sur toutes les pages et un `robots.txt` bloquant — c'est une préproduction, elle
ne doit pas être indexée ni concurrencer le site du client.

Republier depuis `main` : `./_src/deploy-preview.sh "message"`
