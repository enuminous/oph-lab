# Finite premise inventory

Date: 2026-11-05. Scope: `formalization/oph-stage4`, independent OPH Lab fork.
The baseline was `d498af3`; the exact resulting revision is the commit carrying
this document. The authoritative broader OPH premise register is a separate
upstream artifact and is not silently closed by these local results.

## Newly closed finite mathematical steps

For a group carrier `G`, finite direction set `D`, steps `s_i`, and complex
weights, the code defines an actual operator

\[
(L f)(x)=\kappa f(x)+\sum_i J_i
\bigl(2f(x)-f(s_i x)-f(s_i^{-1}x)\bigr).
\]

For each group character `χ`, Lean derives

\[
L\chi=\left[\kappa+\sum_i J_i
(2-\chi(s_i)-\chi(s_i^{-1}))\right]\chi.
\]

This is `shiftLaplacian_character`. The proof requires the character
homomorphism law, not the eigen-equation as a premise. A finite `G` makes this
a finite-matrix result; finiteness of `G` is not needed by the identity itself.
It establishes one eigenfunction for each supplied character, not a complete
spectral decomposition.

`cosineSymbol_eq_latticeOmega` independently proves the exact trigonometric
identity

\[
\kappa+\sum_i J_i(2-2\cos\theta_i)
=\kappa+4\sum_i J_i\sin^2(\theta_i/2).
\]

To join these two declarations into a finite torus Fourier theorem still
requires construction of the torus characters and the identity
`χ(s_i)+χ(s_i⁻¹)=2 cos θ_i`. Neither that phase assignment nor completeness is
hidden inside a claimed fully derived spectrum.

The code also defines a finite graph action on arbitrary source and destination
maps:

\[
Q(u)=\kappa\sum_v u_v^2+
\sum_e w_e(u_{\mathrm{dst}(e)}-u_{\mathrm{src}(e)})^2.
\]

Lean proves nonnegativity for nonnegative coefficients. With `κ>0`, zero
action is equivalent to the identically zero field, with no connectedness
assumption. With `κ=0` and all `w_e>0`, zero action is equivalent to agreement
on every listed edge. These close the positivity and exact kernel criteria
for this declared finite action. They do not identify the action with a
source-selected OPH law.

## Obligations that remain open

| ID | Obligation | Current evidence/status | What would close it |
|---|---|---|---|
| FIN-HAAR | Instantiate the integral theorem on `U(1)^E` with product Haar measure | Abstract translation-invariance theorem only | Explicit product measure, character and integrability construction |
| FIN-INCIDENCE | Derive the product character from integer plaquette incidence | Open | A typed edge/face incidence map and proof that its link exponents equal the character exponents |
| FIN-TOPOLOGY | Infer vanishing plaquette labels from vanishing link exponents | Open and not valid on all topologies | State a concrete cell complex and prove injectivity of the relevant boundary map, or retain its nonzero kernel |
| FIN-TORUS | Construct finite cyclic-torus modes and identify character phases | Partially supported by the generic shift-operator theorem and exact trig identity | Explicit cyclic group characters and their phase identities |
| FIN-BASIS | Establish completeness/orthogonality and diagonalize the whole finite matrix | Open | A finite Fourier basis theorem with dimension and normalization checks |
| FIN-CONNECTED | Upgrade edge agreement to global constant field in the zero-anchor case | Conditional on connectedness; edge criterion proved | A path/connectedness proof for the actual graph |
| FIN-TRANSFER | Derive Mehler kernel, eigenvalues and complete Hermite basis | Open | Independent operator derivation; the existing cosh relation is still supplied |
| FIN-REPAIR | Identify the finite action/shift operator with the source repair implementation | Open | Pinned source code and a correspondence proof, including scheduler and memory behavior |
| FIN-LIVENESS | Every allowed repair schedule reaches the claimed endpoint | Open | Declared scheduling class and fairness/termination proof; a decreasing real potential alone is insufficient |
| FIN-GLUING | Repair completeness and quotient-compatible collar gluing | Open | Constructible local repair map and compatibility theorem for the actual finite source |
| PHYS-CLOCK | Identify the transfer direction with measured physical time | Open | Independent operational clock and causal correspondence |
| PHYS-CONTINUUM | Interacting quantum 3+1D continuum and physical fields | Open | Controlled refinement, reconstruction and source-to-observable bridge |
| PHYS-PARTICLES | Nature's particle identities and pole masses | Open | Spectrum, charges, spin/statistics, physical calibration and independent empirical comparison |

The `graphAction` result permits disconnected graphs. For example, two
disconnected components may have distinct constant values and still have zero
unanchored action. No global-uniqueness claim follows from edge agreement alone.
Likewise, a nonzero kernel of the face-to-edge incidence map is a genuine
topological possibility; it cannot be removed by renaming the zero-flux claim.

## Proof and reproducibility boundary

The eleven named theorems are listed in the [project README](../formalization/oph-stage4/README.md).
`OphStage4Audit.lean` prints their foundational dependencies. The build checks
the exact Lean statements; an axiom report alone does not prove their physical
premises. No fitted particle labels or measured masses enter these statements.

The historical README's `normalized_character_integral` was not an actual
declaration. It is corrected to the two real declarations
`trivial_character_integral` and `nontrivial_character_integral_zero`. The Lake
package's obsolete `defaultTargets` field is replaced by `@[default_target]`.
Toolchain and dependency revisions remain pinned.

The local pinned build passed (2,613 jobs), and all eleven declarations passed
the axiom audit with only `propext`, `Classical.choice`, and `Quot.sound`.
The audit also failed as expected when a temporary negative-control copy
removed `Quot.sound` from its permitted list. A
[validation receipt](../formalization/oph-stage4/validation.json) records the
commands and exact source hashes. The publishing commit's GitHub Actions run
controls remote CI status. The broader theory remains incomplete while the
obligations above remain open.
