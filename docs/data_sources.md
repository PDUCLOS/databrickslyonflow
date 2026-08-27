# Sources de données

## Vélo'v Lyon — GBFS (temps réel)

Producteur : Métropole de Lyon / JCDecaux · Licence Ouverte 2.0 · rafraîchi toutes les minutes.

- Flux GBFS : `https://download.data.grandlyon.com/files/rdata/jcd_jcdecaux.jcdvelov/gbfs.json`
- Alternative GeoJSON/CSV via WFS :
  `https://data.grandlyon.com/geoserver/metropole-de-lyon/ows?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=metropole-de-lyon:jcd_jcdecaux.jcdvelov&outputFormat=application/json&SRSNAME=EPSG:4326`
- Fiche jeu de données : https://transport.data.gouv.fr/datasets/stations-velov-de-la-metropole-de-lyon-disponibilites-temps-reel

Aucune clé API, aucun compte requis.

## CRITER / État du trafic — comptages trafic Grand Lyon

Deux jeux de données distincts existent sur data.grandlyon.com — **à vérifier lequel LyonFlow utilise déjà** (regarder l'URL/table dans la config LyonFlow existante, sans copier son code) :

1. **État du trafic temps réel** (candidat le plus probable — flux vivant, comme décrit dans le projet) :
   - WFS/WMS GetCapabilities : `https://data.grandlyon.com/fr/geoserv/metropole-de-lyon/ows/?service=WFS&version=1.3.0&request=GetCapabilities`
   - Couche (typename) : `pvo_patrimoine_voirie.pvotrafic`
   - Fiche : https://www.data.gouv.fr/datasets/etat-du-trafic-de-la-metropole-de-lyon-disponibilites-temps-reel

2. **Comptage CRITER** (positions capteurs + statistiques semaine de référence n-1, **pas** un flux temps réel minute) :
   - Export GeoJSON/CSV/Shapefile statique, mis à jour périodiquement
   - Fiche : https://www.data.gouv.fr/datasets/comptage-criter-de-la-metropole-de-lyon
   - Timeseries mesures associées : `https://download.data.grandlyon.com/ws/timeseries/pvo_patrimoine_voirie.pvocomptagemeasure/all.json`

`notebooks/02_bronze_ingestion_criter.py` est déjà câblé sur le typename `pvo_patrimoine_voirie.pvotrafic` (option 1). Si LyonFlow utilise en réalité l'option 2, changer le widget `wfs_typename` ou basculer le notebook sur l'endpoint timeseries.

Aucune clé API requise pour ces flux open data Grand Lyon.
