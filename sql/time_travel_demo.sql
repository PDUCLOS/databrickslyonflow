-- Delta Lake Time Travel — démo à exécuter/capturer en Databricks SQL.
-- Table cible : lyonflow.bronze.velov_raw (append-only, accumule une nouvelle
-- version à chaque run du job d'ingestion — bon candidat pour montrer l'historique).

-- 1. Historique des versions de la table
DESCRIBE HISTORY lyonflow.bronze.velov_raw;

-- 2. Compter les lignes à la version actuelle
SELECT count(*) FROM lyonflow.bronze.velov_raw;

-- 3. Requêter une version antérieure (remplacer 0 par un numéro de version
--    visible dans le résultat de DESCRIBE HISTORY ci-dessus)
SELECT count(*) FROM lyonflow.bronze.velov_raw VERSION AS OF 0;

-- Alternative par timestamp :
-- SELECT count(*) FROM lyonflow.bronze.velov_raw TIMESTAMP AS OF '2026-08-27T10:00:00Z';

-- 4. Restaurer la table à une version antérieure (scénario : run corrompu à
--    annuler). À ne PAS exécuter en démo sauf si tu veux vraiment revenir en
--    arrière — decommenter volontairement :
-- RESTORE TABLE lyonflow.bronze.velov_raw TO VERSION AS OF 0;

-- Capture d'écran à garder pour le portfolio : résultat de DESCRIBE HISTORY
-- (colonnes version, timestamp, operation, operationParameters) + un exemple
-- de requête VERSION AS OF renvoyant un count différent de la version actuelle.
