from datetime import datetime, timezone

from lyonflow_databricks.quality_rules import (
    CRITER_RULES,
    VELOV_RULES,
    apply_rules,
    has_unique_keys,
    station_active,
    valid_bikes,
    valid_capacity,
    valid_flow,
    valid_peak_flow,
    valid_sensor_id,
    valid_timestamp,
)

NOW = datetime.now(timezone.utc)


def make_velov_row(**overrides):
    row = {
        "station_id": "1024",
        "capacity": 20,
        "num_bikes_available": 5,
        "is_renting": True,
        "is_installed": True,
        "ingested_at": NOW,
    }
    row.update(overrides)
    return row


def make_criter_row(**overrides):
    row = {
        "identifiantptm": 1789,
        "moyennejoursouvrable": 563,
        "debithorairemax": 103,
        "ingested_at": NOW,
    }
    row.update(overrides)
    return row


class TestVelovRules:
    def test_valid_capacity_accepts_non_negative(self):
        assert valid_capacity(make_velov_row(capacity=0)) is True

    def test_valid_capacity_rejects_none(self):
        assert valid_capacity(make_velov_row(capacity=None)) is False

    def test_valid_capacity_rejects_negative(self):
        assert valid_capacity(make_velov_row(capacity=-1)) is False

    def test_valid_bikes_within_capacity(self):
        assert valid_bikes(make_velov_row(num_bikes_available=5, capacity=20)) is True

    def test_valid_bikes_rejects_over_capacity(self):
        assert valid_bikes(make_velov_row(num_bikes_available=25, capacity=20)) is False

    def test_valid_bikes_rejects_negative(self):
        assert valid_bikes(make_velov_row(num_bikes_available=-1, capacity=20)) is False

    def test_station_active_requires_both_flags(self):
        assert station_active(make_velov_row(is_renting=True, is_installed=False)) is False
        assert station_active(make_velov_row(is_renting=True, is_installed=True)) is True

    def test_valid_timestamp_rejects_none(self):
        assert valid_timestamp(make_velov_row(ingested_at=None)) is False

    def test_apply_rules_drops_closed_station(self):
        rows = [
            make_velov_row(station_id="1"),
            make_velov_row(station_id="2", is_renting=False),
        ]
        kept = apply_rules(rows, VELOV_RULES)
        assert [r["station_id"] for r in kept] == ["1"]

    def test_unique_keys_detects_duplicate_snapshot(self):
        rows = [make_velov_row(), make_velov_row()]
        assert has_unique_keys(rows, ["station_id", "ingested_at"]) is False

    def test_unique_keys_true_for_distinct_stations(self):
        rows = [make_velov_row(station_id="1"), make_velov_row(station_id="2")]
        assert has_unique_keys(rows, ["station_id", "ingested_at"]) is True


class TestCriterRules:
    def test_valid_sensor_id_rejects_none(self):
        assert valid_sensor_id(make_criter_row(identifiantptm=None)) is False

    def test_valid_flow_allows_null(self):
        assert valid_flow(make_criter_row(moyennejoursouvrable=None)) is True

    def test_valid_flow_rejects_negative(self):
        assert valid_flow(make_criter_row(moyennejoursouvrable=-5)) is False

    def test_valid_peak_flow_rejects_negative(self):
        assert valid_peak_flow(make_criter_row(debithorairemax=-1)) is False

    def test_apply_rules_drops_sensor_without_id(self):
        rows = [
            make_criter_row(identifiantptm=1789),
            make_criter_row(identifiantptm=None),
        ]
        kept = apply_rules(rows, CRITER_RULES)
        assert len(kept) == 1
        assert kept[0]["identifiantptm"] == 1789

    def test_unique_keys_detects_duplicate_sensor_snapshot(self):
        rows = [make_criter_row(), make_criter_row()]
        assert has_unique_keys(rows, ["identifiantptm", "ingested_at"]) is False
