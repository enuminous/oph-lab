# Interacting scalar readouts in 3+1 dimensions

**Date:** 2026-11-05. **Evidence status:** demonstrated numerical verification
of a supplied classical model; source-derived interacting quantum continuum
and physical particle interpretation unresolved.

This extends the [earlier linear wave benchmark](OPH_EFMW_CONTINUUM_LIMIT.md)
with a nonzero quartic self-interaction, a Hamiltonian readout, retained time
records, an analytic-solution verification, and an interaction-omission control.
The executable is [oph_interacting_continuum.py](../scripts/oph_interacting_continuum.py);
the frozen receipt is [oph_interacting_continuum.json](data/oph_interacting_continuum.json).
No external observations or measured particle masses enter this benchmark.

## Supplied model and units

On a periodic cubic lattice with spacing \(h=L/N\), the declared action is

\[
S_h=\int dt\,h^3\sum_x\left[\frac12\dot\phi_x^2
-\frac{c^2}{2}\sum_{i=1}^3(D_i^+\phi_x)^2
-\frac{m_0^2}{2}\phi_x^2-\frac{\lambda}{4}\phi_x^4+J_x(t)\phi_x\right].
\]

Here \(D_i^+\phi_x=(\phi_{x+he_i}-\phi_x)/h\). The actual supplied constants
are \(L=2\pi\), \(c=1\), \(m_0^2=0.7\), and \(\lambda=2\). The API allows
nonnegative \(m_0^2,\lambda\), positive \(c,h\), and real finite fields.
All values use dimensionless model units; no clock, field normalization, or
energy conversion to SI/GeV has been identified. In dimensional variables,
\([c]=L/T\), \([m_0^2]=T^{-2}\),
\([\lambda]=T^{-2}[\phi]^{-2}\), and \([J]=[\phi]T^{-2}\).
An overall normalization of the action remains needed to attach physical
energy units. The coefficient \(m_0^2\) is a bare model coefficient.

Variation using periodic summation by parts gives the semi-discrete equation

\[
\ddot\phi=c^2\Delta_h\phi-m_0^2\phi-\lambda\phi^3+J.
\]

Thus all three spatial directions couple, and \(\lambda\ne0\) couples Fourier
modes. The declared model has one real classical scalar field. It does not
contain fermions, gauge fields, a spin-two metric, or a Standard Model spectrum.

## Energy and evolution

With \(v=\dot\phi\), the readout is

\[
H_h=h^3\sum_x\left[\frac{v_x^2}{2}
+\frac{c^2}{2}\sum_i(D_i^+\phi_x)^2
+\frac{m_0^2}{2}\phi_x^2+\frac{\lambda}{4}\phi_x^4\right].
\]

The gradient of this finite Hamiltonian is exactly the negative unforced
acceleration in the volume-weighted inner product. Consequently the exact
semi-discrete ODE obeys \(dH_h/dt=h^3\sum_xJ_xv_x\); it conserves \(H_h\)
when \(J=0\). Velocity-Verlet approximates this ODE. Its numerical energy is
monitored, not asserted to be exactly conserved. The implementation records
kinetic, gradient, quadratic, quartic, and total energy, source work, field RMS,
velocity RMS, and model time after every step. A test checks the energy gradient
by independent directional finite differences. Another checks source work
against the analytic constant-force solution.

An instantaneous frequency guard is checked before each force evaluation:

\[
\Delta t\sqrt{12c^2/h^2+m_0^2+3\lambda\max_x|\phi_x|^2}<1.8.
\]

This is a conservative linearized-frequency rejection rule. It is not a global
nonlinear stability theorem; large forcing can still demand smaller steps.
NaN/Inf, incompatible shapes, complex fields, negative potential coefficients,
and unsafe time steps are rejected. Velocity-Verlet retains both field and
velocity; this is an authored evolution/memory rule, not a derivation from
monotone OPH accepted repairs.

## Verification and controls

The manufactured solution is

\[
\phi_*(x,y,z,t)=0.4\sin x\sin y\sin z\cos(1.7t),\qquad
J_*=(3+0.7-1.7^2)\phi_*+2\phi_*^3.
\]

The source is analytically chosen to test the solver. It is not an independent
prediction, a source-only physical reconstruction, or evidence for the action.
The source expression remains fixed when the negative control removes the
quartic term from the equation.

| Grid N | Final field RMS error at t=0.6 | Observed order from prior grid |
|---|---:|---:|
| 12 | 0.001363740815 | — |
| 18 | 0.000608107084 | 1.991875 |
| 24 | 0.000341668948 | 2.003979 |
| 36 | 0.000152097376 | 1.996032 |

The declared acceptance criteria are all observed field orders above 1.8,
maximum relative unforced energy drift below \(5\times10^{-4}\), energy-drift
improvement above 3 when the step is halved, and an interaction-omission error
ratio above 3. These are implementation-verification criteria, not universal
physical criteria or a preregistered empirical test. The receipt retains the
criteria and full energy trace.

At \(N=16\), over \(0\le t\le2\), maximum relative unforced energy drift is
\(8.96158\times10^{-5}\) at \(\Delta t=0.00980392\), falling to
\(2.24048\times10^{-5}\) at half that step (improvement 3.99986).
At \(N=36\), omitting the interaction increases manufactured field error by
18.1867 times. The finite nonlinear term is therefore exercised by the test.

## Evidence boundary and remaining premises

| Claim or premise | Status | What would be needed next |
|---|---|---|
| The supplied nonlinear semi-discrete action and energy agree | Demonstrated algebraically and numerically | Existing directional-gradient test |
| Three spatial directions and the quartic interaction affect dynamics | Demonstrated for this implementation | Existing eigenmode and interaction-off controls |
| Near-quadratic convergence on the manufactured finite-horizon case | Demonstrated numerically | Uniform error theorem for a specified nonlinear solution class |
| Canonical OPH source forces this action, carrier, or coupling | Unresolved | Source-to-action map independent of desired field equation |
| The model clock is an observer's recorded physical time | Unresolved | Same-source calibrated clock/readout theorem |
| Quantum interacting continuum exists for this OPH construction | Unresolved | Quantization, regulator/renormalization prescription, continuum control and observables |
| Modes identify nature's particles or physical pole masses | Unresolved | Spin/statistics, charges, spectral limits, calibration and independent observations |
| Einstein gravity or EPR-style explanation of all observables follows | Unresolved | Additional gravitational and completeness premises |

Reading the simulator specification is allowed and supplies exact knowledge of
the action, grid, clock, and update law. That knowledge makes the finite model
auditable. It does not establish that these supplied objects are the laws and
observables of nature. No novelty is claimed for the standard phi-four action,
periodic finite differences, or velocity-Verlet scheme.

## Reproduction

From the repository root, with Python and NumPy installed:

```sh
python scripts/oph_interacting_continuum.py --output docs/data/oph_interacting_continuum.json
python -m unittest discover -s tests -p test_interacting_continuum.py -v
```

The receipt includes the implementation SHA-256 and no wall-clock timestamp.
Floating-point last bits can differ across NumPy/platform versions; the
scientific acceptance criteria use tolerances and refinement ratios.
