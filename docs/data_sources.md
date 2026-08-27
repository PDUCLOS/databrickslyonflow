# Sources de données

## Vélo'v Lyon — GBFS (temps réel)

Producteur : Métropole de Lyon / JCDecaux · Licence Ouverte 2.0 · rafraîchi toutes les minutes.

- Flux GBFS : `https://download.data.grandlyon.com/files/rdata/jcd_jcdecaux.jcdvelov/gbfs.json`
- Alternative GeoJSON/CSV via WFS :
  `https://data.grandlyon.com/geoserver/metropole-de-lyon/ows?SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=metropole-de-lyon:jcd_jcdecaux.jcdvelov&outputFormat=application/json&SRSNAME=EPSG:4326`
- Fiche jeu de données : https://transport.data.gouv.fr/datasets/stations-velov-de-la-metropole-de-lyon-disponibilites-temps-reel

Aucune clé API, aucun compte requis.

## CRITER — comptages trafic/vélo Grand Lyon

Deux couches candidates ont été testées en direct sur le WFS `data.grandlyon.com` :

1. **`pvo_patrimoine_voirie.pvotrafic`** (état du trafic temps réel) — **inaccessible en accès public**, renvoie `401 Informations d'authentification non fournies`. Nécessite une authentification non documentée/disponible.

2. **`metropole-de-lyon:pvo_patrimoine_voirie.pvocomptagecriter`** (retenue, ✅ accessible sans clé) :
   - Endpoint : `https://data.grandlyon.com/fr/geoserv/metropole-de-lyon/ows/`
   - Params : `SERVICE=WFS&VERSION=2.0.0&request=GetFeature&typename=metropole-de-lyon:pvo_patrimoine_voirie.pvocomptagecriter&outputFormat=application/json&SRSNAME=EPSG:4326`
   - ~2800 capteurs (boucles inductives Criter, comptage vélo/trafic)
   - Champs : `identifiantptm`, `nom`, `positionnement`, `typecapteur`, `nbvoies`, `moyennejoursouvrable` (débit moyen jour ouvrable), `debithorairemax`, `horairedebitmax`, `anneereference`, `geometry` (point WKT-like en string)
   - Certains champs (ex. `estvalide`) sont `None` sur l'ensemble d'un batch — filtrés avant écriture Delta pour éviter `CANNOT_DETERMINE_TYPE` sur `createDataFrame`
   - **Important :** ce sont des statistiques de référence annuelle par capteur, **pas** un flux temps réel minute par minute. Le Gold (`criter_site_stats`) retient donc le dernier snapshot par capteur plutôt qu'une agrégation horaire.

`notebooks/02_bronze_ingestion_criter.py` est câblé sur la couche 2. Note technique : le typename WFS doit inclure le préfixe de namespace `metropole-de-lyon:`, sans quoi GeoServer répond `401` au lieu d'un message d'erreur explicite.

Aucune clé API requise pour la couche `pvocomptagecriter`.
