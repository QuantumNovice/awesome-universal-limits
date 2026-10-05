"""Every data file: schema-valid, SI units, a source on every row, schemas up to date."""

import json

import pandas as pd
import pytest

from allowed_universe import loaders
from allowed_universe.datasets import DATASETS, schema_for

NAMES = sorted(DATASETS)


@pytest.mark.parametrize("name", NAMES)
def test_schema_file_is_current(name):
    on_disk = json.loads(loaders.schema_path(name).read_text(encoding="utf-8"))
    assert on_disk == schema_for(name), "run: python -m allowed_universe.build --schemas"


@pytest.mark.parametrize("name", NAMES)
def test_loads_and_validates(name):
    df = loaders.load(name)
    assert len(df) > 0


@pytest.mark.parametrize("name", NAMES)
def test_every_row_has_a_source(name):
    df = loaders.load(name)
    assert df["source_url"].str.startswith("https://").all()
    assert (df["citation"].str.len() > 10).all()


@pytest.mark.parametrize("name", NAMES)
def test_no_wikipedia_as_source(name):
    df = loaders.load(name)
    assert not df["source_url"].str.contains("wikipedia.org").any()


@pytest.mark.parametrize("name", NAMES)
def test_missing_values_are_empty_not_zero(name):
    df = loaders.load(name)
    for col, (typ, _) in DATASETS[name]["columns"].items():
        if typ == "pos":
            assert not (df[col] == 0).any(), col


RANGE_SETS = {
    "spin": ("slowest_hz", "fastest_hz", "example_hz", "max_hz"),
    "mass": ("mass_low_kg", "mass_high_kg", "mass_example_kg", "mass_max_kg"),
    "speed": ("speed_low_m_s", "speed_high_m_s", "speed_example_m_s", "speed_max_m_s"),
    "temperature": ("temperature_low_k", "temperature_high_k", "temperature_example_k", "temperature_max_k"),
    "density": ("density_low_kg_m3", "density_high_kg_m3", "density_example_kg_m3", "density_max_kg_m3"),
    "acceleration": ("accel_low_m_s2", "accel_high_m_s2", "accel_example_m_s2", "accel_max_m_s2"),
    "lifetime": ("lifetime_low_s", "lifetime_high_s", "lifetime_example_s", "lifetime_max_s"),
    "biology": ("mass_low_kg", "mass_high_kg", "mass_example_kg", "mass_max_kg"),
    "chemistry": ("energy_low_j", "energy_high_j", "energy_example_j", "energy_max_j"),
    "materials": ("strength_low_pa", "strength_high_pa", "strength_example_pa", "strength_max_pa"),
    "power": ("power_low_w", "power_high_w", "power_example_w", "power_max_w"),
    "radio": ("power_low_w", "power_high_w", "power_example_w", "power_max_w"),
    "black_holes": ("spin_low_a", "spin_high_a", "spin_example_a", "spin_max_a"),
    "flow": ("flow_low_m3_s", "flow_high_m3_s", "flow_example_m3_s", "flow_max_m3_s"),
    "oscillation": ("freq_low_hz", "freq_high_hz", "freq_example_hz", "freq_max_hz"),
    "charge": ("charge_low_c", "charge_high_c", "charge_example_c", "charge_max_c"),
    "voltage": ("voltage_low_v", "voltage_high_v", "voltage_example_v", "voltage_max_v"),
    "magnetic": ("field_low_t", "field_high_t", "field_example_t", "field_max_t"),
    "pressure": ("pressure_low_pa", "pressure_high_pa", "pressure_example_pa", "pressure_max_pa"),
    "epidemics": ("r0_low_x", "r0_high_x", "r0_example_x", "r0_max_x"),
    "structures": ("mass_low_kg", "mass_high_kg", "mass_example_kg", "mass_max_kg"),
    "volumes": ("mass_low_kg", "mass_high_kg", "mass_example_kg", "mass_max_kg"),
}


BAR_SETS = ["cognition", "energy_density", "numbers", "luminous", "sound"]


@pytest.mark.parametrize("name", BAR_SETS)
def test_bar_ranges_contain_value(name):
    df = loaders.load(name)
    for _, r in df.iterrows():
        if pd.notna(r["low"]) and pd.notna(r["high"]):
            assert r["low"] <= r["value"] <= r["high"], r["id"]


def test_black_hole_spins_below_one():
    df = loaders.load("black_holes")
    for col in ("spin_low_a", "spin_high_a", "spin_example_a"):
        assert (df[col].dropna() < 1).all()


def test_every_dataset_is_used_by_a_chart():
    from allowed_universe import charts

    used = {ds for m in charts.all_charts() for ds in m.DATASETS}
    assert used == set(DATASETS)


@pytest.mark.parametrize("name", sorted(RANGE_SETS))
def test_ranges_are_ordered(name):
    lo, hi, ex, mx = RANGE_SETS[name]
    df = loaders.load(name)
    for _, r in df.iterrows():
        if pd.notna(r[lo]) and pd.notna(r[hi]):
            assert r[lo] <= r[hi], r["id"]
        if pd.notna(r[ex]) and pd.notna(r[lo]) and pd.notna(r[hi]):
            assert r[lo] <= r[ex] <= r[hi], r["id"]
        top = r[hi] if pd.notna(r[hi]) else r[ex]
        if pd.notna(r[mx]) and pd.notna(top):
            assert r[mx] >= top, r["id"]
        if pd.notna(r[mx]):
            assert pd.notna(r["max_basis"]), f"{r['id']}: a maximum needs a max_basis"


def test_benchmark_scores_are_percentages():
    df = loaders.load("ai_benchmarks")
    assert df["score_pct"].between(0, 100).all()


def test_moe_active_below_total():
    df = loaders.load("ai_models")
    moe = df[df["params_active"].notna()]
    assert (moe["params_active"] < moe["params_total"]).all()


def test_derived_flop_matches_6nd():
    df = loaders.load("ai_models")
    for _, r in df[df["flop_basis"] == "6ND"].iterrows():
        n = r["params_active"] if pd.notna(r["params_active"]) else r["params_total"]
        assert r["training_flop"] == pytest.approx(6 * n * r["training_tokens"], rel=0.02), r["id"]


def test_bad_row_is_rejected():
    df = loaders.load("spin")
    df.loc[0, "size_m"] = -1.0
    with pytest.raises(loaders.DataError):
        loaders.validate("spin", df)
