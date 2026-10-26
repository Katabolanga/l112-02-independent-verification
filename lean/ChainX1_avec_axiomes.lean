import Mathlib.Algebra.Group.Hom.Defs
import Mathlib.Algebra.Group.Equiv.Defs
import Mathlib.Algebra.Group.Basic
import Mathlib.Tactic.Abel
import Mathlib.Tactic.Ring
import Mathlib.Tactic.ByContra

/-!
# X1 (rang 112) : la déduction « faits calculés ⟹ minimum ≥ 10 » pour un recollement modulo 2 de DEUX réseaux

Lot R112_X1_EFFORT_MAX_20261025 (agent Claude n° 116, 25 oct. 2026). Adaptation, écrite pour ce lot, du fichier
`lean/EEUL/L112/Chain.lean` du dépôt public de roiban1344 (licence MIT ; lu, puis porté), qui traite le recollement
`L₁₁₂ = {(x, x τ + 2 y)/√2}` de DEUX COPIES du même réseau `L₅₆` le long de `τ`, `τ² = -5`.

Ici, deux réseaux pairs DIFFÉRENTS `L` (forme `A.B`) et `L'` (forme `A'.B`), de minimum ≥ 6 (F1 pour chacun), et
le recollement `X = {(x, φ x + 2 y)/√2 : x ∈ L, y ∈ L'}`, où `φ : L → L'` relève modulo 2 une application
bijective `f : L/2L → L'/2L'` qui préserve la parité, et `ψ : L' → L` relève son inverse (`ψ (φ x) = x + 2 χ x`).
Pour X1 : `L = L₅₆,₂(𝔐)` (type b) et `L' = L₅₆,₂(𝔐̃)` (type c, le `L₅₆` du dépôt), `f` calculée exactement.

Différences avec le cas de roiban : il n'y a plus d'endomorphisme `τ` avec `τ² ≡ 1 (mod 2)` ; le type (10,6)
n'est plus équivalent au type (6,10) : il demande une hypothèse de plus, `h6'` (classes `ψ r' + 2L` des vecteurs
minimaux `r'` de `L'`), et la réduction par symétrie se fait avec des PAIRES `(g, g')` d'automorphismes de `L` et `L'`
compatibles avec `φ` et `ψ` modulo 2.

Les faits calculés sont des hypothèses (champs des structures `Lat`, `Glue`, `Data`) ; rien ici ne calcule avec
les matrices. Restent hors de Lean, comme chez roiban : l'unimodularité, la série thêta, la borne `min ≤ 10`, le
passage de `(x, φ x + 2 y)` aux vecteurs de X1, et la proposition « forme canonique hors de K₈ ⟹ pas de vecteur de
norme 8 dans la classe ».
-/

namespace EEUL.X1

/-- Un réseau pair abstrait de minimum ≥ 6 : groupe abélien `L`, forme bilinéaire symétrique entière `B`. -/
structure Lat (L : Type*) [AddCommGroup L] where
  B : L →+ L →+ ℤ
  symm : ∀ x y, B x y = B y x
  even : ∀ x, B x x % 2 = 0
  /-- **F1** (hypothèse) : tout vecteur non nul a une norme ≥ 6. -/
  min6 : ∀ x, x ≠ 0 → 6 ≤ B x x

namespace Lat

variable {L : Type*} [AddCommGroup L] (S : Lat L)

def N (x : L) : ℤ := S.B x x

theorem B_add_left (a b c : L) : S.B (a + b) c = S.B a c + S.B b c := by
  rw [map_add, AddMonoidHom.add_apply]

theorem B_add_right (a b c : L) : S.B a (b + c) = S.B a b + S.B a c := by
  rw [map_add]

theorem B_neg_left (a c : L) : S.B (-a) c = -S.B a c := by
  rw [map_neg, AddMonoidHom.neg_apply]

theorem B_neg_right (a c : L) : S.B a (-c) = -S.B a c := by
  rw [map_neg]

theorem N_add (a b : L) : S.N (a + b) = S.N a + S.N b + 2 * S.B a b := by
  unfold N
  rw [B_add_left, B_add_right, B_add_right, S.symm b a]
  ring

theorem N_neg (a : L) : S.N (-a) = S.N a := by
  unfold N
  rw [B_neg_left, B_neg_right, neg_neg]

theorem N_sub (a b : L) : S.N (a - b) = S.N a + S.N b - 2 * S.B a b := by
  rw [sub_eq_add_neg, N_add, N_neg, B_neg_right]
  ring

theorem N_two (y : L) : S.N (2 • y) = 4 * S.N y := by
  rw [two_nsmul, N_add]
  unfold N
  ring

theorem B_two_right (a y : L) : S.B a (2 • y) = 2 * S.B a y := by
  rw [two_nsmul, B_add_right]
  ring

theorem N_two_ge (y : L) (hy : y ≠ 0) : 24 ≤ S.N (2 • y) := by
  rw [N_two]
  have := S.min6 y hy
  unfold N
  omega

/-- La norme dans une classe `w + 2L` est constante modulo 4. -/
theorem N_add_two (w y : L) : S.N (w + 2 • y) = S.N w + 4 * (S.B w y + S.N y) := by
  rw [N_add, N_two, B_two_right]
  ring

end Lat

/-- Les données du recollement : deux réseaux, un relèvement `φ : L → L'` de `f`, un relèvement `ψ : L' → L` de
`f⁻¹` avec `ψ (φ x) = x + 2 χ x`, et la conservation de la parité (`N x ≡ N' (φ x) (mod 4)`). -/
structure Glue (L L' : Type*) [AddCommGroup L] [AddCommGroup L'] where
  A : Lat L
  A' : Lat L'
  φ : L →+ L'
  ψ : L' →+ L
  χ : L →+ L
  /-- `ψ ∘ φ ≡ id (mod 2L)` (calculé : `f` inversible). -/
  ψφ : ∀ x, ψ (φ x) = x + 2 • χ x
  /-- `f` préserve la parité (calculé ; équivaut à : le recollement est pair). -/
  parity : ∀ x, (A.N x + A'.N (φ x)) % 4 = 0

namespace Glue

variable {L L' : Type*} [AddCommGroup L] [AddCommGroup L'] (Gl : Glue L L')

open Lat

/-- Le recollement est pair : `N x + N' (φ x + 2 y) ≡ 0 (mod 4)`. -/
theorem norm_sum_mod4 (x : L) (y : L') : (Gl.A.N x + Gl.A'.N (Gl.φ x + 2 • y)) % 4 = 0 := by
  rw [Lat.N_add_two]
  have := Gl.parity x
  omega

/-- Si `φ x ∈ 2L'` alors `x ∈ 2L` : `x = 2 (-(ψ y) - χ x)` quand `φ x + 2 y = 0`. -/
theorem two_dvd_of_phi (x : L) (y : L') (h : Gl.φ x + 2 • y = 0) :
    x = 2 • (-(Gl.ψ y) - Gl.χ x) := by
  have h1 : Gl.φ x = -(2 • y) := eq_neg_of_add_eq_zero_left h
  have h2 : Gl.ψ (Gl.φ x) = -(2 • Gl.ψ y) := by rw [h1, map_neg, map_nsmul]
  rw [Gl.ψφ] at h2
  calc x = (x + 2 • Gl.χ x) - 2 • Gl.χ x := by abel
    _ = -(2 • Gl.ψ y) - 2 • Gl.χ x := by rw [h2]
    _ = 2 • (-(Gl.ψ y) - Gl.χ x) := by abel

/-- `x` est dans la classe `ψ v + 2L` de `v = φ x + 2 y` : `x = ψ v + 2 (-(χ x) - ψ y)`. -/
theorem psi_inverse_mod2 (x : L) (y : L') :
    x = Gl.ψ (Gl.φ x + 2 • y) + 2 • (-(Gl.χ x) - Gl.ψ y) := by
  rw [map_add, map_nsmul, Gl.ψφ]
  abel

end Glue

section Main

variable {L L' : Type*} [AddCommGroup L] [AddCommGroup L'] (Gl : Glue L L')

open Lat Glue

/-- **Les trois conditions de classes ⟹ pas de vecteur de norme < 10 dans X**.
`h6`  : types (6,6) et (6,10) — classes `φ r + 2L'` des vecteurs minimaux `r` de `L` ;
`h6'` : type (10,6) — classes `ψ r' + 2L` des vecteurs minimaux `r'` de `L'` ;
`h8`  : type (8,8) — aucune classe `φ x + 2L'` d'un vecteur `x` de norme 8 de `L` ne contient de vecteur de norme 8.
Conclusion : si `(x, φ x + 2 y) ≠ 0` alors `N x + N' (φ x + 2 y) ≥ 20`. -/
theorem no_inner_shell_ne8
    (h6 : ∀ r y, Gl.A.N r = 6 → 14 ≤ Gl.A'.N (Gl.φ r + 2 • y))
    (h6' : ∀ r' y, Gl.A'.N r' = 6 → 14 ≤ Gl.A.N (Gl.ψ r' + 2 • y))
    (h8 : ∀ x y, Gl.A.N x = 8 → Gl.A'.N (Gl.φ x + 2 • y) ≠ 8)
    (x : L) (y : L') (hz : x ≠ 0 ∨ Gl.φ x + 2 • y ≠ 0) :
    20 ≤ Gl.A.N x + Gl.A'.N (Gl.φ x + 2 • y) := by
  have hmod := Gl.norm_sum_mod4 x y
  have hex := Gl.A.even x
  have hev := Gl.A'.even (Gl.φ x + 2 • y)
  unfold Lat.N at hmod
  by_cases hx : x = 0
  · -- x = 0 : v = 2y ≠ 0, de norme ≥ 24
    subst hx
    have hv : Gl.φ 0 + 2 • y ≠ 0 := by
      rcases hz with h | h
      · exact absurd rfl h
      · exact h
    rw [map_zero, zero_add] at hv ⊢
    have hy : y ≠ 0 := by rintro rfl; simp at hv
    have := Gl.A'.N_two_ge y hy
    unfold Lat.N at this ⊢
    simp only [map_zero]
    omega
  by_cases hv : Gl.φ x + 2 • y = 0
  · -- v = 0 : x ∈ 2L et x ≠ 0, de norme ≥ 24
    have hxe := Gl.two_dvd_of_phi x y hv
    have hw : -(Gl.ψ y) - Gl.χ x ≠ 0 := by
      intro h; rw [h, nsmul_zero] at hxe; exact hx hxe
    have := Gl.A.N_two_ge _ hw
    rw [← hxe] at this
    rw [hv]
    unfold Lat.N at this ⊢
    simp only [map_zero]
    omega
  have hx6 := Gl.A.min6 x hx
  have hv6 := Gl.A'.min6 _ hv
  by_contra hlt
  unfold Lat.N at hlt
  have hcases :
      (Gl.A.B x x = 6 ∧
        (Gl.A'.B (Gl.φ x + 2 • y) (Gl.φ x + 2 • y) = 6 ∨
          Gl.A'.B (Gl.φ x + 2 • y) (Gl.φ x + 2 • y) = 10))
      ∨ (Gl.A.B x x = 8 ∧ Gl.A'.B (Gl.φ x + 2 • y) (Gl.φ x + 2 • y) = 8)
      ∨ (Gl.A.B x x = 10 ∧ Gl.A'.B (Gl.φ x + 2 • y) (Gl.φ x + 2 • y) = 6) := by omega
  rcases hcases with ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩
  · -- types (6,6) et (6,10) : exclus par h6
    have := h6 x y h1; unfold Lat.N at this; omega
  · -- type (8,8) : exclu par h8
    exact h8 x y h1 h2
  · -- type (10,6) : x est dans la classe ψ v + 2L, et v est minimal dans L' : h6' s'applique à v
    have := h6' (Gl.φ x + 2 • y) (-(Gl.χ x) - Gl.ψ y) h2
    rw [← Gl.psi_inverse_mod2 x y] at this
    unfold Lat.N at this
    omega

end Main

/-! ## Lemme du milieu et certificats (dans un seul réseau) -/

section Bounding

variable {L : Type*} [AddCommGroup L] (S : Lat L)

open Lat

def SmallIP (w0 : L) : Prop := ∀ u, S.N u = 6 → -6 ≤ S.B w0 u ∧ S.B w0 u ≤ 6

theorem midpoints (w0 y : L) :
    4 * S.N y = S.N (w0 + 2 • y) - S.N w0 - 4 * S.B w0 y ∧
    4 * S.N (w0 + y) = 3 * S.N w0 + S.N (w0 + 2 • y) + 4 * S.B w0 y := by
  constructor
  · rw [N_add, N_two, B_two_right]; ring
  · rw [N_add, N_add, N_two, B_two_right]; ring

theorem coset_norm_mod4 (w0 y : L) : (S.N (w0 + 2 • y) - S.N w0) % 4 = 0 := by
  rw [N_add, N_two, B_two_right]; omega

theorem cert_bound (w0 : L) (hlo : 12 ≤ S.N w0) (hhi : S.N w0 ≤ 20) (hip : SmallIP S w0) (y : L) :
    12 ≤ S.N (w0 + 2 • y) := by
  obtain ⟨e1, e2⟩ := midpoints S w0 y
  have ey := S.even y
  have ewy := S.even (w0 + y)
  have ew := S.even (w0 + 2 • y)
  by_contra hlt
  have hy : y ≠ 0 := by
    rintro rfl; simp at hlt; omega
  have hwy : w0 + y ≠ 0 := by
    intro h
    have : w0 + 2 • y = -w0 := by
      rw [two_nsmul, ← add_assoc, h, zero_add]; exact (eq_neg_of_add_eq_zero_right h)
    rw [this, N_neg] at hlt; omega
  have m1 := S.min6 y hy
  have m2 := S.min6 (w0 + y) hwy
  unfold N at *
  by_cases c1 : S.B y y = 6
  · have := hip (-y) (by unfold N; rw [B_neg_left, B_neg_right, neg_neg]; exact c1)
    rw [B_neg_right] at this
    omega
  · by_cases c2 : S.B (w0 + y) (w0 + y) = 6
    · have h2 := hip (w0 + y) c2
      rw [B_add_right] at h2
      omega
    · omega

theorem odd_bound (w0 : L) (hN : S.N w0 = 14 ∨ S.N w0 = 18) (hip : SmallIP S w0) (y : L) :
    14 ≤ S.N (w0 + 2 • y) := by
  have := cert_bound S w0 (by omega) (by omega) hip y
  have := coset_norm_mod4 S w0 y
  omega

end Bounding

/-! ## Réduction par symétrie et théorème final à partir des faits calculés -/

section Reduction

variable {L L' : Type*} [AddCommGroup L] [AddCommGroup L']

/-- Les faits calculés pour X1. `Sym` : des paires `(g, g')` (l'action d'un même élément de SL₂(29) sur `L` et
sur `L'`), isométries, compatibles avec `φ` et `ψ` modulo 2. `reps6`, `reps6'`, `reps8` : représentants des
orbites (F2 pour `L` et `L'`, F3 pour `L`). `bound6`, `bound6'` : certificats impairs (F5a des deux côtés).
`nocoll8` : F5b par formes canoniques (côté `L`). -/
structure Data (Gl : Glue L L') where
  Sym : Set ((L ≃+ L) × (L' ≃+ L'))
  reps6 : Set L
  reps6' : Set L'
  reps8 : Set L
  iso : ∀ p ∈ Sym, ∀ a b, Gl.A.B (p.1 a) (p.1 b) = Gl.A.B a b
  iso' : ∀ p ∈ Sym, ∀ a b, Gl.A'.B (p.2 a) (p.2 b) = Gl.A'.B a b
  equiv_φ : ∀ p ∈ Sym, ∀ a, ∃ z, Gl.φ (p.1 a) = p.2 (Gl.φ a) + 2 • z
  equiv_ψ : ∀ p ∈ Sym, ∀ a, ∃ z, Gl.ψ (p.2 a) = p.1 (Gl.ψ a) + 2 • z
  cover6 : ∀ x, Gl.A.N x = 6 → ∃ p ∈ Sym, ∃ r ∈ reps6, x = p.1 r
  cover6' : ∀ x, Gl.A'.N x = 6 → ∃ p ∈ Sym, ∃ r ∈ reps6', x = p.2 r
  cover8 : ∀ x, Gl.A.N x = 8 → ∃ p ∈ Sym, ∃ r ∈ reps8, x = p.1 r
  bound6 : ∀ r ∈ reps6, ∃ w0 y0, w0 = Gl.φ r + 2 • y0 ∧ (Gl.A'.N w0 = 14 ∨ Gl.A'.N w0 = 18) ∧
    SmallIP Gl.A' w0
  bound6' : ∀ r ∈ reps6', ∃ w0 y0, w0 = Gl.ψ r + 2 • y0 ∧ (Gl.A.N w0 = 14 ∨ Gl.A.N w0 = 18) ∧
    SmallIP Gl.A w0
  nocoll8 : ∀ r ∈ reps8, ∀ y, Gl.A'.N (Gl.φ r + 2 • y) ≠ 8

variable {Gl : Glue L L'}

open Lat

/-- Transport côté `L` : une propriété de toutes les normes de la classe `φ r + 2L'` passe à la classe
`φ (g r) + 2L'`. -/
theorem pred_transport (D : Data Gl) (P : ℤ → Prop) (p : (L ≃+ L) × (L' ≃+ L')) (hp : p ∈ D.Sym) (r : L)
    (hr : ∀ y, P (Gl.A'.N (Gl.φ r + 2 • y))) (y : L') : P (Gl.A'.N (Gl.φ (p.1 r) + 2 • y)) := by
  obtain ⟨z, hz⟩ := D.equiv_φ p hp r
  have : Gl.φ (p.1 r) + 2 • y = p.2 (Gl.φ r + 2 • p.2.symm (z + y)) := by
    rw [hz, map_add, map_nsmul, AddEquiv.apply_symm_apply, nsmul_add]; abel
  rw [this]
  have := hr (p.2.symm (z + y))
  unfold Lat.N at this ⊢
  rwa [D.iso' p hp]

/-- Transport côté `L'` : de la classe `ψ r' + 2L` à la classe `ψ (g' r') + 2L`. -/
theorem pred_transport' (D : Data Gl) (P : ℤ → Prop) (p : (L ≃+ L) × (L' ≃+ L')) (hp : p ∈ D.Sym) (r : L')
    (hr : ∀ y, P (Gl.A.N (Gl.ψ r + 2 • y))) (y : L) : P (Gl.A.N (Gl.ψ (p.2 r) + 2 • y)) := by
  obtain ⟨z, hz⟩ := D.equiv_ψ p hp r
  have : Gl.ψ (p.2 r) + 2 • y = p.1 (Gl.ψ r + 2 • p.1.symm (z + y)) := by
    rw [hz, map_add, map_nsmul, AddEquiv.apply_symm_apply, nsmul_add]; abel
  rw [this]
  have := hr (p.1.symm (z + y))
  unfold Lat.N at this ⊢
  rwa [D.iso p hp]

theorem bound_of_rep {M : Type*} [AddCommGroup M] (S : Lat M) (c0 w0 y0 : M) (hw : w0 = c0 + 2 • y0) (c : ℤ)
    (hb : ∀ y, c ≤ S.N (w0 + 2 • y)) (y : M) : c ≤ S.N (c0 + 2 • y) := by
  have : c0 + 2 • y = w0 + 2 • (y - y0) := by rw [hw]; abel
  rw [this]; exact hb _

/-- Types (6,6), (6,10) : toute classe `φ r + 2L'` d'un vecteur minimal `r` de `L` a un minimum ≥ 14. -/
theorem odd_cosets_bound (D : Data Gl) (r : L) (y : L') (hr : Gl.A.N r = 6) :
    14 ≤ Gl.A'.N (Gl.φ r + 2 • y) := by
  obtain ⟨p, hp, r0, hr0, rfl⟩ := D.cover6 r hr
  obtain ⟨w0, y0, hw, hN, hip⟩ := D.bound6 r0 hr0
  exact pred_transport D (fun n => 14 ≤ n) p hp r0
    (bound_of_rep Gl.A' (Gl.φ r0) w0 y0 hw 14 (odd_bound Gl.A' w0 hN hip)) y

/-- Type (10,6) : toute classe `ψ r' + 2L` d'un vecteur minimal `r'` de `L'` a un minimum ≥ 14. -/
theorem odd_cosets_bound' (D : Data Gl) (r : L') (y : L) (hr : Gl.A'.N r = 6) :
    14 ≤ Gl.A.N (Gl.ψ r + 2 • y) := by
  obtain ⟨p, hp, r0, hr0, rfl⟩ := D.cover6' r hr
  obtain ⟨w0, y0, hw, hN, hip⟩ := D.bound6' r0 hr0
  exact pred_transport' D (fun n => 14 ≤ n) p hp r0
    (bound_of_rep Gl.A (Gl.ψ r0) w0 y0 hw 14 (odd_bound Gl.A w0 hN hip)) y

/-- **Théorème (partie logique), pour X1** : sous F1 (pour `L` et `L'`) et les faits calculés `Data`,
si `(x, φ x + 2 y) ≠ 0` alors `N x + N' (φ x + 2 y) ≥ 20`, c'est-à-dire : le recollement n'a pas de vecteur
de norme < 10. -/
theorem theoremX1 (D : Data Gl) (x : L) (y : L') (hz : x ≠ 0 ∨ Gl.φ x + 2 • y ≠ 0) :
    20 ≤ Gl.A.N x + Gl.A'.N (Gl.φ x + 2 • y) := by
  apply no_inner_shell_ne8 Gl (odd_cosets_bound D) (odd_cosets_bound' D) _ x y hz
  intro x y hx
  obtain ⟨p, hp, r0, hr0, rfl⟩ := D.cover8 x hx
  exact pred_transport D (fun n => n ≠ 8) p hp r0 (D.nocoll8 r0 hr0) y

end Reduction

end EEUL.X1

#print axioms EEUL.X1.no_inner_shell_ne8
#print axioms EEUL.X1.cert_bound
#print axioms EEUL.X1.odd_bound
#print axioms EEUL.X1.pred_transport
#print axioms EEUL.X1.pred_transport'
#print axioms EEUL.X1.odd_cosets_bound
#print axioms EEUL.X1.odd_cosets_bound'
#print axioms EEUL.X1.theoremX1
