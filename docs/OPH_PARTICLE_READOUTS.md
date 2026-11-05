# Finite particle-channel readouts

Date: 2026-11-05. Scope: the independent `enuminous/oph-lab` finite models.

The implemented readout screens a specified operator's correlator for a stable
single-cosh shape in a fixed transfer-coordinate window. It does not identify
nature's particles. The legacy Stage 3 dataset is **quarantined for an operator
axis mismatch** and remains unresolved in every one of its 12 `(N, L, estimator)`
channels. Its values are retained only as legacy implementation regressions.
They cannot establish the documented physical channel. An absent positive signal
would not establish a clean no-pole result even with correct provenance.

## Executable contract

[`oph_particle_readouts.py`](../scripts/oph_particle_readouts.py) accepts
`lag: (estimate, lower, upper)` for a finite even periodic transfer extent. The
source and coordinate are explicit. Lag zero is never used, because the existing
Rao–Blackwell contact value is not an estimator of the desired contact correlator.

The default policy requires all lags 1–5 and fixes effective-gap centers 2, 3, 4.
At every required lag the supplied lower envelope must be strictly positive.
For a single finite periodic contribution

\[
C(t)=A\left(e^{-Et}+e^{-E(T-t)}\right),\qquad A>0,
\]

adding the neighboring values gives

\[
C(t-1)+C(t+1)=2\cosh(E)C(t),\qquad
E_t=\operatorname{arcosh}\!\left(\frac{C(t-1)+C(t+1)}{2C(t)}\right).
\]

This is an elementary identity of the declared finite shape. It is the entire
mathematical basis of the readout. A spectral representation or a physical-time
interpretation is not assumed to follow from it.

For positive input envelopes `[l_t,u_t]`, the local ratio lies in
`[(l_(t-1)+l_(t+1))/(2u_t), (u_(t-1)+u_(t+1))/(2l_t)]`.
Monotonicity of `arcosh` propagates this interval, with its lower endpoint clipped
to the real domain at 1. If the lower gap then reaches zero, the screen fails.
No joint confidence level is assigned: pointwise bootstrap intervals from the
old study do not automatically become a simultaneous confidence region.

The relative spread of point gaps must be at most 5%, and the full envelope width
relative to their mean must be at most 25%. These are declared **engineering
screening thresholds**, not significance levels or laws of physics. They were
fixed for the implementation controls; applying them to the October data is
retrospective. Any change is a new policy and needs a fresh confirmatory dataset.

Passing emits `single_cosh_shape_candidate` and a dimensionless transfer gap.
All failures emit `unresolved`; missing observations, weak signal and a shape
failure remain distinct reasons. No branch emits a physical particle name or a
no-pole exclusion. A zero gap is not evidence that the source contains photons
or gravitons.

## Falsification controls and result

| Input | Required behavior | Result |
|---|---|---|
| Exact periodic single cosh, gap 0.4 | Recover the declared gap | Candidate; gap 0.4 within floating-point precision |
| Positive two-gap mixture with visible curvature | Fail the fixed-window plateau | Unresolved |
| Zero signal with intervals spanning zero | Emit no gap and no exclusion | Unresolved |
| Negative separated correlator | Reject positive-signal premise | Unresolved |
| Stable central curve with broad intervals | Refuse a precision claim | Unresolved |
| Contaminated contact value | Keep noncontact readout unchanged | Contact ignored |
| Legacy Stage 3 `N=1,2`, `L=4,6,8`, both estimators | Quarantine operator mismatch; retain regression values | All 12 unresolved |

The synthetic single-cosh fixture tests formula and software behavior; its
declared gap is not a new prediction. The mixture is a selected implementation
control, not a benchmark proving general excited-state rejection. Late-time
mixtures can pass this shape screen when one term dominates. Likewise different
charge or spin assignments can share the same scalar correlator: those labels
cannot be inferred from this input alone.

The November 5 source audit found that the old sampler selected `theta[mu]`
before rolling its axes, but then used axes 1 and 2 where the documented
`F_01` needs axes 0 and 1. Averaging axes `(1,2,3)` left axis 0, whereas the
documented separation is axis 3. Correcting today's implementation cannot
retroactively repair the old CSV. Every legacy result therefore carries
`quarantined_axis_mismatch` and cannot become a candidate regardless of its
numerical shape.

The old extents are also too short for the declared three-center window. This
fact does not by itself imply a physical failure. The independent positivity
failure at the required available lags preserves the earlier unresolved result.
Raw Stage 3 chains are not reconstructed from the CSV; no new Monte Carlo run or
confidence analysis is claimed.

## Remaining particle-identification obligations

| Obligation | Present evidence | Status |
|---|---|---|
| Specified finite operator and estimator | Definition available; historical implementation axes mismatch | Historical CSV quarantined; corrected implementation needs new runs |
| Stable single-channel shape on physical source | No resolved positive Stage 3 signal | Unresolved |
| Transfer positivity for the operator's reflection parity | Not provided by the classifier | Unresolved |
| Spin, statistics, charges and gauge-invariant observable dictionary | Not read from a scalar two-point shape | Unresolved |
| Separation from multiparticle thresholds; other operators and volumes | Absent from present receipt | Unresolved |
| Interacting continuum and recorded physical clock | Finite supplied transfer coordinate only | Unresolved |
| Physical masses and independent experimental identification | No source-selected calibration or held-out empirical match | Unresolved |

Reading the simulator specification, observer, scheduler, repair law, and memory
law is legitimate evidence about an implemented model. Those observations must
still be connected to the physical operator and clock, with a traceable
derivation and independent observational tests. Access to the code does not
erase those attachment obligations.

## Reproduction

```bash
python -m unittest discover -s tests -p 'test_particle_readouts.py' -v
python scripts/oph_particle_readouts.py --output docs/data/oph_particle_readouts.json
```

The [machine-readable receipt](data/oph_particle_readouts.json) records the frozen
policy, negative controls, all channel classifications, and SHA-256 of the old
CSV. The earlier [Stage 3 report](OPH_N2_FLUX_STAGE3.md) records its exploratory
sampling design and estimator selection; its operator-to-implementation claim
must be read with the November axis correction above.
