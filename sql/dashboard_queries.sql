-- Databricks SQL — requêtes dashboard Gold (Semaine 4)
-- À importer dans Databricks SQL Editor / Dashboard.

-- 1. Disponibilité moyenne par station, dernière heure
SELECT
  station_id,
  name,
  hour,
  avg_bikes_available,
  avg_docks_available,
  capacity,
  ROUND(avg_bikes_available / capacity * 100, 1) AS occupancy_pct
FROM lyonflow.gold.velov_hourly_agg
WHERE hour >= current_timestamp() - INTERVAL 1 HOUR
ORDER BY occupancy_pct ASC;

-- 2. Stations les plus souvent vides le matin (7h-9h), 7 derniers jours
SELECT
  station_id,
  name,
  COUNT(*) AS nb_heures_vides
FROM lyonflow.gold.velov_hourly_agg
WHERE HOUR(hour) BETWEEN 7 AND 9
  AND hour >= current_date() - INTERVAL 7 DAYS
  AND avg_bikes_available < capacity * 0.1
GROUP BY station_id, name
ORDER BY nb_heures_vides DESC
LIMIT 20;

-- 3. Tendance horaire globale de disponibilité (réseau entier)
SELECT
  HOUR(hour) AS heure_journee,
  AVG(avg_bikes_available / capacity) AS taux_disponibilite_moyen
FROM lyonflow.gold.velov_hourly_agg
GROUP BY HOUR(hour)
ORDER BY heure_journee;

-- 4. Capteurs CRITER avec le débit horaire max le plus élevé (année de référence)
SELECT
  identifiantptm,
  nom,
  positionnement,
  moyennejoursouvrable,
  debithorairemax,
  horairedebitmax,
  anneereference
FROM lyonflow.gold.criter_site_stats
ORDER BY debithorairemax DESC
LIMIT 20;
