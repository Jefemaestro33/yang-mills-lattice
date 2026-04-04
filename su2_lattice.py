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


def qnormalize_pos(u):
    """Project onto SU(2) and flip to a0 > 0 hemisphere.

    U and -U represent the same SU(2) element (center Z₂ ambiguity).
    For smearing, we must pick a consistent sign to prevent cancellations.
    """
    v = qnormalize(u)
    sign = xp.sign(v[..., 0:1])             # sign of a0
    sign = xp.where(sign == 0, 1.0, sign)   # handle exact zero
    return v * sign


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

    def _ape_smear(self, n_smear, alpha):
        """
        APE smearing of spatial links.

        Iteratively replace each spatial link U_i(x) with
            U_i' = Proj_SU2[(1-α)U_i + (α/4) Σ_{j≠i,spatial} C_j]
        where C_j is the smearing staple (NOT the action staple):
            upper: U_j(x) · U_i(x+ĵ) · U_j†(x+î)
            lower: U_j†(x-ĵ) · U_i(x-ĵ) · U_j(x-ĵ+î)
        Only spatial links (i=1,2,3) are smeared; temporal links untouched.

        Returns list [None, U1_sm, U2_sm, U3_sm] of smeared spatial links.
        """
        U_sm = [None, self.U[1].copy(), self.U[2].copy(), self.U[3].copy()]

        for _ in range(n_smear):
            U_new = [None, None, None, None]
            for i in range(1, 4):
                staple = xp.zeros_like(U_sm[i])
                for j in range(1, 4):
                    if j == i:
                        continue
                    # Upper smearing staple: U_j(x) · U_i(x+ĵ) · U_j†(x+î)
                    upper = qmul(qmul(
                        U_sm[j],
                        self._shift(U_sm[i], j, fwd=True)),
                        qdagger(self._shift(U_sm[j], i, fwd=True)))
                    # Lower smearing staple: U_j†(x-ĵ) · U_i(x-ĵ) · U_j(x-ĵ+î)
                    lower = qmul(qmul(
                        qdagger(self._shift(U_sm[j], j, fwd=False)),
                        self._shift(U_sm[i], j, fwd=False)),
                        self._shift(self._shift(U_sm[j], j, fwd=False), i, fwd=True))
                    staple = staple + upper + lower
                blended = (1.0 - alpha) * U_sm[i] + (alpha / 4.0) * staple
                U_new[i] = qnormalize(blended)
            U_sm[1], U_sm[2], U_sm[3] = U_new[1], U_new[2], U_new[3]

        return U_sm

    def _spatial_plaq_timeslice_from_links(self, U_links):
        """
        O(t) from given spatial links [None, U1, U2, U3].
        Returns shape (Nt,).
        """
        Nt = self.dims[0]
        O = xp.zeros(Nt)
        for mu in range(1, 4):
            for nu in range(mu + 1, 4):
                P = qmul(
                    qmul(U_links[mu], self._shift(U_links[nu], mu, fwd=True)),
                    qmul(qdagger(self._shift(U_links[mu], nu, fwd=True)),
                         qdagger(U_links[nu])))
                O = O + xp.sum(P[..., 0], axis=(1, 2, 3))
        return O

    def _smeared_plaquette_avg(self, U_links):
        """Average spatial plaquette from smeared links. For validation."""
        s = 0.0
        count = 0
        for mu in range(1, 4):
            for nu in range(mu + 1, 4):
                P = qmul(
                    qmul(U_links[mu], self._shift(U_links[nu], mu, fwd=True)),
                    qmul(qdagger(self._shift(U_links[mu], nu, fwd=True)),
                         qdagger(U_links[nu])))
                s += float(xp.mean(P[..., 0]))
                count += 1
        return s / count

    def multi_smear_operators(self, smear_levels, alpha=0.3):
        """
        Measure 0++ glueball operators at multiple smearing levels.

        Parameters
        ----------
        smear_levels : list of int — e.g. [0, 5, 10, 20]
        alpha        : float — APE smearing parameter

        Returns
        -------
        operators : ndarray, shape (n_levels, Nt)
        smeared_plaq : list of float — avg spatial plaquette at each level (for validation)
        """
        Nt = self.dims[0]
        n_levels = len(smear_levels)
        operators = xp.zeros((n_levels, Nt))
        smeared_plaq = []

        # Sort levels so we can smear incrementally
        sorted_idx = sorted(range(n_levels), key=lambda k: smear_levels[k])
        sorted_levels = [smear_levels[k] for k in sorted_idx]

        # Start from unsmeared spatial links
        U_sm = [None, self.U[1].copy(), self.U[2].copy(), self.U[3].copy()]
        current_n = 0

        for rank, idx in enumerate(sorted_idx):
            target_n = sorted_levels[rank]
            # Smear incrementally from current level to target
            if target_n > current_n:
                delta = target_n - current_n
                for _ in range(delta):
                    U_new = [None, None, None, None]
                    for i in range(1, 4):
                        staple = xp.zeros_like(U_sm[i])
                        for j in range(1, 4):
                            if j == i:
                                continue
                            upper = qmul(qmul(
                                U_sm[j],
                                self._shift(U_sm[i], j, fwd=True)),
                                qdagger(self._shift(U_sm[j], i, fwd=True)))
                            lower = qmul(qmul(
                                qdagger(self._shift(U_sm[j], j, fwd=False)),
                                self._shift(U_sm[i], j, fwd=False)),
                                self._shift(self._shift(U_sm[j], j, fwd=False), i, fwd=True))
                            staple = staple + upper + lower
                        blended = (1.0 - alpha) * U_sm[i] + (alpha / 4.0) * staple
                        U_new[i] = qnormalize(blended)
                    U_sm[1], U_sm[2], U_sm[3] = U_new[1], U_new[2], U_new[3]
                current_n = target_n

            # Measure operator at this level
            operators[idx] = self._spatial_plaq_timeslice_from_links(U_sm)
            smeared_plaq.append(self._smeared_plaquette_avg(U_sm))

        # Reorder smeared_plaq to match original level order
        plaq_ordered = [0.0] * n_levels
        for rank, idx in enumerate(sorted_idx):
            plaq_ordered[idx] = smeared_plaq[rank]

        return operators, plaq_ordered

    def smeared_spatial_plaquette_timeslice(self, n_smear=20, alpha=0.5):
        """Legacy single-smearing interface."""
        U_sm = self._ape_smear(n_smear, alpha)
        return self._spatial_plaq_timeslice_from_links(U_sm)

    def _plaquette_quat(self, mu, nu):
        """Full quaternion plaquette U_{μν}(x). Shape (Nt,Nx,Ny,Nz,4)."""
        return qmul(
            qmul(self.U[mu], self._shift(self.U[nu], mu, fwd=True)),
            qmul(qdagger(self._shift(self.U[mu], nu, fwd=True)),
                 qdagger(self.U[nu])))

    def _clover_fmunu(self, mu, nu):
        """
        Clover-leaf field strength tensor F_{μν}(x) in quaternion form.

        F_{μν} = (1/8) Im[ C_{μν} − C_{νμ} ]
        where C_{μν} = P_{μν}(x) + P_{ν,-μ}(x) + P_{-μ,-ν}(x) + P_{-ν,μ}(x)
        is the sum of the four plaquettes in the (μ,ν) plane sharing corner x.

        For SU(2) quaternions: Im part = (0, a1, a2, a3), i.e. drop a0.
        The anti-hermitian traceless part is encoded in (a1, a2, a3).
        Returns shape (Nt, Nx, Ny, Nz, 4) with a0 = 0.
        """
        # Four oriented plaquettes sharing corner x in the (mu,nu) plane
        # P1: x → x+μ → x+μ+ν → x+ν → x  (standard plaquette at x)
        P1 = self._plaquette_quat(mu, nu)

        # P2: x → x+ν → x+ν-μ → x-μ → x  (= P_{ν,-μ} at x)
        P2 = qmul(qmul(
            self.U[nu],
            qdagger(self._shift(self._shift(self.U[mu], nu, fwd=True), mu, fwd=False))),
            qmul(qdagger(self._shift(self.U[nu], mu, fwd=False)),
                 self._shift(self.U[mu], mu, fwd=False)))

        # P3: x → x-μ → x-μ-ν → x-ν → x  (= P_{-μ,-ν} at x)
        P3 = qmul(qmul(
            qdagger(self._shift(self.U[mu], mu, fwd=False)),
            qdagger(self._shift(self._shift(self.U[nu], mu, fwd=False), nu, fwd=False))),
            qmul(self._shift(self._shift(self.U[mu], mu, fwd=False), nu, fwd=False),
                 self._shift(self.U[nu], nu, fwd=False)))

        # P4: x → x-ν → x-ν+μ → x+μ → x  (= P_{-ν,μ} at x)
        # Links: U_ν†(x-ν̂) · U_μ(x-ν̂) · U_ν(x-ν̂+μ̂) · U_μ†(x)
        P4 = qmul(qmul(
            qdagger(self._shift(self.U[nu], nu, fwd=False)),          # U_ν†(x-ν̂)
            self._shift(self.U[mu], nu, fwd=False)),                  # U_μ(x-ν̂)
            qmul(self._shift(self._shift(self.U[nu], nu, fwd=False), mu, fwd=True),  # U_ν(x-ν̂+μ̂)
                 qdagger(self.U[mu])))

        # Clover sum
        C = P1 + P2 + P3 + P4  # quaternion sum, shape (..., 4)

        # Clover field strength: F̂ = Im(C) / 4
        # C = sum of 4 plaquettes, each ≈ 1 + a²F_cont in continuum.
        # Im(C) = (0, c1, c2, c3), matrix form = i·c⃗·σ⃗ ≈ 4a²·F_cont
        # Dividing by 4: F̂ ≈ a²·F_cont (correct continuum limit)
        F = C.copy()
        F[..., 0] = 0.0
        F = F / 4.0

        return F

    def gradient_flow_step(self, U_flow, epsilon):
        """
        One Euler step of Wilson gradient flow.

        The flow equation minimizes the Wilson action:
            dU_μ/dt = -g₀² (∂S_W/∂U_μ) U_μ

        The derivative of S_W = β Σ (1 - (1/2) Tr P) w.r.t. U_μ gives
        a force that drives U_μ toward the staple sum V_μ.

        Euler step: U_new = Proj_SU2[ U + ε · V ]
        where V is the action staple sum. This moves U toward V,
        which minimizes the action (smooths the configuration).

        Parameters
        ----------
        U_flow : ndarray, shape (4, Nt, Nx, Ny, Nz, 4)
        epsilon : float — step size (typical: 0.01–0.02)

        Returns
        -------
        U_new : ndarray — flowed config after one step
        """
        U_new = xp.empty_like(U_flow)
        for mu in range(4):
            # Action staple: same formula as in _staple() but on U_flow
            V = xp.zeros_like(U_flow[mu])
            for nu in range(4):
                if nu == mu:
                    continue
                u1 = xp.roll(U_flow[nu], -1, axis=mu)
                u2 = qdagger(xp.roll(U_flow[mu], -1, axis=nu))
                u3 = qdagger(U_flow[nu])
                upper = qmul(qmul(u1, u2), u3)

                u4 = qdagger(xp.roll(xp.roll(U_flow[nu], -1, axis=mu), 1, axis=nu))
                u5 = qdagger(xp.roll(U_flow[mu], 1, axis=nu))
                u6 = xp.roll(U_flow[nu], 1, axis=nu)
                lower = qmul(qmul(u4, u5), u6)

                V = V + upper + lower

            # Move U toward V†/|V| (direction that minimizes action).
            # Simple projected Euler: U_new = Proj_SU2(U + ε·V†)
            U_new[mu] = qnormalize(U_flow[mu] + epsilon * qdagger(V))

        return U_new

    def topological_charge(self, U_in=None):
        """
        Topological charge from clover definition.

        Q = (1/32π²) Σ_x ε_{μνρσ} Tr[F_{μν}(x) F_{ρσ}(x)]

        For SU(2), F_{μν} is in the Lie algebra su(2) ≅ R³.
        Tr(F_{μν} F_{ρσ}) = -2 (f1·g1 + f2·g2 + f3·g3)
        where f = (a1,a2,a3) of F_{μν} quaternion, g = same for F_{ρσ}.

        Parameters
        ----------
        U_in : gauge field array, or None to use self.U

        Returns
        -------
        Q : float — topological charge (should be near-integer after flow)
        """
        # Save and temporarily replace U if external field provided
        if U_in is not None:
            U_save = self.U
            self.U = U_in

        # Compute clover F_{μν} for all 6 planes
        F = {}
        for mu in range(4):
            for nu in range(mu + 1, 4):
                F[(mu, nu)] = self._clover_fmunu(mu, nu)

        # Q = (1/32π²) Σ_x ε_{μνρσ} Tr(F_{μν} F_{ρσ})
        # The nonzero terms of ε_{μνρσ} with μ<ν and ρ<σ:
        # ε_{0123} = +1 → (01)(23)
        # ε_{0213} = -1 → (02)(13) with sign -1
        # ε_{0312} = +1 → (03)(12)
        # For Tr(F·G) with quaternions (0, f1,f2,f3) and (0, g1,g2,g3):
        # Product has a0 = -(f1g1 + f2g2 + f3g3), so Tr = 2·a0 = -2(f·g)

        def tr_cc(mu1, nu1, mu2, nu2):
            f = F[(mu1, nu1)]
            g = F[(mu2, nu2)]
            dot = (f[..., 1] * g[..., 1] + f[..., 2] * g[..., 2]
                   + f[..., 3] * g[..., 3])
            return -2.0 * dot

        # Full ε sum: Σ_{μνρσ} ε_{μνρσ} Tr(F_μν F_ρσ)
        # With F_{μν} = -F_{νμ}, the 3 independent pairs (μ<ν, ρ<��) each
        # appear 8 times in the 24-term sum:
        #   (01,23) with sign +1, (02,13) with sign -1, (03,12) with sign +1
        # So: Σ ε Tr(FF) = 8 × [Tr(F01·F23) - Tr(F02·F13) + Tr(F03·F12)]
        # And: Q = (1/32π²) × 8 × [...] = (1/4π²) × [...]
        q_density = (tr_cc(0, 1, 2, 3) - tr_cc(0, 2, 1, 3) + tr_cc(0, 3, 1, 2))

        # Q = (1/32π²) × Σ ε Tr(F̂·F̂) = (8/32π²) × Σ_x q_density = (1/4π²) × Σ_x q_density
        Q = float(xp.sum(q_density)) / (4.0 * np.pi ** 2)

        if U_in is not None:
            self.U = U_save

        return Q

    def topological_charge_flowed(self, n_flow=100, epsilon=0.01):
        """
        Topological charge after gradient flow smoothing.

        Parameters
        ----------
        n_flow  : int   — number of flow steps
        epsilon : float — step size (flow time = n_flow × epsilon)

        Returns
        -------
        Q       : float — topological charge (near-integer)
        t_flow  : float — total flow time
        """
        U_flow = self.U.copy()
        for _ in range(n_flow):
            U_flow = self.gradient_flow_step(U_flow, epsilon)

        Q = self.topological_charge(U_in=U_flow)
        t_flow = n_flow * epsilon
        return Q, t_flow

    def topological_charge_density(self, U_in=None):
        """
        Topological charge density q(x) at each lattice site.

        q(x) = [Tr(F01·F23) - Tr(F02·F13) + Tr(F03·F12)] / (4π²)

        Parameters
        ----------
        U_in : gauge field array, or None to use self.U

        Returns
        -------
        q : ndarray, shape (Nt, Nx, Ny, Nz) — charge density per site
        """
        if U_in is not None:
            U_save = self.U
            self.U = U_in

        F = {}
        for mu in range(4):
            for nu in range(mu + 1, 4):
                F[(mu, nu)] = self._clover_fmunu(mu, nu)

        def tr_cc(mu1, nu1, mu2, nu2):
            f = F[(mu1, nu1)]
            g = F[(mu2, nu2)]
            dot = (f[..., 1] * g[..., 1] + f[..., 2] * g[..., 2]
                   + f[..., 3] * g[..., 3])
            return -2.0 * dot

        q = (tr_cc(0, 1, 2, 3) - tr_cc(0, 2, 1, 3) + tr_cc(0, 3, 1, 2))
        q = q / (4.0 * np.pi ** 2)

        if U_in is not None:
            self.U = U_save

        return q

    def topological_charge_timeslice(self, U_in=None):
        """
        Q_slice(t) = Σ_{x⃗} q(x⃗, t) — topological charge per time-slice.

        Returns shape (Nt,).
        """
        q = self.topological_charge_density(U_in=U_in)
        return xp.sum(q, axis=(1, 2, 3))

    def multi_flow_measurements(self, flow_times=(0.5, 1.0, 2.0), epsilon=0.01):
        """
        Gradient flow to multiple flow times, measuring Q and Q_slice at each.

        Flows incrementally: t=0 → t₁ → t₂ → t₃ to avoid redundant work.

        Parameters
        ----------
        flow_times : tuple of float — flow times to measure at (must be sorted)
        epsilon    : float — flow step size

        Returns
        -------
        results : dict with keys:
            'Q'       : list of float — global Q at each flow time
            'Q_slice' : list of ndarray (Nt,) — Q_slice(t) at each flow time
            'flow_times' : list of float — actual flow times
        """
        flow_times = sorted(flow_times)
        U_flow = self.U.copy()
        current_t = 0.0

        Q_list = []
        Q_slice_list = []
        t_list = []

        for target_t in flow_times:
            # Flow from current_t to target_t
            n_steps = int(round((target_t - current_t) / epsilon))
            for _ in range(n_steps):
                U_flow = self.gradient_flow_step(U_flow, epsilon)
            current_t += n_steps * epsilon

            # Measure
            Q_slice = self.topological_charge_timeslice(U_in=U_flow)
            Q = float(xp.sum(Q_slice))

            if hasattr(Q_slice, 'get'):
                Q_slice = Q_slice.get()

            Q_list.append(Q)
            Q_slice_list.append(Q_slice)
            t_list.append(current_t)

        return {
            'Q': Q_list,
            'Q_slice': Q_slice_list,
            'flow_times': t_list,
        }

    def pseudoscalar_clover_timeslice(self, U_spatial=None):
        """
        Pseudoscalar (0⁻) operator from clover q(x) using given spatial links.

        Uses the clover field strength with the provided spatial links
        (possibly APE-smeared) and the original temporal links.
        The topological charge density q(x) ∝ ε_{μνρσ} Tr(F_μν F_ρσ)
        is a pseudoscalar under spatial parity.

        Parameters
        ----------
        U_spatial : list [None, U1, U2, U3] of smeared spatial links,
                    or None to use self.U[1:4]

        Returns
        -------
        O : ndarray, shape (Nt,) — pseudoscalar operator per time-slice
        """
        # Temporarily replace spatial links with smeared ones
        if U_spatial is not None:
            U_save = [None, self.U[1].copy(), self.U[2].copy(), self.U[3].copy()]
            for i in range(1, 4):
                if U_spatial[i] is not None:
                    self.U[i] = U_spatial[i]

        # Compute q(x) and sum over spatial sites
        O = self.topological_charge_timeslice()

        # Restore original links
        if U_spatial is not None:
            for i in range(1, 4):
                self.U[i] = U_save[i]

        return O

    def multi_smear_pseudoscalar(self, smear_levels, alpha=0.3):
        """
        Pseudoscalar 0⁻ operators at multiple APE smearing levels.

        Uses the clover topological charge density with APE-smeared spatial
        links + original temporal links.

        Parameters
        ----------
        smear_levels : list of int — e.g. [0, 5, 10, 20]
        alpha        : float — APE smearing parameter

        Returns
        -------
        operators : ndarray, shape (n_levels, Nt)
        """
        Nt = self.dims[0]
        n_levels = len(smear_levels)
        operators = xp.zeros((n_levels, Nt))

        sorted_idx = sorted(range(n_levels), key=lambda k: smear_levels[k])
        sorted_levels = [smear_levels[k] for k in sorted_idx]

        U_sm = [None, self.U[1].copy(), self.U[2].copy(), self.U[3].copy()]
        current_n = 0

        for rank, idx in enumerate(sorted_idx):
            target_n = sorted_levels[rank]
            if target_n > current_n:
                delta = target_n - current_n
                for _ in range(delta):
                    U_new = [None, None, None, None]
                    for i in range(1, 4):
                        staple = xp.zeros_like(U_sm[i])
                        for j in range(1, 4):
                            if j == i:
                                continue
                            upper = qmul(qmul(
                                U_sm[j],
                                self._shift(U_sm[i], j, fwd=True)),
                                qdagger(self._shift(U_sm[j], i, fwd=True)))
                            lower = qmul(qmul(
                                qdagger(self._shift(U_sm[j], j, fwd=False)),
                                self._shift(U_sm[i], j, fwd=False)),
                                self._shift(self._shift(U_sm[j], j, fwd=False), i, fwd=True))
                            staple = staple + upper + lower
                        blended = (1.0 - alpha) * U_sm[i] + (alpha / 4.0) * staple
                        U_new[i] = qnormalize(blended)
                    U_sm[1], U_sm[2], U_sm[3] = U_new[1], U_new[2], U_new[3]
                current_n = target_n

            operators[idx] = self.pseudoscalar_clover_timeslice(U_spatial=U_sm)

        return operators


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


# ---------------------------------------------------------------------------
# Multi-operator correlator matrix and GEVP
# ---------------------------------------------------------------------------

def correlator_matrix(O_all):
    """
    Compute the symmetrized correlator matrix C_ij(τ) with VEV subtraction.

    C_ij(τ) = (1/Nt) Σ_t ⟨O_i(t+τ) O_j(t)⟩ − ⟨O_i⟩⟨O_j⟩

    The result is explicitly symmetrized: C_sym = [C + Cᵀ] / 2.
    This is standard practice — the spectral decomposition guarantees
    C_ij(τ) = C_ji(τ) for hermitian operators, and symmetrization
    removes statistical noise in the antisymmetric part.

    Parameters
    ----------
    O_all : ndarray, shape (n_configs, n_ops, Nt)

    Returns
    -------
    C     : ndarray, shape (n_ops, n_ops, Nt)  — symmetrized correlator matrix
    C_err : ndarray, shape (n_ops, n_ops, Nt)  — jackknife errors
    """
    n_cfg, n_ops, Nt = O_all.shape

    O_vev = np.mean(O_all, axis=(0, 2))  # (n_ops,)

    # C_ij(τ) = (1/Nt) Σ_t O_i(t+τ) · O_j(t) − ⟨O_i⟩⟨O_j⟩
    C_per_cfg = np.zeros((n_cfg, n_ops, n_ops, Nt))
    for tau in range(Nt):
        O_shifted = np.roll(O_all, -tau, axis=2)  # O(t+τ)
        for i in range(n_ops):
            for j in range(n_ops):
                # O_i(t+τ) · O_j(t), averaged over t
                C_per_cfg[:, i, j, tau] = np.mean(
                    O_shifted[:, i, :] * O_all[:, j, :], axis=1
                ) - O_vev[i] * O_vev[j]

    C = np.mean(C_per_cfg, axis=0)

    # Symmetrize: C_sym = [C + Cᵀ] / 2
    for tau in range(Nt):
        C[:, :, tau] = 0.5 * (C[:, :, tau] + C[:, :, tau].T)

    # Jackknife errors (on symmetrized correlator)
    C_jack = np.zeros((n_cfg, n_ops, n_ops, Nt))
    for k in range(n_cfg):
        O_loo = np.delete(O_all, k, axis=0)
        vev_k = np.mean(O_loo, axis=(0, 2))
        for tau in range(Nt):
            O_sh = np.roll(O_loo, -tau, axis=2)
            for i in range(n_ops):
                for j in range(n_ops):
                    C_jack[k, i, j, tau] = np.mean(
                        O_sh[:, i, :] * O_loo[:, j, :]) - vev_k[i] * vev_k[j]
        for tau in range(Nt):
            C_jack[k, :, :, tau] = 0.5 * (C_jack[k, :, :, tau] + C_jack[k, :, :, tau].T)

    C_err = np.sqrt((n_cfg - 1) * np.mean((C_jack - C[None, :, :, :]) ** 2, axis=0))

    return C, C_err


def solve_gevp(C, tau0=1):
    """
    Solve the Generalized Eigenvalue Problem:
        C(τ) v_n = λ_n(τ, τ₀) C(τ₀) v_n

    Parameters
    ----------
    C    : ndarray, shape (n_ops, n_ops, Nt) — correlator matrix
    tau0 : int — reference timeslice (default 1)

    Returns
    -------
    eigenvalues : ndarray, shape (n_ops, Nt) — λ_n(τ) for each state n
    masses      : ndarray, shape (n_ops, Nt-1) — m_n(τ) = ln(λ_n(τ)/λ_n(τ+1))
    """
    from scipy.linalg import eigh

    n_ops, _, Nt = C.shape
    eigenvalues = np.full((n_ops, Nt), np.nan)
    masses = np.full((n_ops, Nt - 1), np.nan)

    C0 = C[:, :, tau0]

    # Check C(τ₀) is symmetric positive definite
    eigvals_c0 = np.linalg.eigvalsh(C0)
    if np.any(eigvals_c0 <= 0):
        print(f"  WARNING: C(tau0={tau0}) is not positive definite. "
              f"Eigenvalues: {eigvals_c0}")
        # Regularize: add small diagonal
        reg = abs(np.min(eigvals_c0)) * 1.1 + 1e-10
        C0 = C0 + reg * np.eye(n_ops)
        print(f"  Regularized with {reg:.2e}")

    for tau in range(Nt):
        Ct = C[:, :, tau]
        # Symmetrize
        Ct = 0.5 * (Ct + Ct.T)
        try:
            evals, _ = eigh(Ct, C0)
            # Sort descending (largest eigenvalue = ground state)
            idx = np.argsort(evals)[::-1]
            eigenvalues[:, tau] = evals[idx]
        except Exception:
            pass

    # Effective masses from eigenvalues
    for n in range(n_ops):
        for tau in range(Nt - 1):
            lam_t = eigenvalues[n, tau]
            lam_t1 = eigenvalues[n, tau + 1]
            if lam_t > 0 and lam_t1 > 0:
                masses[n, tau] = np.log(lam_t / lam_t1)

    return eigenvalues, masses
