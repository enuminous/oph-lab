# A Conditional Continuum Limit from OPH-Inspired Patch Dynamics to an EFMW-Style Scalar Field

**Date:** 2026-10-07  
**Status:** Constructive mathematical model and independently rerunnable numerical example; **not** a theorem from OPH's canonical three axioms; **not** an empirical confirmation of EFMW physics.  
**Repository:** [enuminous/oph-lab](https://github.com/enuminous/oph-lab) (independent fork).  
**Related review:** [EFMW Zoo review of OPH Lab](EFMW_ZOO_REVIEW.md).  
**Executable test:** [scripts/oph_efmw_continuum_demo.py](../scripts/oph_efmw_continuum_demo.py).  
**Recorded results:** [docs/data/oph_efmw_continuum_results.csv](data/oph_efmw_continuum_results.csv).

## Abstract

We ask whether observer-patch interactions can admit a specified continuum limit with the EFMW-style sourced scalar wave form

\[
\nabla^2\phi-\frac{1}{c^2}\partial_t^2\phi
=\frac{4\pi}{c^2}(E+cP).
\tag{1}
\]

**Conditional answer:** yes. On an *assumed* three-dimensional periodic patch lattice, select a scalar overlap observable, a quadratic neighbor-disagreement functional, and a reversible two-step inertial update sourced by prescribed scalar values. A standard centered finite-difference calculation then yields (1), with a second-order error bound under smoothness and a Courant condition. A manufactured nonzero-source three-dimensional example demonstrates approximately quadratic convergence at five grid resolutions.

**Key limitation:** this is an explicitly **augmented OPH-inspired system**. The canonical OPH consensus relation is a descent-based rewriting/repair process on finite patch states; it does not supply a physical clock, a second-order reversible update, a three-torus carrier, the propagation coefficient \(c\), or the EFMW source mapping. The result is an *existence construction for one compatible discrete model*, not a forced consequence of OPH axioms nor a proof that OPH and EFMW describe identical physics.

## 1. OPH source scope and the key obstruction

The canonical paper [*Reality as a Consensus Protocol*](https://github.com/FloatingPragma/observer-patch-holography/blob/main/paper/reality_as_consensus_protocol.tex) defines a finite connected graph \(G=(V,E)\). Each patch \(i\) has a finite state set \(S_i\), and each shared edge has an interface alphabet \(I_e\) with projection maps \(\pi_{i,e},\pi_{j,e}\). Its overlap-inconsistency functional is

\[
\Phi(s)=\sum_{e=\{i,j\}\in E} w_e
d_e(\pi_{i,e}(s_i),\pi_{j,e}(s_j)),
\quad w_e>0,
\tag{2}
\]

where \(d_e(a,b)=0\) if and only if \(a=b\). Its accepted primitive repair proposals must strictly lower the **touched-overlap** part of the potential. It distinguishes the order of repair records from a physically calibrated time coordinate and states that the bare finite consensus reduct does not by itself determine physical spacetime or Einstein dynamics.

Equation (1) is a **hyperbolic** field equation supporting oscillation and waves. Ordinary gradient repair

\[
u^{n+1}=u^n-\eta\nabla_h\Phi_h(u^n)
\]

instead tends in an appropriate scaling to a **first-order diffusion equation**, not automatically to a wave equation.

For example, a free periodic continuum mode \(\phi(x,t)=\sin(kx)\cos(ckt)\) has spatial disagreement energy proportional to \(\cos^2(ckt)\): it rises during part of every oscillation. The rule “every accepted step decreases disagreement” therefore cannot serve directly as a universal identification with every wave-propagation step.

**Bridge needed:** a distinct reversible propagation/record channel, or an enlarged state containing displacement and momentum, with a documented relationship to OPH recovery and acceptance. Merely naming a repair schedule “time” does not meet this requirement.

## 2. Proposed patch model (explicit new hypotheses)

Let \(\Omega=(\mathbb R/L\mathbb Z)^3\) be a flat periodic three-dimensional domain, \(L>0\), and let the patch centers be \(x_i=h i\), \(h=L/N\), \(i\in(\mathbb Z/N\mathbb Z)^3\). This testbed is **not** identified with OPH's oriented spherical screen. Obtaining it from OPH's source-derived three-dimensional carrier is an additional obligation.

**Assumptions A1–A6 of this construction (not OPH's axioms):**

1. **Carrier** — lattice patches have six nearest neighbors and an isotropic spacing \(h\) in an independently chosen three-dimensional Euclidean chart.
2. **Observable** — every patch exposes a common scalar \(u_i^n\) with identity overlap projection, or maps with an explicitly proven equivalent scalar contraction.
3. **Disagreement measure** — each spatial nearest-neighbor discrepancy is quadratic with prescribed scaling.
4. **Clock and memory** — there is a common externally supplied interval \(\Delta t\) and two accessible consecutive scalar time layers.
5. **Propagation law** — a reversible, two-step inertial update couples neighboring patch differences with coefficient \(c^2\). This *does not follow from monotone repair*.
6. **Source** — a specified, independently readable scalar source \(S_i^n\) enters with coefficient \(-4\pi\). We *name* \(S=E+cP\), but do not derive this physical identification from observer histories.

### 2.1 Disagreement functional and discrete Laplacian

For a lattice scalar \(u\), define

\[
\Phi_h(u)=\frac{h^3}{2}
\sum_{i}\sum_{a=1}^{3}
\left(\frac{u_{i+e_a}-u_i}{h}\right)^2.
\tag{3}
\]

The volume-weighted inner product is \(\langle u,v\rangle_h=h^3\sum_i u_i v_i\). The first variation of (3) obeys

\[
\nabla_h\Phi_h(u)=-L_h u,\qquad
(L_hu)_i=\sum_{a=1}^{3}
\frac{u_{i+e_a}-2u_i+u_{i-e_a}}{h^2}.
\tag{4}
\]

Thus an operator resembling a spatial Laplacian arises directly from a particular pairwise overlap energy.

### 2.2 Two-step reversible update

Choose

\[
\frac{u_i^{n+1}-2u_i^n+u_i^{n-1}}{(\Delta t)^2}
=c^2(L_hu^n)_i-4\pi S_i^n.
\tag{5}
\]

Equivalently,

\[
u_i^{n+1}=2u_i^n-u_i^{n-1}
+c^2(\Delta t)^2(L_hu^n)_i
-4\pi(\Delta t)^2S_i^n.
\tag{6}
\]

For prescribed \(S_i^n\), this is algebraically reversible because the prior state can be reconstructed from the next and current states. It is not asserted to be an OPH-accepted monotone repair step. The discrete wave equation is therefore *constructed*, not discovered to be mandatory.

## 3. Target field and physical units

The target form is

\[
\phi_{tt}=c^2\nabla^2\phi-4\pi(E+cP).
\tag{7}
\]

One dimensionally consistent interpretation, **conditional on fixing a reference frame**, is:

| Symbol | Interpretation for this model | SI unit |
|---|---|---|
| \(x,h,L\) | length | m |
| \(t,\Delta t\) | time | s |
| \(c\) | propagation speed | m s\(^{-1}\) |
| \(E\) | energy density | J m\(^{-3}\) |
| \(P\) | scalar component of momentum density | kg m\(^{-2}\) s\(^{-1}\) |
| \(cP\), \(S\) | energy density | J m\(^{-3}\) |
| \(\phi,u\) | scalar potential in this normalization | kg m\(^{-1}\) |
| \(\nabla^2\phi\), \(c^{-2}\phi_{tt}\) | source-normalized curvature | kg m\(^{-3}\) |

Here \((4\pi/c^2)S\) has SI units kg m\(^{-3}\), matching \(\nabla^2\phi\). These are **one possible unit assignments**, not an independently derived EFMW ontology. If \(P\) denotes ordinary pressure rather than momentum density, \(E+cP\) is not dimensionally homogeneous as written. If \(P\) is vector momentum density, a scalar component or a covariant contraction must be specified. The source \(E+cP\) is not automatically Lorentz invariant.

The numerical demonstration nondimensionalizes \(L=c=1\) and chooses \(S\) by exact manufacture. Its dimensionless values are **not measured physical energy densities**.

## 4. Boundary and initial conditions

Use a three-torus (equivalently a cube with periodic identifications):

\[
\phi(x+Le_a,t)=\phi(x,t),\quad a=1,2,3,\quad 0\le t\le T.
\tag{8}
\]

Specify periodic initial data

\[
\phi(x,0)=f(x),\qquad \partial_t\phi(x,0)=g(x).
\tag{9}
\]

Sample \(u_i^0=f(x_i)\) and initialize the first step by a second-order Taylor acceleration:

\[
u_i^1=u_i^0+\Delta t\,g(x_i)
+\frac{(\Delta t)^2}{2}
\left[c^2(L_hu^0)_i-4\pi S(x_i,0)\right].
\tag{10}
\]

Assume a classical solution exists, \(f,g,S\) are regular enough to bound derivatives below, and the source used by the scheme equals \(S(x_i,t_n)\). Treatment of uncertain sensor measurements, asynchronous observer clocks or mismatched source records is outside the theorem.

## 5. Continuum limit and an explicit error bound

At a smooth continuum field sampled on the lattice, centered Taylor expansion yields

\[
L_h\phi(x_i,t)
=\nabla^2\phi(x_i,t)
+O(h^2),
\]

and

\[
\frac{\phi(x_i,t_{n+1})-2\phi(x_i,t_n)+\phi(x_i,t_{n-1})}{(\Delta t)^2}
=\phi_{tt}(x_i,t_n)+O((\Delta t)^2).
\]

If \(h,\Delta t\to0\) with \(\Delta t=O(h)\), equation (5) is consistent with (7).

### 5.1 Stable time-step condition

On a three-dimensional equal-spacing periodic lattice, the largest eigenvalue of \(-L_h\) is at most \(12/h^2\). Fourier-mode stability of the centered recurrence therefore requires

\[
3\left(\frac{c\Delta t}{h}\right)^2\le1.
\tag{11}
\]

In the numerical script the stricter \(\sqrt3\,c\Delta t/h<1\) is asserted.

### 5.2 A conservative finite-horizon bound

Define the volume-normalized discrete norm (RMS)

\[
\|v\|_{2,h}=\sqrt{\frac{h^3}{L^3}\sum_i |v_i|^2}
=\sqrt{\frac1{N^3}\sum_i |v_i|^2}.
\tag{12}
\]

Suppose, for \((x,t)\in\Omega\times[0,T]\),

\[
\begin{aligned}
M_3&=\sup|\partial_t^3\phi|,\qquad
M_4=\sup|\partial_t^4\phi|,\\
X_4&=\sum_{a=1}^3\sup|\partial_{x_a}^4\phi|.
\end{aligned}
\]

Let \(t_n=n\Delta t\le T\). Then, for exact sampled source and initialization (10), a conservative estimate is

\[
\boxed{
\begin{aligned}
\|u^n-\phi(\cdot,t_n)\|_{2,h}
\le{}&\frac{T}{\Delta t}\left[
\frac{(\Delta t)^3M_3}{6}
+\frac{c^2(\Delta t)^2h^2 X_4}{24}\right]\\
&+\frac{T^2}{2}\left[
\frac{(\Delta t)^2M_4}{12}
+\frac{c^2 h^2 X_4}{12}\right].
\end{aligned}}
\tag{13}
\]

**Proof sketch.** The first-step error is bounded by the order-three temporal Taylor remainder plus the spatial Laplacian truncation in the acceleration. At every subsequent step, the exact solution inserted into (5) creates a residual bounded by \((\Delta t)^2M_4/12+c^2h^2 X_4/12\). Under (11), the discrete Fourier propagator satisfies \(|\sin(k\theta)/\sin\theta|\le k\), including endpoint limits, and the error recurrence is bounded by \(n\) times first-step error plus \(n(n-1)(\Delta t)^2/2\) times the maximum residual. Substitute \(n\Delta t\le T\) to get (13).

With \(\Delta t=O(h)\), this proves a **second-order finite-horizon convergence estimate**, \(O(h^2+(\Delta t)^2)\), for this *specific* ideal real-valued scheme, under the stated regularity and initialization assumptions.

### 5.3 Finite alphabet / rounding qualification

OPH's canonical finite patch states are not arbitrary exact real numbers. If a quantized implementation incurs an independently bounded absolute additive field error of at most \(q_h/2\) per update and per patch, the same worst-case recurrence argument gives an **additional** bound

\[
\frac{q_h}{4}\frac{T}{\Delta t}
\left(\frac{T}{\Delta t}-1\right)
=O\left(q_h\left(\frac{T}{\Delta t}\right)^2\right).
\tag{14}
\]

Thus \(q_h=o((\Delta t)^2)\) is sufficient for this bound to vanish, and the stronger \(q_h=O(h^4)\), when \(\Delta t=\Theta(h)\), preserves a second-order error budget. This is a sufficient *conservative* condition, not a lower bound on all possible finite-state encodings or a proof that OPH supplies such encoding.

## 6. Executed manufactured-source experiment

The accompanying [Python script](../scripts/oph_efmw_continuum_demo.py) implements (5) over a periodic three-dimensional cubic lattice using NumPy. It selects

\[
\begin{gathered}
L=c=1,\quad T=0.5,\quad k=\frac{2\pi}{L},\\
\omega=0.8\,c\,k\sqrt3,\\
\phi(x,y,z,t)=\sin(kx)\sin(ky)\sin(kz)\cos(\omega t),
\end{gathered}
\tag{15}
\]

with the manufactured nonzero source

\[
S(x,y,z,t)
=\frac{\omega^2-3c^2k^2}{4\pi}\,\phi(x,y,z,t).
\tag{16}
\]

This yields exactly \(\phi_{tt}=c^2\nabla^2\phi-4\pi S\). The initial velocity is zero. For each \(N\), the script chooses an integer number of time steps so that \(T\) is attained exactly and \(c\Delta t/h\le0.4\).

### Recorded results

| Grid \(N^3\) | Steps | \(h\) | \(\Delta t\) | \(c\Delta t/h\) | RMS error | Bound (13) |
|---:|---:|---:|---:|---:|---:|---:|
| 12³ | 15 | 0.0833333 | 0.0333333 | 0.4000 | 0.018649885 | 0.488376 |
| 18³ | 23 | 0.0555556 | 0.0217391 | 0.3913 | 0.008298779 | 0.211131 |
| 24³ | 30 | 0.0416667 | 0.0166667 | 0.4000 | 0.004605374 | 0.119275 |
| 36³ | 45 | 0.0277778 | 0.0111111 | 0.4000 | 0.002042131 | 0.052594 |
| 48³ | 60 | 0.0208333 | 0.0083333 | 0.4000 | 0.001147773 | 0.029467 |

Successive spatial refinement orders were **1.997, 2.047, 2.006, 2.003**. The script asserted a strict CFL margin, checked the observed error is below bound (13) at every resolution, and confirmed all observed orders exceed 1.75.

**Reproduction** from the repository root (Python 3, NumPy required):

~~~shell
python3 -m pip install numpy
python3 scripts/oph_efmw_continuum_demo.py
~~~

See the [committed CSV](data/oph_efmw_continuum_results.csv) for full machine-readable values. Floating-point outputs can depend modestly on platform/NumPy version. The tolerance assertions concern this manufactured test, not external physical measurements.

## 7. Exact scientific status and non-claims

| Item | Status |
|---|---|
| Quadratic neighbor energy produces a discrete Laplacian | **Derived for the newly defined lattice model** |
| Centered reversible recurrence is consistent with sourced scalar wave PDE | **Derived under assumptions A1–A6** |
| Finite-horizon error bound under CFL and smoothness | **Proved by the stated Fourier/Taylor argument for the ideal recurrence** |
| Manufactured-source numerical convergence | **Reproduced at five resolutions** |
| Same recurrence is a canonical OPH accepted repair rule | **Not established; direct monotone-repair interpretation is obstructed** |
| Physical OPH records supply this clock, geometry, and source | **Open** |
| EFMW source \(E+cP\) is empirically identified and covariant | **Open** |
| OPH implies EFMW or EFMW uniquely follows from OPH | **Not established** |
| New physical law discovered or validated | **Not established** |

The numerical convergence supports the selected discretization and manufactured exact solution; it does not distinguish EFMW from ordinary wave mechanics, because equation (7) is itself a standard sourced scalar wave form once the source is stipulated.

## 8. Next proof and experiment program: the source-to-dynamics bridge

The nontrivial theorem would be to construct, starting from canonical OPH's typed finite observer records and permitted updates:

1. **Observable embedding:** a bounded, compatible map from interface records/quotient classes into scalar and momentum variables \(u_i,p_i\), including an honest account of finite alphabets and gauge ambiguity.
2. **Clock:** an observer-readable calibrated time step, independent of arbitrary repair scheduler order.
3. **Geometry:** source-derived three-dimensional spatial charts, weights and transport operators with a known continuum metric and operator convergence.
4. **Evolution:** a permitted reversible update (or a clean splitting of propagation from strictly descending repair) whose exact difference identity approaches (5). Show why the propagator is selected instead of inserted.
5. **Source:** a target-independent, measurable and dimensionally correct map from records to \(S=E+cP\); specify transformation laws and uncertainty.
6. **Error accounting:** discretization, spatial geometry, finite-state quantization, local asynchronous timing, readout noise, and source approximation bounds.
7. **Falsifiable comparison:** freeze the algorithm and observables, compare on held-out patch graphs with baseline diffusion and wave systems, track residuals, work per step, violations, and rejected cases; distinguish mathematical software behavior from physics.

An EFMW Zoo-style evaluation would apply TORTOISE (freeze/leakage), CROCODILE (physical causal identification), HEDGEHOG (environment transfer), RAVEN (incremental residual structure), MAGPIE (provenance), DRAGON (dynamical regimes), WEASEL (counterexamples), and TURTLE (evidence synthesis). These checks are proposed, **not claimed as executed**.

## 9. Conclusion

**Yes, a defined OPH-inspired patch-update continuum limit can yield an EFMW-form scalar wave equation with explicit units, periodic boundaries, stability conditions and finite-horizon error bounds.** The construction and manufactured-source test are successful *as applied mathematics*. They **do not** establish that OPH's original accepted-consensus repairs have that continuum limit, nor that the equation is a novel or physically validated law.

This distinction is the core result: the missing scientific work is no longer writing down a wave discretization, but demonstrating an authentic **source-to-dynamics bridge** that makes the update and source law unavoidable under independently justified OPH premises.

---

**References:** [Canonical OPH consensus paper](https://github.com/FloatingPragma/observer-patch-holography/blob/main/paper/reality_as_consensus_protocol.tex); [canonical OPH axiom reference](https://github.com/FloatingPragma/observer-patch-holography/blob/main/docs/AXIOM_REFERENCE.md); [OPH Lab README](../README.md); [EFMW Zoo review](EFMW_ZOO_REVIEW.md); [reproduction script](../scripts/oph_efmw_continuum_demo.py).

*Independent research note contributed to the enuminous fork; no upstream endorsement or modifications are implied.*
