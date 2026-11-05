# Mass and energy readouts of the declared finite Gaussian model

Date: 2026-11-05. Baseline inspected: `d498af3926c98889531bca425565867409103a99`.

The new [executable readout](../scripts/oph_mass_energy.py) recovers the
dimensionless Gaussian transfer gap from an independently assembled finite
precision matrix. All 15 frozen cases pass the absolute gap tolerance of
`1e-10`. The [receipt](data/oph_mass_energy.json) includes each direct
covariance, parameters, error, and an uncalibrated readout. This completes a
numerical consistency check for the declared model. It supplies no physical
clock, no measured particle mass, and no identification with nature's particles.
The receipt also fingerprints the executable source with SHA-256 and records
the Python/NumPy versions; the baseline commit records historical context.

## Definitions and dimensions

The source model is the homogeneous periodic Gaussian specialization in
[Stage 1](OPH_ANCHORED_LAPLACIAN_HEAT_BATH_TRANSFER.md). It has three
transverse spatial axes and one chosen Euclidean transfer axis. The action,
field normalization, anchor, couplings, and coordinates are supplied in
dimensionless lattice units. `kappa > 0` and every coupling is positive.
The massless periodic constant mode is deliberately outside this contract:
without an additional constraint it makes the Gaussian measure nonnormalizable.

For lattice momentum angles `theta_i`, define

\[
\omega(\theta)=\kappa+4\sum_{i=1}^{3}J_i\sin^2(\theta_i/2),\qquad
\Delta(\theta)=2\operatorname{asinh}\!\left(\frac12\sqrt{\frac{\omega(\theta)}{J_0}}\right).
\]

The implementation uses `asinh`, rather than subtracting nearly equal
floating-point numbers in `acosh(1+x)`. In particular, an anchor as small as
`1e-24` with unit transfer coupling yields a nonzero gap near `1e-12`.
On a finite spatial torus the caller must use allowed angles `2*pi*n_i/L_i`;
arbitrary angles evaluate the symbol but need not be modes of that torus.

| Quantity | Meaning | Dimension / permitted interpretation |
|---|---|---|
| `kappa` | Supplied uniform quadratic anchor | Dimensionless action coefficient; not a measured mass |
| `omega` | Supplied spatial symbol evaluated at a lattice momentum | Dimensionless |
| `Delta` | One-excitation Gaussian transfer gap, conditional on the Stage 1 spectral relation | Dimensionless decay per transfer step |
| `a_t` | Caller-supplied seconds per transfer step | Seconds; needs an independent clock and spectral bridge |
| `E = hbar Delta / a_t` | Conditional energy-unit conversion | Joules; `E / (10^9 e)` in GeV |
| `m = E(0)/c^2` | Conditional rest-energy conversion at zero momentum | Kilograms or GeV/c²; not emitted at nonzero momentum |

For example, with `kappa=1` and `J0=1`, the zero-momentum gap is
`2 asinh(1/2)`, approximately `0.9624`, not the bare anchor `1`.
In the small-gap regime its leading behavior is `sqrt(kappa/J0)`.
Neither formula identifies an experimental pole mass. The classical
Hamiltonian of the separate interacting benchmark is also a different
readout; no conversion between that model clock and the transfer clock is
assumed here.

## Independent finite check

For each supplied transverse mode, the code constructs the precision matrix
directly by adding edge contributions to the quadratic action

\[
V(q)=\frac12\sum_{t=0}^{T-1}
\left[J_0(q_{t+1}-q_t)^2+\omega q_t^2\right],\qquad q_T=q_0.
\]

It solves `Q C = delta_0` and reads the full periodic covariance `C(t)`.
The gap formula is not used in the matrix construction or linear solve.
Away from the contact index `t=0`, the local recurrence gives the estimator

\[
\Delta_{\mathrm{eff}}(t)=\operatorname{acosh}
\frac{C(t-1)+C(t+1)}{2C(t)}.
\]

The fixed matrix tests use `T=16`, spatial extent `L=8`, anchors
`{0.05, 0.1, 0.25, 0.5, 1.0}`, transverse couplings `(1, 0.8, 1.1)`, and
three predetermined `(J0, mode)` pairs: `(0.5, (0,0,0))`,
`(1, (1,0,0))`, and `(2, (1,1,0))`. Every noncontact lag must return a
finite estimate within `1e-10` of the declared Gaussian transfer gap.
The solve itself must have infinity-norm residual at most `1e-10`.

This is deterministic linear algebra, so the receipt has no Monte Carlo
confidence interval. It checks the per-mode covariance and periodic
wraparound. It does not independently establish the assumed spatial
Fourier symbol, the infinite-dimensional Mehler eigenbasis, or a physical
time interpretation. An arbitrary noisy correlator cannot inherit the
Gaussian interpretation merely because a local cosh estimate is finite.
Use the separate particle-channel classifier for evidence gates and
uncertainty handling.

## Calibration gate and negative controls

`gaussian_readout()` emits a dimensionless gap and `null` physical values by
default. A `ClockCalibration` must supply a positive finite time step,
nonempty clock and spectral-bridge provenance references, the exact
`equilibrium_transfer` coordinate tag, and an explicit declaration of
independence from the mass target. The module refuses sampler-sweep clocks,
missing references, and target-fitted calibrations.

A supplied reference is not a verified proof. Even when a contract passes,
the status is **conditional_unit_conversion**,
`evidence_verified_by_code` stays false, and particle identification stays
**unresolved**. No production physical calibration is included in the
receipt. The unit-conversion tests use conspicuously labeled synthetic
clock and bridge fixtures only.

Boolean/string/nonfinite parameters, negative couplings, and an unpinned zero
anchor are rejected. A nonpositive correlator triplet or a cosh argument
below one returns `null`, not a zero mass and not a no-particle verdict.
The contact estimate is always withheld. Overflow or lost precision in a
matrix solve fails explicitly rather than emitting `NaN` JSON.

## Reproduce

From the repository root with NumPy installed:

```sh
python -m unittest discover -s tests -p test_mass_energy.py -v
python scripts/oph_mass_energy.py --output docs/data/oph_mass_energy.json
```

The 11 unit tests cover the independently assembled action and matrix,
positive spectrum, finite covariance recurrence across 15 frozen cases,
small-anchor precision, momentum dependence, invalid correlators,
uncalibrated withholding, conditional units, moving-energy/rest-mass
separation, and calibration refusal controls. The receipt records
floating-point results; last-bit differences across NumPy/BLAS versions
must be judged against the frozen tolerance, not byte equality.

## Remaining scientific premises

| Premise | Status after this implementation |
|---|---|
| Finite covariance agrees with the supplied Gaussian transfer formula | Demonstrated numerically for the 15 frozen cases |
| Gap is distinct from the bare anchor and sampler update rate | Enforced by the API and tests |
| SI arithmetic follows from a supplied scale and bridge | Demonstrated conditionally; no real scale supplied |
| OPH selects this homogeneous action and its coefficients | Unresolved |
| Chosen transfer axis has a verified physical clock and Hamiltonian reconstruction | Unresolved |
| Renormalized interacting pole spectrum and continuum control | Unresolved; Gaussian validation does not transfer to interactions |
| Spin, statistics, gauge charges, families, and experimental particle identity | Unresolved |
| Independent physical units and held-out mass comparisons | Unresolved |

The defining SI constants used in the arithmetic are the exact values
published by the [BIPM](https://www.bipm.org/en/measurement-units/si-defining-constants):
`h = 6.62607015e-34 J s`, `c = 299792458 m/s`, and
`e = 1.602176634e-19 C`. The code computes `hbar = h/(2*pi)` at floating-point
precision. These constants supply unit conversions, not an OPH prediction.
