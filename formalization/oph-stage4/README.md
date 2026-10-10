# OPH Stage 4 Lean cores

This Lake project contains two narrow proof targets extracted from the Stage 1
and Stage 2 analyses.

1. `normalized_character_integral` proves that a nontrivial integrable group
   character has zero integral under a normalized left-invariant measure, and
   that the trivial character integrates to one. This is the abstract Haar
   selection rule. The explicit finite product `U(1)^E`, link-exponent
   construction, and cell-complex incidence specialization are not yet
   instantiated here.
2. `dispersion_of_transfer_cosh` proves the algebraic conversion from the
   transfer relation `cosh E = 1 + omega/(2j)` to
   `4*j*sinh(E/2)^2 = omega`. It does not prove that the transfer operator is a
   Mehler operator, that its Hermite eigenfunctions are complete, or that the
   transfer coordinate is physical time.

## Build

From this directory, run:

```sh
lake update
lake exe cache get
lake build
```

The Lean and Mathlib revisions are pinned in `lean-toolchain` and `lakefile.lean`.
The GitHub Actions workflow builds this project on changes under this directory.

## Status and limits

The source-pinned OPH `N=1` theorem is still unavailable, so this formalization
does not claim that the abstract character theorem proves Bernhard's intended
zero-flux statement. Likewise, the dispersion lemma checks one algebraic step
of the homogeneous periodic Gaussian calculation, not the full continuous
transfer-spectrum proof. These boundaries are intentional.
