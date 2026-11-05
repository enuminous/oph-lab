# OPH finite Lean core

This pinned project proves finite mathematical statements used by the independent
OPH Lab analyses. It does not identify nature's particles, derive physical time,
or establish an interacting continuum theory.

## Declarations and scope

| Declaration | What it establishes | Inputs still supplied |
|---|---|---|
| `trivial_character_integral` | A constant-one character has integral one | Normalized measure |
| `nontrivial_character_integral_zero` | A nontrivial character has integral zero | Translation invariance and character law; explicit integrability hypothesis retained |
| `dispersion_of_transfer_cosh` | Exact conversion to `4*j*sinh(E/2)^2 = omega` | The transfer-cosh relation and nonzero `j` |
| `latticeOmega_nonneg` | Nonnegative declared spatial symbol | Nonnegative anchor and couplings |
| `latticeOmega_zero_momentum` | Zero-momentum symbol equals the anchor `κ` | Declared symbol |
| `latticeOmega_pos_of_positive_mass` | Positive symbol for positive anchor | `κ > 0`, nonnegative couplings; “mass” in this historical name means the anchor parameter |
| `shiftLaplacian_character` | A group character is an exact eigenfunction of the explicitly defined nearest-neighbor shift operator | Group carrier, finite direction set, character, weights; a finite carrier gives a finite matrix |
| `cosineSymbol_eq_latticeOmega` | Cosine and half-angle spatial symbols agree exactly | Declared real angles and weights |
| `graphAction_nonneg` | Nonnegative finite weighted graph action | Nonnegative anchor and edge weights |
| `graphAction_eq_zero_iff_of_positive_anchor` | Zero anchored action is equivalent to the zero field | Strictly positive anchor, nonnegative edge weights |
| `graphAction_eq_zero_iff_edge_agreement` | Zero unanchored action is equivalent to agreement on every listed edge | Strictly positive edge weights; global constancy additionally needs graph connectedness |

The new operator theorem derives its eigen-equation from the character
homomorphism law; the eigen-equation is not a hypothesis. It does not prove
that the characters form a complete basis or instantiate the cyclic torus's
character phases. The graph-action kernel results do not assume those kernels
as premises. They also do not prove the identification between this action and
the OPH source's repair law.

## Reproduce

From this directory:

```sh
lake exe cache get
lake build OphStage4
lake env lean OphStage4Audit.lean
```

Do not run `lake update` for a frozen replay. Lean is pinned to
`leanprover/lean4:v4.35.0-rc4`; Mathlib is pinned to
`d3739f06187591e81887886ca767b6a2dc1416ea`, including the transitive lockfile.
The standard `@[default_target]` syntax ensures plain `lake build` also builds
the library. Its roots include the audit file.

`OphStage4Audit.lean` prints the axiom dependencies of every public theorem.
No project axiom or admitted proof is permitted. The ordinary foundational
axioms `propext`, `Classical.choice`, and `Quot.sound` are disclosed by the
audit; they do not discharge the hypotheses in the table.
The audit's elaboration code fails the build if any other axiom appears.
The [local validation receipt](validation.json) records the passing build,
eleven axiom reports, source hashes, and a rejection control.

See [finite premise inventory](../../docs/OPH_FINITE_PREMISES.md) for the
remaining proof obligations and the scientific boundary.
