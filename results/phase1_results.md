# Phase 1 Results — Raw Data

## Parameters

- Lattice: 24³ × 48
- Group: SU(2)
- β: 2.5
- Configurations: 1000
- Decorrelation: 200 sweeps
- Smearing: APE, levels [0, 5, 10, 20], α = 0.3
- Gradient flow: 100 steps × ε = 0.01 (t_flow = 1.0)
- GPU: NVIDIA L4 (on-demand, us-east4-c)
- Runtime: 49.92 hours
- GEVP: τ₀ = 0, operators normalized by V_spatial = 24³

## Plaquette

⟨P⟩ = 0.651961 ± 0.000007

## Topological charge

| Q | configs | % |
|---|---|---|
| -7 | 1 | 0.1 |
| -6 | 1 | 0.1 |
| -5 | 4 | 0.4 |
| -4 | 23 | 2.3 |
| -3 | 52 | 5.2 |
| -2 | 127 | 12.7 |
| -1 | 186 | 18.6 |
| 0 | 231 | 23.1 |
| +1 | 170 | 17.0 |
| +2 | 121 | 12.1 |
| +3 | 56 | 5.6 |
| +4 | 22 | 2.2 |
| +5 | 5 | 0.5 |
| +6 | 1 | 0.1 |

⟨Q⟩ = -0.029
⟨Q²⟩ = 3.368
χ_t = ⟨Q²⟩/V = 5.08 × 10⁻⁶ (lattice units)

## Correlator matrix eigenvalues

C(0): [1.48e-08, 1.76e-07, 2.07e-06, 2.62e-05]
C(1): [3.87e-10, 1.18e-08, 2.32e-07, 2.42e-06]

Both positive definite. No regularization needed.

## GEVP effective mass (τ₀ = 0, ground state)

| τ | m_eff (lattice) |
|---|---|
| 0 | 1.0297 |
| 1 | 0.8495 |
| 2 | 0.7759 |
| 3 | 0.8182 |
| 4 | 0.5964 |
| 5 | 0.4038 |
| 6 | 0.1715 |
| 7+ | noise |

## GEVP effective mass (1st excited state)

| τ | m_eff (lattice) |
|---|---|
| 0 | 2.0505 |
| 1 | 1.5104 |
| 2 | 1.5818 |
| 3 | 0.0519 |
| 4+ | noise |

## Single operator (unsmeared) effective mass

| τ | m_eff (lattice) |
|---|---|
| 0 | 2.5420 |
| 1 | 1.9530 |
| 2 | 0.9166 |
| 3 | 0.7958 |

## GEVP by topological sector (τ₀ = 0)

| Sector | configs | m(0) | m(1) | m(2) | m(3) |
|---|---|---|---|---|---|
| all | 1000 | 1.0297 | 0.8495 | 0.7759 | 0.8182 |
| Q=0 | 231 | 1.0362 | 0.8004 | 0.6439 | 0.8533 |
| \|Q\|=1 | 356 | 1.0256 | 0.9428 | 0.8807 | 0.4917 |
| \|Q\|≥2 | 413 | 1.0296 | 0.7959 | 0.7423 | 0.8977 |

## Data files

- `phase1_final.npz`: raw operators (1000 × 4 × 48), Q values, plaquette history
