# OPH Stage 4 — Lean formalization cores

**Scope:** machine-checkable lemmas extracted from the finite-lattice Haar and
anchored-Laplacian analyses. This stage formalizes exact mathematical cores; it
does not validate a physical interpretation.

## Frozen targets

### Haar character selection

For a group `G`, a normalized left-invariant measure `μ`, and an integrable
group character `χ : G →* ℂ`, prove

\[
\int_G \chi(g)\,d\mu(g)=
\begin{cases}
1,&\chi\equiv1,\\
0,&\chi\not\equiv1.
\end{cases}
\]

The Lean proof uses invariance under translation: translating by an element at
which a nontrivial character differs from one multiplies the integral by that
character value, forcing the integral to vanish. This is the abstract
normalized Haar selection rule. To recover the finite-link statement in Stage
2, a later lemma must instantiate `G` as `U(1)^E`, construct the product
character from integer link charges, and show that it is trivial exactly when
every link exponent is zero. The incidence-map condition `∂₂m=0` and the
topology-dependent implication `m=0` remain separate.

### Transfer dispersion algebra

Assuming the Mehler transfer relation

\[
\cosh E=1+\frac{\omega}{2j},
\]

prove

\[
4j\sinh^2(E/2)=\omega.
\]

For the Stage 1 specialization,
`j = J₀ > 0` and
`ω = κ + 4 Σᵢ Jᵢ sin²(kᵢ/2)`. The Lean lemma checks only the hyperbolic
identity and algebra. It assumes the transfer relation; it does not establish
the Mehler kernel, completeness of the Hermite eigenbasis, or a physical-time
interpretation.

## CIRCUS provenance / dependency map

| Claim | Formalized input | Dependency to break or still verify |
|---|---|---|
| Nontrivial character has zero Haar average | Normalized left-invariant measure; group character; integrability | Instantiate the actual finite product `U(1)^E` and its product Haar measure |
| Plaquette assignments survive iff link exponents cancel | Integer incidence matrix and exponent construction | Formalize `∂₂m`; do not strengthen `∂₂m=0` to `m=0` without a proven topological hypothesis |
| Lattice transfer gap has massive-scalar dispersion | Mehler relation plus positive directional coupling | Independently prove the relation from the declared transfer kernel and establish the operator-spectrum theorem |
| Transfer coordinate is physical time | No formal premise in this project | Requires an independent clock/causal identification; currently not established |

No empirical labels, fitted scores, or target-selected examples enter these
algebraic lemmas. The source-to-intended-OPH equivalence is **N/A** until the
exact upstream model and conventions are version-pinned.

## Validation and status

The project is pinned and has a GitHub Actions build. A passing build checks
only the two Lean declarations. It is not a full formalization of either
Stage 1 or Stage 2, does not prove a physical claim, and does not change the
unresolved Stage 3 `N=2` result.

Success criterion: the pinned project builds without `sorry`, axioms added by
this project, or untrusted external theorem assumptions beyond Lean/Mathlib's
kernel and the explicitly stated mathematical inputs. Failure criterion:
any compilation error, hidden admission, or statement broader than the frozen
targets above.
