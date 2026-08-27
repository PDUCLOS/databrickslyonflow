# Plan — 4 semaines

## Semaine 1 — Fondations (Bronze/Silver, Unity Catalog)

- Créer le compte Databricks Free Edition.
- Créer un catalog Unity Catalog `lyonflow` avec schémas `bronze`, `silver`, `gold`.
- Notebook d'ingestion : appel du flux GBFS Vélo'v + CRITER, écriture en table Delta Bronze (append-only, horodatée).
- Premier pipeline DLT simple : Bronze → Silver (typage, dédoublonnage, gestion des stations fermées/inactives).
- **Livrable :** pipeline qui tourne manuellement, données visibles dans Unity Catalog.

## Semaine 2 — Orchestration & qualité

- Étendre le DLT pipeline : Silver → Gold (agrégations horaires : disponibilité moyenne par station, vitesse moyenne par boucle CRITER).
- Databricks Workflows : planifier l'exécution (ex. toutes les 15 min pour Vélo'v).
- Ajouter des règles de qualité DLT (`expect_or_drop` : valeurs négatives, stations hors zone, timestamps aberrants).
- **Livrable :** pipeline automatisé, historique d'exécution visible, qualité contrôlée.

## Semaine 3 — ML & mise en production

- Notebook d'entraînement : modèle de prédiction de disponibilité Vélo'v (XGBoost/Prophet sur séries temporelles).
- Tracking MLflow : paramètres, métriques (MAE, RMSE), comparaison de runs.
- Enregistrement du meilleur modèle dans le Model Registry.
- Déploiement en Model Serving : endpoint REST temps réel interrogeable.
- **Livrable :** endpoint fonctionnel, capture d'écran + exemple d'appel curl/Python dans le README.

## Semaine 4 — BI, valorisation, et (optionnel) agent GenAI

- Dashboard Databricks SQL sur les tables Gold (disponibilité par zone, tendances horaires).
- Configuration Genie pour poser des questions en langage naturel sur les données.
- (Optionnel) Vector Search + petit agent RAG répondant à des questions sur le réseau à partir de la documentation du projet.
- Finalisation du repo GitHub : README clair, captures d'écran, architecture, résultats chiffrés.
- Mise à jour CV/LinkedIn/lettres avec lien concret vers ce projet.
