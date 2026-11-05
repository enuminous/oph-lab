module

public import Mathlib.MeasureTheory.Integral.Bochner.Basic
public import Mathlib.Analysis.Complex.Trigonometric
public meta import Mathlib.Tactic.FieldSimp
public meta import Mathlib.Tactic.Linarith
public meta import Mathlib.Tactic.NormNum
public meta import Mathlib.Tactic.Ring

@[expose] public section

open MeasureTheory
open scoped BigOperators

namespace OphLab.Stage4

/-!
Stage 4 contains the Haar, transfer-algebra, shift-operator and graph-action
cores. The Haar result below is
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
    (_hχ : Integrable (fun x => χ x) μ)
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

namespace OphLab.Stage4

/-! These are finite operator/energy results, independent of the assumed
transfer-cosh relation above. They do not assert a complete Fourier basis,
reflection positivity, or any physical interpretation of the shift coordinate. -/

/-- The actual anchored nearest-neighbour shift operator on a group carrier.
For a finite group this is a finite matrix. No spectral equation is assumed. -/
noncomputable def shiftLaplacian {G D : Type*} [Group G] [Fintype D]
    (κ : ℂ) (J : D → ℂ) (step : D → G) (f : G → ℂ) (x : G) : ℂ :=
  κ * f x + ∑ i, J i * (2 * f x - f (step i * x) - f ((step i)⁻¹ * x))

noncomputable def characterSymbol {G D : Type*} [Group G] [Fintype D]
    (κ : ℂ) (J : D → ℂ) (step : D → G) (χ : G →* ℂ) : ℂ :=
  κ + ∑ i, J i * (2 - χ (step i) - χ ((step i)⁻¹))

/-- Every supplied group character is an exact eigenfunction of the defined
shift operator. This derives the eigen-equation from the homomorphism laws. -/
theorem shiftLaplacian_character {G D : Type*} [Group G] [Fintype D]
    (κ : ℂ) (J : D → ℂ) (step : D → G) (χ : G →* ℂ) (x : G) :
    shiftLaplacian κ J step χ x = characterSymbol κ J step χ * χ x := by
  simp only [shiftLaplacian, characterSymbol, map_mul, add_mul, Finset.sum_mul]
  congr 1
  apply Finset.sum_congr rfl
  intro i hi
  ring

/-- The cosine form of the nearest-neighbour symbol equals the existing
half-angle form. This is an identity, without a small-momentum approximation. -/
theorem cosineSymbol_eq_latticeOmega {d : ℕ} (κ : ℝ) (J θ : Fin d → ℝ) :
    κ + ∑ i, J i * (2 - 2 * Real.cos (θ i)) = latticeOmega κ J θ := by
  unfold latticeOmega
  rw [Finset.mul_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro i hi
  have hdouble := Real.cos_two_mul (θ i / 2)
  rw [show 2 * (θ i / 2) = θ i by ring] at hdouble
  have hcircle := Real.sin_sq_add_cos_sq (θ i / 2)
  have hhalf : 2 - 2 * Real.cos (θ i) = 4 * (Real.sin (θ i / 2)) ^ 2 := by
    nlinarith
  rw [hhalf]
  ring

/-- A finite real graph action with an anchor term. Source and destination
maps may describe a periodic lattice or any other finite directed edge list. -/
noncomputable def graphAction {V E : Type*} [Fintype V] [Fintype E]
    (κ : ℝ) (w : E → ℝ) (src dst : E → V) (u : V → ℝ) : ℝ :=
  κ * ∑ v, (u v) ^ 2 + ∑ e, w e * (u (dst e) - u (src e)) ^ 2

theorem graphAction_nonneg {V E : Type*} [Fintype V] [Fintype E]
    {κ : ℝ} {w : E → ℝ} (src dst : E → V) (u : V → ℝ)
    (hκ : 0 ≤ κ) (hw : ∀ e, 0 ≤ w e) :
    0 ≤ graphAction κ w src dst u := by
  unfold graphAction
  apply add_nonneg
  · exact mul_nonneg hκ (Finset.sum_nonneg (fun v _ => sq_nonneg (u v)))
  · exact Finset.sum_nonneg (fun e _ => mul_nonneg (hw e) (sq_nonneg _))

/-- Positive anchoring removes every zero-action mode, without a connectedness
assumption and without assuming a spectral gap formula. -/
theorem graphAction_eq_zero_iff_of_positive_anchor
    {V E : Type*} [Fintype V] [Fintype E]
    {κ : ℝ} {w : E → ℝ} (src dst : E → V) (u : V → ℝ)
    (hκ : 0 < κ) (hw : ∀ e, 0 ≤ w e) :
    graphAction κ w src dst u = 0 ↔ ∀ v, u v = 0 := by
  constructor
  · intro hzero v
    have hedge : 0 ≤ ∑ e, w e * (u (dst e) - u (src e)) ^ 2 :=
      Finset.sum_nonneg (fun e _ => mul_nonneg (hw e) (sq_nonneg _))
    have hsum : (u v) ^ 2 ≤ ∑ x, (u x) ^ 2 :=
      Finset.single_le_sum (fun x _ => sq_nonneg (u x)) (Finset.mem_univ v)
    have hscaled := mul_le_mul_of_nonneg_left hsum (le_of_lt hκ)
    unfold graphAction at hzero
    have hprod : κ * (u v) ^ 2 ≤ 0 := by linarith
    have hsq : (u v) ^ 2 = 0 :=
      le_antisymm (nonpos_of_mul_nonpos_right hprod hκ) (sq_nonneg _)
    exact sq_eq_zero_iff.mp hsq
  · intro hu
    simp [graphAction, hu]

/-- With zero anchor and strictly positive edge weights, zero action is
exactly agreement along every listed edge. This does NOT infer a globally
constant field unless connectedness of the chosen graph is also proved. -/
theorem graphAction_eq_zero_iff_edge_agreement
    {V E : Type*} [Fintype V] [Fintype E]
    {w : E → ℝ} (src dst : E → V) (u : V → ℝ)
    (hw : ∀ e, 0 < w e) :
    graphAction 0 w src dst u = 0 ↔ ∀ e, u (dst e) = u (src e) := by
  constructor
  · intro hzero e
    have hsum : w e * (u (dst e) - u (src e)) ^ 2 ≤
        ∑ f, w f * (u (dst f) - u (src f)) ^ 2 :=
      Finset.single_le_sum
        (fun f _ => mul_nonneg (le_of_lt (hw f))
          (sq_nonneg (u (dst f) - u (src f))))
        (Finset.mem_univ e)
    simp only [graphAction, zero_mul, zero_add] at hzero
    rw [hzero] at hsum
    have hsq : (u (dst e) - u (src e)) ^ 2 = 0 :=
      le_antisymm (nonpos_of_mul_nonpos_right hsum (hw e)) (sq_nonneg _)
    exact sub_eq_zero.mp (sq_eq_zero_iff.mp hsq)
  · intro he
    simp [graphAction, he]

end OphLab.Stage4
