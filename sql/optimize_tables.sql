-- Optimisation Spark/Delta — OPTIMIZE + Z-Ordering.
--
-- Principe : Z-Ordering co-localise physiquement les lignes qui partagent des
-- valeurs proches sur les colonnes indiquées, dans les mêmes fichiers Parquet.
-- Databricks peut alors *skip* des fichiers entiers (data skipping) au lieu de
-- les scanner, pour toute requête qui filtre/groupe sur ces colonnes — ça
-- réduit le volume de données lues et donc le shuffle en aval (agrégations,
-- jointures).
--
-- Sur le volume actuel du projet (quelques centaines à quelques milliers de
-- lignes), l'effet est négligeable — l'intérêt ici est de démontrer la
-- technique, qui devient significative à partir de dizaines/centaines de Go.

-- Table Silver Vélo'v — requêtée le plus souvent filtrée par station et par
-- fenêtre temporelle (voir sql/dashboard_queries.sql).
OPTIMIZE lyonflow.silver.velov_clean
ZORDER BY (station_id, ingested_at);

-- Table Gold agrégée — le dashboard filtre/trie par station et par heure.
OPTIMIZE lyonflow.gold.velov_hourly_agg
ZORDER BY (station_id, hour);

-- Table Silver CRITER — requêtée par identifiant capteur.
OPTIMIZE lyonflow.silver.criter_clean
ZORDER BY (identifiantptm);

-- Vérifier l'effet : compare le nombre de fichiers avant/après.
DESCRIBE DETAIL lyonflow.gold.velov_hourly_agg;

-- Note partitionnement : ces tables restent petites, donc pas de partitioning
-- physique (PARTITIONED BY) — le découpage par date deviendrait pertinent si
-- le volume d'historique bronze grossit significativement (des mois
-- d'ingestion toutes les 30 min), pour éviter de scanner tout l'historique à
-- chaque lecture incrémentale du DLT pipeline.
