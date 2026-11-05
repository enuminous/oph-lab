#!/usr/bin/env python3
"""Independent heat-bath implementation of the finite matter/link/Gamma model.

This implements only the model dictionary in Bernhard Mueller's 2026-10-09
email: N complex scalar species, U(1) oriented links, independent Gamma(shape=alpha,
rate=beta) conductances, and V=m2 sum |psi|^2 + sum_e w_e sum_s|psi_s(x)-U_e psi_s(x+mu)|^2.
It is an exploratory finite-model implementation, not a physical validation.
"""
from __future__ import annotations
import argparse, hashlib, json, platform, time
from pathlib import Path
import numpy as np
import scipy
from scipy.special import i0e, i1e

READOUT_VERSION = "F01-axis3-v2"


def plaquette_product(links, mu=0, nu=1):
    """Oriented U_mu(x) U_nu(x+mu) U_mu(x+nu)* U_nu(x)*.

    links has one link-direction axis followed by four coordinate axes.
    Indexing links[mu] removes the direction axis; coordinate axes are 0..3.
    The same product computes a conditional mean when links are E[U|psi,w]
    and the four distinct link variables are conditionally independent.
    """
    links = np.asarray(links, dtype=complex)
    if links.ndim != 5 or links.shape[0] != 4 or min(links.shape[1:]) < 2:
        raise ValueError("links must have shape (4,L0,L1,L2,L3), all L>=2")
    if not np.isfinite(links).all() or mu == nu or mu not in range(4) or nu not in range(4):
        raise ValueError("finite links and distinct directions 0..3 required")
    return (links[mu] * np.roll(links[nu], -1, axis=mu)
            * np.conj(np.roll(links[mu], -1, axis=nu)) * np.conj(links[nu]))


def spatial_flux_slices(links, transfer_axis=3):
    """Average Im(F01 Wilson product) on slices normal to transfer_axis."""
    if transfer_axis not in range(4):
        raise ValueError("transfer_axis must be 0..3")
    spatial_axes = tuple(axis for axis in range(4) if axis != transfer_axis)
    return np.imag(plaquette_product(links)).mean(axis=spatial_axes)


def run(L=4, N=2, alpha=2.0, beta=1.0, m2=1.0, seed=20261010,
        warmup=1000, samples=2000, thin=4, *, start='hot', diagnostics=False,
        warmup_diagnostic_interval=16):
    if (not all(isinstance(v, (int, np.integer)) and not isinstance(v, bool)
                for v in (L, N, seed, warmup, samples, thin))
            or L < 4 or L % 2 or N < 1
            or not all(np.isfinite(v) and v > 0 for v in (alpha, beta, m2))
            or warmup < 0 or samples < 1 or thin < 1 or seed < 0):
        raise ValueError("Require even L>=4 and positive N, alpha, beta, m2")
    if (start not in ('hot', 'cold') or type(diagnostics) is not bool
            or type(warmup_diagnostic_interval) is not int or warmup_diagnostic_interval < 1):
        raise ValueError('Require hot/cold start and positive warmup diagnostic interval')
    total_start = time.perf_counter()
    rng = np.random.default_rng(seed)
    shape = (L,)*4
    axes = (1,2,3,4)
    parity = (np.indices(shape).sum(axis=0) & 1).astype(bool)
    psi = (rng.normal(size=(N,)+shape)+1j*rng.normal(size=(N,)+shape))/np.sqrt(2*m2)
    theta = rng.uniform(-np.pi,np.pi,size=(4,)+shape)
    w = rng.gamma(alpha, 1/beta, size=(4,)+shape)
    if start == 'cold':
        psi.fill(0); theta.fill(0); w.fill(alpha / beta)

    def sweep():
        nonlocal psi, theta, w
        # Red/black exact complex-Gaussian site conditionals.
        for color in (False, True):
            mask = parity == color
            for s in range(N):
                A = np.full(shape, m2, dtype=float)
                B = np.zeros(shape, dtype=np.complex128)
                p = psi[s]
                for mu, ax in enumerate(axes):
                    pax = ax-1
                    wp = w[mu]
                    U = np.exp(1j*theta[mu])
                    # Outgoing edge x -> x+mu.
                    A += wp
                    B += wp * U * np.roll(p, -1, axis=pax)
                    # Incoming edge x-mu -> x.
                    win = np.roll(wp, 1, axis=pax)
                    Uin = np.roll(U, 1, axis=pax)
                    A += win
                    B += win * np.conj(Uin) * np.roll(p, 1, axis=pax)
                z = B/A + (rng.normal(size=shape)+1j*rng.normal(size=shape))/np.sqrt(2*A)
                p[mask] = z[mask]
        # Exact link-phase von Mises conditionals.
        for mu, ax in enumerate(axes):
            Q = np.zeros(shape, dtype=np.complex128)
            for s in range(N):
                Q += np.conj(psi[s]) * np.roll(psi[s], -1, axis=ax-1)
            kappa = 2*w[mu]*np.abs(Q)
            theta[mu] = rng.vonmises(-np.angle(Q), kappa)
        # Exact Gamma conductance conditionals.
        for mu, ax in enumerate(axes):
            S = np.zeros(shape, dtype=float)
            U = np.exp(1j*theta[mu])
            for s in range(N):
                d = psi[s] - U*np.roll(psi[s], -1, axis=ax-1)
                S += np.abs(d)**2
            w[mu] = rng.gamma(alpha, 1/(beta+S))

    def flux_slice():
        # Oriented plaquette (0,1), separated along fourth (time) axis.
        return spatial_flux_slices(np.exp(1j * theta))

    def rb_flux_slice():
        # Rao-Blackwellize over all independent link phases conditional on psi,w.
        # E[U|psi,w] = I1(kappa)/I0(kappa) * exp(-i arg(Q)).
        r=[]
        for mu, ax in enumerate(axes):
            Q=np.zeros(shape,dtype=np.complex128)
            for s in range(N):
                Q += np.conj(psi[s])*np.roll(psi[s],-1,axis=ax-1)
            kap=2*w[mu]*np.abs(Q)
            ratio=np.divide(i1e(kap),i0e(kap),out=np.zeros_like(kap),where=i0e(kap)>0)
            r.append(ratio*np.exp(-1j*np.angle(Q)))
        # Conditional mean of sin(F_01), with oriented plaquette boundary.
        return spatial_flux_slices(r)

    def scalar_diagnostics():
        # Gauge-invariant monitors, not a physical Hamiltonian/energy readout.
        norm = float(np.sum(np.abs(psi)**2) / L**4)
        action = m2 * norm
        for mu in range(4):
            delta = psi - np.exp(1j * theta[mu]) * np.roll(psi, -1, axis=mu+1)
            action += float(np.sum(w[mu] * np.sum(np.abs(delta)**2, axis=0)) / L**4)
        return {'psi_norm2_per_site': norm, 'mean_conductance': float(w.mean()),
                'matter_link_action_per_site': action,
                'real_plaquette_mean': float(plaquette_product(np.exp(1j*theta)).real.mean())}

    warmup_trace = []
    if diagnostics:
        warmup_trace.append({'sweep': 0, **scalar_diagnostics()})
    for step in range(1, warmup + 1):
        sweep()
        if diagnostics and (step % warmup_diagnostic_interval == 0 or step == warmup):
            warmup_trace.append({'sweep': step, **scalar_diagnostics()})
    warmup_seconds = time.perf_counter() - total_start
    obs=[]; rb_obs=[]
    measurement_trace = []
    t0=time.perf_counter()
    for _ in range(samples):
        for __ in range(thin): sweep()
        obs.append(flux_slice())
        rb_obs.append(rb_flux_slice())
        if diagnostics:
            measurement_trace.append(scalar_diagnostics())
    obs=np.asarray(obs)
    rb_obs=np.asarray(rb_obs)
    # translation-average, connected, periodic-time correlator
    mean=float(obs.mean())
    corr=[]
    for d in range(L//2+1):
        prod=np.mean(obs*np.roll(obs,-d,axis=1))
        corr.append(float(prod-mean*mean))
    rb_mean=float(rb_obs.mean())
    rb_corr=[]
    for d in range(L//2+1):
        prod=np.mean(rb_obs*np.roll(rb_obs,-d,axis=1))
        # At contact the plaquettes share links: E[F|psi,w]^2 != E[F^2|psi,w].
        # Distinct axis-3 slices use disjoint links, so d>0 factorizes.
        rb_corr.append(None if d == 0 else float(prod-rb_mean*rb_mean))
    # Simple independent-chain standard error is invalid for Markov samples;
    # report naive SE solely as a diagnostic, and retain raw per-sample data.
    return {
        "raw_schema_version": "oph-flux-chain-v3",
        "readout_version": READOUT_VERSION,
        "provenance": {
            "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "python_version": platform.python_version(),
            "rng": type(rng.bit_generator).__name__,
            "status": "finite_model_exploratory_not_particle_identification",
            "coordinate_order": ["x0", "x1", "x2", "x3"],
            "plaquette_directions": [0, 1],
            "transfer_axis": 3,
            "averaged_axes": [0, 1, 2],
            "physical_time_identified": False,
            "rao_blackwell_contact": "withheld_shared_links_require_second_moment",
        },
        "model": {"L":L,"dimension":4,"N":N,"alpha_gamma_shape":alpha,
                  "beta_gamma_rate":beta,"m2":m2,"volume":L**4},
        "sampler": {"seed":seed,"warmup_sweeps":warmup,"measurements":samples,
                    "sweeps_between_measurements":thin,"elapsed_seconds":time.perf_counter()-t0,
                    "warmup_elapsed_seconds":warmup_seconds,
                    "total_elapsed_seconds":time.perf_counter()-total_start,
                    "initialization":start, "diagnostics_recorded":diagnostics,
                    "warmup_diagnostic_interval":warmup_diagnostic_interval,
                    "updates": "red-black complex Gaussian; von Mises link phase; Gamma conductance"},
        "observable": "connected periodic correlator of spatially averaged sin(plaquette angle 01), separated along axis 3",
        "mean_flux":mean,"correlator":corr,
        "rao_blackwell_mean_flux":rb_mean,"rao_blackwell_correlator":rb_corr,
        "sampled_slice_series":obs.tolist(),
        "rao_blackwell_slice_series":rb_obs.tolist(),
        "warmup_diagnostics":warmup_trace,
        "measurement_diagnostics":measurement_trace
    }

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--L',type=int,default=4); p.add_argument('--N',type=int,default=2)
    p.add_argument('--alpha',type=float,default=2); p.add_argument('--beta',type=float,default=1)
    p.add_argument('--m2',type=float,default=1); p.add_argument('--seed',type=int,default=20261010)
    p.add_argument('--warmup',type=int,default=1000); p.add_argument('--samples',type=int,default=2000)
    p.add_argument('--thin',type=int,default=4); p.add_argument('--output')
    p.add_argument('--start', choices=('hot', 'cold'), default='hot')
    p.add_argument('--diagnostics', action='store_true')
    a=p.parse_args()
    r=run(a.L,a.N,a.alpha,a.beta,a.m2,a.seed,a.warmup,a.samples,a.thin,
          start=a.start, diagnostics=a.diagnostics)
    s=json.dumps(r,indent=2)
    if a.output:
        with open(a.output,'w') as f:f.write(s+'\n')
    else:print(s)
