# Databricks notebook source
# MAGIC %md
# MAGIC # DLT — Bronze → Silver
# MAGIC
# MAGIC Typage, dédoublonnage, exclusion des stations fermées/inactives et des
# MAGIC comptages aberrants. Règles de qualité en `expect_or_drop` (équivalent
# MAGIC Databricks de la validation Evidently AI déjà en place dans LyonFlow).

# COMMAND ----------

import dlt
from pyspark.sql import functions as F

# COMMAND ----------
# MAGIC %md ## Vélo'v — Silver

# COMMAND ----------

@dlt.table(
    name="velov_clean",
    comment="Snapshots Vélo'v typés, dédupliqués, stations actives uniquement.",
)
@dlt.expect_or_drop("valid_capacity", "capacity IS NOT NULL AND capacity >= 0")
@dlt.expect_or_drop("valid_bikes", "num_bikes_available >= 0 AND num_bikes_available <= capacity")
@dlt.expect_or_drop("station_active", "is_renting = true AND is_installed = true")
@dlt.expect_or_drop("valid_timestamp", "ingested_at IS NOT NULL")
def velov_clean():
    return (
        dlt.read_stream("lyonflow.bronze.velov_raw")
        .withColumn("station_id", F.col("station_id").cast("string"))
        .withColumn("num_bikes_available", F.col("num_bikes_available").cast("int"))
        .withColumn("num_docks_available", F.col("num_docks_available").cast("int"))
        .withColumn("capacity", F.col("capacity").cast("int"))
        .dropDuplicates(["station_id", "ingested_at"])
    )

# COMMAND ----------
# MAGIC %md ## CRITER — Silver

# COMMAND ----------

@dlt.table(
    name="criter_clean",
    comment="Comptages trafic CRITER typés, dédupliqués, valeurs aberrantes exclues.",
)
@dlt.expect_or_drop("valid_flow", "debit IS NULL OR debit >= 0")
@dlt.expect_or_drop("valid_speed", "vitesse IS NULL OR (vitesse >= 0 AND vitesse < 200)")
@dlt.expect_or_drop("valid_timestamp", "ingested_at IS NOT NULL")
def criter_clean():
    return (
        dlt.read_stream("lyonflow.bronze.criter_raw")
        .dropDuplicates(["identifiant_arc", "ingested_at"])
    )
