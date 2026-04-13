# Architecture

## 1. Core objective

Port the collapse periodic table into FARD as a deterministic, artifact-oriented build.

The elemental field is the foundation.
Every later layer depends on it.

---

## 2. Package graph

```text
collapse-core
    ↓
collapse-data
    ↓
collapse-elements
    ↓
collapse-compounds
    ↓
collapse-spin
    ↓
collapse-render
```

For this scaffold, the implemented graph is:

```text
collapse-core
    ↓
collapse-data
    ↓
collapse-elements
```

---

## 3. Canonical records

### Element record

```json
{
  "Z": 6,
  "symbol": "C",
  "name": "Carbon",
  "ionization_energy": 11.26,
  "electron_affinity": 1.262,
  "electronegativity": 2.55,
  "polarizability_au": 11.3,
  "hardness": 9.998,
  "phi_star": -0.021,
  "phase": "Z",
  "color": "white",
  "group": 14,
  "period": 2
}
```

### Build config

```json
{
  "w_chi": 1.0,
  "w_eta": 0.7,
  "w_alpha": 0.5,
  "phi_threshold": 0.5
}
```

---

## 4. Elemental build flow

1. read source CSVs
2. normalize rows
3. merge on `AtomicNumber`
4. compute `hardness = I - A_clean`
5. compute z-score stats
6. compute `phi_star`
7. classify phase
8. emit records and summaries

---

## 5. Future layers

### Compounds
Binary compounds will add:
- `phi_avg`
- `delta_phi`
- `ionicity`
- geometry corrections
- compound phase

### Spin
Spin will add:
- elemental magnetic moments
- `phi_spin`
- spin phase classification

### Rendering
Rendering will convert record sets into deterministic image artifacts.
