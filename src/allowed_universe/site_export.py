"""Export everything the website needs into site/public/.

    site/public/data/index.json          chart list, groups, titles
    site/public/data/charts/<name>.json  one chart: axes, sampled limit lines, objects, sources, explainer
    site/public/data/json/<dataset>.json raw datasets (copied from data/json)
    site/public/figures/<name>.png|pdf   static figures (copied from figures/)

The site never evaluates a formula: every line arrives as sampled points.
"""

from __future__ import annotations

import json
import math
import shutil

import numpy as np
import pandas as pd

from allowed_universe import charts, engine, loaders, style
from allowed_universe.charts._bars import BarSpec
from allowed_universe.datasets import DATASETS

ROOT = loaders.ROOT
PUBLIC = ROOT / "site" / "public"
EXPLAINERS = ROOT / "docs" / "explainers"

# matplotlib marker -> Observable Plot symbol
SYMBOLS = {"o": "circle", "^": "triangle", "D": "diamond", "s": "square", "h": "hexagon", "v": "star", "P": "cross"}


def _clean(v):
    if v is None:
        return None
    if isinstance(v, float | np.floating):
        return None if math.isnan(v) or math.isinf(v) else float(v)
    if isinstance(v, np.integer):
        return int(v)
    return v


def _records(df: pd.DataFrame, cols) -> list[dict]:
    out = []
    for rec in df[[c for c in cols if c in df.columns]].to_dict(orient="records"):
        out.append({k: _clean(v) for k, v in rec.items()})
    return out


def _categories(cats: dict) -> dict:
    out = {}
    for key, (label, slot) in cats.items():
        color, marker = style.SLOTS[slot]
        out[key] = {"label": label, "color": color, "symbol": SYMBOLS[marker]}
    return out


def _explainer(mod) -> str:
    name = getattr(mod, "EXPLAINER", mod.NAME)
    p = EXPLAINERS / f"{name}.md"
    if not p.exists():
        return ""
    lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if not ln.startswith("![")]
    return "\n".join(lines).strip() + "\n"


def _sources(mod) -> list[dict]:
    from allowed_universe import references

    return [{"url": u, "citation": c} for u, c in references._sources_for(mod).items()]


def _xy(mod) -> dict:
    spec: engine.ChartSpec = mod.spec()
    obj_cols = ["id", "name", "category", "x", "lo", "hi", "ex", "mx", "source_url", "citation", "notes"]
    lines = engine.sample_lines(spec, n=400)
    for line, src in zip(lines, spec.lines, strict=True):
        line["shade"] = src.shade
        line["forbidden_xy"] = list(src.forbidden_xy) if src.forbidden_xy else None
        if "points" in line:
            line["points"] = [[a, _clean(b)] for a, b in line["points"]]
    return {
        "kind": "xy",
        "xlabel": spec.xlabel,
        "ylabel": spec.ylabel,
        "xlim": list(spec.xlim),
        "ylim": list(spec.ylim),
        "xscale": spec.xscale,
        "yscale": spec.yscale,
        "footnote": spec.footnote,
        "categories": _categories(spec.categories),
        "lines": lines,
        "objects": _records(spec.objects, obj_cols),
        "tracks": [
            {
                "name": t.name,
                "category": t.category,
                "points": [[float(a), float(b)] for a, b in zip(t.x, t.y, strict=True)],
            }
            for t in spec.tracks
        ],
        "labels": {"range": spec.range_label, "max": spec.max_label, "cap": spec.cap_label},
    }


def _bars(mod) -> dict:
    spec: BarSpec = mod.bars()
    df = loaders.load(spec.dataset)
    cols = ["id", "name", "category", "value", "low", "high", "source_url", "citation", "notes"]
    return {
        "kind": "bars",
        "footnote": spec.footnote,
        "unit": "dB" if spec.value_fmt.__name__ == "fmt_db" else "",
        "categories": _categories(spec.categories),
        "panels": [
            {
                "key": p.key,
                "title": p.title,
                "xlabel": p.xlabel,
                "xlim": list(p.xlim),
                "xscale": p.xscale,
                "lines": [{"x": ln.x, "label": ln.label, "kind": ln.kind, "shade": ln.shade} for ln in p.lines],
                "rows": _records(df[df["panel"] == p.key], cols),
            }
            for p in spec.panels
        ],
    }


def _benchmarks(mod) -> dict:
    scores = loaders.load("ai_benchmarks")
    refs = loaders.load("ai_benchmark_refs")
    return {
        "kind": "benchmarks",
        "panels": [{"key": k, "title": t} for k, t in mod.PANELS],
        "xlim": list(mod.XLIM),
        "scores": _records(scores, list(scores.columns)),
        "refs": _records(refs, list(refs.columns)),
    }


def export() -> None:
    data_dir = PUBLIC / "data"
    (data_dir / "charts").mkdir(parents=True, exist_ok=True)
    index = {"groups": [], "charts": {}}
    for group, names in charts.CHART_GROUPS.items():
        index["groups"].append({"name": group, "charts": names})
        for name in names:
            mod = charts.load(name)
            if hasattr(mod, "spec"):
                body = _xy(mod)
                title = mod.spec().title
            elif hasattr(mod, "bars"):
                body = _bars(mod)
                title = mod.bars().title
            else:
                body = _benchmarks(mod)
                title = mod.TITLE
            doc = {
                "name": name,
                "title": title,
                "group": group,
                "datasets": list(mod.DATASETS),
                "explainer": _explainer(mod),
                "sources": _sources(mod),
                "png": f"figures/{name}.png",
                "pdf": f"figures/{name}.pdf",
                **body,
            }
            (data_dir / "charts" / f"{name}.json").write_text(
                json.dumps(doc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
            )
            index["charts"][name] = {"title": title, "group": group, "kind": body["kind"]}
    index["datasets"] = {n: DATASETS[n]["title"] for n in DATASETS}
    (data_dir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")

    # raw datasets and figures
    shutil.copytree(ROOT / "data" / "json", data_dir / "json", dirs_exist_ok=True)
    fig_dir = PUBLIC / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    for f in (ROOT / "figures").glob("*.*"):
        shutil.copy2(f, fig_dir / f.name)
