# Stage 1 — Heat-Bath Repair and the Anchored-Laplacian Transfer Spectrum

**Date:** 2026-10-09  
**Repository:** [enuminous/oph-lab](https://github.com/enuminous/oph-lab)  
**Status:** Analytic derivation for an explicitly stated homogeneous-lattice specialization; not yet Lean-checked; not evidence that the transfer direction is physical time.  
**Scope:** Warm-up only. The N=1 flux check and N=2 pole search are outside this document.

## Executive result

For a real scalar field on a periodic hypercubic lattice with nearest-neighbour quadratic repair energy and a **uniform positive anchor at every site**, single-site heat-bath conditionals preserve the Gibbs distribution. Separately, the equilibrium transfer operator along one lattice direction is a product of harmonic-oscillator transfer operators. Its one-mode gap (E(k)) obeys

\[
4J_0\sinh^2\!\left(\frac{E(k)}2\right)
=\kappa+4\sum_{j=1}^{d-1}J_j\sin^2\!\left(\frac{k_j}2\right),
\]

or equivalently

\[
\cosh E(k)=1+\frac{\kappa+4\sum_{j=1}^{d-1}J_j\sin^2(k_j/2)}{2J_0}.
\]

Here (J_0>0) is the coupling along the transfer direction, (J_j>0) are transverse couplings, and (kappa>0) is the uniform anchor strength. With isotropic unit couplings, this is the usual massive free-scalar lattice dispersion. No separate inertial variable or second-order repair update was added. The directional nearest-neighbour term already present in the potential supplies the transfer coupling.

**Important scope correction:** Section 3 of the fork’s common-core proposal states a general finite connected graph with arbitrary nonnegative anchors and only requires at least one positive anchor. That general model does **not** have translation symmetry and does not imply a plane-wave dispersion. The equation above follows only after specializing to a regular periodic lattice and replacing the general anchor matrix (D\) by κ I. A single pinned site or nonuniform anchors generally mix momenta. The specialization is useful and exactly analyzable, but it must not be represented as a consequence of the full arbitrary-graph statement.

## 1. Frozen target and assumptions

Let the lattice be a finite (d)-dimensional torus, with coordinates (x=(t,x_1,\ldots,x_{d-1})). The field is real-valued, φ_x ∈ ℝ. Use dimensionless lattice coordinates and the quadratic potential

\[
V(\phi;y)=\frac12\sum_x\left[
J_0(\phi_{x+e_0}-\phi_x)^2
+\sum_{j=1}^{d-1}J_j(\phi_{x+e_j}-\phi_x)^2
+\kappa(\phi_x-y)^2\right],
\]

with (J_0,J_j>0), κ>0, and a constant evidence value (y). Translating φ by (y) removes the constant source from the fluctuation calculation, so set (y=0) below. The anchor is uniform. This is a massive Gaussian measure:

\[
\pi(d\phi)=Z^{-1}e^{-V(\phi;0)}\prod_xd\phi_x.
\]

The positive uniform anchor makes the precision operator strictly positive, so (Z) is finite. For the transfer calculation, the transverse directions are periodic. A finite periodic extent in the transfer direction gives the usual wraparound; the transfer gap is the same.

These are assumptions, not outputs of the heat-bath construction. In particular, neither the coupling constants nor the uniform anchor are inferred from OPH axioms here.

## 2. Heat-bath repair preserves the target Gibbs measure

For a site (x), write (N(x)) for its nearest neighbours and let

\[
D_x=\kappa+2J_0+2\sum_{j=1}^{d-1}J_j.
\]

Completing the square in the terms involving φ_x gives

\[
\phi_x\mid\phi_{z\ne x}
\sim \mathcal N\!\left(
\frac{J_0(\phi_{x+e_0}+\phi_{x-e_0})+
\sum_{j=1}^{d-1}J_j(\phi_{x+e_j}+\phi_{x-e_j})}{D_x},
\frac1{D_x}\right).
\]

For nonzero constant (y), add κ y to the numerator. (For site-dependent evidence (y_x), add κ y_x, but that breaks translation invariance unless the source is treated separately and then shifted away.)

The single-site heat-bath kernel (K_x) replaces φ_x by a draw from this conditional while leaving all other coordinates fixed. The Gibbs density factors as

\[
\pi(d\phi)=\pi(d\phi_{-x})\,\pi(d\phi_x\mid\phi_{-x}),
\]

so resampling from the conditional leaves π invariant; the same factorization gives detailed balance for (K_x). Any random-scan mixture \(K=\sum_x p_xK_x\), with fixed (p_x\ge0\) summing to one, is therefore reversible and stationary for π. A deterministic scan composed from these kernels also preserves π, but its composition need not itself be reversible. A synchronous independent resampling of every coordinate is **not** licensed by this proof and is not assumed.

This establishes stationarity of the stochastic repair process. It does not identify its Monte Carlo step count with the transfer coordinate or with physical time.

## 3. Transfer operator along one lattice direction

Fourier transform only the transverse coordinates. For each transverse momentum

\[
k_j=\frac{2\pi n_j}{L_j},\qquad n_j\in\{0,\ldots,L_j-1\},
\]

the transverse Laplacian contributes

\[
\Omega^2(k)=\kappa+4\sum_{j=1}^{d-1}J_j\sin^2\!\left(\frac{k_j}{2}\right).
\]

The action for that mode along the transfer coordinate becomes

\[
V_k(q)=\frac12\sum_t\left[J_0(q_{t+1}-q_t)^2+\Omega^2(k)q_t^2\right].
\]

Splitting each on-slice term equally between neighbouring transfer steps gives the symmetric transfer kernel

\[
T_k(q,q')=\exp\!\left[-\frac{J_0}{2}(q'-q)^2
-\frac{\Omega^2(k)}4(q^2+q'^2)\right].
\]

This is a Mehler (harmonic-oscillator) kernel. For a kernel of the form \(e^{-a(q^2+q'^2)+bqq'}\), the geometric ratio of successive Hermite-mode eigenvalues (r=e^{-E}) satisfies (r+r^{-1}=4a/b). Here (a=J_0/2+\Omega^2/4) and (b=J_0), hence

\[
2\cosh E(k)=2+\frac{\Omega^2(k)}{J_0}.
\]

Therefore

\[
\boxed{\;4J_0\sinh^2(E(k)/2)=\Omega^2(k)\;}
\]

and the transfer eigenvalues in that mode are

\[
\lambda_n(k)=\lambda_0(k)e^{-nE(k)},\qquad n=0,1,2,\ldots.
\]

The one-excitation transfer gap is (E(k)); the corresponding infinite-direction two-point function decays proportionally to (e^{-E(k)|t|}). For a finite periodic transfer length, add the reflected wraparound contribution. In the isotropic unit-coupling case,

\[
4\sinh^2(E(k)/2)=\kappa+4\sum_{j=1}^{d-1}\sin^2(k_j/2).
\]

This is the lattice dispersion of a massive free scalar. In the small-momentum, small-κ regime, (E(k)^2=\kappa+\sum_jJ_jk_j^2+O((\kappa+|k|^2)^2)) when (J_0=1); for general (J_0), the leading term is Ω²/J₀. This is a transfer-spectrum calculation, not a separately postulated inertial equation.

## 4. What this does and does not say about time

There are two different notions of progression in this construction:

1. **Heat-bath algorithm time:** the count/order of conditional resampling steps. Its behavior depends on the scan schedule and is not the transfer spectrum.
2. **Transfer coordinate:** a chosen lattice direction in the equilibrium Gibbs weight. Correlations along it decay with gap (E(k)), even though the potential contains no separate momentum variable or inertial update rule.

The calculation demonstrates that a time-like transfer spectrum can be encoded by directional couplings in a static quadratic measure. It does **not** prove that OPH derives physical time, Lorentzian dynamics, causal propagation, or an inertial term. Those require an independent identification of the transfer direction and additional physical premises. The result is Euclidean and conditional on the declared lattice model.

## 5. Boundary of the result: arbitrary anchors versus a uniform mass

The fork’s Section 3 model is stated on a finite connected graph with (A=L_w+D), (D=\operatorname{diag}(\kappa_i)), and only one or more positive κ_i. That is enough for positive definiteness when at least one anchor is positive. It is not enough for the calculation above:

- An irregular graph has no transverse plane-wave basis.
- Nonconstant κ_i break translation symmetry, so transverse momenta mix.
- A single-site anchor is a localized defect, not a uniform mass. Its finite-volume spectrum is a defect problem; it is not the exact free-scalar dispersion above.
- If κ=0 on a periodic torus, the constant mode is unpinned and the Gaussian partition function diverges unless a zero-mean constraint or other boundary condition removes that mode.

Accordingly, the derivation passes only for the uniform periodic specialization. The inference “the general anchored graph has the massive scalar dispersion” fails at the symmetry assumption.

## 6. Lean formalization target and proof obligations

The exact finite-site model has a finite number of lattice sites but a **continuous** state space ℝ^|V|. The transfer operator acts on a function space; “finite lattice” does not reduce the exact spectrum to a finite matrix. A formal proof can be split into small lemmas, but completeness of the Hermite eigenbasis is a genuine analytic obligation.

A Lean project should freeze these objects and prove, in order:

1. **Precision matrix:** the quadratic form equals φᵀAφ/2 and (A) is positive definite for κ>0.
2. **Conditional Gaussian:** extracting the φ_x terms yields the stated mean and variance.
3. **Gibbs invariance:** the conditional-resampling kernel preserves the density; the random-scan mixture is stationary and reversible; deterministic scan is stationary without an asserted detailed-balance result.
4. **Fourier diagonalization:** the periodic transverse graph Laplacian has eigenvalue (4\sum_jJ_j\sin^2(k_j/2)).
5. **Transfer kernel:** splitting the action gives the stated Mehler kernel.
6. **Mode spectrum:** establish the Hermite eigenfunction relation and eigenvalue ratio (e^{-E}), then derive the boxed dispersion identity from the hyperbolic identity.
7. **Scope guards:** do not state plane-wave diagonalization for nonuniform anchors, irregular graphs, or the unpinned periodic massless zero mode.

The algebraic identity from λ=e⁻ᵉ to the boxed equation is a small Lean target. Proving that the displayed Mehler eigenfunctions exhaust the spectrum needs the relevant real-analysis and (L^2) foundations; it must not be replaced by a finite sampled kernel and called exact. This document provides a proof plan, not a checked Lean theorem.

## 7. Full Zoo pass: operation ledger

**Source boundary.** The available `Monolithic-Zoo-Lean4` repository registers 46 modules. Its README labels the tree an uncompiled formalization draft; the module contracts are written but not compiler-checked there. `CIRCUS` and `MONSTER`, as defined for this research program, are not present in that Lean registry. The table below accounts for the complete registered 46-module roster plus those two supplemental audits. “N/A” means required inputs or the animal’s operation are absent; it is never counted as a pass. This is an audit application, not execution of 46 verified Lean programs.

| Animal(s) | Stage-one application | Status |
|---|---|---|
| TORTOISE | Keep model/derivation fixed before any comparison; no training/test or empirical split exists for this analytic result. | Applied as a freeze requirement; split N/A |
| OWL, OCTOPUS, GECKO, HIVE, EAGLE, CRAB, SHEPHERD, PULSE, FOX, SPIDER, RAVEN, DOLPHIN, ANT, MOTH, SHARK, PENGUIN, DRAGON | Their registered kernels aggregate supplied feature columns. No scored feature matrix or labels exists here. | N/A; no aggregation pass claimed |
| CAT | No components have been ablated or assigned performance contributions. | N/A |
| BAT | The source is a declared quadratic model; no fitted predictor or placebo source exists. | Applied as a provenance warning: the target form is assumed |
| HEDGEHOG | No independent environment or held-out lattice family was used to test generalization. | N/A |
| CROCODILE | No treatment/control groups or difference-in-differences design. | N/A |
| TURTLE | A verdict must remain conditional: the math result does not support a physical-time conclusion. | Applied as a scope veto |
| MAGPIE | No sequence history or alarm labels. | N/A |
| WOLF | No channel contributions or network aggregation. | N/A |
| ELEPHANT | No event-memory lineage or active-event data. | N/A |
| CHAMELEON | No measured noise residuals or fitted centroid distances. | N/A |
| JELLYFISH | No dynamically weighted repair graph or health traces. | N/A |
| BEAVER | No external repair implementation, rollback behavior, or acceptance bounds. | N/A |
| MANTIS | No calibration set or empirical z-scores. | N/A |
| BISON | No queue process. | N/A |
| WEASEL | No scored candidate-search corpus or budgeted finding filter. | N/A |
| SALMON | No unresolved-mass history or trace. | N/A |
| ORCA | No distributed handoff events. | N/A |
| MOLE | The source equation is visible, but no coverage indicators exist for external physical claims. | Applied as an observability limit; physical coverage N/A |
| LYNX | The transfer calculation matches the standard Gaussian free-field/Mehler construction; no novelty or replication claim is made. | Applied: no novelty claimed; independent replication N/A |
| HORSE | No workload/trust scores or handoffs. | N/A |
| TERMITE | Distinguish conditional-resampling updates from transfer-direction evolution; do not conflate their clocks. | Applied as an update/clock separation check |
| PHOENIX | No recovery sequence or checkpoint evidence. | N/A |
| COBRA | No proxy estimator or reference divergence. | N/A |
| WHALE | No cumulative-deviation time series. | N/A |
| FALCON | No latency, missed-event, or reaction-margin data. | N/A |
| RHINO | The target Gibbs law is invariant under the specified heat-bath kernels. | Applied analytically, conditional on the model |
| BONOBO | No multi-agent gain/cooperation data. | N/A |
| AXOLOTL | No measured recovery, efficiency, or resilience transformation. | N/A |
| BUTTERFLY | No bounded simulated trajectory or graph-comparison experiment. | N/A |
| CIRCUS | Trace claim → operational definition → data → labels → score → validation. Here, the “massive free-scalar dispersion” is built into the homogeneous Laplacian-plus-κI model; the derivation is conditional algebra, not independent empirical confirmation. No external labels/data exist. | Applied: construction dependence flagged; empirical validation N/A |
| MONSTER | Predeclared nuisance families: anchor κ, coupling anisotropy, dimension, transverse momenta, boundary condition, lattice sizes, scan schedule, random seed, and uniform versus sparse anchors. Exact formula is stable under positive uniform κ and positive directional couplings with the corresponding formula; the plane-wave claim fails when translation symmetry is broken. κ=0 on an unconstrained periodic torus fails by the zero mode. | Applied symbolically; no numerical envelope or empirical pass claimed |

### CIRCUS provenance map

| Claim layer | Source used | Dependency | Independent check |
|---|---|---|---|
| Operational model | Declared (V) above | Uniform nearest-neighbour quadratic form and κI are assumptions | Re-derive from the intended Section 3 source and confirm it matches; current proposal states a more general (L_w+D) model |
| Heat-bath law | Conditional factorization of (e^{-V}) | Same (V) fixes the conditional | Independent completion-of-square derivation; no empirical labels needed |
| Transfer kernel | Symmetric split of the same action | Same (V), with a selected transfer direction | Independently derive the kernel from the finite-volume partition function |
| Expected dispersion | Massive scalar form | Uniform mass and translation symmetry were selected before diagonalization | Independent symbolic derivation from the covariance/precision operator |
| Physical interpretation | “Where OPH puts time” | Not entailed by the transfer eigenvalue alone | Independent clock/causal/physical identification; absent here |

The key feedback path is explicit: the requested outcome helped select the uniform massive Gaussian specialization. This makes the calculation useful as a consistency and mechanism demonstration, but it cannot serve as independent evidence that OPH or nature produces this law.

### MONSTER preregistration and failure boundary

For a computational follow-up, freeze before running: κ ∈ {0.05, 0.1, 0.25, 0.5, 1}; (J_0/J_j) ratios {0.5, 1, 2}; transverse sizes {4, 8, 16}; transfer lengths {8, 16, 32}; periodic and open transfer boundaries; homogeneous and one-site/sparse anchors; random-scan and deterministic-scan heat-bath updates; fixed seed list; and direct precision-matrix covariance as the conventional baseline. The primary score is the fitted transfer gap from separated-time covariance versus the predicted (E(k)), with predeclared tolerance (10^{-6}) for direct deterministic linear algebra and separately reported Monte Carlo uncertainty for sampled heat-bath estimates. (The Monte Carlo tolerance must be frozen with a sample budget before that experiment; this document does not report such a run.)

Expected exact failure boundaries: sparse/nonuniform anchors destroy transverse translation invariance and therefore the momentum-resolved scalar formula; zero anchor on the unconstrained periodic torus leaves a divergent constant mode; asynchronous update order may change autocorrelation time while leaving the Gibbs stationary law intact. These are structural outcomes, not post-hoc exceptions.

## 8. Result classification

- **Demonstrated analytically, conditional on assumptions:** heat-bath invariance; transverse Laplacian eigenvalues; the Mehler-kernel transfer gap and boxed dispersion for the uniform periodic Gaussian specialization.
- **Not demonstrated:** exact result for the general arbitrary-graph/sparse-anchor Section 3 model; a compiler-checked Lean formalization; physical time, Lorentzian dynamics, or a physical field identification; independent empirical validation.
- **Novelty:** the derived dispersion is a standard free-scalar lattice transfer result. No novelty claim is made for the formula. The potentially useful OPH question is whether the chosen repair construction and observer interpretation justify this transfer direction without importing it as a physical premise.
- **Stage-one decision:** conditional analytic pass for the homogeneous periodic specialization; no pass for the broader Section 3 model or physical interpretation.

## Sources and provenance

- [The fork’s common-core proposal](CADENCE_OPH_EFMW_COMMON_CORE_PROPOSAL.md), especially its Section 3 finite graph potential (V(z;y)=\tfrac12\sum w_{ij}(z_i-z_j)^2+\tfrac12\sum_i\kappa_i(z_i-y_i)^2).
- [OPH Lab fork](https://github.com/enuminous/oph-lab) and [canonical OPH research repository](https://github.com/FloatingPragma/observer-patch-holography).
- [Monolithic Zoo Lean 4 registry](https://github.com/enuminous/Monolithic-Zoo-Lean4), whose published README describes a 46-module uncompiled formalization draft.
