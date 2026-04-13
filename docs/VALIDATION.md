# Validation

## Element-level descriptor

The elemental descriptor is:

\[
\phi^* = \chi_t - 0.7\eta_t + 0.5\alpha_t
\]

Interpretation:

- **E**: \(\phi^* > 0.5\) → electronically responsive / flexible
- **Z**: \(-0.5 \le \phi^* \le 0.5\) → electronically balanced / ordinary
- **1**: \(\phi^* < -0.5\) → electronically rigid / closed

This is a unary response coordinate built from electronegativity, hardness, and polarizability.

## Compound-level descriptor

For binary compounds, the useful lifted descriptor is the 2D geometry:

- `phi_avg` = weighted average constituent response
- `delta_phi` = mismatch in constituent response

Derived quantity:

- `ionicity = delta_phi / (delta_phi + 1)`

Important: `ionicity` is a monotone transform of `delta_phi`, so it is descriptive but not geometrically independent.

## Benchmark classes

The compound benchmark uses 23 binaries across 5 classes:

- IONIC
- POLAR_COVALENT
- NETWORK_COVALENT
- INTERMETALLIC
- TM_OXIDE

## 2D centroid result

Using nearest-centroid classification in `(phi_avg, delta_phi)` space:

- total compounds: **23**
- accuracy: **14 / 23 = 60.9%**
- chance baseline: **20%**
- improvement over chance: **3.04×**

### 2D centroids

| Class | phi_avg | delta_phi | n |
|---|---:|---:|---:|
| IONIC | 0.760718 | 1.050917 | 5 |
| POLAR_COVALENT | 0.416254 | 0.829293 | 5 |
| NETWORK_COVALENT | 0.544898 | 0.216117 | 4 |
| INTERMETALLIC | 0.321873 | 0.240002 | 4 |
| TM_OXIDE | 0.642068 | 0.589736 | 5 |

## Negative results

The following interpretations were tested and falsified:

### 1. `phi_comp` as a single compressed compound scalar
Using

\[
\phi_{\mathrm{comp}} = \phi_{\mathrm{avg}} - \mathrm{ionicity}
\]

collapses too many compounds into the same coarse region and loses separability visible in 2D.

### 2. Band gap prediction
`phi_comp`, `phi_avg`, and `delta_phi` do not directly predict band gap.

Therefore the descriptor is **not** a transport-gap or carrier-excitation axis.

### 3. 3D centroid classification with `(phi_avg, delta_phi, ionicity)`
Adding `ionicity` reduces simple nearest-centroid performance:

- 2D accuracy: **60.9%**
- 3D accuracy: **56.5%**

This is expected because `ionicity` is a monotone transform of `delta_phi` and therefore largely duplicates the mismatch axis.

## Positive conclusion

The descriptor is not random and not empty.

The elemental `phi*` axis measures **electronic responsiveness**.

Lifted to compounds through `(phi_avg, delta_phi)`, it defines a low-dimensional **bonding map** that separates several important binary-compound families with meaningful accuracy using only intrinsic elemental properties.

## Artifacts

Generated artifacts:

- `out/compound_validation.csv`
- `out/compound_validation_summary.json`

These should be treated as the canonical validation outputs for the current descriptor family.
