# Lean

`ChainX1.lean` formalizes the deduction "computed facts ⟹ no vector of norm below 10" for a gluing modulo 2 of **two different** lattices. It is an adaptation of `lean/EEUL/L112/Chain.lean` of roiban1344's repository (MIT licence, see `THIRD_PARTY_NOTICES.md`), which treats the gluing of two copies of one lattice.

Main statement (namespace `EEUL.X1`):

```lean
theorem theoremX1 (D : Data Gl) (x : L) (y : L') (hz : x ≠ 0 ∨ Gl.φ x + 2 • y ≠ 0) :
    20 ≤ Gl.A.N x + Gl.A'.N (Gl.φ x + 2 • y)
```

that is, every nonzero vector (x, φ(x) + 2y)/√2 of the gluing has norm at least 10. The computed facts are **hypotheses**: they are the fields of the structures `Lat` (bilinear form, symmetry, evenness, minimum 6, for each of the two lattices), `Glue` (φ, ψ, χ with ψ∘φ = id + 2χ, parity) and `Data` (the pairs of isometries, the orbit representatives of norms 6 and 8, the coverage statements, the certificate bounds in both directions and the absence of (8,8) collisions). Lean does not execute the lattice computations: their correspondence with these hypotheses is given by the verifiers and the logs. As in roiban1344's work, the following stay outside Lean: the identification of L112.02 with this gluing, unimodularity and positivity, the theta series, the bound min ≤ 10, and the proposition on canonical forms modulo 2.

| file | contents |
|---|---|
| `ChainX1.lean` | the formalization |
| `ChainX1_avec_axiomes.lean` | the same file followed by `#print axioms` commands |
| `ChainX1_compilation_4_32.log` | compilation with Lean 4.32.0 and Mathlib v4.32.0 on machine A, 25 October 2026: exit code 0, 18 seconds |
| `ChainX1_axiomes_4_32.log` | axioms used: `propext`, `Classical.choice`, `Quot.sound` (theoremX1); no `sorry` |
| `compiler_lean.sh` | the command used: `lake env lean FILE` inside a project pinned to Lean 4.32.0 and Mathlib v4.32.0, without network access |

Only Lean 4.32.0 with Mathlib v4.32.0 was used.
