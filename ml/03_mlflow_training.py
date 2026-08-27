# Databricks notebook source
# MAGIC %md
# MAGIC # MLflow — Entraînement modèle de prédiction disponibilité Vélo'v
# MAGIC
# MAGIC Réutilise la logique de features déjà validée dans LyonFlow (XGBoost sur
# MAGIC séries temporelles), réécrite ici indépendamment sur les tables Gold
# MAGIC Databricks. Tracking MLflow (paramètres, métriques) + enregistrement du
# MAGIC meilleur modèle dans le Model Registry Unity Catalog.

# COMMAND ----------

import mlflow
import mlflow.xgboost
import xgboost as xgb
from pyspark.sql import functions as F
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

CATALOG = "lyonflow"
MODEL_NAME = f"{CATALOG}.gold.velov_availability_predictor"

mlflow.set_registry_uri("databricks-uc")

# COMMAND ----------

df = (
    spark.table(f"{CATALOG}.gold.velov_hourly_agg")
    .withColumn("hour_of_day", F.hour("hour"))
    .withColumn("day_of_week", F.dayofweek("hour"))
    .withColumn("occupancy_ratio", F.col("avg_bikes_available") / F.col("capacity"))
    .dropna()
    .toPandas()
)

feature_cols = ["hour_of_day", "day_of_week", "capacity", "avg_docks_available"]
target_col = "avg_bikes_available"

X_train, X_test, y_train, y_test = train_test_split(
    df[feature_cols], df[target_col], test_size=0.2, random_state=42
)

# COMMAND ----------

with mlflow.start_run(run_name="velov_xgboost_baseline") as run:
    params = {
        "n_estimators": 200,
        "max_depth": 6,
        "learning_rate": 0.05,
        "objective": "reg:squarederror",
        "random_state": 42,
    }
    mlflow.log_params(params)

    model = xgb.XGBRegressor(**params)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = mean_squared_error(y_test, preds, squared=False)

    mlflow.log_metrics({"mae": mae, "rmse": rmse})
    mlflow.xgboost.log_model(
        model,
        artifact_path="model",
        registered_model_name=MODEL_NAME,
    )

    print(f"Run {run.info.run_id} — MAE={mae:.3f} RMSE={rmse:.3f}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Étape suivante — Model Serving
# MAGIC
# MAGIC 1. Databricks UI → Model Registry → `velov_availability_predictor` → *Serve this model*.
# MAGIC 2. Attendre le déploiement de l'endpoint (`Ready`).
# MAGIC 3. Tester avec `ml/04_model_serving_example.py` ou l'exemple curl du README.
