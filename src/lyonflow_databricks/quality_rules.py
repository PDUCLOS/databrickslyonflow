"""Pure-Python mirror of the DLT `expect_or_drop` rules defined in
`dlt_pipelines/bronze_to_silver.py`.

These run only inside a Databricks DLT pipeline (they need `dlt`/Spark), so
they can't be unit tested directly outside Databricks. This module re-expresses
the same predicates as plain functions on dict rows, so the *business logic*
can be tested locally and in CI without a Spark cluster.

If a rule changes here, the matching `@dlt.expect_or_drop` in
`dlt_pipelines/bronze_to_silver.py` must change too — names are kept identical
on purpose to make that link obvious.
"""

from typing import Any


def valid_capacity(row: dict[str, Any]) -> bool:
    return row.get("capacity") is not None and row["capacity"] >= 0


def valid_bikes(row: dict[str, Any]) -> bool:
    bikes = row.get("num_bikes_available")
    capacity = row.get("capacity")
    if bikes is None or capacity is None:
        return False
    return 0 <= bikes <= capacity


def station_active(row: dict[str, Any]) -> bool:
    return row.get("is_renting") is True and row.get("is_installed") is True


def valid_timestamp(row: dict[str, Any]) -> bool:
    return row.get("ingested_at") is not None


VELOV_RULES = {
    "valid_capacity": valid_capacity,
    "valid_bikes": valid_bikes,
    "station_active": station_active,
    "valid_timestamp": valid_timestamp,
}


def valid_sensor_id(row: dict[str, Any]) -> bool:
    return row.get("identifiantptm") is not None


def valid_flow(row: dict[str, Any]) -> bool:
    value = row.get("moyennejoursouvrable")
    return value is None or value >= 0


def valid_peak_flow(row: dict[str, Any]) -> bool:
    value = row.get("debithorairemax")
    return value is None or value >= 0


CRITER_RULES = {
    "valid_sensor_id": valid_sensor_id,
    "valid_flow": valid_flow,
    "valid_peak_flow": valid_peak_flow,
    "valid_timestamp": valid_timestamp,
}


def apply_rules(rows: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    """Mirrors expect_or_drop semantics: a row survives only if it passes
    every rule (AND), otherwise it's dropped — same as DLT's behavior."""
    return [row for row in rows if all(rule(row) for rule in rules.values())]


def has_unique_keys(rows: list[dict[str, Any]], key_fields: list[str]) -> bool:
    """Mirrors the dropDuplicates(key_fields) primary-key uniqueness check
    used in dlt_pipelines/bronze_to_silver.py for both velov_clean and
    criter_clean."""
    keys = [tuple(row.get(f) for f in key_fields) for row in rows]
    return len(keys) == len(set(keys))
