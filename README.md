# LyonFlow · Databricks Lakehouse

Preuve concrète de compétences Databricks (Delta Lake, Delta Live Tables, Unity Catalog, MLflow, Model Serving, Databricks SQL/Genie) construite sur des données ouvertes temps réel de la Métropole de Lyon.

Ce projet **ne remplace pas** [LyonFlow](https://github.com/PDUCLOS) (PostgreSQL/PostGIS, Airflow, MinIO, MLflow, Evidently AI, FastAPI/Streamlit) — il le complète avec une couche Databricks démontrable, sur un dépôt séparé.

**Pourquoi ce projet, où on en est, comment le valoriser :** [`docs/vision.md`](docs/vision.md).
**Prochaine étape autonome (Semaine 2) :** [`docs/semaine2_checklist.md`](docs/semaine2_checklist.md).

---

## Sources de données

| Source | Type | Fréquence | Licence |
|---|---|---|---|
| Vélo'v Lyon (GBFS) | Disponibilité stations temps réel | 1 min | Licence Ouverte 2.0 — Métropole de Lyon / JCDecaux |
| CRITER (comptages trafic) | Boucles de comptage trafic | variable | Licence Ouverte 2.0 — Métropole de Lyon |

Aucune clé API, aucun compte requis. Endpoints dans [`docs/data_sources.md`](docs/data_sources.md).

## Architecture

```
Vélo'v GBFS (JSON, 1 min)  ─┐
                             ├─► Bronze (Delta, raw, append-only)
CRITER comptages trafic  ───┘

Bronze ──[DLT: nettoyage, dédup, typage]──► Silver (Delta, qualité contrôlée)

Silver ──[DLT: agrégations horaires/journalières]──► Gold (Delta, tables métier)

Gold ──► Databricks SQL / Genie (dashboard, questions langage naturel)
Gold ──► MLflow (entraînement modèle prédiction) ──► Model Registry ──► Model Serving (endpoint temps réel)

Databricks Workflows orchestre l'ensemble · Unity Catalog gouverne l'ensemble
```

Détail dans [`docs/architecture.md`](docs/architecture.md).

## Structure du repo

```
lyonflow-databricks/
├── databricks.yml              # Asset Bundle — déploiement infra-as-code
├── resources/                  # Définitions job + pipeline DLT (asset bundle)
├── notebooks/                  # Ingestion Bronze (Vélo'v, CRITER)
├── dlt_pipelines/              # Pipelines déclaratifs Bronze→Silver→Gold
├── ml/                         # Entraînement MLflow + exemple appel Model Serving
├── sql/                        # Requêtes Databricks SQL (dashboard Gold)
└── docs/                       # Architecture, sources de données, avancement
```

## Statut d'avancement

- [x] Semaine 1 — Fondations : Unity Catalog, ingestion Bronze, DLT Bronze→Silver→Gold (465 stations Vélo'v, 2799 capteurs CRITER)
- [ ] Semaine 2 — Orchestration & qualité : DLT Silver→Gold, Workflows, règles `expect_or_drop`
- [ ] Semaine 3 — ML & mise en production : MLflow Tracking, Model Registry, Model Serving
- [ ] Semaine 4 — BI & valorisation : Databricks SQL, Genie, README final, résultats chiffrés

Plan détaillé semaine par semaine : [`docs/plan.md`](docs/plan.md).

## Prérequis

1. Compte [Databricks Free Edition](https://www.databricks.com/learn/free-edition) (gratuit, sans carte bancaire).
2. [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html) installé et authentifié (`databricks auth login`).
3. Unity Catalog activé sur le workspace (par défaut sur Free Edition).

## Déploiement (Databricks Asset Bundles)

```bash
databricks bundle validate
databricks bundle deploy -t dev
databricks bundle run lyonflow_ingestion_job -t dev
```

## Résultats

_À compléter au fil du projet : MAE du modèle, captures d'écran dashboard Genie, exemple d'appel à l'endpoint Model Serving._
