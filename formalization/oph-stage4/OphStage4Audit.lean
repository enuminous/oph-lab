module

import OphStage4

/-! Replayable dependency audit for every public theorem in this finite core.
The corresponding CI build must show no `sorryAx` and no project-defined axiom.
Ordinary Mathlib foundations (`propext`, `Classical.choice`, `Quot.sound`)
are disclosed; the printed dependencies do not erase theorem hypotheses. -/

#print axioms OphLab.Stage4.trivial_character_integral
#print axioms OphLab.Stage4.nontrivial_character_integral_zero
#print axioms OphLab.Stage4.dispersion_of_transfer_cosh
#print axioms OphLab.Stage4.latticeOmega_nonneg
#print axioms OphLab.Stage4.latticeOmega_zero_momentum
#print axioms OphLab.Stage4.latticeOmega_pos_of_positive_mass
#print axioms OphLab.Stage4.shiftLaplacian_character
#print axioms OphLab.Stage4.cosineSymbol_eq_latticeOmega
#print axioms OphLab.Stage4.graphAction_nonneg
#print axioms OphLab.Stage4.graphAction_eq_zero_iff_of_positive_anchor
#print axioms OphLab.Stage4.graphAction_eq_zero_iff_edge_agreement

-- Fail the build if any audited theorem gains an admission or another axiom.
run_elab do
  let permitted : Array Lean.Name := #[``propext, ``Classical.choice, ``Quot.sound]
  let declarations : Array Lean.Name := #[
    ``OphLab.Stage4.trivial_character_integral,
    ``OphLab.Stage4.nontrivial_character_integral_zero,
    ``OphLab.Stage4.dispersion_of_transfer_cosh,
    ``OphLab.Stage4.latticeOmega_nonneg,
    ``OphLab.Stage4.latticeOmega_zero_momentum,
    ``OphLab.Stage4.latticeOmega_pos_of_positive_mass,
    ``OphLab.Stage4.shiftLaplacian_character,
    ``OphLab.Stage4.cosineSymbol_eq_latticeOmega,
    ``OphLab.Stage4.graphAction_nonneg,
    ``OphLab.Stage4.graphAction_eq_zero_iff_of_positive_anchor,
    ``OphLab.Stage4.graphAction_eq_zero_iff_edge_agreement]
  for declaration in declarations do
    for dependency in (← Lean.collectAxioms declaration) do
      unless permitted.contains dependency do
        throwError "Unexpected axiom {dependency} in {declaration}"
