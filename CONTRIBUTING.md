# Contributing

Thanks for helping map the allowed universe. A few rules keep the data trustworthy.

## Adding or correcting an object

- **One object per pull request**, with a primary source link in `source_url` and a short `citation` (authors, year, title, venue).
- **Primary sources only.** Use a journal paper (DOI preferred), an agency fact sheet (NASA, NIST, NOAA, PDG) or a manufacturer specification. Wikipedia is fine for *finding* a source, but not as the source itself (a test rejects it).
- **SI units.** Column names carry the unit (`size_m`, `mass_example_kg`, ...). Leave unknown values empty, never zero.
- **Give the class range** (slowest to fastest, lightest to heaviest), not one cherry-picked value. Put the marked example in the `*_example_*` column.
- **A maximum needs a reason.** If you fill a `*_max_*` column, set `max_basis` too.
- If a value is derived (for example a mean density from mass and radius), say so in `notes`.

## Checks

```bash
make figures   # regenerates schemas, JSON exports, figures and docs/REFERENCES.md
make test      # must pass
make lint
make sources   # optional, needs network: confirms each DOI matches its citation
```

CI must pass: schema valid, tests green, and figures plus generated files regenerated and committed.

## New chart families

Open an issue first with the bound formulas written out and a hand-computed test value for each. Then add:

1. pure functions in `src/allowed_universe/limits.py` plus tests in `tests/test_limits.py`
2. a dataset entry in `src/allowed_universe/datasets.py` and a CSV in `data/`
3. a chart module in `src/allowed_universe/charts/`, registered in `charts/__init__.py`
4. a short explainer in `docs/explainers/`

No speculative physics: only limits from established theory.
