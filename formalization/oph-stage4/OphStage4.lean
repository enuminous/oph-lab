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

theorem trivial_character_integral
    {G : Type*} [Monoid G] [MeasurableSpace G]
    (μ : Measure G) (χ : G →* ℂ)
    (hμ : μ.real Set.univ = 1)
    (htriv : ∀ x, χ x = 1) :
    (∫ x, χ x ∂μ) = 1 := by
  have heq : (fun x => χ x) = fun _ => (1 : ℂ) := funext htriv
  rw [heq]
  simp [hμ]

theorem nontrivial_character_integral_zero
    {G : Type*} [Group G] [MeasurableSpace G]
    (μ : Measure G) (χ : G →* ℂ)
    (hleft : ∀ (g : G) (f : G → ℂ),
      (∫ x, f (g * x) ∂μ) = ∫ x, f x ∂μ)
    (hχ : Integrable (fun x => χ x) μ)
    (hnontriv : ∃ g, χ g ≠ 1) :
    (∫ x, χ x ∂μ) = 0 := by
  obtain ⟨g, hg⟩ := hnontriv
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
  have hI : I = χ g * I := by
    simpa [I] using htranslate.symm.trans hfactor
  have hz : (χ g - 1) * I = 0 := by
    calc
      (χ g - 1) * I = χ g * I - I := by ring
      _ = I - I := by rw [← hI]
      _ = 0 := sub_self I
  have hne : χ g - 1 ≠ 0 := sub_ne_zero.mpr hg
  rcases mul_eq_zero.mp hz with hzero | hzero
  · exact (hne hzero).elim
  · exact hzero

theorem dispersion_of_transfer_cosh
    {j omega E : ℝ} (hj : j ≠ 0)
    (hE : Real.cosh E = 1 + omega / (2 * j)) :
    4 * j * (Real.sinh (E / 2)) ^ 2 = omega := by
  have hdouble : Real.cosh E = 1 + 2 * (Real.sinh (E / 2)) ^ 2 := by
    have htwo := Real.cosh_two_mul (E / 2)
    rw [show 2 * (E / 2) = E by ring] at htwo
    nlinarith [htwo, Real.cosh_sq_sub_sinh_sq (E / 2)]
  have hgap : 2 * j * (Real.cosh E - 1) = omega := by
    rw [hE]
    field_simp [hj]
    ring
  calc
    4 * j * (Real.sinh (E / 2)) ^ 2 =
        2 * j * (Real.cosh E - 1) := by rw [hdouble]; ring
    _ = omega := hgap

/-! The spatial part of the anchored nearest-neighbor lattice operator is a
finite sum of nonnegative mode contributions when its couplings are
nonnegative. At zero momentum all of those contributions vanish, leaving the
mass parameter `κ`. This is an algebraic statement about the declared lattice
symbol; it does not prove that an operator has this symbol. -/

noncomputable def latticeOmega {d : ℕ} (κ : ℝ) (J θ : Fin d → ℝ) : ℝ :=
  κ + 4 * ∑ i : Fin d, J i * (Real.sin (θ i / 2)) ^ 2

theorem latticeOmega_nonneg {d : ℕ} {κ : ℝ} {J θ : Fin d → ℝ}
    (hκ : 0 ≤ κ) (hJ : ∀ i, 0 ≤ J i) :
    0 ≤ latticeOmega κ J θ := by
  unfold latticeOmega
  apply add_nonneg hκ
  apply mul_nonneg (by norm_num)
  apply Finset.sum_nonneg
  intro i hi
  exact mul_nonneg (hJ i) (sq_nonneg (Real.sin (θ i / 2)))

theorem latticeOmega_zero_momentum {d : ℕ} (κ : ℝ) (J : Fin d → ℝ) :
    latticeOmega κ J (fun _ => 0) = κ := by
  simp [latticeOmega, Real.sin_zero]

theorem latticeOmega_pos_of_positive_mass {d : ℕ} {κ : ℝ}
    {J θ : Fin d → ℝ} (hκ : 0 < κ) (hJ : ∀ i, 0 ≤ J i) :
    0 < latticeOmega κ J θ := by
  unfold latticeOmega
  apply add_pos_of_pos_of_nonneg hκ
  apply mul_nonneg (by norm_num)
  apply Finset.sum_nonneg
  intro i hi
  exact mul_nonneg (hJ i) (sq_nonneg (Real.sin (θ i / 2)))

end OphLab.Stage4
