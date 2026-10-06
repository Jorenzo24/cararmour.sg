# Sources d'images

Déposer ici les PNG et JPEG d'origine fournis par le client, **avant**
conversion en WebP. Ne pas les supprimer après génération.

Motif : le traitement colorimétrique est cuit dans les WebP. Quand il faut
le changer, repartir du WebP oblige à inverser le traitement, ce qui est
approximatif et passe par une seconde compression. C'est arrivé sur la photo
de la Ferrari, dont le rouge n'a pas pu être rendu exactement.

Ce dossier n'est pas publié : `.htaccess` bloque `/_src/`, et le script de
préproduction ne copie que `assets/`.
