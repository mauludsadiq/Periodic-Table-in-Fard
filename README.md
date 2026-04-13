# Periodic Table in FARD

A complete scientific computing project built entirely in [FARD](https://github.com/mauludsadiq/FARD) — a deterministic, functional, artifact-oriented programming language. The project models the periodic table through a four-phase computational ladder, producing validated element and compound records, spin classifications, and raster renders from raw CSV data.

-----

## What this is

The periodic table is one of the most information-dense structures in science. This project treats it as a data pipeline problem: raw experimental measurements go in, a calibrated field theory comes out.

Every element receives a scalar score — φ* — computed from its electronegativity, hardness, and polarizability. That score determines phase classification, drives compound modeling, feeds spin calculations, and ultimately maps to pixels in a rendered layout.

Nothing here is hardcoded chemistry intuition. It is all math applied to data.

-----

## Build status

```
total elements: 118
E phase (electropositive):  33
Z phase (zero-belt):        66
1 phase (electronegative):  19
```

All four phases of the modeling ladder are implemented and producing output.

-----

## The φ* field

The core computation:

```
φ* = w_χ · χ̃  −  w_η · η̃  +  w_α · ᾱ
```

Each descriptor is z-score normalized across the element population. Hardness is derived from ionization energy and electron affinity:

```
η = I − A
```

Default weights: `w_χ = 1.0`, `w_η = 0.7`, `w_α = 0.5`

Phase boundaries are set at ±0.5:

|φ*         |Phase              |Color|
|-----------|-------------------|-----|
|> 0.5      |E (electropositive)|red  |
|−0.5 to 0.5|Z (zero-belt)      |white|
|< −0.5     |1 (electronegative)|blue |

For binary compounds, the compound field is:

```
φ_compound = φ_avg − ionicity
ionicity = Δφ / (Δφ + 1)
```

Compound spin reduces by ionicity: more ionic bonds damp the spin signal.

-----

## Package structure

```
packages/
├── collapse-core/       pure math — z-score, hardness, phi_star, phase, spin classification
├── collapse-data/       CSV loading — PubChem table, polarizability dataset, merge
├── collapse-elements/   table builder, calibrator, element records, analysis, export
├── collapse-compounds/  binary compound field construction
├── collapse-spin/       elemental and compound spin (standard and tight calibration)
├── collapse-render/     PPM scene generation, layout engine, pixel rendering
└── collapse-validate/   ground truth joins, element and compound validation
```

The separation is intentional. Formulas never touch files. File I/O never touches formulas.

-----

## Apps

|App                                        |What it does                                        |
|-------------------------------------------|----------------------------------------------------|
|`build_periodic_table.fard`                |Builds the full elemental table, writes JSON and CSV|
|`build_binary_compounds.fard`              |Computes compound fields for element pairs          |
|`build_elemental_spin.fard`                |Computes spin classification for each element       |
|`build_tight_spin.fard`                    |Tight-calibration spin variant                      |
|`build_compound_spin.fard`                 |Compound-level spin from element pair spin fields   |
|`build_element_validation.fard`            |Joins computed fields against ground truth          |
|`build_compound_validation.fard`           |Validates compound predictions                      |
|`build_compound_bandgap_validation.fard`   |Bandgap-specific validation                         |
|`build_compound_dielectric_validation.fard`|Dielectric validation                               |
|`build_validation_ground_truth.fard`       |Exports the ground truth reference table            |
|`render_layouts.fard`                      |Renders phone, tablet, and desktop PPM layouts      |
|`build_final.fard`                         |Full pipeline in one app                            |

-----

## Running a build

```bash
# Elemental table
fardrun run --program apps/build_periodic_table.fard --out out

# Compound field
fardrun run --program apps/build_binary_compounds.fard --out out

# Spin
fardrun run --program apps/build_elemental_spin.fard --out out
fardrun run --program apps/build_compound_spin.fard --out out

# Validation
fardrun run --program apps/build_element_validation.fard --out out
fardrun run --program apps/build_compound_validation.fard --out out

# Render
fardrun run --program apps/render_layouts.fard --out out
```

Each run writes its output into `out/<app-name>/` with a full artifact set.

-----

## What FARD produces per run

Every execution emits:

- `result.json` — the return value of the program
- `digests.json` — content hashes of all inputs and outputs
- `module_graph.json` — the complete import graph for that run
- `trace.ndjson` — a full execution trace
- `artifacts/` — any files written by the program

This means every build is reproducible, auditable, and comparable across versions.

-----

## Data

### `data/pubchem_periodic_table.csv`

PubChem element table. Provides atomic number, symbol, name, ionization energy, electron affinity, and electronegativity for all 118 elements.

### `data/polarizability_2020.csv`

Polarizability values in atomic units (α_au). Elements without a polarizability value are included in the element table using the calibrator mean as a fallback, but are excluded from calibrator fitting.

-----

## Design notes

**No mutation.** Every statistic — mean, variance, standard deviation — is computed through pure `list.fold` and `list.map` chains. No accumulators are modified in place.

**Calibration is explicit.** The calibrator fits means and standard deviations from the element population, then applies those parameters uniformly. The config record controls all weights and thresholds.

**Records are typed at construction.** Every element record is built through a single `make_element_record` call with all fields stated explicitly. There is no dynamic key insertion.

**Packages only talk through their exports.** Each module returns a record of functions. Nothing leaks. Cross-package dependencies are declared at the top of every file as named imports.

**The render is deterministic.** The PPM renderer assigns colors purely from phase classification and grid position. Given the same element table and layout, it produces the same bytes every time.
