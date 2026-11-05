# Corrected N2 particle-channel pilot

2026-11-05. Independent `enuminous/oph-lab` finite-model experiment.
Baseline inspected: `693e574aa1519d5785c1c30ae2283eda6c423786`.

**Question:** can the corrected F01/axis-3 correlator be sampled precisely and
consistently enough to apply the already frozen single-cosh shape screen?
This pilot is not a particle-discovery, mass-measurement or continuum experiment.
All spectral and physical interpretations remain unresolved.

## Frozen model, geometry and estimators

The sampler represents two complex scalar species, oriented U(1) links and
positive Gamma conductances on a periodic four-dimensional **cubic** lattice.
Its supplied parameters are `N=2, alpha=2, beta=1, m2=1`. A sweep updates both
checkerboard colors for each species, all four link directions with von Mises
conditionals, then all four conductance directions with Gamma conditionals.
The kernel has no accept/reject rate; acceptance is not a useful mixing diagnostic.

The operator is the spatial average over axes 0,1,2 of the imaginary part of
`U0(x) U1(x+0) conjugate(U0(x+1)) conjugate(U1(x))`. Separation is along axis 3.
The direct and Rao–Blackwell (RB) estimators measure the same noncontact
connected correlator. RB is the preselected primary estimator; direct is a paired
cross-check. They share configurations and are never counted as independent
replications. Contact is excluded; the RB contact value remains JSON `null`.

The classifier is unchanged: required lags **1–5**, centers **2,3,4**, positive
lower envelopes at every lag, positive real gaps, at most **5%** relative point
gap spread and **25%** total relative gap-envelope width. These are engineering
thresholds, not statistical significance levels.

| Extent T=L | Frozen window | Use |
|---|---|---|
| 4, 6, 8 | Insufficient: lag 5 exceeds T/2 | Old data cannot meet this screen |
| 10 | Minimum even extent: lag 5 is the midpoint | Timing/geometry boundary control |
| 12 | All required lags fit; lag 5 precedes midpoint 6 | Bounded pilot |
| 16 | More transfer and spatial extent | Independent larger-volume follow-up |
| 20 or larger | Further extent comparison | Required if 12/16 disagree or finite-size control is inadequate |

Even extents are required by the periodic checkerboard update. `L>=10` follows
from the classifier, **not** from a demonstrated correlation length. Cubic
`L=12,16` comparisons change all four extents together; the current sampler has
no separately configurable spatial and transfer extents. An anisotropic study
would require a separate reviewed implementation and geometry tests. No lattice
spacing or renormalized trajectory is supplied, so increasing L at fixed bare
couplings is a finite-volume comparison, not a continuum extrapolation.

## Bounded sampling plan

The machine-readable pre-analysis plan is
[`experiments/oph_n2/pilot_v1.json`](../experiments/oph_n2/pilot_v1.json).

| Item | Frozen pilot |
|---|---|
| Lattice | 12^4 = 20,736 sites; 82,944 oriented links |
| Replicas | Four separate generator seeds; no resumed/common chain |
| Seeds and starts | 20261105101 hot; 20261105102 cold; 20261105103 hot; 20261105104 cold |
| Hot initialization | Independent complex Gaussian fields, uniform phases, prior Gamma conductances |
| Cold initialization | Fields zero, link phases zero, conductances alpha/beta |
| Warmup | 512 full sweeps per chain, discarded from correlators |
| Production | 1,024 measurements per chain; one full sweep between measurements |
| Cap | 6,144 total sweeps; 509,607,936 link updates, plus site/conductance/readout work |
| Resampling | 2,000 joint chain/circular-block replicates at each block size 16,32,64 |
| Block count | 64,32,16 full blocks per chain respectively |
| Bootstrap seed | 20261105901 + block length |

The cap bounds work; there is no promise that 512 sweeps thermalize the model or
that 1,024 observations resolve the flux. Saving each sweep permits diagnostics
without hiding correlation through thinning. Cold/hot agreement is a useful
challenge to initialization dependence, not proof that all modes were explored.
Seed diversity itself does not prove stationarity or adequate effective size.

## Raw schema and provenance

The observable version remains `F01-axis3-v2`; its geometry is unchanged. New
records use `raw_schema_version=oph-flux-chain-v3`, adding initialization, Python
and bit-generator versions, separate warmup/measurement/total elapsed times,
warmup diagnostic traces (initial state, every 16 sweeps, final warmup state),
and scalar diagnostics at every retained measurement. Scalars are:

- `psi_norm2_per_site`: sum over species and sites divided by site volume;
- `mean_conductance`: mean over all links;
- `matter_link_action_per_site`: the declared matter/link V divided by volume,
  **not** the full negative log density including Gamma priors and not a physical energy;
- `real_plaquette_mean`: mean real F01 Wilson product.

Both raw slice arrays retain shape `(measurements,L)`; measurement index is
sampler time, array column is the transfer coordinate. All lags, means and
diagnostics are computed from these raw records; no historical chain is
reconstructed. The run manifest hashes the exact configuration, sampler,
classifier, runner, requirements and every raw chain. The recorded parent git
revision may have a dirty tree during development; **the file hashes identify
the actual executed code**, not an implied clean parent checkout.

The runner refuses existing output directories. Interrupted/incomplete batches
remain on disk and cannot be analyzed as a complete four-chain experiment. A
fresh execution requires a new directory. Analysis verifies hashes, model,
seed/start assignments, sampling counts, geometry, diagnostics and RB contact.

The [preservation manifest](../experiments/oph_n2/preserved_evidence.json) binds
the October CSV, frozen historical classifier receipt, corrected smoke summary
and all four smoke chains to their original bytes. An exact smoke-sampler source
snapshot is retained alongside it. The integrity checker validates those chains
against that archived source, not the subsequently instrumented sampler.

## Sampling diagnostics and fail-closed decision

For every scalar, each estimator's mean flux, each lag-1–5 product, and each
connected-correlator influence series `q_t - 2*pooled_mean_flux*mean_flux_sample`:

1. Estimate the autocorrelation by FFT, with the biased 1/n autocovariance.
   Use `tau_int=1/2+sum(rho[1:W+1])`, the first self-consistent `W>=6*tau_int`
   up to n/4, conservatively clipping tau_int to at least 1/2. Report both
   measurement and sweep units. Report the first 64 autocorrelation lags.
2. Report each chain's estimated ESS `n/(2*tau_int)`, its mean and standard
   deviation. Reject zero variance, unresolved windows, chain length below
   100 tau_int, ESS below 100 per chain, or combined estimated ESS below 400.
   Combined ESS is the sum of per-chain estimates; it is not a certified ESS
   for nonlinear arcosh gap estimates or a tail-ESS calculation.
3. Compute the maximum of rank-normalized split R-hat and folded split R-hat
   across the independent chains; require <=1.01. Compare first/second-half
   means using autocorrelation-adjusted errors and flag differences above
   three estimated standard errors. These are screening alarms, not calibrated
   multiple-testing p-values or guarantees about unobserved slow modes.
4. Require the largest block to span at least 10 times the largest measured
   tau_int and retain at least 16 full blocks per chain. Require each channel
   and lag's largest/smallest block-bootstrap standard-error ratio <=1.25.

The resampler uses the **same** selected chains and circular block positions for
both estimators and all five lags. It recomputes pooled `mean(q)-mean(flux)^2`
inside every draw. The receipt retains the full 10-by-10 cross-lag/estimator
bootstrap covariance for each block length. It reports direct-minus-RB paired
errors and flags discrepancies above three estimated standard errors. Four
chains only give a small estimate of between-chain variability.

Classifier inputs are the envelope of pointwise 2.5/97.5 percentiles across all
three block sizes, expanded if necessary to contain the original point estimate.
The unexpanded quantiles are also retained. These are **exploratory envelopes**;
neither simultaneous coverage across five lags nor a formal gap confidence level
is asserted. Connected-mean subtraction has finite-sample bias; resampling is
not an exact bias correction. Autocorrelation estimates can miss long tails.

Any diagnostic alarm withholds numerical eligibility. The shape screen is still
shown separately so missing precision, positivity, geometry and shape failures
are distinguishable. A pilot candidate would remain only a finite shape
candidate; `stable_transfer_gap`, spectral reconstruction, volume stability,
physical identity and mass remain unresolved in this one-volume pilot.

The diagnostics are informed by [Wolff, *Monte Carlo errors with less errors*](https://arxiv.org/abs/hep-lat/0306017)
and [Vehtari et al., rank-normalized/folded R-hat](https://arxiv.org/abs/1903.08008).
This compact estimator is not a full implementation of every error-analysis
procedure in those papers. Known-scale IID/AR(1), offset-invariance, paired
bootstrap and shifted/scaled-chain controls test the implemented formulas.

## Exact reproduction

Run from the repository root at the commit containing this plan and its source
hashes. Python 3.12 with the pinned numerical dependencies is the recorded
environment. Timing fields and platform metadata vary; identical numerical raw
arrays are expected with the same RNG/numerical environment, not promised across
different NumPy/SciPy versions or floating-point platforms.

```bash
python -m pip install -r requirements-research.txt
python -m unittest discover -s tests -v
python scripts/check_research_contracts.py
python scripts/oph_observer_contract.py --check docs/data/oph_observer_contract.json
python scripts/run_oph_n2_pilot.py --config experiments/oph_n2/pilot_v1.json --dry-run
python scripts/analyze_oph_n2_pilot.py docs/data/oph_n2_pilot_v1 \
  --check docs/data/oph_n2_pilot_v1/analysis.json

# New measurements: choose a new output directory; existing evidence is protected.
python scripts/run_oph_n2_pilot.py --config experiments/oph_n2/pilot_v1.json \
  --output /tmp/oph-n2-pilot-replay
python scripts/analyze_oph_n2_pilot.py /tmp/oph-n2-pilot-replay \
  --output /tmp/oph-n2-pilot-replay/analysis.json

# Timing probes only; run without other sampling jobs on the same CPU.
python scripts/benchmark_oph_n2.py --output /tmp/oph-n2-timing-replay.json
```

CI runs the fast tests, preserved-evidence checks and deterministic **reanalysis
of archived raw data**. It does not rerun the 6,144-sweep pilot or certify mixing.
The old smoke-only `summarize_oph_flux.py` remains available for historical
reproduction; use the new analyzer for pilot diagnostics and the classifier bridge.

### Portable replay correction

The first published CI run passed all 88 implementation tests and source/data
integrity checks, but failed the exact floating-point receipt comparison. A
local replay with `NPY_DISABLE_CPU_FEATURES=AVX2,FMA3,AVX512F` and
`OPENBLAS_CORETYPE=NEHALEM` reproduced 4,740 floating-only differences, with
maximum relative difference 3.031e-13 and no categorical/structural changes.
Bit-for-bit equality of derived FFT/BLAS statistics was an excessive portability
requirement, even with the same raw data and pinned NumPy/SciPy versions.

Analysis schema v2 uses relative tolerance **1e-10** and absolute tolerance
**1e-30** for finite floating-point replay values only. The tiny absolute floor
cannot hide the approximately 1e-11 RB signal or its uncertainty. Structure,
hashes, policy names, integer counts and all categorical decisions must match
exactly. These are computational replay tolerances; no sampler, shape-screen,
diagnostic or statistical threshold changed. Two added tests reject material
changes to tiny signals/covariances and any decision/provenance/structure change.
The original [v1 receipt](data/oph_n2_pilot_v1/analysis_exact_v1.json) and
[v1 analyzer source](../experiments/oph_n2/sources/analyze_oph_n2_pilot_exact_v1.py)
remain hash-protected. On the recorded platform, v2 changes only the schema,
analysis-source hash and explicit replay policy; every computed scientific
value and classification is unchanged.

```bash
NPY_DISABLE_CPU_FEATURES=AVX2,FMA3,AVX512F OPENBLAS_CORETYPE=NEHALEM \
  python scripts/analyze_oph_n2_pilot.py docs/data/oph_n2_pilot_v1 \
  --check docs/data/oph_n2_pilot_v1/analysis.json
```

## Evidence produced and measured costs

See the [raw manifest](data/oph_n2_pilot_v1/manifest.json),
[analysis receipt](data/oph_n2_pilot_v1/analysis.json) and
[timing probes](data/oph_n2_timing_v1.json). The outcome and timing table below
are filled from the completed run, without changing the frozen policy.

Validation includes twelve new pilot tests (portable replay, extent boundary, frozen-plan guards,
non-overwrite behavior, archived/current sampler equality, diagnostic replay,
known IID/AR(1) autocorrelation, rank/folded R-hat alarms, connected-offset
invariance, paired bootstrap and corrupted/incomplete evidence rejection).
The existing geometry, classifier, finite-model and ledger checks remain in the
full test suite. Web lint, production build, observer receipt and research
integrity checks also pass locally. No Lean source or theorem is changed by
this experiment.

The four N2/L=12 chains completed in **322.77 s (5.38 min)** serial wall time. Both corrected channels remain **unresolved**: all five required lower envelopes are nonpositive; no effective gap or mass is emitted. All 12 historical classifications remain unchanged and unresolved.

The largest rank/folded split R-hat was 1.00162; maximum estimated tau_int was 0.9608 measurements and minimum estimated per-chain ESS was 532.90 across the monitored series. These short-chain estimates are not a mixing certificate. Block standard-error ratios were 1.020–1.068; maximum paired direct/RB discrepancy was 1.523 estimated standard errors. The second chain (cold start, seed 20261105102) nevertheless had **3.599** estimated standard errors of first/second-half drift in direct mean flux, exceeding the frozen threshold 3. Therefore the numerical diagnostic gate is **unresolved**, independently of the signal failure.

| Lag | Primary RB estimate | Exploratory lower envelope | Exploratory upper envelope |
|---|---:|---:|---:|
| 1 | 8.442571e-12 | -4.476396e-12 | 2.130375e-11 |
| 2 | -7.175483e-12 | -2.156345e-11 | 6.807952e-12 |
| 3 | -9.306176e-16 | -1.638768e-11 | 1.520972e-11 |
| 4 | 4.344954e-12 | -8.786772e-12 | 1.720311e-11 |
| 5 | -3.155057e-12 | -1.539611e-11 | 9.147214e-12 |

These are dimensionless finite-model connected flux correlators. The intervals are pointwise bootstrap envelopes, not simultaneous confidence bands or evidence of zero correlation.

Timing used three isolated probes per size, each with 16 warmup sweeps and 32 measured sweeps, including both readouts and scalar diagnostics. Hardware/runtime and probe seeds are in the timing receipt. No benchmark correlator enters inference.

| L | Sites | Measured seconds / measured sweep, median (range) | Four-chain pilot projection | Four-chain 2,048+8,192-sweep proposal |
|---|---:|---:|---:|---:|
| 10 | 10,000 | 0.0306 (0.0291–0.0372) | 2.66 min | 18.97 min |
| 12 | 20,736 | 0.0654 (0.0601–0.0670) | 5.73 min | 40.81 min |
| 16 | 65,536 | 0.1943 (0.1859–0.2026) | 16.92 min | 120.72 min |

The L=12+16 longer proposal projects to **2.69 hours serial wall time** here; reserve approximately **5.4 hours** with a 2x margin, before any doubled-length or third-volume work. This is a work estimate, not a guarantee of precision. Four truly available CPU workers might reduce elapsed time, but memory bandwidth, CPU quotas and independent process overhead prevent assuming a 4x speedup; the supplied runner is serial.

The largest timing-probe process peak RSS was 66.4 MiB on this Linux runtime. This is a small-probe measurement, not a full-run upper bound. The bare state is `96*L^4` bytes for N=2 (1.90 MiB at L=12, 6.00 MiB at L=16), plus checkerboard masks, temporary arrays, Python/runtime and retained observations. Work per sweep is approximately proportional to L^4 at fixed N; the measured L=16/L=12 sweep-cost ratio is 2.97, versus volume ratio 3.16. Full pilot raw JSON occupies **3,883,323 bytes**; longer-run storage grows roughly linearly with measurement count and transfer extent. Budget generously for temporaries and measure peak memory before adding parallel workers.

## Requirements before interpreting a stable transfer gap

| Evidence layer | Required before advancing | What it cannot establish |
|---|---|---|
| Software correctness | Direct-index, local-gauge and orientation tests; replay; schema/provenance checks; classifier and statistical controls | Sampling equilibrium or a physical spectrum |
| Numerical convergence | Stable warmup/production traces, adequately long independent hot/cold chains, reliable autocorrelation and ESS, block stability, paired estimator agreement; longer fresh-seed and volume replication | Positivity/reconstruction, particle species or SI masses |
| Finite spectral evidence | Positive separated correlator with quantified uncertainty, frozen-window stable nonzero gap, operator reflection parity and positive transfer reconstruction; other operators/momenta, threshold and excited-state separation | A continuum quantum theory or identity with a natural particle |
| Physical identification | Source-selected action/operator dictionary, controlled interacting continuum, spin/statistics/charges, dispersion, target-independent physical clock/scale and held-out empirical tests | Completion of untested observables or EPR completeness by itself |

Only after software checks and numerical diagnostics pass should a candidate
gap be interpreted as evidence for the **finite correlator's declared shape**.
A transfer-eigenvalue interpretation additionally requires the spectral layer.
A mass would require a physical-time and scale attachment; sampler sweeps are
never that clock. A failed/negative/insensitive correlator screen yields
`unresolved`, not a clean exclusion or proof that the theory has no particles.

## Next run and stopping rules

Treat this pilot as a design/sensitivity dataset. A later confirmatory batch
must use a new versioned configuration and new seeds, frozen before inspecting
its data. Do not pool it with the pilot to manufacture a threshold crossing.
Retain all chains and failed channels; do not select the best seed, block size,
estimator, lag window or lattice after seeing the signal.

A reasonable **initial budget proposal**, not a mixing guarantee, is four
chains each at L=12 and L=16, 2,048 warmup sweeps, 8,192 measurements at thin=1,
with new seeds `20261106101..104` (L=12) and `20261106201..204` (L=16), alternating
hot/cold as above. Use blocks 64,128,256 only if the pilot/long-chain tau estimates
justify them and at least 16 full blocks remain. Freeze a fresh config (and its
explicit work caps) before execution; this proposal is **not executed here**.
The invariant classifier window and shape tolerances must remain unchanged.

For thermalization/length sensitivity, additionally compare a separately seeded
batch with doubled warmup and production length. A longer first batch may be
needed if slow modes or signal-to-noise demand it. Require fresh-seed agreement
and prespecified precision on the gap differences: merely overlapping very wide
intervals or failing to reject a difference is not evidence of stability. Freeze
an equivalence margin and a joint uncertainty procedure before interpreting
volume/length agreement. L=12/16 cannot alone separate spatial-size from
transfer-wrap effects. If significant differences persist, add L=20 or a reviewed
anisotropic implementation; do not call fixed-coupling size scaling a continuum
limit. New operators/momenta and reconstruction proofs are separate work items.

At the resource cap, stop and report the actual diagnostics and sensitivity.
Increasing sample size reduces error roughly as inverse square root of
effective samples only under stable autocorrelation and finite variance; a
timing extrapolation cannot promise adequate signal at lag 5. If the channel
remains unresolved, archive that outcome before proposing a new experiment.
