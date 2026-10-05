"""Registry of every data file: columns, types and units.

The JSON Schemas in ``data/schema/`` are generated from this registry
(``python -m allowed_universe.build --schemas``) and checked in CI.
"""

from __future__ import annotations

# column -> (type, description). Types:
#   slug  : lowercase id      text : free text      url : https link
#   pos   : positive float, may be empty           num : any float, may be empty
#   year  : decimal year                           enum:<a|b|c> : one of the values

_COMMON_TAIL = {
    "source_url": ("url", "Primary source for the values (journal DOI, agency fact sheet, spec sheet)."),
    "citation": ("text", "Short citation: authors, year, title, venue."),
    "notes": ("opt", "One line shown in the hover tooltip."),
}


def _range_cols(q: str, unit: str, what: str, max_basis: str):
    return {
        f"{q}_low_{unit}": ("pos", f"Lowest known {what} of the class."),
        f"{q}_high_{unit}": ("pos", f"Highest known {what} of the class."),
        f"{q}_example_{unit}": ("pos", f"{what.capitalize()} of the marked example object."),
        f"{q}_max_{unit}": ("pos", f"Maximum allowable {what}; empty if none."),
        "max_basis": (f"enum:{max_basis}", "Physics behind the maximum."),
    }


_PHYS_CATS = "enum:particle|molecular|living|human|astro|lab"

DATASETS: dict[str, dict] = {
    "spin": {
        "title": "Spin rate vs size",
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label shown on the plot."),
            "category": ("enum:molecular|living|human|astro|orbit", "Object class."),
            "size_m": ("pos", "Diameter in metres."),
            "slowest_hz": ("pos", "Slowest known member of the class, Hz."),
            "fastest_hz": ("pos", "Fastest known member, Hz."),
            "example_hz": ("pos", "Value of the marked example object, Hz."),
            "max_hz": ("pos", "Maximum allowable spin (breakup), Hz; empty if none."),
            "max_basis": (
                "enum:material|gravity|black-hole|quantum|centrifugal-dissociation",
                "Physics behind max_hz.",
            ),
            **_COMMON_TAIL,
        },
    },
    "spin_orbits": {
        "title": "Orbit tracks for the spin chart",
        "columns": {
            "id": ("slug", "Unique id."),
            "track": ("slug", "Points with the same track are joined by a curve."),
            "name": ("text", "Label."),
            "mass_kg": ("pos", "Central (or total) mass, kg."),
            "size_m": ("pos", "Orbit diameter 2a, m."),
            "freq_hz": ("pos", "Orbital frequency, Hz."),
            **_COMMON_TAIL,
        },
    },
    "mass": {
        "title": "Mass vs size",
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "category": (_PHYS_CATS, "Object class."),
            "size_m": ("pos", "Diameter, m."),
            **_range_cols("mass", "kg", "mass", "black-hole|nuclear-density|chandrasekhar|tov|none"),
            **_COMMON_TAIL,
        },
    },
    "speed": {
        "title": "Speed vs size",
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "category": (_PHYS_CATS, "Object class."),
            "size_m": ("pos", "Size (length or diameter), m."),
            **_range_cols("speed", "m_s", "speed", "light|escape|material|none"),
            **_COMMON_TAIL,
        },
    },
    "temperature": {
        "title": "Temperature vs size",
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "category": (_PHYS_CATS, "Object class."),
            "size_m": ("pos", "Size, m."),
            **_range_cols("temperature", "k", "temperature", "melting|vaporisation|biology|none"),
            **_COMMON_TAIL,
        },
    },
    "density": {
        "title": "Density vs size",
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "category": (_PHYS_CATS, "Object class."),
            "size_m": ("pos", "Size, m."),
            **_range_cols("density", "kg_m3", "density", "black-hole|tov|none"),
            **_COMMON_TAIL,
        },
    },
    "acceleration": {
        "title": "Acceleration vs size",
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "category": (_PHYS_CATS, "Object class."),
            "size_m": ("pos", "Size, m."),
            **_range_cols("accel", "m_s2", "acceleration", "human-tolerance|material|rated|none"),
            **_COMMON_TAIL,
        },
    },
    "lifetime": {
        "title": "Lifetime vs size",
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "category": (_PHYS_CATS, "Object class."),
            "size_m": ("pos", "Size, m (Compton wavelength h/mc for point particles)."),
            **_range_cols("lifetime", "s", "lifetime", "lower-bound|none"),
            **_COMMON_TAIL,
        },
    },
    "biology": {
        "title": "Living things: mass vs length",
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "category": ("enum:molecule|virus|cell|animal|plant|fungus", "Class."),
            "length_m": ("pos", "Largest linear dimension, m."),
            **_range_cols("mass", "kg", "mass", "none"),
            **_COMMON_TAIL,
        },
    },
    "chemistry": {
        "title": "Binding energy vs size",
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "category": ("enum:nuclear|atomic|covalent|ionic|weak", "Bond class."),
            "size_m": ("pos", "Bond length or system diameter, m."),
            **_range_cols("energy", "j", "binding energy", "none"),
            **_COMMON_TAIL,
        },
    },
    "materials": {
        "title": "Tensile strength vs density",
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "category": ("enum:metal|polymer|fibre|ceramic|natural|nano", "Material class."),
            "density_kg_m3": ("pos", "Density, kg/m^3."),
            **_range_cols("strength", "pa", "tensile strength", "ideal|none"),
            **_COMMON_TAIL,
        },
    },
    "ai_models": {
        "title": "AI model size and training compute",
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "category": ("enum:early|cnn|rnn|transformer|moe", "Architecture family."),
            "year": ("year", "Publication year (decimal)."),
            "params_total": ("pos", "Total trainable parameters."),
            "params_active": ("pos", "Parameters active per token (mixture-of-experts); empty if dense."),
            "training_tokens": ("pos", "Training tokens, if reported."),
            "training_flop": ("pos", "Training compute in FLOP, if reported or derived as 6ND."),
            "flop_basis": ("enum:reported|6ND|none", "How training_flop was obtained."),
            **_COMMON_TAIL,
        },
    },
    "ai_benchmarks": {
        "title": "Reported AI benchmark scores",
        "columns": {
            "id": ("slug", "Unique id."),
            "benchmark": ("enum:imagenet|mmlu|gsm8k|gpqa|swebench|arcagi", "Benchmark."),
            "model": ("text", "Model or system."),
            "year": ("year", "Date reported (decimal year)."),
            "score_pct": ("num", "Reported score, percent."),
            "setting": ("text", "Evaluation setting as reported."),
            **_COMMON_TAIL,
        },
    },
    "ai_benchmark_refs": {
        "title": "Benchmark reference levels",
        "columns": {
            "id": ("slug", "Unique id."),
            "benchmark": ("enum:imagenet|mmlu|gsm8k|gpqa|swebench|arcagi", "Benchmark."),
            "level": ("enum:chance|human|ceiling", "Kind of reference level."),
            "score_pct": ("num", "Level, percent."),
            "name": ("text", "Label."),
            **_COMMON_TAIL,
        },
    },
    "cognition": {
        "title": "Human cognitive limits",
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "panel": ("enum:rate|capacity", "rate = bits per second; capacity = count of items."),
            "category": ("enum:behaviour|sensory|physics|memory|social|language", "Kind."),
            "value": ("pos", "Representative value."),
            "low": ("pos", "Low end of the reported range; empty if none."),
            "high": ("pos", "High end of the reported range; empty if none."),
            **_COMMON_TAIL,
        },
    },
    "research": {
        "title": "Researcher limits",
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "panel": ("enum:papers|team", "papers = papers per year; team = people."),
            "category": ("enum:person|world|bound|record|social", "Kind."),
            "value": ("pos", "Value."),
            **_COMMON_TAIL,
        },
    },
}


def _xy(title: str, x_col: str, x_desc: str, q: str, unit: str, what: str, cats: str, basis: str = "none"):
    """A size-style dataset: one x column and a low/high/example/max range of one quantity."""
    return {
        "title": title,
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "category": (f"enum:{cats}", "Object class."),
            x_col: ("pos", x_desc),
            **_range_cols(q, unit, what, basis),
            **_COMMON_TAIL,
        },
    }


def _bars(title: str, panels: str, cats: str, value_type: str = "pos"):
    """A bar-chart dataset: one representative value per row, with an optional reported range."""
    return {
        "title": title,
        "columns": {
            "id": ("slug", "Unique id."),
            "name": ("text", "Label."),
            "panel": (f"enum:{panels}", "Which panel of the figure."),
            "category": (f"enum:{cats}", "Kind."),
            "value": (value_type, "Representative value."),
            "low": (value_type if value_type == "num" else "pos", "Low end of the reported range; empty if none."),
            "high": (value_type if value_type == "num" else "pos", "High end of the reported range; empty if none."),
            **_COMMON_TAIL,
        },
    }


DATASETS.update(
    {
        "energy_density": _bars(
            "Stored energy per kilogram",
            "store",
            "electrochemical|mechanical|chemical|nuclear|gravitational",
        ),
        "power": _xy(
            "Power vs mass",
            "mass_kg",
            "Mass of the engine, animal or object, kg.",
            "power",
            "w",
            "power",
            "living|human|astro",
            "eddington|none",
        ),
        "radio": _xy(
            "Radio links: transmit power vs distance",
            "distance_m",
            "Link distance, m.",
            "power",
            "w",
            "transmit power",
            "human|lab|astro",
        ),
        "black_holes": _xy(
            "Black hole spin vs mass",
            "mass_kg",
            "Black hole mass, kg.",
            "spin",
            "a",
            "dimensionless spin parameter a",
            "stellar|merger|supermassive",
            "kerr|none",
        ),
        "pulsars": {
            "title": "Pulsars and magnetars: period vs spin-down rate",
            "columns": {
                "id": ("slug", "Unique id."),
                "name": ("text", "Label."),
                "category": ("enum:pulsar|millisecond|magnetar|long-period", "Class."),
                "period_s": ("pos", "Spin period, s."),
                "pdot": ("pos", "Period derivative dP/dt, s/s."),
                **_COMMON_TAIL,
            },
        },
        "numbers": _bars(
            "The scale of numbers",
            "count",
            "life|earth|cosmos|games|physics",
        ),
        "flow": _xy(
            "Volumetric flow vs channel size",
            "width_m",
            "Channel diameter or width, m.",
            "flow",
            "m3_s",
            "volumetric flow",
            "living|human|earth",
        ),
        "oscillation": _xy(
            "To-and-fro motion: oscillation frequency vs size",
            "size_m",
            "Size of the oscillating object, m.",
            "freq",
            "hz",
            "oscillation frequency",
            "molecular|lab|living|human|astro",
        ),
        "charge": _xy(
            "Electric charge vs size",
            "size_m",
            "Size of the charged object, m.",
            "charge",
            "c",
            "net charge magnitude",
            "particle|lab|earth|astro",
        ),
        "voltage": _xy(
            "Voltage vs gap size",
            "gap_m",
            "Distance over which the voltage is held, m.",
            "voltage",
            "v",
            "voltage",
            "atomic|living|human|earth|astro",
        ),
        "magnetic": _xy(
            "Magnetic field vs size",
            "size_m",
            "Size of the magnetised region, m.",
            "field",
            "t",
            "magnetic field",
            "living|lab|earth|astro",
        ),
        "pressure": _xy(
            "Pressure vs size",
            "size_m",
            "Size of the pressurised region, m.",
            "pressure",
            "pa",
            "pressure",
            "particle|lab|earth|astro",
        ),
        "luminous": _bars(
            "Luminous intensity",
            "intensity",
            "flame|electric|astro|physics",
        ),
        "sound": _bars(
            "Sound levels",
            "air|water",
            "living|human|nature|limit",
            value_type="num",
        ),
        "epidemics": _xy(
            "Spread rate of infections: R0 vs serial interval",
            "serial_days",
            "Serial interval (days between successive cases).",
            "r0",
            "x",
            "basic reproduction number",
            "airborne|contact|influenza|coronavirus",
        ),
        "genomes": {
            "title": "Genome size vs number of genes",
            "columns": {
                "id": ("slug", "Unique id."),
                "name": ("text", "Label."),
                "category": ("enum:virus|bacterium|fungus|plant|animal", "Kingdom."),
                "genome_bp": ("pos", "Genome length in base pairs (nucleotides for RNA viruses)."),
                "genes": ("pos", "Protein-coding genes."),
                **_COMMON_TAIL,
            },
        },
        "buildings": {
            "title": "Tallest buildings over time",
            "columns": {
                "id": ("slug", "Unique id."),
                "name": ("text", "Label."),
                "category": ("enum:ancient|tower|skyscraper", "Kind."),
                "year": ("num", "Year completed (negative = BCE)."),
                "height_m": ("pos", "Architectural height, m."),
                **_COMMON_TAIL,
            },
        },
        "structures": _xy(
            "Structure mass vs height",
            "height_m",
            "Height, m.",
            "mass",
            "kg",
            "mass",
            "ancient|tower|skyscraper|dam",
            "none",
        ),
        "volumes": _xy(
            "Gas and water volumes: mass vs volume",
            "volume_m3",
            "Volume, m^3.",
            "mass",
            "kg",
            "mass",
            "gas|water|ice",
        ),
    }
)


def schema_for(name: str) -> dict:
    """JSON Schema (draft 2020-12) for one row of a dataset."""
    ds = DATASETS[name]
    props, required = {}, []
    for col, (typ, desc) in ds["columns"].items():
        p: dict = {"description": desc}
        if typ == "slug":
            p.update(type="string", pattern=r"^[a-z0-9][a-z0-9-]*$")
            required.append(col)
        elif typ == "text":
            p.update(type="string", minLength=1)
            required.append(col)
        elif typ == "opt":
            p.update(type=["string", "null"])
        elif typ == "url":
            p.update(type="string", pattern=r"^https://\S+$")
            required.append(col)
        elif typ == "pos":
            p.update(type=["number", "null"], exclusiveMinimum=0)
        elif typ == "num":
            p.update(type=["number", "null"])
        elif typ == "year":
            p.update(type="number", minimum=1900, maximum=2100)
            required.append(col)
        elif typ.startswith("enum:"):
            if col.endswith("_basis"):
                p.update(enum=typ[5:].split("|") + [None])
            else:
                p.update(type="string", enum=typ[5:].split("|"))
                required.append(col)
        else:  # pragma: no cover
            raise ValueError(typ)
        props[col] = p
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://github.com/QuantumNovice/the-allowed-universe/data/schema/{name}.schema.json",
        "title": ds["title"],
        "type": "object",
        "properties": props,
        "required": required,
        "additionalProperties": False,
    }
