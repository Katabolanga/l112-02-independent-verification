# Code

Licence: MIT (`LICENSE`), except that the parts copied, ported or adapted from roiban1344's code keep his copyright notice (`THIRD_PARTY_NOTICES.md`). Comments and messages are mostly in French. The header of each file states what it does, how it is called, and what it takes from roiban1344's repository.

## `verification/`: the verifiers run on both machines

| file | step | role |
|---|---|---|
| `enum_interval.c` | B01, B03, F01, F02 | roiban1344's enumerator in interval arithmetic (verbatim copy of `code/verify/enum_interval.c`), compiled with `gcc -O2 -std=c11 -fno-fast-math -ffp-contract=off … -lm` |
| `raccord_entrees_f1_rep_v1.py` | R01 | exact check that the two inputs of `enum_interval` correspond to the Gram matrices of L and L56 (U·G·Uᵀ, \|det U\| = 1, the 1 596 intervals contain the exact LDL values, D > 0); standard library |
| `parite_x1_rep_v1.py` | R02 | parity of the gluing (D = G_L − f·G·fᵀ: 56 + 1 540 congruences); standard library |
| `theta_extremale_56.gp` | R03 | extremal theta series of dimension 56 (PARI/GP, exact): \|L₆\| and \|L₈\| |
| `verif_phi_L56_int64_v3.py` | V01 | φ side (types (6,6) and (6,10)) in exact `int64` arithmetic: 7 checks, including the coset of each certificate |
| `formes_canoniques.c` | V02, V03 | canonical forms modulo 2, used by the second implementation |
| `verif_independante_int16_v3.py` | V02, V03 | the second implementation (written without roiban1344's library): groups, coverages of norms 6 and 8 on both sides, type (8,8), certificates in both directions; rule J = 1 (X1: 0 hits required) or J = 4 (X4: hits required) |
| `verdict_x1_v3_POUR_MEMOIRE.py` | — | the verdict rule applied on machine A to the outputs of 25 and 26 October (kept for reference; it reads machine A's historical outputs) |

## `replication/`

| file | role |
|---|---|
| `lancer_x1_rep_v2.sh` | the launcher run on machine B: frozen copy checked by SHA-256, twelve blocking steps in series with exit codes captured, time budget, memory limit, one thread, then the verdict |
| `verdict_x1_rep_v2.py` | the verdict rule fixed before the run (23 conditions; standard library; reads only the outputs of the run) |
| `assemble_package.sh` | builds, from this repository, a package with the layout expected by the launcher (see the main README, Section 7) |

The launcher and the verdict are copies of the files that were run, with local paths and names masked (`logs/SANITIZATION.md` gives the SHA-256 of the files that were run). In particular the directory of reference outputs, called after machine A, is named `REFERENCE_MACHINE_A` here; `assemble_package.sh` creates it from `logs/machine_A/reference_for_replication/`.

## `production/`: how the frozen data were produced (machine A)

These programs produced `data/frozen/` on 25 October 2026. They need SageMath and a copy of roiban1344's repository (several of them call his library), and they are not needed to check the result: everything they produced is re-checked by the verifiers above. They include the first implementation of the checks (`certificats_impairs_x1.py`, `collisions8_x1.py`), the replay of roiban1344's own verification (`rejeu_roiban/`), and the first runs of the second implementation (`second_implementation_first_runs/`, including the version with the `int8` storage defect described in the main README). `collisions8_x1_v3.py` differs from `collisions8_x1.py` only by a corrected comment (1 528 956 pairs); `raccord_f1.py` and `verdict_x1_v3.py` are the scripts of the consolidated chain on machine A.

## `reduced_basis/`

The programs that produced the reduced basis and its subgroup of order 292 320 (BKZ with fpylll, weighted Seysen reduction, reservoir of norm-10 vectors, group computations, export), `theta_extremale_112.gp` (theta series of an extremal lattice of dimension 112), and `compute_reduced_basis_figures.py`, which recounts the figures quoted in the README (standard library).
