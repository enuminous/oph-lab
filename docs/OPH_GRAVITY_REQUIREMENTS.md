# Gravity readouts: exact finite tomography and the remaining physical premises

**Date:** 2026-11-05  
**Scope:** independent `enuminous/oph-lab` implementation; supplied flat tensor interface  
**Result:** the finite null readout determines a symmetric tensor modulo the metric. Physical Einstein dynamics, measured Newton coupling, and a source-selected cosmological constant remain **UNRESOLVED**.

The implementation is [`scripts/oph_gravity_requirements.py`](../scripts/oph_gravity_requirements.py),
the regression controls are [`tests/test_gravity_requirements.py`](../tests/test_gravity_requirements.py),
and the deterministic receipt is [`docs/data/oph_gravity_requirements.json`](data/oph_gravity_requirements.json).
It uses Python's exact rational arithmetic and standard library only.

## Frozen target and provenance

The inspected baseline is `d498af3` of this fork. Its
[`README.md`](../README.md#gravity--lorentz-branch),
[`GRAVITY_SURFACE`](../src/content/paperSurface.ts), and
[`GravityPage`](../src/pages/Gravity.tsx) already distinguish finite directional
balances, tensor conservation, physical stress and coupling, continuum bridges,
and the metric ambiguity. This implementation supplies local executable
diagnostics for that boundary. It does not reproduce the absent sibling
research repository's complete proof chain or revise its canonical claim IDs.
The local requirement IDs below are explicitly new audit identifiers.

Introspection of observer, scheduler, repair, and memory specifications is an
allowed source of model evidence. Reading a supplied implementation can identify
its action, state, or clock convention. A claim that those objects are measured
physical stress, curvature, or time still requires a documented identification
with observations. The evaluator accepts such evidence records rather than
treating implementation access itself as a completed identification.

## Exact nine-direction finite result

Supply a real symmetric covariant tensor \(H_{ab}\) on a four-dimensional vector
space and the metric \(\eta=\operatorname{diag}(-1,1,1,1)\). Read

\[
q_H(k)=H_{ab}k^ak^b
\]

on the following nine null vectors:

\[
(1,\pm1,0,0),\quad (1,0,\pm1,0),\quad (1,0,0,\pm1),
\]

\[
(1,3/5,4/5,0),\quad (1,3/5,0,4/5),\quad(1,0,3/5,4/5).
\]

**Finite lemma.** If all nine readings vanish then
\(H=\lambda\eta\), with \(\lambda=-H_{00}\).

**Proof.** The sum and difference of the two axial readings in direction \(i\)
give \(H_{ii}=-H_{00}\) and \(H_{0i}=0\). Substitution into each mixed reading
cancels its diagonal terms; the remaining term is \((24/25)H_{ij}\).
Therefore all three spatial off-diagonal entries vanish. These relations give
exactly \(H=\lambda\eta\). Conversely, every such tensor has zero null readings.

The corresponding linear map has a ten-dimensional input, rank nine, and a
one-dimensional kernel. The code verifies the rank using exact row reduction
and reconstructs a representative with \(H_{00}=0\). This reporting convention
is **not** an observation of the missing metric component. Applied to the
difference of any two tensors, the lemma proves that identical readings imply
they differ by a metric multiple.

The six axial vectors alone have rank six and miss all three spatial shear
components. The tests include a nonzero \(H_{12}=H_{21}=1\) tensor that all six
axial readings miss, while a mixed reading detects it. Supplying a non-null
vector, nonsymmetric tensor, non-finite coefficient, or zero vector is rejected.

**Evidence status:** demonstrated analytic finite linear algebra with exact
computational checks. These statements concern the supplied tensor interface;
they do not establish source selection of nine physical directions or the
equation relating curvature and stress. This new Python module is not a Lean
proof and is not represented as one.

## Conservation removes variation, not the free constant

In a metric-compatible smooth continuum, if an independently established
tensor identity gives \(H_{ab}=\lambda g_{ab}\) and
\(\nabla^aH_{ab}=0\), then \(\nabla_b\lambda=0\). With the necessary regularity
and connectedness, \(\lambda\) is constant. Its value is still undetermined.
For \(H_{ab}=G_{ab}-\kappa T_{ab}\), the conventional Einstein form is
\(G_{ab}+\Lambda g_{ab}=\kappa T_{ab}\), so \(\Lambda=-\lambda\).

The finite executable checks only the analogous, explicitly supplied scalar
incidence law: on every graph edge \((u,v)\),
\(\lambda_v-\lambda_u=0\). A connected graph leaves one constant; a graph with
\(c\) connected components leaves \(c\) constants. This follows by following
paths from one vertex to another. The receipt checks both a varying assignment
that fails and a disconnected assignment with distinct component constants
that passes. Neither a discrete Bianchi identity nor physical stress
conservation is inferred from this graph test.

The metric-shift counterexample is exact: the supplied test tensor and that
tensor plus \((7/3)\eta\) have identical readings on all nine directions.
Any constant shift also survives the finite conservation diagnostic. Thus null
tomography and conservation alone cannot select the cosmological term.

## Requirements evaluator

`evaluate_requirements(evidence, route, require_lambda)` validates a manifest.
Every selected requirement must have a `demonstrated` status, a nonempty
artifact locator, and explicit `same_family: true` and
`target_independent: true` attestations. Missing records produce `UNRESOLVED`;
a selected rejected premise produces `REJECTED`. A fully populated manifest
produces `READY_FOR_REVIEW`, **never** an automatic physical-proof claim.
The code validates record structure; it does not dereference or certify the
truth of artifact locators or human attestations.

| Local requirement ID | Required evidence | Present local status |
|---|---|---|
| `finite_tensor_interface` | Same-source symmetric rank-two field and Lorentz metric | Supplied interface in this diagnostic; physical realization unresolved |
| `nine_direction_balances` | Source-derived spanning physical directional balances | Algebra conditional on readings; source balances unresolved |
| `ward_bianchi_conservation` | Compatible conservation identities for those same tensors | Finite scalar incidence test only |
| `connectedness` | Connected event domain with relevant regularity | Declared finite graph checked; physical domain unresolved |
| `event_signal_clock` | Event, signal, clock, and volume attachment | Unresolved |
| `stress_vacuum` | Physical stress operator, vacuum subtraction, normalization | Unresolved |
| `coupling_scale` | Same-family coupling and independent physical scale | Supplied no-G display certificate is not independently validated here |
| `tensor_curvature_limit` | Controlled rank-two curvature convergence for the same family | Unresolved; scalar-curvature convergence is insufficient |
| `small_ball_null_balance` | Independent continuum small-ball/null-balance identification | Unresolved alternative route |
| `null_modular_bridge` | Physical null-stress/modular-charge identification | Branch claim reported by lab; full evidence not reproduced here |
| `bounded_interval_transport` | Compatible bounded intervals and projective limit | Unresolved |
| `entropy_stationarity` | Fixed-cap stationarity on a justified variation class | Supplied conditional premise |
| `bw_realized_cap_pair` | Realization from transported cap marginals | Unresolved named UV/BW scaffold |
| `bw_rigidity` | Independent BW rigidity on the realized limit | Unresolved named UV/BW scaffold |
| `bw_collar_floor` | Eventual fixed local collar floor | Unresolved lower blocker |
| `capacity_carrier` | Source-selected positive capacity | Unresolved |
| `same_invariant_capacity` | Construction/readback use the same invariant | Unresolved |
| `horizon_saturation` | Physical horizon records and saturation | Unresolved |
| `independent_gravity_test` | Frozen independent gravitational comparison | Not supplied in this work |

All evaluations require the finite and physical interface entries and an
independent observation test. The declared routes are:

- `tensor_limit`: requires `tensor_curvature_limit`.
- `null_balance`: requires the independent `small_ball_null_balance` route.
- `bw_null_balance`: requires the small-ball, modular, bounded-interval,
  stationarity, and three BW scaffold entries together.

The explicit route choice prevents an unproved branch from being silently
replaced by a different assumption stack. `require_lambda=True` adds all three
capacity entries. Turning it off means that the requested contract leaves
Lambda unspecified; it cannot justify a numerical Lambda claim.

## Units and calibration

The exact diagnostic coefficients are dimensionless formal data. For physical
readouts with coordinates of length and the usual SI stress-energy convention,
the Einstein relation is

\[
G_{ab}+\Lambda g_{ab}=\frac{8\pi G}{c^4}T_{ab}.
\]

| Quantity | Required physical units or convention |
|---|---|
| Curvature components in an orthonormal length convention | \(\mathrm{m}^{-2}\) |
| Stress-energy density components | \(\mathrm{J}\,\mathrm{m}^{-3}\) |
| Newton coupling | \(\mathrm{m}^3\,\mathrm{kg}^{-1}\,\mathrm{s}^{-2}\) |
| Cosmological constant | \(\mathrm{m}^{-2}\) |
| Display algebra with \(c=1\) and scale ratio one | Declared normalized convention, not an SI measurement |

[`newtonConstantFromScaleCertificate`](../src/core/ophMath.ts) returns a stored
reference in the existing display. Its constancy under the pixel slider does
not produce a new measurement of \(G\). `lambdaFromScreen` depends on a capacity
comparison coordinate; a target-exposed coordinate is not a source prediction.
The requirements report therefore emits `G_SI: null` and
`Lambda_m_minus_2: null`. An eventual calibrated implementation needs the actual
versioned scale certificate, units, source attachment, and independent evidence.

## Reproduce and interpret

From the repository root:

```sh
python -m unittest discover -s tests -p test_gravity_requirements.py -v
python scripts/oph_gravity_requirements.py --output docs/data/oph_gravity_requirements.json
```

The frozen receipt has exact tomography rank **9**, nullity **1**, identical
readings after the metric shift, a passing constant connected assignment, a
failing varying assignment, and two undetermined constants for the disconnected
example. The physical requirements report remains **UNRESOLVED**.
`implementation_sha256` binds that receipt to the current script bytes.

The 17 regression tests include 25 independently generated rational symmetric
tensors, incomplete-direction controls, invalid-input rejection, independent
connectedness and conservation controls, missing-lineage controls, target-leak
controls, and branch-selection checks. Passing these tests establishes the
specified diagnostic behavior; it does not establish physical gravity.

## Relation to established work and next decisive step

The null-tensor argument is ordinary finite linear algebra, and the conservation
argument is the standard source of an integration-constant freedom. They are
not claimed as novel gravity laws. Jacobson's equation-of-state route explicitly
adds horizon entropy and local energy/temperature assumptions; it is relevant
background for why those physical identifications cannot be omitted:
[T. Jacobson, *Thermodynamics of Spacetime: The Einstein Equation of State*,
Phys. Rev. Lett. 75, 1260 (1995)](https://doi.org/10.1103/PhysRevLett.75.1260),
[arXiv:gr-qc/9504004](https://arxiv.org/abs/gr-qc/9504004).

The next admissible positive step is a versioned same-family packet containing
the source-selected nine readings, tensor interface, conservation proof, and
one explicit continuum route. Before inspecting an observational target, freeze
the readout, units, admissible variations, uncertainties, comparison dataset,
and failure threshold. Missing or contradicted components leave the physical
claim unresolved or reject that branch. A finite rank check, a slider identity,
or a fitted value cannot substitute for that packet.
