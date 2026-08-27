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
# MAGIC %md ## CRITER — Gold : dernier snapshot par capteur
# MAGIC
# MAGIC Les statistiques CRITER sont des références annuelles (`anneereference`),
# MAGIC pas un flux temps réel — le Gold retient donc le dernier snapshot ingéré
# MAGIC par capteur plutôt qu'une agrégation horaire.

# COMMAND ----------

@dlt.table(
    name="criter_site_stats",
    comment="Dernier snapshot de statistiques de référence par capteur CRITER.",
)
def criter_site_stats():
    from pyspark.sql.window import Window

    w = Window.partitionBy("identifiantptm").orderBy(F.desc("ingested_at"))
    return (
        dlt.read("criter_clean")
        .withColumn("rn", F.row_number().over(w))
        .filter("rn = 1")
        .drop("rn")
        .select(
            "identifiantptm", "nom", "positionnement", "typecapteur",
            "nbvoies", "moyennejoursouvrable", "debithorairemax",
            "horairedebitmax", "anneereference", "lon", "lat", "ingested_at",
        )
    )
