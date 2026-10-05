# The Allowed Universe: Repo Spec

Oct 3, 2026 · @Haseeb

## How to use this spec

Paste this whole doc into an AI coding assistant (Claude Code, Cursor, etc.) with the instruction below, then work through the milestones one at a time.

> You are building a new open-source GitHub repository described in the spec below. Read the whole spec first. Then build Milestone 1 only, following the repository structure, data format and plot style exactly. Every physical constant and every data value must carry a source. Ask me before adding any dependency not listed in the tech stack. When Milestone 1 passes its acceptance criteria, stop and summarise what you built.

The repo name below is a working title. Replace it everywhere if a different name is chosen.

## Project overview

**Name:** `the-allowed-universe` (owner: github.com/QuantumNovice)

**Tagline:** Everything from molecules to galaxies, plotted between the hard limits of physics.

**Description (for the GitHub About box):** Log-log plots that place real objects, from a hydrogen molecule to the Milky Way, inside the bounds physics allows. Each chart shades the forbidden zones (faster than light, below one quantum, older than the universe) and shows how close each object comes to its own breakup limit. Open data, sourced values, reproducible figures.

**Core idea.** Every chart has the same three layers:

1. **Hard physical bounds** that nothing can cross (light speed, quantum limits, the age of the universe, black hole formation). The regions beyond them are shaded as forbidden.
2. **Practical limits** where a class of object fails (material strength, self-gravity breakup). Drawn as dashed or dotted lines.
3. **Real objects** as points, with a vertical range bar from the slowest or smallest known member to the fastest or largest, plus a cap at the object’s own maximum allowable value.

The first chart is spin rate against size. The same template then extends to other quantities (see Scope).

## Goals and non-goals

**Goals**

- Publication-quality static figures (PNG and PDF) that are readable on a phone and printable on A4.
- An interactive web version where hovering a point shows its value, source and notes.
- All data in plain, versioned files with a source URL for every value, so anyone can audit or extend it.
- Limit lines computed from formulas in code, never hand-drawn.
- One command regenerates every figure from the data.
- Easy contributions: adding an object means adding one row to a data file.

**Non-goals**

- Not a physics textbook. Each chart gets a short explainer, not a chapter.
- Not a link list. The repo is original plots, data and code, so it does not use the `awesome-` prefix.
- No speculative physics (wormholes, string theory). Only limits from established physics.

## Scope

The repo launches with the spin chart and grows to seven charts. Every chart puts size (m) on the x-axis unless noted, both axes logarithmic.

| # | Chart | Y-axis (units) | Hard bounds | Practical limits | Example objects |
| --- | --- | --- | --- | --- | --- |
| 1 | Spin rate vs size | turns per second (Hz) | light-speed rim, one quantum of spin, one turn in the age of the universe | material strength, self-gravity breakup | H₂ molecule, dental drill, Earth, pulsars, black holes, Milky Way |
| 2 | Mass vs size | kg | black hole line (Schwarzschild), quantum (Compton wavelength) | nuclear density, atomic density | electron, proton, human, Earth, Sun, neutron star, observable universe |
| 3 | Speed vs size | m/s | speed of light | escape speeds, sound speed in materials | bacteria, cheetah, bullet, Voyager 1, solar wind, relativistic jets |
| 4 | Temperature vs size | K | absolute zero, Planck temperature | melting/vaporisation points | Bose-Einstein condensate, Sun’s core, LHC collisions, cosmic background |
| 5 | Density vs size | kg/m³ | black hole density at that size | nuclear density | interstellar gas, air, water, osmium, white dwarf, neutron star |
| 6 | Acceleration vs size | m/s² | Planck acceleration, horizon surface gravity | human tolerance, material failure | car, fighter pilot, centrifuge, neutron star surface |
| 7 | Lifetime vs size | s | Planck time, age of the universe | radioactive half-lives | top quark, free neutron, human, Sun, proton (lower bound) |

Charts 2 to 7 follow the same three-layer template as chart 1. Each gets its own data file, plot script and explainer page.

## Physics of the limits (chart 1, spin)

All limits live in `src/limits.py` as pure functions of size d (diameter, m), with constants from CODATA 2022 via `scipy.constants`. Unit tests check each against the hand-computed values given here.

**Upper bound: rim at light speed.** The edge of a spinning object cannot outrun light.

```latex
f_{\max}(d) = \frac{c}{\pi d}
```

**Lower bound, small objects: one quantum of spin.** Angular momentum comes in units of ħ. The slowest nonzero spin uses the densest ordinary matter (ρ ≈ 22,600 kg/m³, osmium) with mass at the rim (I = m d²/4, m = ρπd³/6).

```latex
f_{\min}(d) = \frac{\hbar}{2\pi I} = \frac{12\,\hbar}{\pi^{2} \rho\, d^{5}} \approx \frac{5.7\times10^{-39}}{d^{5}}\ \text{Hz}
```

**Lower bound, large objects: one turn in the age of the universe** (t₀ = 13.8 Gyr). This is an observability floor, not a law, and the explainer must say so.

```latex
f_{\min} = \frac{1}{t_0} \approx 2.3\times10^{-18}\ \text{Hz}
```

**Practical: material strength.** A rim tears once its speed exceeds about √(σ/ρ). Use v ≈ 3 km/s for the strongest materials.

```latex
f_{\text{mat}}(d) = \frac{v_{\text{rim}}}{\pi d}, \qquad v_{\text{rim}} \approx \sqrt{\sigma/\rho}
```

**Practical: self-gravity breakup.** Surface gravity balances centrifugal force. Depends only on density, so it is a horizontal line (about one turn per 2.2 h for rock, ρ ≈ 2,000 kg/m³).

```latex
f_{\text{grav}} = \frac{1}{2\pi}\sqrt{\frac{4\pi G \rho}{3}}
```

**Per-object cap: maximally spinning black hole** of mass M (spin parameter a = 1). For a general spin a, the horizon frequency is a c / (4π r₊) with r₊ = (GM/c²)(1 + √(1 − a²)).

```latex
f_{H,\max} = \frac{c^{3}}{4\pi G M}
```

**Orbiting systems** (planet orbits, black hole mergers) are drawn as curves from Kepler’s third law, with d = 2a the orbit diameter.

```latex
f_{\text{orb}} = \frac{1}{2\pi}\sqrt{\frac{G M}{a^{3}}}
```

Charts 2 to 7 each need the same treatment: every bound written as a formula with a test value before any plotting.

## Data format and seed dataset

Each chart has one CSV in `data/` (one row per object or class) and is validated by a JSON Schema in `data/schema/` on every commit. SI units only. Missing values stay empty, never zero.

**Columns for `data/spin.csv`:**

| Column | Type | Meaning |
| --- | --- | --- |
| `id` | slug | unique, e.g. `neutron-stars` |
| `name` | text | label shown on the plot |
| `category` | enum | `molecular`, `living`, `human`, `astro`, `orbit` |
| `size_m` | float | diameter in metres |
| `slowest_hz` | float | slowest known member of the class |
| `fastest_hz` | float | fastest known member |
| `example_hz` | float | value of the marked example object |
| `max_hz` | float | maximum allowable spin (breakup), empty if none |
| `max_basis` | enum | `material`, `gravity`, `black-hole`, `quantum`, `centrifugal-dissociation` |
| `source_url` | url | primary source for the values |
| `notes` | text | one line shown in the hover tooltip |

**Seed values.** These are approximate figures from an initial draft. Every row needs a primary source (journal paper, NASA/ESA fact sheet, manufacturer spec) found and checked before merging. Correct any value that disagrees with its source. The seed omits the source\_url column, which is added as each source is confirmed.

```csv
id,name,category,size_m,slowest_hz,fastest_hz,example_hz,max_hz,max_basis,notes
h2,H2 molecule,molecular,7.4e-11,3.6e12,3e13,3.6e12,6e13,centrifugal-dissociation,Lowest rotational state J=1 is one quantum
flagellar-motor,Bacterial flagellar motor,living,4.5e-8,10,1700,1700,,,Vibrio sodium-driven motor
nanoparticle,Levitated nanoparticle,molecular,1.5e-7,1e3,5e9,5e9,6e9,material,Laser-spun silica record
dental-drill,Dental drill,human,8e-3,8,6700,6700,2e4,material,Air turbine about 400000 rpm
centrifuge,Centrifuge rotor,human,0.1,10,2500,2500,4000,material,Ultracentrifuge about 150000 rpm
car-wheel,Car wheel,human,0.65,0.1,40,40,60,material,300 km/h
skater,Figure skater,human,1.7,0.3,5.7,5.7,,,Fastest spins about 340 rpm
wind-turbine,Wind turbine,human,150,0.05,0.2,0.2,0.3,material,150 m rotor
small-asteroids,Small asteroids,astro,20,1e-6,0.063,0.063,,,2014 RC about 16 s per turn
rubble-asteroids,Rubble-pile asteroids,astro,3e3,2.4e-7,1.26e-4,1.26e-4,1.26e-4,gravity,Spin barrier about 2.2 h
neutron-stars,Neutron stars,astro,2e4,4.2e-5,716,716,1500,gravity,PSR J1748-2446ad
stellar-bh,Stellar black holes (10 Msun),astro,4.5e4,80,1300,1300,1613,black-hole,Spin a from 0.1 to 0.98
white-dwarfs,White dwarfs,astro,7e6,1e-5,0.04,0.04,0.077,gravity,Fastest about 25 s per turn
rocky-planets,Rocky planets,astro,1.27e7,4.8e-8,1.16e-5,1.16e-5,2e-4,gravity,Venus to Earth
gas-giants,Gas giants,astro,1.4e8,1.6e-5,2.8e-5,2.8e-5,9.7e-5,gravity,Uranus to Jupiter
sun-like,Sun-like stars,astro,1.39e9,2.3e-7,1.2e-5,4.6e-7,1e-4,gravity,Sun marked at 25 days
sgr-a,Sgr A*,astro,1.8e10,,,,4e-3,black-hole,Spin not measured
betelgeuse,Betelgeuse,astro,1.06e12,1e-10,8.8e-10,8.8e-10,2.1e-8,gravity,About 36 years per turn
m87,M87* black hole,astro,2.5e13,1.25e-7,1.6e-6,1.6e-6,2.5e-6,black-hole,Spin a about 0.9
```

Orbiting systems go in a separate `data/spin_orbits.csv` (columns `id, name, mass_kg, size_m, freq_hz, source_url`), one row per point along the track: planet orbits Mercury to Neptune, GW150914 final orbits (17.5 to 125 Hz, total mass 65 M☉), and the Milky Way rotation curve (flat at 230 km/s, Sun at 8.2 kpc).

## Repository structure and tech stack

Python builds the static figures, and TypeScript builds the interactive site from the same CSV files. Both read the limits from one shared source so they never disagree.

```text
the-allowed-universe/
├── README.md
├── LICENSE                 # MIT for code
├── LICENSE-DATA            # CC BY 4.0 for data and figures
├── CONTRIBUTING.md
├── CITATION.cff
├── pyproject.toml          # uv-managed
├── Makefile                # make figures | make test | make site
├── data/
│   ├── spin.csv
│   ├── spin_orbits.csv
│   └── schema/spin.schema.json
├── src/allowed_universe/
│   ├── constants.py        # wraps scipy.constants, CODATA 2022
│   ├── limits.py           # one pure function per bound
│   ├── loaders.py          # read + validate CSV
│   ├── style.py            # shared matplotlib style
│   └── charts/spin.py      # one module per chart
├── tests/
│   ├── test_limits.py      # each bound vs hand-computed value
│   └── test_data.py        # schema, units, every row has a source
├── figures/                # generated PNG + PDF, committed
├── docs/explainers/spin.md # short plain-language explainer per chart
├── site/                   # TypeScript + Vite + Observable Plot
│   ├── src/limits.ts       # loads public/limits.json, no formulas here
│   └── src/charts/spin.ts
└── .github/workflows/
    ├── ci.yml              # lint, test, validate data on every PR
    └── pages.yml           # build figures + site, deploy to GitHub Pages
```

**Python:** 3.12, numpy, scipy, matplotlib, pandas, jsonschema, pytest, ruff. Managed with uv.

**Web:** TypeScript, Vite, Observable Plot (log scales and tooltips built in). Deployed to GitHub Pages.

**Keeping limits in sync:** `limits.py` exports each bound as sampled points to `site/public/limits.json` during `make figures`. The site reads that file, so the formulas live in one place only.

## Plot style guide

Every chart uses one shared style so the set reads as a series.

| Element | Style |
| --- | --- |
| Font | Times New Roman (fallback: Liberation Serif, then serif), all text black |
| Axes | log-log, labels with units, ticks every 5 decades as 10ⁿ, light grey major grid |
| Upper hard bound | solid red line #e34948, 2.5 pt, region beyond shaded red at 10% opacity |
| Lower hard bound | solid blue line #2a78d6, 2.5 pt (dashed for observability floors), region shaded blue at 10% |
| Practical limits | thinner lines: material in dotted amber #d08a00, gravity in dashed grey #888888 |
| Object categories | molecular/living teal #1baf7a circles, human orange #eb6834 triangles, astronomical violet #6250d6 diamonds, orbits pink #d55181 squares with connecting curves |
| Range bars | solid 3 pt from slowest to fastest known, dotted 1.6 pt from fastest to max allowable, black cap at max |
| Forbidden zones | italic label inside each shaded region, e.g. “Forbidden: faster than light” |
| Labels | 10 pt, placed beside the marker, never overlapping a line or another label |
| Output | PNG at 200 dpi and vector PDF, 12 × 10 in |

Colour never carries meaning alone: every category also has its own marker shape, so the charts work in greyscale and for colour-blind readers. A legend explains every line style, bar style and marker.

## README, topics, license and contributing

**README outline** (in this order, short sections):

1. Title, tagline, and the spin chart as the hero image
2. Badges: CI status, license, GitHub Pages link
3. “What am I looking at?” in three sentences: forbidden zones, practical limits, real objects
4. Gallery: a thumbnail per chart linking to its full figure and explainer
5. Quick start: `uv sync`, `make figures`, `make site`
6. How to add an object (one CSV row with a source)
7. Data sources and how values are checked
8. How to cite (from `CITATION.cff`) and license

**GitHub topics:** `physics`, `physical-limits`, `scale-comparison`, `data-visualization`, `log-log`, `astrophysics`, `matplotlib`, `open-data`, `science-communication`

**License:** MIT for code. CC BY 4.0 for data and figures, so people can reuse the charts with credit.

**Contributing rules** (for `CONTRIBUTING.md`):

- One object per pull request, with a primary source link in `source_url`.
- Values in SI units. Give the class range (slowest to fastest), not one cherry-picked value.
- Wikipedia is fine for finding a source but not as the source itself.
- CI must pass: schema valid, tests green, figures regenerated and committed.
- New chart families start as an issue with the bound formulas written out first.

## Milestones and acceptance criteria

Build in this order. Each milestone is done only when every criterion in its row passes.

| # | Milestone | Done when |
| --- | --- | --- |
| 1 | Skeleton + spin limits | Repo structure in place. `limits.py` has all chart 1 bounds. `test_limits.py` passes, e.g. f\_max at d = 1 m ≈ 9.54 × 10⁷ Hz and f\_min at d = 10⁻¹⁰ m ≈ 5.7 × 10¹¹ Hz. CI runs on push. |
| 2 | Spin data | `spin.csv` and `spin_orbits.csv` validate against the schema. Every row has a working primary-source URL. Values corrected where sources disagree with the seed. |
| 3 | Spin figure | `make figures` writes `figures/spin.png` and `figures/spin.pdf` matching the style guide. No label overlaps a line or another label. Every real object sits inside the allowed band. |
| 4 | README + explainer | README follows the outline with the spin chart as hero. `docs/explainers/spin.md` explains the three layers in under 500 words. Licenses and `CITATION.cff` present. |
| 5 | Interactive site | GitHub Pages shows the spin chart with hover tooltips (name, value, source, notes) and a category toggle. Limits come from `limits.json`. Works on a 380 px phone screen. |
| 6+ | Charts 2 to 7 | One chart per milestone, each repeating milestones 1 to 5 for its own quantity. |
