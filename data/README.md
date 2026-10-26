# Data

All matrices use the row convention of roiban1344's repository: a vector is a row of coordinates x, its norm is x·G·xᵀ, and an isometry g satisfies g·G·gᵀ = G. The SHA-256 of every file is in `SHA256SUMS.txt` at the root of the repository. Licence: CC BY 4.0 (`LICENSE-CC-BY-4.0`). These data are derived from roiban1344's data (CC BY 4.0), as described below; the changes are ours.

## `frozen/`: the inputs of the verifiers

These are the files that were frozen before the two runs of Section 3 of the main README and read, unchanged, on both machines. In the names, X1 is L112.02, L is L₅₆,₂(𝔐), L56 is roiban1344's 56-dimensional lattice, and X4 is the class of the same genus used as a positive control.

| file | contents | produced by (in `code/production/`) |
|---|---|---|
| `F1/L_bkz40_rayon4.entree` | input of `enum_interval` for L: Gram matrix of a BKZ-40 reduced basis of L, with the interval data | `reduction_L.py` |
| `F1/reduction_L_bkz40.npz` | `U` (56×56, det −1) and `Gr` = U·G_L·Uᵀ | `reduction_L.py` |
| `F1/L56.entree` | input of `enum_interval` for L56, built from roiban1344's `L56_gram.txt` and `reduction_L.txt` | `rejeu_roiban/v1_entrees_manuel.py` |
| `F1/E8.entree`, `F1/leech.entree`, `F1/leech2_e8.entree` | roiban1344's three control inputs of `enum_interval` (same construction) | `rejeu_roiban/v1_entrees_manuel.py` |
| `X1/structure_x1.npz` | `G_L` (Gram matrix of L), `f` (the gluing map modulo 2), `h1`, `h2` (the action of the two generators of S on L), `Y1c`, `Y2c` (the two sublattices in the coordinates of the published Gram matrix), and the Hermitian data `mu`, `Lambda_num`, `Lambda_den`, `T_num`, `T_den` | `structure_x1.py` (SageMath), from `genus_class_1.txt` |
| `X1/donnees_L.npz` | `S` (the elements of S acting on L, up to sign: 12 180 matrices, int16), `commutant` (a ℤ-basis of End_S(L), of rank 8), `units` (the 12 elements of C_L/{±1}, where C_L is the centralizer of S in Aut(L)) | `donnees_L.py` |
| `X1/min_reps_L.npz` | `reps`: 656 representatives of the S-orbits of minimal vectors of L | `orbites_min_L.py` (roiban1344's generic program, run on L) |
| `X1/norm8_reps_L.npz` | `reps`, `sizes`: 127 413 representatives of the orbits of S·C_L on the norm-8 vectors of L, with their sizes; with the 12 elements of C_L/{±1} they give the 1 528 956 pairs (127 413 × 12) | `orbites8_L.py` (roiban1344's generic program, run on L) |
| `X1/certificats_X1/certificats_phi_L_vers_L56.npz` | `w0`, `norms`, `maxip`: the 656 certificates of the φ direction (types (6,6) and (6,10)) | `certificats_impairs_x1.py` |
| `X1/certificats_X1/certificats_psi_L56_vers_L.npz` | the 656 certificates of the ψ direction (type (10,6)) | `certificats_impairs_x1.py` |
| `X4/…` | the same files for the positive control X4 (roiban1344's `certificates/genus_class_4.txt`) | `structure_classe.py` (class 4), `isometrie_L4_L1.py`, `transporter_L4.py`, `certificats_impairs.py` (class 4) |

The SHA-256 of these files when they were frozen, and the place where each was produced on machine A, were recorded before the replication; the copies here are byte-identical (compare `SHA256SUMS.txt` with `logs/machine_B/run_20261026/MANIFESTE_COPIE_FIGEE.sha256`).

Largest files: `X4/donnees_L4.npz` (27 126 660 bytes) and `X1/donnees_L.npz` (25 550 538 bytes); no file exceeds 50 MB.

## `roiban/`: public files of roiban1344 (not redistributed)

The verifiers also read six public files of roiban1344, and the check of the reduced basis reads `lattices/L112.02/gram.txt`. They are not copied into this repository. `roiban/ROIBAN_FILES.tsv` gives, for each of them, the repository, the commit or release, the path and the SHA-256; `roiban/fetch_roiban_data.sh` downloads them into `frozen/roiban_112/` and `frozen/roiban_sl2_29/` and checks their SHA-256 (about 14 MB).

| file | source |
|---|---|
| `data/L56_gram.txt`, `data/sl2_29_generators.txt`, `certificates/reduction_L.txt`, `certificates/genus_class_1.txt` | roiban1344/112-dimensional-extremal-even-unimodular-lattice, commit `3db9dac5ac13de4c90109bbdc4176b7b7a0a4ca1` |
| `certificates/centralizer.npz`, `certificates/min_reps.npz`, `certificates/norm8_reps.npz` | the same repository, release `certificates-v2` |
| `lattices/L112.02/gram.txt` | roiban1344/sl-2-29-rank-112-extremal-lattice, commit `d868927ada7bfbbcc0d6fad88cb8a25c75de9155` |

## `reduced_basis/`

The reduced basis of L112.02 and the generators of its known subgroup of order 292 320; see `reduced_basis/README.md`.
