# Semaine 2 — Checklist autonome (Orchestration & qualité)

À suivre seul dans Databricks, sans attendre de retour. Coche au fur et à mesure.

**Pré-requis (déjà fait fin Semaine 1) :** pipeline DLT `bronze to gold` créé et fonctionnel (465 stations Vélo'v, ~2799→3.9K capteurs CRITER, tables silver/gold peuplées).

---

## 0. Règle d'or Free Edition (leçon de la Semaine 1)

**Ne jamais faire tourner deux choses en même temps** (notebook + pipeline, ou requête SQL + pipeline) — ça a fait planter le run gold hier (`RESOURCE_EXHAUSTED` / "Pipeline compute was terminated"). Avant de lancer quoi que ce soit :
- **Compute** (sidebar) → vérifie que rien d'autre ne tourne, stop si besoin.
- Lance UNE chose, attends qu'elle finisse (statut vert), puis la suivante.

---

## 1. Créer le Workflow d'orchestration Vélo'v

1. **Jobs & Pipelines** → onglet **Jobs** → **Create Job**
2. Nom : `lyonflow-ingestion-and-pipeline`
3. **Task 1** — `ingest_velov`
   - Type : Notebook
   - Notebook path : le chemin de `notebooks/01_bronze_ingestion_velov.py` dans ton Git folder (`Workspace > Repos > ... > databrickslyonflow > notebooks > 01_bronze_ingestion_velov`)
   - Paramètre `catalog` = `lyonflow` (si le widget le demande)
4. **Task 2** — `run_dlt_pipeline`
   - Clique **+** pour ajouter une tâche, **Depends on** : `ingest_velov`
   - Type : **Pipeline**
   - Sélectionne ton pipeline existant **`bronze to gold`** (celui déjà créé, ne pas en recréer un)
5. **Notifications** — onglet **Notifications** du job → **Add** → sur "On failure" → ton adresse email. Ça donne l'alerting automatique attendu en prod.
6. **Schedule** (en haut à droite du job) :
   - Trigger type : **Scheduled**
   - Toutes les **30 minutes** pour commencer (pas 15 min tout de suite — laisse de la marge quota Free Edition, tu resserreras plus tard si stable)
   - Timezone : Europe/Paris
   - **Laisse le job en pause au début** (case "Paused" cochée) — tu le lanceras manuellement une première fois avant d'activer le auto-schedule
7. **Save**

## 2. Premier run manuel (validation avant auto-schedule)

1. Sur le job créé → **Run now**
2. Attends la fin complète des 2 tasks (vert)
3. Vérifie les données (une requête à la fois, jamais en même temps que le job tourne) :
   ```sql
   SELECT count(*) FROM lyonflow.bronze.velov_raw;
   ```
   Le nombre doit avoir augmenté par rapport à avant (nouveau snapshot ajouté, append-only).
4. Si tout est vert → retourne dans le job → **Unpause** le schedule.

## 3. Job séparé pour CRITER (fréquence rare)

CRITER est une stats de référence **annuelle** par capteur (pas un flux temps réel) — pas besoin de le réingérer toutes les 30 min. Job séparé, cadence hebdomadaire :

1. **Create Job** → nom `lyonflow-criter-refresh`
2. Une seule task : notebook `notebooks/02_bronze_ingestion_criter.py`
3. Schedule : hebdomadaire (ex. lundi 6h)
4. Pas besoin de le lancer maintenant — les 2799/3.9K lignes déjà en base suffisent pour la démo. Active juste le schedule, laisse tourner en fond.

## 4. Qualité — vérifier ce qui existe déjà

Les règles `expect_or_drop` sont déjà en place dans [`dlt_pipelines/bronze_to_silver.py`](../dlt_pipelines/bronze_to_silver.py) :
- Vélo'v : capacité valide, vélos dispo cohérents, station active, timestamp non nul
- CRITER : id capteur non nul, débits ≥ 0, timestamp non nul

**Rien à coder ici.** Juste vérifier après quelques runs auto que les compteurs "expectations met/unmet" restent stables dans l'onglet **Tables** du pipeline — si un chiffre d'unmet explose d'un coup, ça vaut le coup de creuser (source de données changée, bug amont).

## 5. Preuves à capturer pour le portfolio (déjà préparées, juste à exécuter)

Le reste — architecture visuelle, tests, CI, Time Travel, Z-Ordering — est déjà écrit dans le repo. Il ne reste que des actions à faire **dans Databricks** pour en avoir la preuve (screenshot) :

- [ ] **Data lineage** — Catalog Explorer → une table gold → onglet **Lineage** → screenshot (voir [`docs/architecture.md`](architecture.md#gouvernance--lineage-unity-catalog))
- [ ] **Time Travel** — exécuter [`sql/time_travel_demo.sql`](../sql/time_travel_demo.sql) une requête à la fois, screenshot de `DESCRIBE HISTORY` + d'un `VERSION AS OF`
- [ ] **OPTIMIZE/Z-Order** — exécuter [`sql/optimize_tables.sql`](../sql/optimize_tables.sql), screenshot du résultat
- [ ] **Spark UI** — pendant un run du pipeline DLT, ouvrir l'onglet Spark UI du cluster (Compute → cluster actif → Spark UI) et screenshot un DAG de stage

## 6. Livrable Semaine 2 (check final)

- [ ] Job `lyonflow-ingestion-and-pipeline` actif, tourne toutes les 30 min sans erreur
- [ ] Job `lyonflow-criter-refresh` actif, hebdomadaire
- [ ] Alerting on-failure configuré
- [ ] Historique d'exécution visible (onglet **Runs** du job) — au moins 2-3 runs verts consécutifs
- [ ] 4 preuves de la section précédente capturées

Une fois ces cases cochées → Semaine 2 terminée, passe à `docs/plan.md` Semaine 3 (MLflow).
