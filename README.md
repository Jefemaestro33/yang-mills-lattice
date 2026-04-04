# Topological Structure of the Vacuum and Glueball Spectrum in SU(2)

Lattice Monte Carlo study of how topological fluctuations couple to the glueball spectrum in pure SU(2) Yang-Mills theory.

## What this project does

Three measurements that have never been done before:

1. **Glueball masses by topological sector** — First test of the Aoki-Fukaya formula for glueball masses. First measurement of m₂(SU(2)), the θ-dependence coefficient of the glueball mass.

2. **GEVP with topological operators** (priority) — First inclusion of the topological charge density q(x) in a variational basis for glueball spectroscopy. Tests whether glueballs have differentiated "topological character."

3. **Q² correlator** — First use of the composite operator Q²(t) as a spectroscopic tool in the 0⁺⁺ channel.

All four novelty claims verified by exhaustive literature search (April 2026).

## Status

**Phase 2 running** — 5000 configurations on 24³×48 at β=2.5 with:
- 4 scalar (0⁺⁺) operators: spatial plaquette at APE levels [0, 5, 10, 20]
- 4 pseudoscalar (0⁻) operators: clover q(x) at APE levels [0, 5, 10, 20]
- Q_slice(t) at 3 gradient flow times [0.5, 1.0, 2.0]
- Global topological charge Q

First 100 configs validate: ⟨Q²⟩ = 34.6 (expected ~34), σ_Q = 5.9 (expected ~5.8). ✓

## Key parameters

| Parameter | Value |
|-----------|-------|
| Gauge group | SU(2), Wilson plaquette action |
| β | 2.5 |
| Lattice | 24³ × 48 |
| a√σ | 0.190(10) |
| a | 0.085(5) fm |
| Configs | 5000 (generating) |
| Separation | 100 heat-bath sweeps |
| Gradient flow | Euler, ε=0.01, t_flow = 0.5, 1.0, 2.0 |
| Topological charge | Clover definition after gradient flow |

## Code

| File | Description |
|------|-------------|
| `su2_lattice.py` | Core library: SU(2) quaternion arithmetic, heat-bath, APE smearing, gradient flow, clover F_μν, topological charge, GEVP solver |
| `run_phase2.py` | Generation + measurement script (all observables in one pass) |
| `run_phase1.py` | Earlier script (0⁺⁺ only, superseded by phase2) |
| `analysis.py` | Offline analysis utilities |

### Key functions in `su2_lattice.py`

**Generation:**
- `GaugeField.sweep()` — Kennedy-Pendleton heat-bath with checkerboard
- `GaugeField.gradient_flow_step()` — Wilson flow, projected Euler

**Scalar (0⁺⁺) operators:**
- `GaugeField.multi_smear_operators()` — spatial plaquette at multiple APE smearing levels

**Pseudoscalar (0⁻) operators:**
- `GaugeField.multi_smear_pseudoscalar()` — clover q(x) at multiple APE smearing levels
- `GaugeField.multi_flow_measurements()` — Q_slice(t) at multiple flow times

**Topology:**
- `GaugeField.topological_charge()` — global Q from clover
- `GaugeField.topological_charge_density()` — q(x) per site
- `GaugeField.topological_charge_timeslice()` — Q_slice(t) = Σ_x q(x,t)

**Analysis:**
- `correlator_matrix()` — C_ij(τ) with VEV subtraction and jackknife
- `solve_gevp()` — generalized eigenvalue problem

## Running

```bash
# Generate 5000 configs with all measurements (GPU)
python3 run_phase2.py --gpu --n-cfg 5000 --n-skip 100 --outdir results/phase2

# Resume from checkpoint after interruption
python3 run_phase2.py --gpu --n-cfg 5000 --n-skip 100 --outdir results/phase2
# (automatically detects checkpoint and resumes)

# Different β for continuum extrapolation
python3 run_phase2.py --gpu --beta 2.6 --ns 32 --nt 64 --n-cfg 5000 --outdir results/phase2_beta26
```

## Output format

`phase2_data.npz` contains:

| Array | Shape | Description |
|-------|-------|-------------|
| `O_scalar` | (n_cfg, 4, 48) | 0⁺⁺ operators at 4 APE levels |
| `O_pseudo` | (n_cfg, 4, 48) | 0⁻ clover operators at 4 APE levels |
| `Q_slice_all` | (n_cfg, 3, 48) | Q_slice(t) at 3 flow times |
| `Q_all` | (n_cfg,) | Global Q at t_flow=1.0 |
| `plaq_all` | (n_cfg,) | Average plaquette |

## Papers

1. **"θ-dependence of the SU(2) glueball mass"** — m₂(SU(2)) at two lattice spacings
2. **"Topological charge density in the glueball variational basis"** — GEVP with q(x) operators (priority)
3. **"Spectroscopy of topological fluctuations with Q²"** — exploratory

## Documentation

- `docs/Plan_Ejecucion_YM_v2.md` — Execution plan v4.1
- `docs/Verificacion_Plan_YM_v3.md` — Fact-check of all claims and citations (v3)

## References

- Athenodorou, Teper — JHEP 12, 082 (2021) — SU(N) glueball spectrum
- Bonanno, Bonati, Papace, Vadacchino — JHEP 05, 163 (2024) — θ-dependence continuum extrapolation
- Del Debbio, Manca, Panagopoulos, Skouroupathis, Vicari — JHEP 06, 005 (2006) — θ-dependence of spectrum
- Berg, Clarke — Phys. Rev. D 97, 054506 (2018) — SU(2) topological susceptibility
- Aoki, Fukaya, Hashimoto, Onogi — Phys. Rev. D 76, 054508 (2007) — Fixed-topology formalism
- Morningstar, Peardon — Phys. Rev. D 60, 034509 (1999) — Glueball spectroscopy methods
