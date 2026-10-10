import Mathlib

open MeasureTheory

namespace OphLab.Stage4

/-!
Stage 4 contains two small machine-checkable cores.  The Haar result below is
abstract: it applies to any normalized left-invariant measure and any
integrable group character.  An explicit `U(1)^E` representation and its
incidence-matrix specialization remain separate obligations.

The transfer result is deliberately conditional on the Mehler/transfer-gap
relation.  It checks the algebra converting that relation to the lattice
dispersion formula; it does not prove the Mehler spectral theorem or identify
the transfer coordinate with physical time.
-/

theorem normalized_character_integral
    {G : Type*} [Group G]
    (μ : Measure G) (χ : G →* ℂ)
    (hleft : ∀ (g : G) (f : G → ℂ),
      (∫ x, f (g * x) ∂μ) = ∫ x, f x ∂μ)
    (hμ : μ Set.univ = 1)
    (hχ : Integrable (fun x => χ x) μ) :
    (∫ x, χ x ∂μ) = if ∀ x, χ x = 1 then 1 else 0 := by
  by_cases htriv : ∀ x, χ x = 1
  · have heq : (fun x => χ x) = fun _ => (1 : ℂ) := funext htriv
    rw [heq, if_pos htriv]
    simp [hμ]
  · rw [if_neg htriv]
    obtain ⟨g, hg⟩ := not_forall.mp htriv
    let I : ℂ := ∫ x, χ x ∂μ
    have htranslate : (∫ x, χ (g * x) ∂μ) = ∫ x, χ x ∂μ :=
      hleft g (fun x => χ x)
    have hfactor : (∫ x, χ (g * x) ∂μ) = χ g * I := by
      calc
        (∫ x, χ (g * x) ∂μ) = ∫ x, χ g * χ x ∂μ := by
          congr 1
          funext x
          exact map_mul χ g x
        _ = χ g * I := by
          rw [integral_const_mul]
          rfl
    have hI : I = χ g * I := by
      simpa [I] using htranslate.symm.trans hfactor
    have hz : (χ g - 1) * I = 0 := by
      rw [mul_sub, one_mul, hI]
      ring
    have hne : χ g - 1 ≠ 0 := sub_ne_zero.mpr hg
    rcases mul_eq_zero.mp hz with hzero | hzero
    · exact (hne hzero).elim
    · exact hzero

theorem dispersion_of_transfer_cosh
    {j omega E : ℝ} (hj : j ≠ 0)
    (hE : Real.cosh E = 1 + omega / (2 * j)) :
    4 * j * (Real.sinh (E / 2)) ^ 2 = omega := by
  have hdouble : Real.cosh E = 1 + 2 * (Real.sinh (E / 2)) ^ 2 := by
    rw [show E = 2 * (E / 2) by ring, Real.cosh_two_mul, Real.cosh_sq]
    ring
  have hgap : 2 * j * (Real.cosh E - 1) = omega := by
    rw [hE]
    field_simp [hj]
    ring
  calc
    4 * j * (Real.sinh (E / 2)) ^ 2 =
        2 * j * (Real.cosh E - 1) := by rw [hdouble]; ring
    _ = omega := hgap

end OphLab.Stage4
