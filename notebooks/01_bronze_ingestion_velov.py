# Databricks notebook source
# MAGIC %md
# MAGIC # Ingestion Bronze — Vélo'v Lyon (GBFS)
# MAGIC
# MAGIC Appelle le flux GBFS temps réel de la Métropole de Lyon et écrit un snapshot
# MAGIC horodaté, append-only, dans `lyonflow.bronze.velov_raw`.
# MAGIC
# MAGIC Source : https://download.data.grandlyon.com/files/rdata/jcd_jcdecaux.jcdvelov/gbfs.json
# MAGIC Licence Ouverte 2.0 — aucune clé API requise.

# COMMAND ----------

import requests
from datetime import datetime, timezone
from pyspark.sql import functions as F

GBFS_URL = "https://download.data.grandlyon.com/files/rdata/jcd_jcdecaux.jcdvelov/gbfs.json"
CATALOG = "lyonflow"
SCHEMA = "bronze"
TABLE = "velov_raw"

dbutils.widgets.text("catalog", CATALOG, "Unity Catalog")
catalog = dbutils.widgets.get("catalog")

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{SCHEMA}")

# COMMAND ----------

response = requests.get(GBFS_URL, timeout=30)
response.raise_for_status()
payload = response.json()

stations = payload["data"]["stations"] if "data" in payload else payload["stations"]
ingested_at = datetime.now(timezone.utc)

# COMMAND ----------

df = spark.createDataFrame(stations)
df = df.withColumn("ingested_at", F.lit(ingested_at).cast("timestamp")) \
       .withColumn("ingestion_date", F.to_date(F.lit(ingested_at)))

(
    df.write
      .format("delta")
      .mode("append")
      .option("mergeSchema", "true")
      .saveAsTable(f"{catalog}.{SCHEMA}.{TABLE}")
)

print(f"{df.count()} stations Vélo'v ingérées dans {catalog}.{SCHEMA}.{TABLE} à {ingested_at.isoformat()}")

# COMMAND ----------

display(spark.table(f"{catalog}.{SCHEMA}.{TABLE}").orderBy(F.desc("ingested_at")).limit(20))
