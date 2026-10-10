# Stage 2 — Independent Finite-Lattice Check of the (N=1) Zero-Flux Claim

**Date:** 2026-10-09  
**Repository:** [enuminous/oph-lab](https://github.com/enuminous/oph-lab)  
**Status:** Independent proof of a precisely stated (U(1)) Haar-selection theorem; the match to the intended OPH (N=1) claim is **unresolved** because its source statement and model definitions were not found in the fork or in the public OPH files searched. This is not a Lean-checked proof and not a physical validation.

## Finding first: the intended claim is not frozen

The Stage 2 task refers to “the (N=1) zero-flux statement” and describes it as a finite-lattice result involving Gaussian integrals and Haar links. The available `enuminous/oph-lab` proposal and docs do not state the theorem or define (N), the gauge group, the lattice complex, boundary conditions, the Gaussian action, or the flux observable. Searches of the accessible public OPH tree did not identify that exact statement. I therefore do **not** claim to have checked Bernhard’s intended theorem.

To make useful independent progress without silently filling that gap, this note proves the minimal exact finite-lattice result matching the description under the explicit interpretation (N=1 equiv U(1)). The theorem is a Haar projection rule. Whether it implies the intended “zero flux” conclusion depends on the lattice topology and on what “flux” denotes.

## 1. Frozen model for the independent check

Let (K) be a finite oriented cell complex with link set (E) and plaquette set (F). Assign each link an independent (U(1)) variable

\[
U_e=e^{i\theta_e},\qquad dU_e=\frac{d\theta_e}{2\pi},\quad 0\le\theta_e<2\pi.
\]

For an integer link-charge vector (j=(j_e)_{e\in E}\in\mathbb Z^E), define the character

\[
\chi_j(U)=\prod_{e\in E}U_e^{j_e}.
\]

The normalized product Haar measure is (dU=\prod_e dU_e). All exponents are integers; all links are integrated; the measure is normalized. These assumptions are load-bearing.

## 2. Independent proof: Haar links project onto zero link charge

**Theorem (finite (U(1)) character orthogonality).**

\[
\int_{U(1)^E}\chi_j(U)\,dU
=\prod_{e\in E}\mathbf 1_{\{j_e=0\}}.
\]

**Proof.** Product measure and the product character factor the integral into one-link integrals:

\[
\int\chi_j(U)dU
=\prod_{e\in E}\frac1{2\pi}\int_0^{2\pi}e^{ij_e\theta_e}\,d\theta_e.
\]

For integer (m), the last integral is (1) if (m=0); if (m\ne0), its antiderivative gives

\[
\frac{e^{2\pi im}-1}{2\pi im}=0.
\]

Multiplying the factors proves the identity. \(\square\)

By linearity, Haar integration of any absolutely integrable Fourier/Laurent series

\[
f(U)=\sum_{j\in\mathbb Z^E}c_j\chi_j(U)
\]

returns its zero-character coefficient (c_0). This is a finite-link statement; the Fourier series can have infinitely many terms, with convergence required to justify termwise integration.

## 3. What the plaquette-flux version actually says

Let (\partial_2:\mathbb Z^F\to\mathbb Z^E) be the oriented plaquette-boundary map. A plaquette occupation/flux vector (m\in\mathbb Z^F) contributes the link character

\[
\chi_{\partial_2m}(U).
\]

The Haar theorem therefore gives

\[
\int\chi_{\partial_2m}(U)dU
=\mathbf 1_{\{\partial_2m=0\}}.
\]

That is **zero net link exponent**, equivalently a closed plaquette 2-chain. It is not generally the assertion (m=0).

For a finite (U(1)) Wilson plaquette action, use the absolutely convergent Fourier expansion

\[
\exp\!\left(\beta\sum_{p\in F}\cos\theta_p\right)
=\prod_{p\in F}\sum_{m_p\in\mathbb Z}I_{m_p}(\beta)e^{im_p\theta_p},
\]

where (I_m) is the modified Bessel coefficient and θ_p is the oriented plaquette angle. Integrating every link gives the exact finite-volume character sum

\[
Z_K(\beta)=\sum_{m\in\mathbb Z^F}
\left(\prod_{p\in F}I_{m_p}(\beta)\right)
\mathbf 1_{\{\partial_2m=0\}}.
\]

Thus the Haar links remove non-closed flux assignments. They do **not** in general remove every nonzero flux assignment.

### Boundary/topology boundary

- On a finite simply connected planar cellulation with no nonzero closed 2-cycles, (\ker\partial_2=\{0\}); the character sum is supported only at (m=0). Under this topology, “only zero plaquette flux contributes” follows.
- On a periodic two-dimensional torus, the fundamental 2-cycle is nonzero and has zero boundary. Nonzero constant plaquette flux assignments satisfy (\partial_2m=0), so Haar orthogonality alone does not force (m=0).
- With boundaries, whether relative cycles are allowed depends on which boundary links are integrated or fixed. That choice must be part of the theorem statement.

This distinction is the main independent check: “zero flux” is valid only after specifying whether it means zero link charge, no local divergence, zero plaquette occupation, or zero topological sector.

## 4. Gaussian integration: exact factor, separate condition

For a real vector (x\in\mathbb R^n), symmetric positive-definite precision matrix (A), and real source (J),

\[
\int_{\mathbb R^n}\exp\!\left(-\tfrac12x^TAx+J^Tx\right)dx
=(2\pi)^{n/2}(\det A)^{-1/2}
\exp\!\left(\tfrac12J^TA^{-1}J\right).
\]

This follows independently by completing the square:

\[
x^TAx-2J^Tx
=(x-A^{-1}J)^TA(x-A^{-1}J)-J^TA^{-1}J.
\]

If (A) and (J) are link-independent, the Gaussian factor is constant with respect to (U), so it multiplies the Haar projection without changing its support. If the Gaussian source or precision depends on the links, the result is a link-dependent function—possibly with nontrivial character content. Haar integration then extracts its zero-character coefficient; it does not automatically set every intermediate flux to zero. A singular (A) also invalidates the displayed normalized Gaussian formula unless zero modes are constrained or separately integrated.

For a combined finite integral with link-dependent source (J(U)), but fixed (A\succ0), the exact reduction is

\[
\int dU\int dx\,e^{-x^TAx/2+J(U)^Tx}
=(2\pi)^{n/2}(\det A)^{-1/2}
\int dU\,e^{J(U)^TA^{-1}J(U)/2}.
\]

The last Haar integral must be evaluated or its Fourier support proved. The Gaussian calculation does not replace that step.

## 5. Lean-sized proof plan

A small Lean development can isolate the exact reusable claims:

1. Define a finite link type (E), integer exponent vector (j:E\to\mathbb Z), and normalized Haar measure on the finite product (U(1)^E).
2. Prove one-link character orthogonality, then lift it by finite product integration to the displayed link theorem.
3. Define the integer boundary matrix (\partial_2) from oriented cell incidence; prove the plaquette-character exponent is (\partial_2m).
4. State the resulting condition as (\partial_2m=0), without replacing it by (m=0).
5. Prove (\ker\partial_2=0) only for a separately declared finite complex with a checked incidence matrix or a formal topological hypothesis. A torus fixture should demonstrate a nonzero kernel element.
6. For the Gaussian part, prove the quadratic completion algebraically and either use a sourced theorem for the multivariate Gaussian integral or formalize its one-dimensional integral and finite-dimensional product/linear-change steps. Keep (A\succ0) explicit.
7. Compose the two integrals only after proving absolute integrability/Fubini conditions for the declared finite model.

The Haar character step is elementary. The exact Gaussian normalization and the topological assertion (\ker\partial_2=0) are separate proof obligations. No Lean source was added or compiler-checked in this stage.

## 6. CIRCUS provenance and dependency audit

| Claim | Operational definition used here | Evidence source | Dependency / circularity risk | Status |
|---|---|---|---|---|
| Haar links select zero link charge | Product integral of integer (U(1)) characters | Direct one-link integral and finite product factorization | No data labels or fitted result; definitions fixed before proof | Demonstrated under stated measure |
| Zero plaquette flux follows | (m=0) for all contributing plaquette occupations | Requires (\ker\partial_2=0), plus boundary conditions | If “zero flux” is used to select a disk/open lattice and then claimed as topology-independent, the conclusion was built into the domain choice | Conditional; topology missing for intended claim |
| Gaussian integration preserves the support rule | Gaussian factor is independent of links, or its Fourier content is separately tracked | Complete-square identity | If (A(U)) or (J(U)) is suppressed, the evidence omits link-dependent character terms | Conditional; intended coupling missing |
| (N=1) is the case proved by this note | (N=1\) means compact gauge group (U(1)) | No source definition located | Meaning of (N) is assumed for this independent candidate | N/A for intended OPH claim |

No independent labels or empirical dataset exist for this exact theorem. Missing provenance is marked N/A, not passed. The standard character identity is independently derived here, but it is not independent confirmation that the intended OPH source uses these definitions.

## 7. MONSTER stress families and failure boundaries

Predeclare these finite mathematical perturbations before any numerical check:

| Family | Severity settings | Expected invariant / failure boundary |
|---|---|---|
| Link count and graph size | Multiple finite (V,E,F), including one plaquette and small periodic tori | Character orthogonality is size-invariant; cycle space may change |
| Topology and boundaries | Disk/open, cylinder, periodic torus; integrated versus fixed boundary links | “Only (m=0)” passes only when (\ker\partial_2=0); nonzero cycles are the first failure for that stronger claim |
| Flux support | Single plaquette, closed surface, global torus cycle | Haar retains exactly assignments with zero link-boundary exponent |
| Gaussian precision | Condition number sweep; positive-definite, near-singular, singular | Formula holds for (A\succ0); singular zero modes require a separate constraint and otherwise fail the stated integral |
| Link coupling | (J(U)) independent, linear character source, link-dependent precision (A(U)) | Constant Gaussian factor preserves support directly; link-dependent factor needs its own character expansion |
| Haar normalization and charge | Normalized Haar; integer versus noninteger exponents | Exact selection is for normalized Haar and integer characters; changing either invalidates the stated theorem |
| Baseline | Direct character orthogonality versus explicit angle quadrature / exact finite Fourier sum | Agreement checks implementation only; the analytic theorem remains primary |

This is a symbolic failure map, not a run: no quadrature results or performance envelope are claimed. The first failure boundary is already exact: allow a nonzero 2-cycle on a periodic torus and Haar integration admits nonzero plaquette flux. Therefore a topology-free “all flux is zero” statement fails.

## 8. Full Zoo accounting

The 46 registered module contracts in [Monolithic-Zoo-Lean4](https://github.com/enuminous/Monolithic-Zoo-Lean4) are accounted for in the Stage 1 ledger in this same repo. For Stage 2, the directly relevant operations are TORTOISE (freeze the model and boundary conditions), BAT (no source-derived data or fitted fit), TURTLE (veto the topology-free zero-flux overclaim), LYNX (classify character orthogonality as standard mathematics, not novelty), RHINO (retain the Haar-invariant subspace), and TERMITE (keep the Gaussian and link integrations as separate composable steps). CIRCUS supplies the dependency audit above; MONSTER supplies the perturbation/failure families above.

All data-driven scoring, calibration, ranking, monitoring, queue, event-history, recovery, and multi-agent kernels have no inputs in this analytic check: N/A, not pass. The Zoo repository itself describes its Lean modules as an uncompiled formalization draft, so no result here is represented as a successful execution of all 46 Lean modules.

## 9. Stage 2 verdict

- **Conditional theorem pass:** normalized (U(1)) Haar integration projects integer link characters onto zero net link exponent; on a plaquette expansion it keeps exactly the closed 2-chain sector.
- **Conditional zero-plaquette-flux pass:** only when the explicitly chosen finite complex and integrated/fixed boundaries establish (\ker\partial_2=0).
- **Counterexample to a topology-free stronger claim:** periodic torus permits nonzero closed 2-cycles, so “Haar links force every plaquette flux to vanish” is false in that setting.
- **Gaussian factor:** exact under (A\succ0); link dependence must be retained and separately expanded.
- **Intended OPH (N=1) claim:** **N/A / unresolved** until its source statement specifies (N), link group, finite complex, boundary treatment, Gaussian action, flux observable, and claimed integral.
- **Lean status:** proof plan only; no Lean file compiled.

## Sources and related work

- [Stage 1 heat-bath and transfer-spectrum analysis](OPH_ANCHORED_LAPLACIAN_HEAT_BATH_TRANSFER.md)
- [Cadence–OPH–EFMW common-core proposal](CADENCE_OPH_EFMW_COMMON_CORE_PROPOSAL.md)
- [OPH Lab fork](https://github.com/enuminous/oph-lab)
- [Canonical OPH repository](https://github.com/FloatingPragma/observer-patch-holography)
