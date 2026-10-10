# Stage 3 — Independent 4D N=2 Flux-Channel Simulation

**Date:** 2026-10-10  
**Repository:** `enuminous/oph-lab`  
**Status:** Exploratory independent implementation. It resolves neither a one-particle pole nor a clean no-pole result. No physical photon or Coulomb-phase claim is made.

## Executive result

I independently implemented the finite matter/link/conductance heat-bath model described in Bernhard Mueller's 2026-10-09 email and extended the lattice from the previously reported `L=4,6` to `L=8`. I added a Rao–Blackwell estimator that integrates the conditionally independent link phases analytically when estimating the separated-time odd-flux correlator.

At the fixed parameter point `alpha=2`, Gamma rate `beta=1`, `m^2=1`, three independently seeded chains per size, the improved `N=1` separated-slice control is consistent with zero for `L=4,6,8`. For `N=2`, the first three separated-time correlators on `L=8` are consistent with zero. The opposite-slice (`t=L/2`) estimate is negative and remains negative under the tested block lengths. The direct estimator is much noisier but agrees in sign at that midpoint.

There is no positive, stable correlator plateau from which to extract a one-particle transfer gap. The result is **unresolved**, not a clean no-pole: a pole with sufficiently small residue is not excluded, the source's exact operator/parameter dictionary is not pinned to a public model revision, and no retirement threshold was supplied. The negative midpoint also needs an explicit reflection-positivity/parity derivation before it can be interpreted as a physical obstruction.

## Frozen finite-model interpretation

The email specifies `N` complex components per patch, oriented `U(1)` links, positive conductances, and

\[
V(\psi,U,w)=m^2\sum_{x,s}|\psi_{s,x}|^2+
\sum_{e=(x,y)}w_e\sum_{s=1}^{N}|\psi_{s,x}-U_e\psi_{s,y}|^2.
\]

The implementation interprets each conductance reference law as independent `Gamma(shape=alpha, rate=beta)` and sets `alpha=2`, `beta=1`, `m^2=1`. It uses an even, periodic, four-dimensional hypercubic lattice. This is an explicit interpretation of the email, not a source-pinned OPH specification; the Gamma scale/rate convention and exact observable convention need Bernhard's confirmation before a confirmatory run.

Each sweep applies exact conditionals of this law:

- Checkerboard complex-Gaussian site conditionals. At site `x`, the conditional precision is `m^2 + sum_{e incident to x} w_e`; the linear term is the sum of neighboring matter fields parallel-transported by the oriented links.
- Independent von Mises link conditionals with concentration `2 w_e |Q_e|`, where `Q_e=sum_s conjugate(psi[s,x])*psi[s,y]`, and center `-arg(Q_e)`.
- Gamma conductance conditionals with shape `alpha` and rate `beta + sum_s |psi[s,x]-U_e psi[s,y]|^2`.

Each coordinate update preserves the stated joint density. The product of sequential updates is used as a Gibbs sampler; its sweep index is algorithmic sampling time, not physical time.

## Observable and estimator

I operationalized “odd Wilson flux” as the imaginary part of an oriented spatial plaquette,

\[
O_{01}(x)=\sin F_{01}(x),\qquad
F_{01}(x)=\theta_0(x)+\theta_1(x+\hat0)-\theta_0(x+\hat1)-\theta_1(x).
\]

The plaquette plane is directions 0–1. Direction 3 is used as the transfer/separation direction. On each direction-3 slice, `O_t` is the spatial average over the other three coordinates. The connected periodic correlator is

\[
C_N(t)=\langle O_0 O_t\rangle-\langle O\rangle^2.
\]

The direct estimator samples the link phases and computes `sin(F)`. The improved estimator conditions on all matter and conductance variables. For each link,

\[
r_e=\mathbb E[U_e\mid\psi,w]
=\frac{I_1(\kappa_e)}{I_0(\kappa_e)}e^{-i\arg Q_e},\qquad \kappa_e=2w_e|Q_e|.
\]

For a plaquette, its conditional odd-flux mean is the imaginary part of the oriented product of the four corresponding `r_e` factors. For edge-disjoint plaquettes on distinct slices, conditional link independence makes the product of these conditional means an unbiased Rao–Blackwell estimate of their flux product. This factorization is used only for `t>=1`; the reported Rao–Blackwell contact value at `t=0` is not a valid estimator for `C(0)` and is excluded from the conclusions.

## Run protocol and numerical record

| Setting | Value |
|---|---:|
| Dimension and boundaries | 4D, periodic in all directions |
| Lattice sizes | `L=4,6,8` |
| Species | Matched `N=1` null/control and `N=2` target |
| Gamma reference | Shape `alpha=2`, rate `beta=1` |
| Matter mass | `m^2=1` |
| Independent seeds per `(L,N)` | `20261010, 20261011, 20261012` |
| Warm-up | 1,000 complete sweeps per chain |
| Measurements | 3,000 per chain, 2 sweeps between measurements |
| Bootstrap | Chain resampling plus circular time blocks of 50, 100, and 200 measurements; 500 replicates per block length |
| Software | Python 3.12, NumPy 2.3.5, SciPy 1.17.0 |

The fixed point and lattice family mirror the email's previously unresolved `L=4,6`, `alpha=2`, `beta=m^2=1` run. The `L=8` extension and three-seed schedule were chosen before the rerun. However, initial direct-estimator summaries were inspected before the Rao–Blackwell estimator was selected; the estimator choice is therefore post-selection and the full study remains exploratory.

### Primary Rao–Blackwell estimates

Values are in the model's unscaled lattice units. Intervals show the envelope of the 95% chain/block-bootstrap intervals over block lengths 50, 100, and 200.

| N | L | `C(1)` | 95% interval envelope |
|---:|---:|---:|---:|
| 1 | 4 | `+2.77e-11` | `[-4.21e-11, +1.08e-10]` |
| 1 | 6 | `+2.49e-11` | `[-1.32e-12, +4.87e-11]` |
| 1 | 8 | `-3.58e-13` | `[-8.54e-12, +8.73e-12]` |
| 2 | 4 | `+2.73e-11` | `[-7.56e-10, +8.39e-10]` |
| 2 | 6 | `+3.15e-11` | `[-9.94e-11, +1.59e-10]` |
| 2 | 8 | `-2.20e-11` | `[-7.65e-11, +2.85e-11]` |

For `N=2,L=8`, the primary correlator estimates at separations `t=1,2,3,4` are respectively `-2.20e-11`, `-3.90e-11`, `-1.86e-11`, and `-8.62e-11`. The 95% block-bootstrap intervals for `t=1,2,3` include zero for all tested block lengths. The `t=4` interval is negative for all three block lengths; its envelope is `[-1.68e-10,-7.74e-12]`.

The direct sampled-flux estimator gives `N=2,L=8` `C(1)=-6.91e-6` with a 95% interval envelope `[-1.77e-5,+2.82e-6]`, and `C(4)=-1.02e-5` with envelope `[-2.28e-5,+2.09e-6]`. It is noisier and does not independently resolve either value. The two estimators use the same Markov chains, so they are dependent checks, not independent replications.

The scale of `C(0)` falls with the spatial averaging volume as expected; it is a contact/normalization diagnostic only. No effective-mass plateau is reported: there is no positive signal at two successive separated times, and the midpoint sign is negative. A cosh fit or pole claim would not be justified by these data.

## CIRCUS provenance and circularity audit

| Claim path | Operational definition | Evidence used | Feedback/leakage risk | Status |
|---|---|---|---|---|
| `N=2` has a separated odd-flux channel | `C_2(t)` for the declared `sin(F_01)` slice observable | Bernhard's email supplied the channel and motivated this observable | The claim selected the observable and therefore helped define the evidence channel | Supported as an operational definition; physical interpretation unresolved |
| The channel contains a one-particle pole | Positive, stable transfer correlator with a stable finite-size effective gap | Direct and Rao–Blackwell estimates from the same chains | No pole label or amplitude threshold was independently supplied; the estimator change followed a look at direct summaries | N/A as a confirmed pole/no-pole classification |
| `N=1` is the null comparator | Same action/parameters and operator with `N=1` | Three seeds at each size; Rao–Blackwell `C(1)` consistent with zero | The reported exact theorem motivated the null; simulation is a check, not its independent proof | Consistent with the stated control; theorem not reproved here |
| Larger volume resolves the channel | Compare `L=4,6,8` at fixed parameters | Three chains per size | `L=4,6` were selected by the upstream unresolved run; only `L=8` is new | No positive pole resolved; resolution remains insufficient |

**Material missing provenance:** no public, versioned source for the full N=2 model, no frozen source commit for the prior `L=4,6` simulation, no raw upstream trajectories, no external pole labels, no preregistered residue threshold, and no published proof that this odd operator must have a nonnegative reflection-positive correlator. These are N/A, not passes.

The largest feedback path is `open pole question → choose odd flux observable → inspect direct estimates → choose a lower-noise conditional estimator → interpret its near-zero channel`. The Rao–Blackwell estimator is mathematically motivated and unbiased for disjoint slices under the stated model, but its selection after seeing initial summaries prevents this rerun from serving as a blind confirmation.

## MONSTER stress-test record

| Perturbation family | Run status | Finding / boundary |
|---|---|---|
| Lattice size | Run at `L=4,6,8` | `N=2 C(1)` is consistent with zero at all three sizes; no finite-size pole plateau appears |
| Seeds | Three fixed seeds per size and N | Seed/block uncertainty included; only three independent chains, so weak effects remain unresolved |
| Estimator | Direct sampled flux vs conditional Rao–Blackwell | Same trajectories; Rao–Blackwell greatly reduces link-phase noise but is not an independent replica |
| Nuisance parameters (`alpha`, `beta`, `m^2`) | Not varied | Robustness outside `(2,1,1)` is N/A |
| Boundary/topology and aspect ratio | Periodic, isotropic 4-torus only | Alternate boundaries and anisotropic boxes not tested |
| Nulls | `N=1` control | Separated-slice result consistent with zero; no other null model run |

The first diagnostic boundary is already visible: no positive separated-time signal at `t=1,2,3` for `L=8`. At the opposite slice `t=4`, the Rao–Blackwell estimate is negative across block choices. That blocks a positive-pole extraction under this operator and parameter point, but it does not prove a general absence of poles. A clean no-pole conclusion would require a preregistered residue sensitivity bound and stable exclusion over larger volumes or a controlled transfer-spectrum argument.

## EFMW Zoo accounting

This is a bounded application of the same fork's EFMW Zoo review, not a claim that all 46 registered Lean modules were executed. The full 46-module roster and its N/A ledger are in [Stage 1](OPH_ANCHORED_LAPLACIAN_HEAT_BATH_TRANSFER.md).

| Animal | Stage 3 operation | Result |
|---|---|---|
| TORTOISE | Freeze model, lattice family, parameters, seeds and observable | Applied with the exploratory/post-selection limitation recorded |
| BAT | Trace the declared action and conditional kernels; compare with independent expression | Applied for this reimplementation; upstream source/revision match N/A |
| RHINO | Check that exact conditional updates preserve the stated target law | Conditional update derivation checked; no independent invariant-measure implementation supplied |
| TURTLE | Prevent an algorithmic sweep from being called physical time | Applied; no physical-time interpretation made |
| LYNX | Novelty check | Rao–Blackwellization and heat-bath sampling are standard; no novelty claim |
| CIRCUS | Trace definitions, data selection, labels and score dependencies | Applied above; key source/label paths remain N/A or dependent |
| MONSTER | Stress families, severity and first observed failure boundary | Applied to sizes, seeds, estimator and N=1 control; other nuisance families N/A |
| Remaining data/queue/agent animals | No matching input schema or evidence in this finite scalar simulation | N/A; no pass inferred |

## Verdict and next decisive check

- **Demonstrated:** exact Gibbs conditionals for the explicitly stated finite action; implementation runs at `L=4,6,8`; conditional phase averaging produces an unbiased disjoint-slice correlator under that action.
- **Supported but incomplete:** the `N=1` separated-slice Monte Carlo control is consistent with zero; the `N=2` channel has no resolved positive signal at the tested point.
- **Unresolved:** whether the intended OPH `N=2` source has a one-particle pole, a Coulomb regime, only a continuum, or a reflection-positivity obstruction.
- **Not established:** a clean no-pole result or a physical photon claim.

The most useful next check is a source-pinned replication with Bernhard's exact conductance reference convention, operator orientation, and reflection-positivity statement. It should freeze a pole-residue sensitivity threshold before any new data, retain raw chains, include at least one larger spatial volume, and use the Rao–Blackwell estimator as primary from the start. The current evidence does not meet a clean retirement criterion.

## Reproduction

The independent sampler is [`scripts/oph_n2_flux_mc.py`](../scripts/oph_n2_flux_mc.py); block-bootstrap summarization is [`scripts/summarize_oph_flux.py`](../scripts/summarize_oph_flux.py); the compact per-lag results are in [`docs/data/oph_n2_flux_stage3_summary.csv`](data/oph_n2_flux_stage3_summary.csv). The run JSON records include per-measurement direct and Rao–Blackwell slice series when generated by the script.

Example invocation:

```bash
python scripts/oph_n2_flux_mc.py --L 8 --N 2 --alpha 2 --beta 1 --m2 1 \
  --seed 20261010 --warmup 1000 --samples 3000 --thin 2 --output run.json
```

The upstream programme gate is distinct from this fork's exploratory work: public issues [#1025](https://github.com/FloatingPragma/observer-patch-holography/issues/1025) and [#1026](https://github.com/FloatingPragma/observer-patch-holography/issues/1026) currently report that no testable physical model has passed the positive selection gate. This finite-lattice run does not change that status.
