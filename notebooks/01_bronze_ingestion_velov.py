# Databricks notebook source
# MAGIC %md
# MAGIC # Ingestion Bronze — Vélo'v Lyon (GBFS)
# MAGIC
# MAGIC Le flux racine `gbfs.json` est un index GBFS (auto-discovery) qui liste les
# MAGIC sous-flux — il ne contient pas les stations directement. On interroge donc
# MAGIC les deux sous-flux nécessaires et on les fusionne par `station_id` :
# MAGIC - `station_information.json` (statique : nom, capacité, lat/lon)
# MAGIC - `station_status.json` (dynamique : vélos/docks disponibles, état)
# MAGIC
# MAGIC Écrit un snapshot horodaté, append-only, dans `lyonflow.bronze.velov_raw`.
# MAGIC Licence Ouverte 2.0 — aucune clé API requise.

# COMMAND ----------

import requests
from datetime import datetime, timezone
from pyspark.sql import functions as F

BASE_URL = "https://download.data.grandlyon.com/files/rdata/jcd_jcdecaux.jcdvelov"
STATION_INFO_URL = f"{BASE_URL}/station_information.json"
STATION_STATUS_URL = f"{BASE_URL}/station_status.json"

CATALOG = "lyonflow"
SCHEMA = "bronze"
TABLE = "velov_raw"

dbutils.widgets.text("catalog", CATALOG, "Unity Catalog")
catalog = dbutils.widgets.get("catalog")

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{SCHEMA}")

# COMMAND ----------

info_resp = requests.get(STATION_INFO_URL, timeout=30)
info_resp.raise_for_status()
status_resp = requests.get(STATION_STATUS_URL, timeout=30)
status_resp.raise_for_status()

station_info = {s["station_id"]: s for s in info_resp.json()["data"]["stations"]}
station_status = status_resp.json()["data"]["stations"]
ingested_at = datetime.now(timezone.utc)

# COMMAND ----------

records = []
for status in station_status:
    info = station_info.get(status["station_id"], {})
    records.append({
        "station_id": status["station_id"],
        "name": info.get("name"),
        "lat": info.get("lat"),
        "lon": info.get("lon"),
        "capacity": info.get("capacity"),
        "num_bikes_available": status.get("num_bikes_available"),
        "num_docks_available": status.get("num_docks_available"),
        "is_installed": bool(status.get("is_installed")),
        "is_renting": bool(status.get("is_renting")),
        "is_returning": bool(status.get("is_returning")),
        "last_reported": status.get("last_reported"),
    })

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

print(f"{df.count()} stations Vélo'v ingérées dans {catalog}.{SCHEMA}.{TABLE} à {ingested_at.isoformat()}")

# COMMAND ----------

display(spark.table(f"{catalog}.{SCHEMA}.{TABLE}").orderBy(F.desc("ingested_at")).limit(20))
