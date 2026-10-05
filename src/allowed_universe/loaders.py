"""Read and validate the CSV data files."""

from __future__ import annotations

import json
import math
from functools import cache
from pathlib import Path

import jsonschema
import pandas as pd

from allowed_universe.datasets import DATASETS, schema_for

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
SCHEMA_DIR = DATA / "schema"


class DataError(ValueError):
    pass


def schema_path(name: str) -> Path:
    return SCHEMA_DIR / f"{name}.schema.json"


def write_schemas() -> list[Path]:
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    out = []
    for name in DATASETS:
        p = schema_path(name)
        p.write_text(json.dumps(schema_for(name), indent=2) + "\n", encoding="utf-8")
        out.append(p)
    return out


def _records(df: pd.DataFrame) -> list[dict]:
    rows = []
    for rec in df.to_dict(orient="records"):
        rows.append({k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in rec.items()})
    return rows


def validate(name: str, df: pd.DataFrame) -> None:
    """Raise DataError listing every invalid row."""
    expected = list(DATASETS[name]["columns"])
    if list(df.columns) != expected:
        raise DataError(f"{name}.csv columns {list(df.columns)} != {expected}")
    schema = json.loads(schema_path(name).read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    errors = []
    for i, rec in enumerate(_records(df), start=2):  # line 1 is the header
        for err in validator.iter_errors(rec):
            errors.append(f"{name}.csv line {i} ({rec.get('id')}): {err.message}")
    if df["id"].duplicated().any():
        errors.append(f"{name}.csv duplicate ids: {df['id'][df['id'].duplicated()].tolist()}")
    if errors:
        raise DataError("\n".join(errors))


@cache
def _load_cached(name: str) -> pd.DataFrame:
    path = DATA / f"{name}.csv"
    df = pd.read_csv(path, keep_default_na=False, na_values=[""], comment=None, dtype=str)
    for col, (typ, _) in DATASETS[name]["columns"].items():
        if typ in ("pos", "num", "year"):
            df[col] = pd.to_numeric(df[col], errors="raise")
        else:
            df[col] = df[col].where(df[col].notna(), None)
    validate(name, df)
    return df


def load(name: str) -> pd.DataFrame:
    """Load and validate data/<name>.csv. Returns a copy."""
    return _load_cached(name).copy()


def export_json(name: str, out_dir: Path = DATA / "json") -> Path:
    """Write data/json/<name>.json: metadata, column units and rows."""
    out_dir.mkdir(parents=True, exist_ok=True)
    df = load(name)
    ds = DATASETS[name]
    doc = {
        "dataset": name,
        "title": ds["title"],
        "license": "CC-BY-4.0",
        "columns": {c: d for c, (_, d) in ds["columns"].items()},
        "rows": _records(df),
    }
    p = out_dir / f"{name}.json"
    p.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return p


def to_objects(df: pd.DataFrame, x: str, lo: str, hi: str, ex: str, mx: str | None) -> pd.DataFrame:
    """Rename a dataset's columns to the engine's generic x/lo/hi/ex/mx."""
    cols = {x: "x", lo: "lo", hi: "hi", ex: "ex"}
    if mx:
        cols[mx] = "mx"
    out = df.rename(columns=cols)
    if "mx" not in out:
        out["mx"] = float("nan")
    return out
