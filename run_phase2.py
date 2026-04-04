#!/usr/bin/env python3
"""
Phase 2 — Full measurement run for Papers 1 & 2.

Measures per configuration:
  - 4 scalar (0++) operators: spatial plaquette at APE levels [0, 5, 10, 20]
  - 4 pseudoscalar (0-) operators: clover q(x) at APE levels [0, 5, 10, 20]
  - Q_slice(t) at 3 gradient flow times [0.5, 1.0, 2.0]
  - Global Q (from t_flow=1.0)
  - Plaquette

Parameters:
  24³×48, β=2.5, 5000 configs, 100 sweeps separation
  Gradient flow: Euler, ε=0.01, up to t=2.0 (200 steps)
"""

import os
import sys
import time
import argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from su2_lattice import set_backend, GaugeField, xp


def run(args):
    set_backend(use_gpu=args.gpu)

    dims = (args.nt, args.ns, args.ns, args.ns)
    smear_levels = [0, 5, 10, 20]
    flow_times = [0.5, 1.0, 2.0]
    n_ops_scalar = len(smear_levels)
    n_ops_pseudo = len(smear_levels)
    n_flow_ops = len(flow_times)
    Nt = args.nt

    print(f"=== Phase 2: Full measurement run ===")
    print(f"Lattice: {args.ns}³ × {args.nt}, β={args.beta}")
    print(f"Configs: {args.n_cfg}, separation: {args.n_skip} sweeps")
    print(f"Smearing: APE levels {smear_levels}, α={args.alpha}")
    print(f"Flow times: {flow_times}, ε={args.flow_eps}")
    print()

    # Initialize gauge field
    gf = GaugeField(dims, beta=args.beta, start="hot")

    # Time one sweep for ETA
    t0 = time.time()
    gf.sweep()
    dt_sweep = time.time() - t0
    est_hours = (args.n_therm + args.n_cfg * args.n_skip) * dt_sweep / 3600
    print(f"1 sweep = {dt_sweep:.3f}s")
    print(f"Estimated sweep time: {est_hours:.1f}h (not counting measurements)")
    print()

    # Thermalize
    print("=== Thermalization ===")
    t0 = time.time()
    for i in range(1, args.n_therm + 1):
        gf.sweep()
        if i % 100 == 0 or i == 1:
            p = gf.plaquette()
            print(f"  sweep {i}/{args.n_therm}  P={p:.6f}  [{time.time()-t0:.0f}s]")
    print()

    # Storage arrays
    os.makedirs(args.outdir, exist_ok=True)
    O_scalar = np.zeros((args.n_cfg, n_ops_scalar, Nt))
    O_pseudo = np.zeros((args.n_cfg, n_ops_pseudo, Nt))
    Q_slice_all = np.zeros((args.n_cfg, n_flow_ops, Nt))
    Q_all = np.zeros(args.n_cfg)
    plaq_all = np.zeros(args.n_cfg)

    # Check for checkpoint
    ckpt_path = os.path.join(args.outdir, "phase2_checkpoint.npz")
    start_cfg = 0
    if os.path.exists(ckpt_path):
        ckpt = np.load(ckpt_path)
        start_cfg = int(ckpt["last_cfg"]) + 1
        if start_cfg > 0 and start_cfg < args.n_cfg:
            O_scalar[:start_cfg] = ckpt["O_scalar"][:start_cfg]
            O_pseudo[:start_cfg] = ckpt["O_pseudo"][:start_cfg]
            Q_slice_all[:start_cfg] = ckpt["Q_slice_all"][:start_cfg]
            Q_all[:start_cfg] = ckpt["Q_all"][:start_cfg]
            plaq_all[:start_cfg] = ckpt["plaq_all"][:start_cfg]
            print(f"Resumed from checkpoint at cfg {start_cfg}")
            # Re-thermalize since we don't save gauge field state
            print("Re-thermalizing...")
            for _ in range(args.n_therm):
                gf.sweep()
        else:
            start_cfg = 0

    print("=== Measurement ===")
    t0 = time.time()
    for icfg in range(start_cfg, args.n_cfg):
        # Decorrelation sweeps
        for _ in range(args.n_skip):
            gf.sweep()

        # Plaquette
        plaq_all[icfg] = gf.plaquette()

        # 0++ operators (spatial plaquette, 4 APE levels)
        ops_s, _ = gf.multi_smear_operators(smear_levels, alpha=args.alpha)
        if hasattr(ops_s, 'get'):
            ops_s = ops_s.get()
        O_scalar[icfg] = ops_s

        # 0- operators (clover q(x), 4 APE levels)
        ops_p = gf.multi_smear_pseudoscalar(smear_levels, alpha=args.alpha)
        if hasattr(ops_p, 'get'):
            ops_p = ops_p.get()
        O_pseudo[icfg] = ops_p

        # Gradient flow: Q_slice at 3 flow times + global Q
        flow_res = gf.multi_flow_measurements(
            flow_times=flow_times, epsilon=args.flow_eps)
        Q_all[icfg] = flow_res['Q'][1]  # Q at t_flow=1.0
        for iflow in range(n_flow_ops):
            Q_slice_all[icfg, iflow] = flow_res['Q_slice'][iflow]

        # Progress
        if (icfg + 1) % 10 == 0:
            elapsed = time.time() - t0
            rate = elapsed / (icfg + 1 - start_cfg)
            eta = rate * (args.n_cfg - icfg - 1)
            Q = Q_all[icfg]
            print(f"  cfg {icfg+1:5d}/{args.n_cfg}  P={plaq_all[icfg]:.5f}  "
                  f"Q={Q:.2f}  [{elapsed/3600:.1f}h, ETA {eta/3600:.1f}h]")

        # Checkpoint every 100 configs
        if (icfg + 1) % 100 == 0:
            np.savez(ckpt_path,
                     last_cfg=icfg,
                     O_scalar=O_scalar, O_pseudo=O_pseudo,
                     Q_slice_all=Q_slice_all, Q_all=Q_all,
                     plaq_all=plaq_all)
            print(f"  [checkpoint saved at cfg {icfg+1}]")

    total_time = time.time() - t0
    print(f"\nDone: {args.n_cfg - start_cfg} configs in {total_time/3600:.2f}h")

    # Save final data
    outfile = os.path.join(args.outdir, "phase2_data.npz")
    np.savez(outfile,
             dims=np.array(dims),
             beta=args.beta,
             smear_levels=np.array(smear_levels),
             alpha=args.alpha,
             flow_times=np.array(flow_times),
             flow_eps=args.flow_eps,
             n_skip=args.n_skip,
             O_scalar=O_scalar,           # (n_cfg, 4, Nt) — 0++ operators
             O_pseudo=O_pseudo,           # (n_cfg, 4, Nt) — 0- clover operators
             Q_slice_all=Q_slice_all,     # (n_cfg, 3, Nt) — Q_slice at 3 flow times
             Q_all=Q_all,                 # (n_cfg,) — global Q at t_flow=1.0
             plaq_all=plaq_all)           # (n_cfg,) — plaquette
    print(f"Data saved to {outfile}")

    # Quick analysis
    print("\n=== Quick Analysis ===")

    # Plaquette
    print(f"Plaquette: {np.mean(plaq_all):.6f} ± {np.std(plaq_all)/np.sqrt(len(plaq_all)):.6f}")

    # Topological charge
    Q_round = np.round(Q_all).astype(int)
    print(f"\n<Q>   = {np.mean(Q_all):.3f}")
    print(f"<Q²>  = {np.mean(Q_all**2):.3f}  (expected ~34 for 24³×48)")
    print(f"σ_Q   = {np.std(Q_all):.3f}")
    print(f"|Q-round(Q)| mean = {np.mean(np.abs(Q_all - Q_round)):.3f}")

    # Q distribution
    print(f"\nQ distribution:")
    for q in sorted(set(Q_round)):
        n = np.sum(Q_round == q)
        if n > 0:
            print(f"  Q={q:+3d}: {n:4d} ({100*n/len(Q_round):5.1f}%)")


def main():
    p = argparse.ArgumentParser(description="Phase 2: Full run for Papers 1 & 2")
    p.add_argument("--ns", type=int, default=24)
    p.add_argument("--nt", type=int, default=48)
    p.add_argument("--beta", type=float, default=2.5)
    p.add_argument("--n-therm", type=int, default=500)
    p.add_argument("--n-cfg", type=int, default=5000)
    p.add_argument("--n-skip", type=int, default=100)
    p.add_argument("--alpha", type=float, default=0.3)
    p.add_argument("--flow-eps", type=float, default=0.01)
    p.add_argument("--gpu", action="store_true")
    p.add_argument("--outdir", default="results/phase2")
    run(p.parse_args())


if __name__ == "__main__":
    main()
