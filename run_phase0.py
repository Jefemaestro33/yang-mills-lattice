#!/usr/bin/env python3
"""
Phase 0 — Validation run on a small lattice.

Goal: demonstrate the code works before spending any money.
  - Lattice:  12³ × 24,  SU(2),  β = 2.5
  - Hot start → thermalize 200 sweeps
  - Generate 200 configurations, 100 sweeps apart
  - Measure: plaquette average (~0.62) and 0++ correlator

Checkpoints:
  1. ⟨P⟩ = 0.62 ± 0.01  →  heat-bath is correct
  2. Exponential decay in correlator  →  mass extraction works

Output:  results/phase0_data.npz
"""

import os
import sys
import time
import argparse
import numpy as np

from su2_lattice import set_backend, GaugeField, glueball_correlator, effective_mass


def run(args):
    # ---- backend ----------------------------------------------------------
    set_backend(use_gpu=args.gpu)

    # ---- lattice ----------------------------------------------------------
    dims = (args.nt, args.ns, args.ns, args.ns)
    print(f"\nLattice: {args.ns}³ × {args.nt},  β = {args.beta}")
    print(f"Thermalization: {args.n_therm} sweeps")
    print(f"Configurations:  {args.n_cfg},  {args.n_skip} sweeps apart\n")

    gf = GaugeField(dims, beta=args.beta, start="hot")

    # ---- thermalize -------------------------------------------------------
    print("=== Thermalization ===")
    t0 = time.time()
    gf.thermalize(args.n_therm, verbose=True)
    dt = time.time() - t0
    print(f"  done in {dt:.1f}s  ({dt/args.n_therm:.2f} s/sweep)\n")

    # ---- measurement ------------------------------------------------------
    print("=== Measurement ===")
    plaq_history = []
    O_samples = []

    t0 = time.time()
    for icfg in range(args.n_cfg):
        # decorrelation sweeps
        for _ in range(args.n_skip):
            gf.sweep()

        # measure
        p = gf.plaquette()
        plaq_history.append(p)

        from su2_lattice import xp
        O_t = gf.spatial_plaquette_timeslice()
        if xp is not np:
            O_t = O_t.get()  # cupy → numpy
        O_samples.append(O_t)

        if (icfg + 1) % 10 == 0 or icfg == 0:
            elapsed = time.time() - t0
            print(f"  cfg {icfg+1:4d}/{args.n_cfg}  ⟨P⟩ = {p:.6f}  "
                  f"[{elapsed:.0f}s elapsed]")

    dt = time.time() - t0
    print(f"\n  {args.n_cfg} configs in {dt:.1f}s  "
          f"({dt/args.n_cfg:.1f} s/cfg, {dt/args.n_cfg/args.n_skip:.2f} s/sweep)\n")

    # ---- results ----------------------------------------------------------
    plaq_history = np.array(plaq_history)
    O_samples = np.array(O_samples)  # (n_cfg, Nt)

    plaq_mean = np.mean(plaq_history)
    plaq_err = np.std(plaq_history) / np.sqrt(len(plaq_history))

    print("=== Results ===")
    print(f"  ⟨P⟩ = {plaq_mean:.6f} ± {plaq_err:.6f}")
    print(f"  Expected for SU(2) β=2.5: ~0.62")

    if abs(plaq_mean - 0.62) < 0.02:
        print("  ✓ Plaquette CHECK PASSED")
    else:
        print("  ✗ Plaquette CHECK FAILED — possible bug")

    # correlator
    C, C_err = glueball_correlator(O_samples)
    m_eff, m_err = effective_mass(C, C_err)

    print(f"\n  Effective mass (lattice units):")
    for tau in range(min(8, len(m_eff))):
        if not np.isnan(m_eff[tau]):
            err_str = f" ± {m_err[tau]:.4f}" if m_err is not None and not np.isnan(m_err[tau]) else ""
            print(f"    m_eff(τ={tau}) = {m_eff[tau]:.4f}{err_str}")

    # ---- save -------------------------------------------------------------
    os.makedirs("results", exist_ok=True)
    outfile = os.path.join("results", "phase0_data.npz")
    np.savez(
        outfile,
        dims=np.array(dims),
        beta=args.beta,
        plaquette_history=plaq_history,
        O_timeslice=O_samples,
        correlator=C,
        correlator_err=C_err,
        effective_mass=m_eff,
        effective_mass_err=m_err if m_err is not None else np.array([]),
    )
    print(f"\n  Data saved to {outfile}")


def main():
    parser = argparse.ArgumentParser(description="Phase 0: SU(2) lattice validation")
    parser.add_argument("--ns", type=int, default=12, help="Spatial extent (default: 12)")
    parser.add_argument("--nt", type=int, default=24, help="Temporal extent (default: 24)")
    parser.add_argument("--beta", type=float, default=2.5, help="Coupling (default: 2.5)")
    parser.add_argument("--n-therm", type=int, default=200, help="Thermalization sweeps (default: 200)")
    parser.add_argument("--n-cfg", type=int, default=200, help="Configurations (default: 200)")
    parser.add_argument("--n-skip", type=int, default=100, help="Sweeps between configs (default: 100)")
    parser.add_argument("--gpu", action="store_true", help="Use CuPy GPU backend")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
