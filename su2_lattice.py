"""
SU(2) Lattice Gauge Theory — Vectorized Implementation

Pure SU(2) Yang-Mills on a 4D Euclidean lattice with Wilson action.
Kennedy-Pendleton heat-bath, checkerboard parallelization.

Quaternion convention:
    U = a0·I + i·(a1·σ1 + a2·σ2 + a3·σ3)
    stored as ndarray with last axis = 4: (a0, a1, a2, a3)
    constraint: a0² + a1² + a2² + a3² = 1

Backend: numpy (CPU) or cupy (GPU), selected at runtime.
"""

import numpy as np

# ---------------------------------------------------------------------------
# Backend (numpy / cupy)
# ---------------------------------------------------------------------------

xp = np  # global backend, switched by set_backend()


def set_backend(use_gpu=True):
    """Switch between numpy (CPU) and cupy (GPU)."""
    global xp
    if use_gpu:
        try:
            import cupy as cp
            xp = cp
            print(f"Backend: CuPy (GPU) — {cp.cuda.runtime.getDeviceProperties(0)['name'].decode()}")
            return
        except Exception:
            pass
    xp = np
    print("Backend: NumPy (CPU)")


# ---------------------------------------------------------------------------
# SU(2) quaternion arithmetic
# ---------------------------------------------------------------------------

def qmul(u, v):
    """Quaternion product u·v  (batch, last axis = 4)."""
    a0, a1, a2, a3 = u[..., 0], u[..., 1], u[..., 2], u[..., 3]
    b0, b1, b2, b3 = v[..., 0], v[..., 1], v[..., 2], v[..., 3]
    return xp.stack([
        a0*b0 - a1*b1 - a2*b2 - a3*b3,
        a0*b1 + a1*b0 + a2*b3 - a3*b2,
        a0*b2 - a1*b3 + a2*b0 + a3*b1,
        a0*b3 + a1*b2 - a2*b1 + a3*b0,
    ], axis=-1)


def qdagger(u):
    """Hermitian conjugate (= inverse for SU(2)): (a0, -a1, -a2, -a3)."""
    r = u.copy()
    r[..., 1:] *= -1
    return r


def qnorm(u):
    """Quaternion norm  sqrt(a0² + a1² + a2² + a3²)."""
    return xp.sqrt(xp.sum(u ** 2, axis=-1))


def qnormalize(u):
    """Project onto unit quaternion (SU(2))."""
    n = qnorm(u)[..., xp.newaxis]
    return u / xp.maximum(n, 1e-30)


def qidentity(shape):
    """Batch of identity quaternions (1, 0, 0, 0).  Returns shape + (4,)."""
    u = xp.zeros(shape + (4,))
    u[..., 0] = 1.0
    return u


def qrandom(shape):
    """Haar-uniform random SU(2) elements.  Returns shape + (4,)."""
    u = xp.random.standard_normal(shape + (4,))
    return qnormalize(u)


# ---------------------------------------------------------------------------
# Gauge field
# ---------------------------------------------------------------------------

class GaugeField:
    """
    SU(2) gauge field on a 4D Euclidean lattice.

    Wilson action:  S = β Σ_{x, μ<ν} [1 - (1/2) Re Tr U_{μν}(x)]

    Attributes
    ----------
    U : ndarray, shape (4, Nt, Nx, Ny, Nz, 4)
        First axis = link direction μ ∈ {0,1,2,3}.
        Last axis  = quaternion components.
    """

    def __init__(self, dims, beta, start="hot"):
        self.dims = tuple(dims)          # (Nt, Nx, Ny, Nz)
        self.beta = float(beta)
        if start == "hot":
            self.U = qrandom((4,) + self.dims)
        else:
            self.U = qidentity((4,) + self.dims)
        # checkerboard parity  (t + x + y + z) mod 2
        idx = xp.indices(self.dims)
        self.parity = (idx[0] + idx[1] + idx[2] + idx[3]) % 2

    @property
    def volume(self):
        v = 1
        for d in self.dims:
            v *= d
        return v

    # ---- helpers ----------------------------------------------------------

    def _shift(self, field, mu, fwd=True):
        """field(x) → field(x ± μ̂).  mu indexes within (Nt, Nx, Ny, Nz, 4)."""
        return xp.roll(field, -1 if fwd else +1, axis=mu)

    # ---- staple -----------------------------------------------------------

    def _staple(self, mu):
        """
        Sum of staples around link U_μ(x) for ALL sites.

        V_μ(x) = Σ_{ν≠μ} [ upper(ν) + lower(ν) ]

        upper(ν) = U_ν(x+μ̂) · U_μ†(x+ν̂) · U_ν†(x)
        lower(ν) = U_ν†(x+μ̂−ν̂) · U_μ†(x−ν̂) · U_ν(x−ν̂)

        Returns shape (Nt, Nx, Ny, Nz, 4)  — general quaternion (not unit).
        """
        V = xp.zeros_like(self.U[mu])
        for nu in range(4):
            if nu == mu:
                continue
            # upper staple
            u1 = self._shift(self.U[nu], mu, fwd=True)        # U_ν(x+μ̂)
            u2 = qdagger(self._shift(self.U[mu], nu, fwd=True))  # U_μ†(x+ν̂)
            u3 = qdagger(self.U[nu])                            # U_ν†(x)
            upper = qmul(qmul(u1, u2), u3)

            # lower staple
            u4 = qdagger(self._shift(                           # U_ν†(x+μ̂−ν̂)
                self._shift(self.U[nu], mu, fwd=True), nu, fwd=False))
            u5 = qdagger(self._shift(self.U[mu], nu, fwd=False))  # U_μ†(x−ν̂)
            u6 = self._shift(self.U[nu], nu, fwd=False)           # U_ν(x−ν̂)
            lower = qmul(qmul(u4, u5), u6)

            V = V + upper + lower
        return V

    # ---- heat-bath --------------------------------------------------------

    def _sample_a0(self, alpha_flat):
        """
        Sample a0 from  P(a0) ∝ √(1 − a0²) · exp(α·a0)   on [−1, 1].

        Uses Creutz/Fabricius-Haan method:
          1. Proposal from  exp(α·a0)  via inverse CDF.
          2. Accept/reject with  √(1 − a0²)   (Haar measure).

        Parameters
        ----------
        alpha_flat : 1-D array, shape (n,)

        Returns
        -------
        a0 : 1-D array, shape (n,)
        """
        n = alpha_flat.shape[0]
        a0 = xp.empty(n)
        todo = xp.ones(n, dtype=bool)

        while int(xp.sum(todo)) > 0:
            m = int(xp.sum(todo))
            al = xp.maximum(alpha_flat[todo], 1e-10)

            r1 = xp.random.uniform(0.0, 1.0, m)
            exp_m2a = xp.exp(-2.0 * al)
            x = 1.0 + xp.log(exp_m2a + r1 * (1.0 - exp_m2a)) / al
            x = xp.clip(x, -1.0, 1.0)

            r2 = xp.random.uniform(0.0, 1.0, m)
            accept = r2 ** 2 <= 1.0 - x ** 2

            # write accepted values back
            todo_idx = xp.where(todo)[0]
            acc_idx = todo_idx[accept]
            a0[acc_idx] = x[accept]
            todo[acc_idx] = False

        return a0

    def _heatbath_update(self, mu, par):
        """Heat-bath update of U_μ at all sites with parity == par."""
        V = self._staple(mu)                       # (Nt, Nx, Ny, Nz, 4)
        k = qnorm(V)                               # (Nt, Nx, Ny, Nz)
        alpha = self.beta * k                       # α = β·k  (correct, no factor ½)
        V_hat = qnormalize(V)                       # V̂ ∈ SU(2)

        mask = self.parity == par                   # (Nt, Nx, Ny, Nz)
        n_sites = int(xp.sum(mask))

        # --- sample W = (w0, w1, w2, w3) from Haar × exp(α w0) -----------
        alpha_flat = alpha[mask]                    # (n_sites,)
        w0 = self._sample_a0(alpha_flat)            # includes √(1−w0²) Haar factor

        r = xp.sqrt(xp.maximum(1.0 - w0 ** 2, 0.0))
        phi = xp.random.uniform(0.0, 2.0 * np.pi, n_sites)
        cos_th = xp.random.uniform(-1.0, 1.0, n_sites)
        sin_th = xp.sqrt(1.0 - cos_th ** 2)

        W = xp.stack([
            w0,
            r * sin_th * xp.cos(phi),
            r * sin_th * xp.sin(phi),
            r * cos_th,
        ], axis=-1)                                 # (n_sites, 4)

        # --- U_new = W · V̂†  (recover from change of variable) -----------
        V_hat_masked = V_hat[mask]                  # (n_sites, 4)
        U_new = qmul(W, qdagger(V_hat_masked))     # (n_sites, 4)

        self.U[mu][mask] = U_new

    def sweep(self):
        """One full sweep: checkerboard heat-bath over all links."""
        for mu in range(4):
            for par in (0, 1):
                self._heatbath_update(mu, par)

    def thermalize(self, n_sweeps, verbose=True):
        """Run n_sweeps sweeps, printing plaquette every 10."""
        for i in range(1, n_sweeps + 1):
            self.sweep()
            if verbose and (i % 10 == 0 or i == 1):
                print(f"  therm sweep {i:4d}/{n_sweeps}  ⟨P⟩ = {self.plaquette():.6f}")

    # ---- observables ------------------------------------------------------

    def _plaquette_field(self, mu, nu):
        """(1/2) Re Tr U_{μν}(x) = a0 of quaternion product.  Shape (Nt,Nx,Ny,Nz)."""
        P = qmul(
            qmul(self.U[mu], self._shift(self.U[nu], mu, fwd=True)),
            qmul(qdagger(self._shift(self.U[mu], nu, fwd=True)), qdagger(self.U[nu])),
        )
        return P[..., 0]    # a0 = (1/2) Re Tr P

    def plaquette(self):
        """Average plaquette  ⟨P⟩ = (1/6V) Σ_{x, μ<ν} (1/2) Re Tr U_{μν}."""
        s = 0.0
        for mu in range(4):
            for nu in range(mu + 1, 4):
                s += float(xp.mean(self._plaquette_field(mu, nu)))
        return s / 6.0

    def spatial_plaquette_timeslice(self):
        """
        O(t) = Σ_{x⃗} Σ_{i<j spatial} (1/2) Re Tr P_{ij}(x⃗, t)

        Returns shape (Nt,).  This is the 0++ glueball interpolating operator
        at zero spatial momentum.
        """
        Nt = self.dims[0]
        O = xp.zeros(Nt)
        for mu in range(1, 4):
            for nu in range(mu + 1, 4):
                pf = self._plaquette_field(mu, nu)   # (Nt, Nx, Ny, Nz)
                O = O + xp.sum(pf, axis=(1, 2, 3))   # sum over spatial
        return O

    def smeared_spatial_plaquette_timeslice(self, n_smear=20, alpha=0.5):
        """
        0++ glueball operator built from APE-smeared spatial links.

        APE smearing: iteratively replace each spatial link U_i(x) with
            U_i' = Proj_SU2[(1-α)U_i + (α/4) Σ_{j≠i,spatial} staple_j]
        Only spatial links (i=1,2,3) are smeared; temporal links untouched.
        This dramatically improves overlap with the glueball ground state.

        Parameters
        ----------
        n_smear : int   — number of smearing iterations (default 20)
        alpha   : float — smearing fraction (default 0.5)
        """
        # Work on a COPY of spatial links — don't modify the gauge field
        U_sm = [None, self.U[1].copy(), self.U[2].copy(), self.U[3].copy()]

        for _ in range(n_smear):
            U_new = [None, None, None, None]
            for i in range(1, 4):
                staple = xp.zeros_like(U_sm[i])
                for j in range(1, 4):
                    if j == i:
                        continue
                    # upper spatial staple: U_j(x+î) · U_i†(x+ĵ) · U_j†(x)
                    upper = qmul(qmul(
                        self._shift(U_sm[j], i, fwd=True),
                        qdagger(self._shift(U_sm[i], j, fwd=True))),
                        qdagger(U_sm[j]))
                    # lower spatial staple: U_j†(x+î-ĵ) · U_i†(x-ĵ) · U_j(x-ĵ)
                    lower = qmul(qmul(
                        qdagger(self._shift(
                            self._shift(U_sm[j], i, fwd=True), j, fwd=False)),
                        qdagger(self._shift(U_sm[i], j, fwd=False))),
                        self._shift(U_sm[j], j, fwd=False))
                    staple = staple + upper + lower
                # Blend and project back to SU(2)
                blended = (1.0 - alpha) * U_sm[i] + (alpha / 4.0) * staple
                U_new[i] = qnormalize(blended)
            U_sm[1], U_sm[2], U_sm[3] = U_new[1], U_new[2], U_new[3]

        # Measure spatial plaquettes with smeared links
        Nt = self.dims[0]
        O = xp.zeros(Nt)
        for mu in range(1, 4):
            for nu in range(mu + 1, 4):
                P = qmul(
                    qmul(U_sm[mu], self._shift(U_sm[nu], mu, fwd=True)),
                    qmul(qdagger(self._shift(U_sm[mu], nu, fwd=True)),
                         qdagger(U_sm[nu])))
                O = O + xp.sum(P[..., 0], axis=(1, 2, 3))
        return O

    def topological_charge(self):
        """
        Naive lattice topological charge (clover definition).
        Q = (1/32π²) Σ_x εμνρσ Tr[F_μν F_ρσ]
        Computed from clover-leaf F_μν.
        Returns float.
        """
        # Clover plaquette in each plane
        def _clover(mu, nu):
            """(1/4)(P_{μν} + P_{ν,-μ} + P_{-μ,-ν} + P_{-ν,μ}) at each site."""
            p1 = self._plaq_quat(mu, nu)
            p2 = self._plaq_quat_rev(nu, mu)
            p3 = self._plaq_quat_rev(mu, nu)
            p4 = self._plaq_quat(nu, mu)
            # Anti-hermitian traceless part ~ F_μν
            c = p1 + p2 + p3 + p4
            return c

        # For the topological charge we need the full quaternion plaquettes,
        # not just traces. This is a placeholder for Phase 1+.
        # For Phase 0, we skip this.
        raise NotImplementedError("Topological charge requires Phase 1 implementation")


# ---------------------------------------------------------------------------
# Correlator analysis
# ---------------------------------------------------------------------------

def glueball_correlator(O_samples):
    """
    C(τ) = ⟨O(t+τ) O(t)⟩_{t,configs} − ⟨O⟩²

    Parameters
    ----------
    O_samples : ndarray, shape (n_configs, Nt)

    Returns
    -------
    C     : ndarray, shape (Nt,)      — correlator
    C_err : ndarray, shape (Nt,)      — jackknife error
    """
    n_cfg, Nt = O_samples.shape
    O_mean = np.mean(O_samples)

    # correlator per config (average over source time t)
    C_per_cfg = np.zeros((n_cfg, Nt))
    for tau in range(Nt):
        O_shifted = np.roll(O_samples, -tau, axis=1)
        C_per_cfg[:, tau] = np.mean(O_samples * O_shifted, axis=1)
    C_per_cfg -= O_mean ** 2                       # VEV subtraction (Bug 4 fix)

    C = np.mean(C_per_cfg, axis=0)

    # jackknife
    C_jack = np.zeros((n_cfg, Nt))
    for j in range(n_cfg):
        leave_out = np.delete(O_samples, j, axis=0)
        Om_j = np.mean(leave_out)
        for tau in range(Nt):
            O_sh = np.roll(leave_out, -tau, axis=1)
            C_jack[j, tau] = np.mean(leave_out * O_sh) - Om_j ** 2

    C_err = np.sqrt((n_cfg - 1) * np.mean((C_jack - C[None, :]) ** 2, axis=0))
    return C, C_err


def effective_mass(C, C_err=None):
    """
    m_eff(τ) = ln |C(τ) / C(τ+1)|

    Returns m, dm (both shape (Nt-1,)).  NaN where undefined.
    """
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.abs(C[:-1]) / np.maximum(np.abs(C[1:]), 1e-30)
        m = np.log(ratio)
        bad = (C[:-1] <= 0) | (C[1:] <= 0)
        m[bad] = np.nan

    if C_err is not None:
        with np.errstate(divide="ignore", invalid="ignore"):
            dm = np.sqrt(
                (C_err[:-1] / np.maximum(np.abs(C[:-1]), 1e-30)) ** 2
                + (C_err[1:] / np.maximum(np.abs(C[1:]), 1e-30)) ** 2
            )
            dm[bad] = np.nan
        return m, dm
    return m, None
