# Databricks notebook source
# MAGIC %md
# MAGIC # Ingestion Bronze — Comptage CRITER (Grand Lyon)
# MAGIC
# MAGIC Couche WFS `pvo_patrimoine_voirie.pvocomptagecriter` : position des ~2800
# MAGIC capteurs de comptage trafic/vélo (boucles inductives Criter) avec leurs
# MAGIC statistiques de référence (moyenne jour ouvrable, débit horaire max) pour
# MAGIC l'année de référence `anneereference`.
# MAGIC
# MAGIC Note : ce n'est **pas** un flux temps réel minute par minute — les
# MAGIC statistiques sont mises à jour périodiquement (annuellement). L'autre
# MAGIC couche candidate, `pvo_patrimoine_voirie.pvotrafic` (état trafic temps
# MAGIC réel), nécessite une authentification non disponible en accès public
# MAGIC (`401 - Informations d'authentification non fournies`) — voir
# MAGIC `docs/data_sources.md`.
# MAGIC
# MAGIC Écrit un snapshot horodaté, append-only, dans `lyonflow.bronze.criter_raw`.

# COMMAND ----------

import requests
from datetime import datetime, timezone
from pyspark.sql import functions as F

WFS_BASE = "https://data.grandlyon.com/fr/geoserv/metropole-de-lyon/ows/"
WFS_TYPENAME = "metropole-de-lyon:pvo_patrimoine_voirie.pvocomptagecriter"

CATALOG = "lyonflow"
SCHEMA = "bronze"
TABLE = "criter_raw"

dbutils.widgets.text("catalog", CATALOG, "Unity Catalog")
catalog = dbutils.widgets.get("catalog")

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{SCHEMA}")

# COMMAND ----------

params = {
    "SERVICE": "WFS",
    "VERSION": "2.0.0",
    "request": "GetFeature",
    "typename": WFS_TYPENAME,
    "outputFormat": "application/json",
    "SRSNAME": "EPSG:4326",
}

response = requests.get(WFS_BASE, params=params, timeout=60)
response.raise_for_status()
payload = response.json()

features = payload["features"]
ingested_at = datetime.now(timezone.utc)

records = [
    {**f.get("properties", {}), "geometry": str(f.get("geometry"))}
    for f in features
]

# COMMAND ----------

# Certains champs (ex. estvalide) sont None sur l'ensemble des capteurs pour
# ce batch — Spark ne peut pas inférer le type d'une colonne 100% nulle lors
# du createDataFrame (CANNOT_DETERMINE_TYPE). On les retire avant construction
# du DataFrame plutôt que de forcer un schéma explicite, pour rester robuste
# si un futur batch a la colonne partiellement remplie.
none_cols = {k for k in records[0] if all(r.get(k) is None for r in records)}
records = [{k: v for k, v in r.items() if k not in none_cols} for r in records]

df = spark.createDataFrame(records)
df = df.withColumn("ingested_at", F.lit(ingested_at).cast("timestamp")) \
       .withColumn("ingestion_date", F.to_date(F.lit(ingested_at)))

(
    df.write
      .format("delta")
      .mode("append")
      .option("mergeSchema", "true")
      .saveAsTable(f"{catalog}.{SCHEMA}.{TABLE}")
)

print(f"{df.count()} capteurs CRITER ingérés dans {catalog}.{SCHEMA}.{TABLE} à {ingested_at.isoformat()}")

# COMMAND ----------

display(spark.table(f"{catalog}.{SCHEMA}.{TABLE}").orderBy(F.desc("ingested_at")).limit(20))
