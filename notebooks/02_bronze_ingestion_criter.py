# Databricks notebook source
# MAGIC %md
# MAGIC # Ingestion Bronze — État du trafic / CRITER (Grand Lyon)
# MAGIC
# MAGIC Même famille de flux open data que celle déjà utilisée dans LyonFlow —
# MAGIC ingérée ici indépendamment, sans réutiliser le code du projet LyonFlow.
# MAGIC
# MAGIC Câblé par défaut sur le flux **État du trafic temps réel**
# MAGIC (`pvo_patrimoine_voirie.pvotrafic`) — voir `docs/data_sources.md` pour le
# MAGIC détail des deux jeux de données CRITER disponibles et vérifier lequel
# MAGIC correspond à l'intégration déjà en place dans LyonFlow avant le premier run.

# COMMAND ----------

import requests
from datetime import datetime, timezone
from pyspark.sql import functions as F

CATALOG = "lyonflow"
SCHEMA = "bronze"
TABLE = "criter_raw"
WFS_BASE = "https://data.grandlyon.com/fr/geoserv/metropole-de-lyon/ows/"

dbutils.widgets.text("catalog", CATALOG, "Unity Catalog")
dbutils.widgets.text("wfs_typename", "pvo_patrimoine_voirie.pvotrafic", "Nom de couche WFS trafic")
catalog = dbutils.widgets.get("catalog")
wfs_typename = dbutils.widgets.get("wfs_typename")

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{SCHEMA}")

# COMMAND ----------

params = {
    "SERVICE": "WFS",
    "VERSION": "2.0.0",
    "request": "GetFeature",
    "typename": wfs_typename,
    "outputFormat": "application/json",
    "SRSNAME": "EPSG:4326",
}

response = requests.get(WFS_BASE, params=params, timeout=30)
response.raise_for_status()
payload = response.json()

features = payload["features"]
ingested_at = datetime.now(timezone.utc)

records = [
    {**f.get("properties", {}), "geometry": str(f.get("geometry"))}
    for f in features
]

# COMMAND ----------

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

print(f"{df.count()} comptages CRITER ingérés dans {catalog}.{SCHEMA}.{TABLE} à {ingested_at.isoformat()}")
