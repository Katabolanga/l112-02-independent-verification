# Independent verification of min(L112.02) = 10

This repository contains a computer-assisted verification that the even unimodular lattice **L112.02** of dimension 112, published by roiban1344, has minimum norm **10**, and is therefore extremal. The lattice, its announcement as extremal, the method and the code on which this work is based are due to roiban1344. What is added here is an independent check of the minimum: the data, the programs, the logs of two runs on two different machines, and a Lean file for the final deduction.

Status: computer-assisted, not peer-reviewed. Before publication, the chain of arguments, the corrected scripts and the replication were reviewed and accepted within our team; this is not an external review.

## 1. The lattice

L112.02 is defined by the Gram matrix `lattices/L112.02/gram.txt` of the repository [roiban1344/sl-2-29-rank-112-extremal-lattice](https://github.com/roiban1344/sl-2-29-rank-112-extremal-lattice), commit `d868927ada7bfbbcc0d6fad88cb8a25c75de9155` (SHA-256 of the file: `7751107bf646e1bb55c5a7ad41a1c21e6f38a842d857e96107db62d93785d4ea`). That repository announces L112.02 as extremal; at the time of writing it does not include a proof for it.

This Gram matrix is identical, entry by entry, to `certificates/genus_class_1.txt` of [roiban1344/112-dimensional-extremal-even-unimodular-lattice](https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice) (commit `3db9dac5ac13de4c90109bbdc4176b7b7a0a4ca1`), the class X₁ of Theorem S6.1 of the Supplement of roiban1344's paper, whose minimum that paper leaves open. In our files and logs this lattice is called **X1**.

## 2. What is verified

The method is roiban1344's (paper, Sections 4 to 6, and his verification programs), extended from the gluing of two copies of one 56-dimensional lattice to the gluing of two **different** 56-dimensional lattices. The lattice contains √2·L ⊥ √2·L56 with index 2⁵⁶ and is the gluing

  X1 = { (x, v)/√2 : x ∈ L, v ∈ L56, v ≡ x·f (mod 2) },

where L = L₅₆,₂(𝔐) and L56 ≅ L₅₆,₂(M̃) are, up to isometry, the two SL₂(29)-invariant even unimodular lattices of dimension 56 that G. Nebe attached to the two conjugacy classes of maximal orders [Neb98]; L56 is the lattice of roiban1344's paper. A group S ≅ SL₂(29) acts on both blocks, and f is an S-equivariant bijection L/2L → L56/2L56. The decomposition, the Gram matrix of L and the map f were computed from the published Gram matrix (`code/production/structure_x1.py`).

A nonzero vector (x, v)/√2 of norm less than 10 would satisfy N(x) + N(v) < 20. If one component is zero, the other lies in twice a lattice of minimum 6, and the norm is at least 12. Since both blocks have minimum 6 and N(x) + N(v) ≡ 0 (mod 4), only four types (N(x), N(v)) remain: **(6,6), (6,10), (10,6) and (8,8)**. Each of them is excluded:

| fact | how it is checked | result |
|---|---|---|
| min L = 6 and min L56 = 6 (F1) | roiban1344's enumerator in interval arithmetic `enum_interval.c`, on inputs whose exact correspondence with the two Gram matrices is checked (U·G·Uᵀ with \|det U\| = 1, 1 596 exact intervals on each side) | L: 9 905 828 434 nodes, one leaf (the zero vector); L56: 8 454 837 756 nodes, one leaf; 0 untabulated vectors; exit code 0 |
| parity of the gluing | D = G_L − f·G·fᵀ in exact integers | 56 diagonal entries ≡ 0 (mod 4), 1 540 off-diagonal entries ≡ 0 (mod 2) |
| theta coefficients of an extremal lattice of dimension 56 | PARI/GP, exact | \|L₆\| = 15 590 400, \|L₈\| = 36 957 286 800 |
| types (6,6) and (6,10), direction φ | 656 certificates, one per S-orbit of minimal vectors of L: each coset φ(r) + 2·L56 has minimum at least 14 | 656 valid certificates, norms in {14, 18}, each in the coset of its representative; max \|⟨w₀, u⟩\| = 6 over the 7 795 200 minimal vectors u of L56 up to sign (\|L₆\| = 15 590 400) |
| type (10,6), direction ψ (ψ lifts f⁻¹) | 656 certificates in the other direction: each coset ψ(r′) + 2·L has minimum at least 14 | 656 valid certificates, norms in {14, 18}; max \|⟨w₀, u⟩\| ≤ 6 over the 7 795 200 minimal vectors u of L up to sign |
| coverage of the norm-8 vectors | orbit representatives under S | L: 1 528 956 pairs (representative, element of the centralizer of S), giving 1 517 130 distinct regular S-orbits whose sizes add up to \|L₈\|; L56: 1 527 984 pairs, 1 517 130 regular orbits, sizes adding up to \|L₈\| |
| type (8,8) | canonical forms modulo 2 (in a lattice of minimum ≥ 6, two vectors of norm 6 or 8 that are congruent modulo 2 are equal up to sign; roiban1344, Proposition 6.3): no class x·f + 2·L56, x of norm 8 in L, contains a vector of norm 8 | **0 hits on the 1 528 956 pairs** |
| positive control | the same programs on another lattice of roiban1344's classification (`certificates/genus_class_4.txt`, our X4), which contains vectors of norm 8 | 20 colliding pairs of type (8,8), 14 orbits, 682 080 vectors of norm 8 found |
| second implementation | C and Python written without roiban1344's library, sharing only the input files; it recomputes the groups, both coverages, the (8,8) test and the certificates in both directions | same results: 0 hits for X1, the collisions above for X4 |
| final deduction | `lean/ChainX1.lean` (Lean 4, Mathlib), adapted from roiban1344's `lean/EEUL/L112/Chain.lean`; the computed facts are hypotheses | compiled with Lean 4.32.0 and Mathlib v4.32.0; axioms: propext, Classical.choice, Quot.sound |

With the classical bound 2⌊112/24⌋ + 2 = 10 for an even unimodular lattice of dimension 112, these facts give min(L112.02) = 10.

A first run of the second implementation reported two failures on the φ side; they came from an `int8` storage of coordinates (largest coordinate 135). With `int16` storage and an exact `int64` re-check of the φ side, all checks pass; only the corrected versions were used in the runs of Section 3.

## 3. Replication on a second machine

The verifiers (not the production of the data) were run twice, on two different computers, from the same frozen data:

- **machine A** (Windows 11 with WSL2, Ubuntu 24.04; GCC 13.3.0, Python 3.11 with NumPy 2.4.6, PARI/GP 2.17.2), 25 and 26 October 2026;
- **machine B** (Linux 7.0, Ubuntu 24.04; GCC 13.3.0, Python 3.12 with NumPy 2.5.3, PARI/GP 2.17.3), 26 October 2026, from 18:02 to 19:47 UTC, one CPU core, memory limited to 6 GiB.

On machine B, a single launcher recompiled the C programs, ran twelve steps in series and applied a verdict rule fixed in advance. Result: **"REPLICATION X1 CONFORME (23 conditions sur 23 PASS)"**; the twelve steps, the global run and the verdict have exit code 0 (14 exit codes, all 0); peak memory 3 807 326 208 bytes, no swap. The recompiled `enum_interval` binary has the same SHA-256 on both machines, and the outputs of F1 and the result lines of the three long checks are identical on both machines (timestamps removed).

| step | machine A | machine B |
|---|---|---|
| F1 for L (`enum_interval`) | 16 min 56 s | 810 s |
| F1 for L56 | 23 min 05 s | 687 s |
| φ side in exact `int64` arithmetic | 2 min 32 s | 137 s |
| second implementation, X1 | 58 min 12 s | 2 314 s |
| second implementation, X4 (positive control) | 51 min 34 s | 2 361 s |
| compilations, controls, gluing checks, parity, theta | a few seconds | 2 s |

The complete raw output of machine B is an archive of 301 910 607 bytes (364 members, SHA-256 `e91636b90b26ba077ea684cd332280df71e152be04fddb35f8006bb0b327f617`); it is not included. `logs/` contains sanitized copies of the relevant members, with the SHA-256 of each original (`logs/SANITIZATION.md`).

## 4. What is not claimed

- No new lattice: L112.02 and its announcement as extremal are roiban1344's.
- No determination of the full automorphism group: only a known subgroup of order 292 320 is given (Section 5).
- No statement of non-isometry beyond what roiban1344 establishes.
- The Lean file checks only the deduction from the computed facts, which enter as hypotheses; it was compiled with Lean 4.32.0 and Mathlib v4.32.0 only. The computations themselves are not formally verified.
- Nothing is claimed about the other lattices of roiban1344's collection.

## 5. A reduced basis for L112.02

In the basis of the published Gram matrix, whose diagonal entries lie between 62 and 180, the generators of the known subgroup of automorphisms described below have entries up to 2 252. We provide a reduced basis, obtained by BKZ with block size 48 (fpylll) followed by a weighted Seysen reduction. Its Gram matrix has diagonal entries between 10 and 38, seven of its basis vectors have norm 10, and its off-diagonal entries have absolute value at most 15. The same generators have entries at most 185 in this basis. The unimodular change of basis to `lattices/L112.02/gram.txt` is included and checked by `verify_X1.py`. We hope this smaller presentation will be convenient for further computations, and for a possible entry of L112.02 in the catalogue of lattices maintained by Gabriele Nebe.

The generators s29 and s4 generate a group isomorphic to SL₂(29); c2 and c6 commute with it and generate C₂ × C₆; T normalizes it and induces an outer automorphism. Together they generate a group of order 292 320 = 2⁵·3²·5·7·29, that is SL₂(29)∘(C₂ × C₆) extended by an outer automorphism. **This is a known subgroup of Aut(L112.02); whether it is the full automorphism group is not claimed.** Files: `data/reduced_basis/` (see its README).

## 6. Contents

| path | contents |
|---|---|
| `data/frozen/` | the frozen data read by the verifiers (our files only; about 62 MB) |
| `data/roiban/` | the list of the public files of roiban1344 that are used (URL, commit or release, SHA-256) and `fetch_roiban_data.sh`, which downloads and checks them; they are not redistributed here |
| `data/reduced_basis/` | the reduced basis of Section 5, the change of basis, the generators and `verify_X1.py` |
| `code/verification/` | the verifiers that were run on both machines |
| `code/replication/` | the launcher and the verdict rule used on machine B, and `assemble_package.sh` |
| `code/production/` | the programs that produced the frozen data on machine A (they need SageMath and roiban1344's library; not needed to check the result) |
| `code/reduced_basis/` | the programs that produced the reduced basis and its subgroup, and the script that recounts the figures of Section 5 |
| `lean/` | `ChainX1.lean`, its compilation and axiom logs |
| `logs/` | sanitized logs of machine A and machine B, and `SANITIZATION.md` |

Most scripts and logs are in French, as they were written during the work. `SHA256SUMS.txt` gives the SHA-256 of every file of the repository.

## 7. How to reproduce

Requirements: Linux or WSL2 with bash, coreutils, awk and curl; GCC (C11, 128-bit integers); Python 3.10 or later with NumPy for the long checks; PARI/GP; at least 10 GiB of available memory for the launcher as configured (the peak was 3.8 GB); about two hours on one core.

```bash
sha256sum -c SHA256SUMS.txt                     # integrity of this repository
bash data/roiban/fetch_roiban_data.sh           # public files of roiban1344 (about 14 MB), checked by SHA-256
bash code/replication/assemble_package.sh ../l112_run
cd ../l112_run
PY=/usr/bin/python3 PYN=/path/to/python3-with-numpy GP=/path/to/gp CC=/usr/bin/gcc \
  bash lanceurs/lancer_x1_rep_v2.sh RUN_1
cat RUN_1/VERDICT_X1_REP_V2.txt                  # expected last line: VERDICT GLOBAL : REPLICATION X1 CONFORME (23 conditions sur 23 PASS)
```

Set PY, PYN, GP and CC explicitly: the default paths written in the launcher are those of machine B and are masked in this copy. The launcher refuses to start if less than 10 GiB of memory is available (variable `R96_MEM_ADMISSION_KIO`, in KiB). Its exit code is 0 only if the verdict is conforming. The twelve steps and their commands are listed in the header and at the end of `code/replication/lancer_x1_rep_v2.sh`; their durations on both machines are in the table of Section 3.

Reduced basis (about one minute, standard library and NumPy for `--orbit`):

```bash
python3 data/reduced_basis/verify_X1.py data/reduced_basis/L112.02_reduced.std \
  --passage data/reduced_basis/X1_passage_from_roiban.txt data/frozen/roiban_sl2_29/lattices/L112.02/gram.txt --orbit
```

Lean: compile `lean/ChainX1.lean` with `lake env lean` inside a project that uses Lean 4.32.0 and Mathlib v4.32.0 (about 20 seconds on machine A); see `lean/README.md`.

## 8. Credits and acknowledgements

- **roiban1344**: the lattice L112.02 and its announcement as extremal; the method (gluing modulo 2, odd-coset certificates, canonical forms modulo 2, enumeration in interval arithmetic); the code from which parts of ours are derived (MIT licence); the data that we use (CC BY 4.0).
- **G. Nebe**: the lattices L₅₆,₂(𝔐) and L₅₆,₂(M̃) [Neb98].

We thank Gabriele Nebe for pointing us to roiban1344's repository. The 56-dimensional lattice L₅₆,₂(𝔐) used in the gluing is from G. Nebe, Some cyclo-quaternionic lattices, J. Algebra 199 (1998) 472–498.

## 9. Author

Ivan Gauvin. AI assistants were used for the computations, the code and the writing; I remain responsible for every statement.

## 10. Licences

- Code (`code/`, `lean/`, `data/roiban/fetch_roiban_data.sh`, `data/reduced_basis/verify_X1.py`, the shell and Python scripts): MIT licence, `LICENSE`. Files derived from roiban1344's code keep his copyright notice and MIT licence: see `THIRD_PARTY_NOTICES.md`.
- Texts, data and logs: CC BY 4.0, `LICENSE-CC-BY-4.0`. The reduced basis and the frozen data are derived from roiban1344's data (CC BY 4.0) as described in `data/README.md` and `THIRD_PARTY_NOTICES.md`.

## 11. References

- [Neb98] G. Nebe, Some cyclo-quaternionic lattices, J. Algebra 199 (1998) 472–498.
- roiban1344, An extremal even unimodular lattice in dimension 112, draft (2026), with supplement, code and data: https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice (commit `3db9dac5ac13de4c90109bbdc4176b7b7a0a4ca1`; release `certificates-v2` for the large data files).
- roiban1344, rank-112 lattices with an action of SL₂(29): https://github.com/roiban1344/sl-2-29-rank-112-extremal-lattice (commit `d868927ada7bfbbcc0d6fad88cb8a25c75de9155`).
- G. Nebe and N. J. A. Sloane, A catalogue of lattices: https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/

To cite this repository, see `CITATION.cff`.
