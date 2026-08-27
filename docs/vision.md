# Vision du projet

## Pourquoi ce projet existe

Transformer une affirmation ("Databricks Lakehouse / Data Engineering / GenAI Fundamentals") en un **livrable vérifiable**, démontrable en entretien, aligné sur les compétences demandées par le marché lyonnais actuel (KAIZEN, Amaris Consulting, Sully Group, MasOrange, Talan, ENOVA France — au moins 8 offres actives mentionnent explicitement Databricks/Delta Lake/Lakehouse).

Ce projet complète [LyonFlow](https://github.com/PDUCLOS) (PostgreSQL/PostGIS, Airflow, MinIO, MLflow, Evidently AI, FastAPI/Streamlit) sur un dépôt séparé — il ne le remplace pas, il ajoute une vraie couche Databricks démontrable là où le marché recrute massivement.

## Ce que ça résout concrètement

- **Preuve vs affirmation** : plus besoin d'inventer des compétences en lettre de motivation faute de projet réel à montrer.
- **Substance pour le RNCP en cours** (examen 3 octobre 2026) — "en cours de certification Lead Data Science / AI Architect" plus crédible avec un projet concret en ligne.
- **Différenciant vs concurrence** : la plupart des candidats juniors/confirmés sur ces offres n'ont pas de portfolio Databricks vérifiable.

## Comment le valoriser une fois construit

1. **CV** — ligne factuelle sous LyonFlow : "Lakehouse Databricks (Delta Lake, DLT, Unity Catalog, MLflow, Model Serving) — pipeline Vélo'v/trafic Lyon en production, MAE modèle X."
2. **Lettres ciblées Databricks** — citer le projet avec lien GitHub direct.
3. **LinkedIn** — post court avec capture dashboard Genie ou endpoint Model Serving.
4. **Entretien** — réponse concrète à "parlez-moi d'un projet Databricks" : démo 5 minutes au lieu de zéro réponse crédible.

## Où on en est

| Semaine | Statut | Détail |
|---|---|---|
| **1 — Fondations** | ✅ Terminée | Unity Catalog `lyonflow` (bronze/silver/gold), ingestion Vélo'v (465 stations) + CRITER (2799→3.9K capteurs), pipeline DLT avec règles qualité `expect_or_drop` |
| **2 — Orchestration & qualité** | 🔜 Prête à démarrer | Voir [`semaine2_checklist.md`](semaine2_checklist.md) — checklist clic-par-clic, autonome |
| **3 — ML & mise en production** | ⏳ À venir | MLflow Tracking, Model Registry, Model Serving |
| **4 — BI & valorisation** | ⏳ À venir | Databricks SQL/Genie, finalisation portfolio |

Détail complet du plan : [`plan.md`](plan.md).

## Frictions déjà rencontrées et résolues (pour référence future)

- **GBFS `gbfs.json`** est un index de flux, pas les données stations — il faut `station_information.json` + `station_status.json`.
- **CRITER `pvotrafic`** (temps réel) demande une authentification non disponible en public → basculé sur `pvocomptagecriter` (stats de référence annuelle par capteur, accessible sans clé).
- **WFS typename** doit être qualifié avec le namespace (`metropole-de-lyon:...`) sinon GeoServer répond `401` au lieu d'une erreur explicite.
- **Colonnes 100% nulles** (ex. `estvalide`) font planter `createDataFrame` — les filtrer avant écriture plutôt que forcer un schéma.
- **DLT sans schema qualifié** publie tout dans un seul schema par défaut — qualifier chaque table `silver.xxx` / `gold.xxx` dans le nom pour respecter l'architecture Unity Catalog prévue.
- **Free Edition** a un quota serverless strict — ne jamais faire tourner deux ressources compute en parallèle (notebook + pipeline + requête SQL).

## Principe de collaboration

Repo séparé de LyonFlow — **jamais** de modification sur le projet ou le repo LyonFlow existant. Tout le travail Databricks vit ici : [github.com/PDUCLOS/databrickslyonflow](https://github.com/PDUCLOS/databrickslyonflow).
