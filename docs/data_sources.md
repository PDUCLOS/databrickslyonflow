# Sources de données

## Vélo'v Lyon — GBFS (temps réel)

Producteur : Métropole de Lyon / JCDecaux · Licence Ouverte 2.0 · rafraîchi toutes les minutes.

- Flux GBFS : `https://download.data.grandlyon.com/files/rdata/jcd_jcdecaux.jcdvelov/gbfs.json`
- Alternative GeoJSON/CSV via WFS :
  `https://data.grandlyon.com/geoserver/metropole-de-lyon/ows?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=metropole-de-lyon:jcd_jcdecaux.jcdvelov&outputFormat=application/json&SRSNAME=EPSG:4326`
- Fiche jeu de données : https://transport.data.gouv.fr/datasets/stations-velov-de-la-metropole-de-lyon-disponibilites-temps-reel

Aucune clé API, aucun compte requis.

## CRITER — comptages trafic (boucles de comptage Grand Lyon)

Même famille de flux que celle déjà intégrée dans LyonFlow (comptages trafic Grand Lyon).

**TODO :** renseigner ici l'URL exacte du flux CRITER utilisée (endpoint WFS/API data.grandlyon.com), disponible publiquement sur le portail open data de la Métropole de Lyon (https://data.grandlyon.com). Ce dépôt ne réutilise aucun code du projet LyonFlow — uniquement la référence à la source de données publique, à ingérer indépendamment via `notebooks/02_bronze_ingestion_criter.py`.

Aucune clé API requise pour les flux open data Grand Lyon.
