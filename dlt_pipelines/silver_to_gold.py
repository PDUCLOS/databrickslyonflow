# Databricks notebook source
# MAGIC %md
# MAGIC # DLT — Silver → Gold
# MAGIC
# MAGIC Agrégations horaires prêtes pour le dashboard Databricks SQL / Genie et
# MAGIC pour l'entraînement du modèle MLflow.

# COMMAND ----------

import dlt
from pyspark.sql import functions as F

# COMMAND ----------
# MAGIC %md ## Vélo'v — Gold : disponibilité moyenne par station / heure

# COMMAND ----------

@dlt.table(
    name="velov_hourly_agg",
    comment="Disponibilité moyenne Vélo'v par station et par heure.",
)
def velov_hourly_agg():
    return (
        dlt.read("velov_clean")
        .withColumn("hour", F.date_trunc("hour", "ingested_at"))
        .groupBy("station_id", "name", "hour")
        .agg(
            F.avg("num_bikes_available").alias("avg_bikes_available"),
            F.avg("num_docks_available").alias("avg_docks_available"),
            F.first("capacity").alias("capacity"),
            F.count("*").alias("nb_observations"),
        )
    )

# COMMAND ----------
# MAGIC %md ## CRITER — Gold : trafic moyen par boucle / heure

# COMMAND ----------

@dlt.table(
    name="criter_hourly_agg",
    comment="Débit et vitesse moyens par boucle de comptage et par heure.",
)
def criter_hourly_agg():
    return (
        dlt.read("criter_clean")
        .withColumn("hour", F.date_trunc("hour", "ingested_at"))
        .groupBy("identifiant_arc", "hour")
        .agg(
            F.avg("debit").alias("avg_debit"),
            F.avg("vitesse").alias("avg_vitesse"),
            F.count("*").alias("nb_observations"),
        )
    )
