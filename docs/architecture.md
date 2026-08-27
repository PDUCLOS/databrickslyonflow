# Architecture

## Vue d'ensemble

```
Vélo'v GBFS (JSON, 1 min)  ─┐
                             ├─► Bronze (Delta, raw, append-only)
CRITER comptages trafic  ───┘

Bronze ──[DLT: nettoyage, dédup, typage]──► Silver (Delta, qualité contrôlée)

Silver ──[DLT: agrégations horaires/journalières]──► Gold (Delta, tables métier)

Gold ──► Databricks SQL / Genie (dashboard, questions langage naturel)
Gold ──► MLflow (entraînement modèle prédiction dispo/trafic) ──► Model Registry ──► Model Serving (endpoint temps réel)
Gold + docs projet ──► Vector Search (optionnel) ──► Agent RAG (Model Serving)

Databricks Workflows orchestre l'ensemble (planification, historique, alerting)
Unity Catalog gouverne l'ensemble (catalogue, schémas, permissions)
```

## Catalogue Unity Catalog

```
lyonflow (catalog)
├── bronze
│   ├── velov_raw        # append-only, 1 snapshot GBFS par ingestion
│   └── criter_raw       # append-only, comptages trafic bruts
├── silver
│   ├── velov_clean       # typé, dédupliqué, stations fermées filtrées
│   └── criter_clean      # typé, dédupliqué, valeurs aberrantes exclues
└── gold
    ├── velov_hourly_agg  # disponibilité moyenne par station / heure
    └── criter_site_stats # dernier snapshot de stats de référence par capteur
```

## Composants Databricks utilisés

| Composant | Rôle |
|---|---|
| Notebooks (Python/SQL) | Exploration, ingestion Bronze |
| Delta Lake | Format de stockage Bronze/Silver/Gold |
| Delta Live Tables (DLT) | Pipeline déclaratif Bronze→Silver→Gold, règles qualité |
| Unity Catalog | Gouvernance, catalogage, permissions |
| Databricks Workflows | Orchestration planifiée |
| MLflow (Tracking + Model Registry) | Suivi/versioning modèle de prédiction |
| Model Serving | Endpoint REST temps réel |
| Databricks SQL / Genie | Dashboard + requêtes langage naturel |
| Vector Search (optionnel) | Agent RAG sur documentation projet |
