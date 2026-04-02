#!/usr/bin/env python3
"""
Phase 1 — SU(2) glueball spectrum with GEVP on 24³×48.

Measures:
  - 4 operators at smearing levels 0, 5, 10, 20 (α=0.3)
  - Topological charge Q via gradient flow (t_flow=1.0)
  - Raw operator timeslices saved per config (correlators computed offline)

Parameters:
  24³×48, β=2.5, 1000 configs, 200 sweeps separation
  Estimated: ~20 hours on T4, ~$7-10 spot / ~$20 on-demand
"""

import os
import sys
import time
import argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from su2_lattice import (
    set_backend, GaugeField, correlator_matrix, solve_gevp, effective_mass, xp
)


def run(args):
    set_backend(use_gpu=args.gpu)

    dims = (args.nt, args.ns, args.ns, args.ns)
    smear_levels = [0, 5, 10, 20]
    n_ops = len(smear_levels)

    print(f"Lattice: {args.ns}**3 x {args.nt}, beta={args.beta}")
    print(f"Configs: {args.n_cfg}, skip: {args.n_skip}")
    print(f"Smearing: levels {smear_levels}, alpha={args.alpha}")
    print(f"Flow: {args.n_flow} steps x eps={args.flow_eps} = t={args.n_flow*args.flow_eps}")

    # Time one sweep
    gf = GaugeField(dims, beta=args.beta, start="hot")
    t0 = time.time()
    gf.sweep()
    dt = time.time() - t0
    total_sweeps = args.n_therm + args.n_cfg * args.n_skip
    est_hours = total_sweeps * dt / 3600
    print(f"1 sweep = {dt:.3f}s -> sweeps only: {est_hours:.1f}h")
    print()

    # Thermalize
    print("=== Thermalization ===")
    t0 = time.time()
    for i in range(1, args.n_therm + 1):
        gf.sweep()
        if i % 50 == 0:
            p = gf.plaquette()
            print(f"  sweep {i}/{args.n_therm}  P={p:.6f}  [{time.time()-t0:.0f}s]")
    print()

    # Storage: save raw operators per config (not correlators)
    os.makedirs(args.outdir, exist_ok=True)
    Nt = dims[0]

    O_all = np.zeros((args.n_cfg, n_ops, Nt))
    Q_all = np.zeros(args.n_cfg)
    plaq_all = np.zeros(args.n_cfg)

    # Checkpoint interval
    ckpt_every = 100

    print("=== Measurement ===")
    t0 = time.time()
    for icfg in range(args.n_cfg):
        # Resume from checkpoint if exists
        if icfg == 0 and os.path.exists(os.path.join(args.outdir, "checkpoint.npz")):
            ckpt = np.load(os.path.join(args.outdir, "checkpoint.npz"))
            start_cfg = int(ckpt["last_cfg"]) + 1
            if start_cfg > 0:
                O_all[:start_cfg] = ckpt["O_all"][:start_cfg]
                Q_all[:start_cfg] = ckpt["Q_all"][:start_cfg]
                plaq_all[:start_cfg] = ckpt["plaq_all"][:start_cfg]
                print(f"  Resumed from checkpoint at cfg {start_cfg}")
                # Need to re-thermalize from hot start since we don't save configs
                # This means checkpoint only saves measurements, not the Markov chain
                # For a real checkpoint we'd need to save the full gauge field
                # For now, just re-thermalize
                for _ in range(args.n_therm):
                    gf.sweep()
                icfg = start_cfg
                # Skip ahead
                for skip_cfg in range(start_cfg):
                    pass  # already loaded

        for _ in range(args.n_skip):
            gf.sweep()

        plaq_all[icfg] = gf.plaquette()

        # Multi-smearing operators
        ops, splaq = gf.multi_smear_operators(smear_levels, alpha=args.alpha)
        if hasattr(ops, 'get'):
            ops = ops.get()
        O_all[icfg] = ops

        # Topological charge with gradient flow
        Q, t_flow = gf.topological_charge_flowed(
            n_flow=args.n_flow, epsilon=args.flow_eps)
        Q_all[icfg] = Q

        if (icfg + 1) % 10 == 0:
            elapsed = time.time() - t0
            eta = elapsed / (icfg + 1) * (args.n_cfg - icfg - 1)
            print(f"  cfg {icfg+1:4d}/{args.n_cfg}  P={plaq_all[icfg]:.5f}  "
                  f"Q={Q:.2f}  [{elapsed/60:.1f}min, ETA {eta/60:.1f}min]")

        # Checkpoint
        if (icfg + 1) % ckpt_every == 0:
            np.savez(os.path.join(args.outdir, "checkpoint.npz"),
                     last_cfg=icfg, O_all=O_all, Q_all=Q_all, plaq_all=plaq_all)

    total_time = time.time() - t0
    print(f"\nDone: {args.n_cfg} configs in {total_time/3600:.2f}h")

    # Save final data
    np.savez(os.path.join(args.outdir, "phase1_operators.npz"),
             dims=np.array(dims),
             beta=args.beta,
             smear_levels=np.array(smear_levels),
             alpha=args.alpha,
             n_flow=args.n_flow,
             flow_eps=args.flow_eps,
             plaquette_history=plaq_all,
             O_all=O_all,
             Q_all=Q_all)
    print(f"Operators saved to {args.outdir}/phase1_operators.npz")

    # Offline analysis
    print("\n=== Analysis ===")

    # Plaquette
    p_mean = np.mean(plaq_all)
    p_err = np.std(plaq_all) / np.sqrt(len(plaq_all))
    print(f"Plaquette: {p_mean:.6f} +/- {p_err:.6f}")

    # Topological charge
    Q_rounded = np.round(Q_all).astype(int)
    print(f"\nTopological charge:")
    print(f"  <Q>  = {np.mean(Q_all):.3f}")
    print(f"  <Q^2> = {np.mean(Q_all**2):.3f}")
    for q in sorted(set(Q_rounded)):
        n = np.sum(Q_rounded == q)
        print(f"  Q={q:+d}: {n} configs ({100*n/len(Q_rounded):.1f}%)")

    # Correlator matrix and GEVP
    print("\nCorrelator matrix and GEVP:")
    C, C_err = correlator_matrix(O_all)

    print("  C_ij(0) eigenvalues:", np.round(np.linalg.eigvalsh(C[:, :, 0]), 2))
    print("  C_ij(1) eigenvalues:", np.round(np.linalg.eigvalsh(C[:, :, 1]), 2))

    eigenvalues, masses = solve_gevp(C, tau0=1)

    print(f"\n  GEVP effective mass (ground state):")
    for tau in range(min(6, Nt - 1)):
        if not np.isnan(masses[0, tau]):
            print(f"    m_eff(tau={tau}) = {masses[0, tau]:.4f}")

    # GEVP by topological sector
    print("\nGEVP by topological sector:")
    for q_bin_name, q_mask in [("Q=0", Q_rounded == 0),
                                ("|Q|>=1", np.abs(Q_rounded) >= 1)]:
        n_in_bin = np.sum(q_mask)
        if n_in_bin < 20:
            print(f"  {q_bin_name}: {n_in_bin} configs (too few, skipping)")
            continue

        O_bin = O_all[q_mask]
        C_bin, _ = correlator_matrix(O_bin)
        _, masses_bin = solve_gevp(C_bin, tau0=1)

        m_str = ""
        for tau in range(min(4, Nt - 1)):
            if not np.isnan(masses_bin[0, tau]):
                m_str += f"m({tau})={masses_bin[0, tau]:.3f} "
        print(f"  {q_bin_name} ({n_in_bin} cfgs): {m_str}")

    # Save analysis
    np.savez(os.path.join(args.outdir, "phase1_analysis.npz"),
             correlator=C, correlator_err=C_err,
             gevp_eigenvalues=eigenvalues, gevp_masses=masses,
             Q_rounded=Q_rounded)
    print(f"\nAnalysis saved to {args.outdir}/phase1_analysis.npz")


def main():
    p = argparse.ArgumentParser(description="Phase 1: SU(2) GEVP + topology")
    p.add_argument("--ns", type=int, default=24)
    p.add_argument("--nt", type=int, default=48)
    p.add_argument("--beta", type=float, default=2.5)
    p.add_argument("--n-therm", type=int, default=200)
    p.add_argument("--n-cfg", type=int, default=1000)
    p.add_argument("--n-skip", type=int, default=200)
    p.add_argument("--alpha", type=float, default=0.3)
    p.add_argument("--n-flow", type=int, default=100, help="Gradient flow steps")
    p.add_argument("--flow-eps", type=float, default=0.01)
    p.add_argument("--gpu", action="store_true")
    p.add_argument("--outdir", default="results")
    run(p.parse_args())


if __name__ == "__main__":
    main()
