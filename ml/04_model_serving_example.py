"""
Exemple d'appel à l'endpoint Databricks Model Serving une fois déployé.

Usage :
    export DATABRICKS_HOST="https://<workspace>.cloud.databricks.com"
    export DATABRICKS_TOKEN="dapiXXXXXXXX"
    python ml/04_model_serving_example.py
"""

import os
import requests

DATABRICKS_HOST = os.environ["DATABRICKS_HOST"]
DATABRICKS_TOKEN = os.environ["DATABRICKS_TOKEN"]
ENDPOINT_NAME = "velov-availability-predictor"

url = f"{DATABRICKS_HOST}/serving-endpoints/{ENDPOINT_NAME}/invocations"
headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json",
}
payload = {
    "dataframe_records": [
        {"hour_of_day": 8, "day_of_week": 2, "capacity": 20, "avg_docks_available": 5},
    ]
}

response = requests.post(url, headers=headers, json=payload, timeout=30)
response.raise_for_status()
print(response.json())

# Équivalent curl :
#
# curl -X POST "$DATABRICKS_HOST/serving-endpoints/velov-availability-predictor/invocations" \
#   -H "Authorization: Bearer $DATABRICKS_TOKEN" \
#   -H "Content-Type: application/json" \
#   -d '{"dataframe_records": [{"hour_of_day": 8, "day_of_week": 2, "capacity": 20, "avg_docks_available": 5}]}'
