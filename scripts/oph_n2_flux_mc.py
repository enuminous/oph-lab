#!/usr/bin/env python3
"""Independent heat-bath implementation of the finite matter/link/Gamma model.

This implements only the model dictionary in Bernhard Mueller's 2026-10-09
email: N complex scalar species, U(1) oriented links, independent Gamma(shape=alpha,
rate=beta) conductances, and V=m2 sum |psi|^2 + sum_e w_e sum_s|psi_s(x)-U_e psi_s(x+mu)|^2.
It is an exploratory finite-model implementation, not a physical validation.
"""
from __future__ import annotations
import argparse, json, time
import numpy as np
from scipy.special import i0e, i1e


def run(L=4, N=2, alpha=2.0, beta=1.0, m2=1.0, seed=20261010,
        warmup=1000, samples=2000, thin=4):
    if L < 4 or L % 2 or N < 1 or alpha <= 0 or beta <= 0 or m2 <= 0:
        raise ValueError("Require even L>=4 and positive N, alpha, beta, m2")
    rng = np.random.default_rng(seed)
    shape = (L,)*4
    axes = (1,2,3,4)
    parity = (np.indices(shape).sum(axis=0) & 1).astype(bool)
    psi = (rng.normal(size=(N,)+shape)+1j*rng.normal(size=(N,)+shape))/np.sqrt(2*m2)
    theta = rng.uniform(-np.pi,np.pi,size=(4,)+shape)
    w = rng.gamma(alpha, 1/beta, size=(4,)+shape)

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
        f = (theta[0] + np.roll(theta[1], -1, axis=1)
             - np.roll(theta[0], -1, axis=2) - theta[1])
        return np.sin(f).mean(axis=(1,2,3))  # one value per time slice x_3

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
        z=(r[0]*np.roll(r[1],-1,axis=1)
           *np.conj(np.roll(r[0],-1,axis=2))*np.conj(r[1]))
        return np.imag(z).mean(axis=(1,2,3))

    for _ in range(warmup): sweep()
    obs=[]; rb_obs=[]
    t0=time.time()
    for _ in range(samples):
        for __ in range(thin): sweep()
        obs.append(flux_slice())
        rb_obs.append(rb_flux_slice())
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
        rb_corr.append(float(prod-rb_mean*rb_mean))
    # Simple independent-chain standard error is invalid for Markov samples;
    # report naive SE solely as a diagnostic, and retain raw per-sample data.
    return {
        "model": {"L":L,"dimension":4,"N":N,"alpha_gamma_shape":alpha,
                  "beta_gamma_rate":beta,"m2":m2,"volume":L**4},
        "sampler": {"seed":seed,"warmup_sweeps":warmup,"measurements":samples,
                    "sweeps_between_measurements":thin,"elapsed_seconds":time.time()-t0,
                    "updates": "red-black complex Gaussian; von Mises link phase; Gamma conductance"},
        "observable": "connected periodic correlator of spatially averaged sin(plaquette angle 01), separated along axis 3",
        "mean_flux":mean,"correlator":corr,
        "rao_blackwell_mean_flux":rb_mean,"rao_blackwell_correlator":rb_corr,
        "sampled_slice_series":obs.tolist(),
        "rao_blackwell_slice_series":rb_obs.tolist()
    }

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--L',type=int,default=4); p.add_argument('--N',type=int,default=2)
    p.add_argument('--alpha',type=float,default=2); p.add_argument('--beta',type=float,default=1)
    p.add_argument('--m2',type=float,default=1); p.add_argument('--seed',type=int,default=20261010)
    p.add_argument('--warmup',type=int,default=1000); p.add_argument('--samples',type=int,default=2000)
    p.add_argument('--thin',type=int,default=4); p.add_argument('--output')
    a=p.parse_args()
    r=run(a.L,a.N,a.alpha,a.beta,a.m2,a.seed,a.warmup,a.samples,a.thin)
    s=json.dumps(r,indent=2)
    if a.output:
        with open(a.output,'w') as f:f.write(s+'\n')
    else:print(s)
