#!/usr/bin/env python3
"""
Phase 0 analysis — load saved data, make diagnostic plots.

Usage:
    python analysis.py [results/phase0_data.npz]
"""

import sys
import numpy as np
import matplotlib.pyplot as plt


def load_data(path="results/phase0_data.npz"):
    d = np.load(path)
    return {k: d[k] for k in d.files}


def plot_plaquette_history(data, ax):
    """Plaquette vs configuration number."""
    plaq = data["plaquette_history"]
    ax.plot(plaq, "o-", ms=2, lw=0.5)
    ax.axhline(np.mean(plaq), color="r", ls="--", label=f"⟨P⟩ = {np.mean(plaq):.5f}")
    ax.axhline(0.62, color="gray", ls=":", alpha=0.5, label="expected ~0.62")
    ax.set_xlabel("Configuration")
    ax.set_ylabel("⟨P⟩")
    ax.set_title("Plaquette history")
    ax.legend(fontsize=8)


def plot_correlator(data, ax):
    """C(τ) with error bars (log scale)."""
    C = data["correlator"]
    C_err = data["correlator_err"]
    Nt = len(C)
    tau = np.arange(Nt)

    # Only plot where C > 0
    pos = C > 0
    ax.errorbar(tau[pos], C[pos], yerr=C_err[pos], fmt="o-", ms=3, lw=0.8, capsize=2)
    ax.set_yscale("log")
    ax.set_xlabel("τ (lattice units)")
    ax.set_ylabel("C(τ)")
    ax.set_title("Glueball correlator (0⁺⁺)")
    ax.set_xlim(-0.5, Nt // 2 + 1)


def plot_effective_mass(data, ax):
    """m_eff(τ) with error bars."""
    m = data["effective_mass"]
    m_err = data["effective_mass_err"] if len(data["effective_mass_err"]) > 0 else None
    Nt = len(m)
    tau = np.arange(Nt)

    good = ~np.isnan(m)
    if m_err is not None:
        good &= ~np.isnan(m_err)
        ax.errorbar(tau[good], m[good], yerr=m_err[good], fmt="s-", ms=4, lw=0.8, capsize=2)
    else:
        ax.plot(tau[good], m[good], "s-", ms=4, lw=0.8)

    ax.set_xlabel("τ (lattice units)")
    ax.set_ylabel("m_eff(τ) [lattice units]")
    ax.set_title("Effective mass")
    ax.set_xlim(-0.5, min(12, Nt))

    # If there's a visible plateau, highlight it
    if np.sum(good) > 3:
        # rough plateau: τ = 1..4
        plateau = m[1:5]
        plateau = plateau[~np.isnan(plateau)]
        if len(plateau) > 0:
            m_plat = np.mean(plateau)
            ax.axhline(m_plat, color="r", ls="--", alpha=0.5,
                        label=f"plateau ~ {m_plat:.3f}")
            ax.legend(fontsize=8)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "results/phase0_data.npz"
    data = load_data(path)

    dims = data["dims"]
    beta = float(data["beta"])
    plaq = data["plaquette_history"]

    print(f"Lattice: {dims[1]}³ × {dims[0]},  β = {beta}")
    print(f"Configs: {len(plaq)}")
    print(f"⟨P⟩ = {np.mean(plaq):.6f} ± {np.std(plaq)/np.sqrt(len(plaq)):.6f}")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    plot_plaquette_history(data, axes[0])
    plot_correlator(data, axes[1])
    plot_effective_mass(data, axes[2])

    fig.suptitle(f"Phase 0 — SU(2)  {dims[1]}³×{dims[0]}  β={beta}", fontsize=13)
    fig.tight_layout()

    outpath = path.replace(".npz", "_plots.png")
    fig.savefig(outpath, dpi=150)
    print(f"\nPlots saved to {outpath}")
    plt.show()


if __name__ == "__main__":
    main()
