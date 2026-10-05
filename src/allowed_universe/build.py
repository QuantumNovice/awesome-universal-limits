"""Regenerate everything from the data: schemas, JSON exports, limits.json, figures, references.

python -m allowed_universe.build            # everything
python -m allowed_universe.build spin mass  # only these charts
python -m allowed_universe.build --schemas  # only rewrite data/schema/*.json
"""

from __future__ import annotations

import argparse
import json
import sys

from allowed_universe import charts, engine, loaders, references, site_export
from allowed_universe.datasets import DATASETS

ROOT = loaders.ROOT
SITE_LIMITS = ROOT / "site" / "public" / "limits.json"


def render_chart(mod):
    if hasattr(mod, "spec"):
        spec = mod.spec()
        bad = engine.violations(spec)
        if bad:
            raise SystemExit(f"{mod.NAME}: objects cross a hard bound: {bad}")
        return engine.render(spec)
    return mod.render()  # bar charts and custom layouts


def export_limits(mods) -> None:
    out = {"generated_by": "allowed_universe.build", "charts": {}}
    for mod in mods:
        if not hasattr(mod, "spec"):
            continue
        spec = mod.spec()
        out["charts"][mod.NAME] = {
            "title": spec.title,
            "xlabel": spec.xlabel,
            "ylabel": spec.ylabel,
            "xlim": list(spec.xlim),
            "ylim": list(spec.ylim),
            "xscale": spec.xscale,
            "yscale": spec.yscale,
            "lines": engine.sample_lines(spec),
        }
    SITE_LIMITS.parent.mkdir(parents=True, exist_ok=True)
    SITE_LIMITS.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")


def chart_title(mod) -> str:
    if hasattr(mod, "spec"):
        return mod.spec().title
    if hasattr(mod, "bars"):
        return mod.bars().title
    return mod.TITLE


def write_readme_gallery(mods) -> None:
    """Regenerate the gallery between the markers in README.md."""
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    start, end = "<!-- gallery:start -->", "<!-- gallery:end -->"
    if start not in text or end not in text:
        return
    by_name = {m.NAME: m for m in mods}
    out = [start, ""]
    for group, names in charts.CHART_GROUPS.items():
        out.append(f"**{group}**")
        out.append("")
        out.append("| | | |")
        out.append("|:-:|:-:|:-:|")
        cells = []
        for n in names:
            mod = by_name[n]
            explainer = getattr(mod, "EXPLAINER", n)
            cells.append(
                f"[![{n}](figures/{n}.png)](docs/explainers/{explainer}.md)<br>[{chart_title(mod)}](docs/explainers/{explainer}.md)"
            )
        while len(cells) % 3:
            cells.append(" ")
        for i in range(0, len(cells), 3):
            out.append("| " + " | ".join(cells[i : i + 3]) + " |")
        out.append("")
    out.append(end)
    head, rest = text.split(start, 1)
    _, tail = rest.split(end, 1)
    readme.write_text(head + "\n".join(out) + tail, encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("charts", nargs="*", help="chart names (default: all)")
    ap.add_argument("--schemas", action="store_true", help="only regenerate JSON schemas")
    args = ap.parse_args(argv)

    loaders.write_schemas()
    if args.schemas:
        return 0
    for name in DATASETS:
        loaders.export_json(name)

    mods = charts.all_charts()
    export_limits(mods)
    selected = [m for m in mods if not args.charts or m.NAME in args.charts]
    for mod in selected:
        fig = render_chart(mod)
        engine.save(fig, mod.NAME)
        print(f"figures/{mod.NAME}.png, .pdf")
    references.write()
    print("docs/REFERENCES.md, docs/references.bib")
    write_readme_gallery(mods)
    site_export.export()
    print("site/public/data, site/public/figures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
