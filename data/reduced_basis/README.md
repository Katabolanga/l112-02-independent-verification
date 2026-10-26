# A reduced basis for L112.02

Row convention: a vector is a row x, its norm is x·G·xᵀ, and an isometry g satisfies g·G·gᵀ = G.

| file | contents |
|---|---|
| `X1_gram.txt` | the Gram matrix GRAM of L112.02 in the reduced basis (112 full rows) |
| `X1_gram_gap_magma.txt` | the same matrix as a list of lists (GAP and Magma syntax) |
| `X1_passage_from_roiban.txt` | P (112 × 112, integer, det ±1): the rows are the reduced basis written in the basis of roiban1344's Gram matrix; GRAM = P·G·Pᵀ, where G is `lattices/L112.02/gram.txt` (identical, entry by entry, to `certificates/genus_class_1.txt`) |
| `X1_generators.txt` | s29, s4, c2, c6 and T in the reduced basis (g·GRAM·gᵀ = GRAM) |
| `X1_generators_gap.txt` | the same generators in GAP syntax |
| `L112.02_reduced.std` | the same Gram matrix and generators in the format of the entries of the Catalogue of Lattices (G. Nebe and N. J. A. Sloane), with references and notes |
| `verify_X1.py` | exact checks of `L112.02_reduced.std` (Python 3, standard library; NumPy only for `--orbit`) |

Properties (recounted by `code/reduced_basis/compute_reduced_basis_figures.py`; logs in `logs/machine_A/reduced_basis_check_20261026/`):

- GRAM is even, has determinant 1 and is positive definite (exact checks in `verify_X1.py`);
- diagonal entries between 10 and 38; seven basis vectors have norm 10; off-diagonal entries of absolute value at most 15;
- the generators have entries of absolute value at most 185 in this basis, and up to 2 252 in the basis of `lattices/L112.02/gram.txt` (diagonal entries between 62 and 180);
- s29 and s4 (orders 29 and 4, s4² = −1) generate a group isomorphic to SL₂(29); c2 and c6 (orders 2 and 6) commute with it and generate C₂ × C₆; T (order 60) normalizes it (two relations, checked by `verify_X1.py`) and induces an outer automorphism of it (checked with GAP); the five generators generate a group of order 292 320 = 2⁵·3²·5·7·29 (computed with GAP; `verify_X1.py --orbit` checks an orbit of length 292 320, which bounds the order from below).

This group is a **known subgroup** of Aut(L112.02); whether it is the full automorphism group is **not** claimed. `verify_X1.py` does **not** check the minimum; the line KISSING_NUMBER of `L112.02_reduced.std` is the coefficient of q⁵ of the extremal theta series of weight 56, which counts the vectors of norm 10 once the minimum 10 is known.

The basis was obtained from roiban1344's Gram matrix by BKZ (fpylll, block sizes up to 52, best result at 48) and a weighted Seysen reduction with insertion of norm-10 vectors (objective 1000·Σ|bᵢ|² + Σ|bᵢ^#|², where b^# is the dual basis); the programs are in `code/reduced_basis/`. The norm-10 vectors inserted come from the gluing: BKZ alone found none.

Check (about one minute):

```bash
bash data/roiban/fetch_roiban_data.sh       # provides data/frozen/roiban_sl2_29/lattices/L112.02/gram.txt
python3 data/reduced_basis/verify_X1.py data/reduced_basis/L112.02_reduced.std \
  --passage data/reduced_basis/X1_passage_from_roiban.txt data/frozen/roiban_sl2_29/lattices/L112.02/gram.txt --orbit
```

Expected last line: `ALL CHECKS PASSED`.

`L112.02_reduced.std` is derived from a draft catalogue entry prepared on 26 October 2026: its sections GRAM, SUBGROUP_ORDER, SUBGROUP_NAME and SUBGROUP_GENERATORS and the two RELATION lines are unchanged; NAME, REFERENCES and NOTES were rewritten for this repository. These data are derived from roiban1344's Gram matrix (CC BY 4.0) by the integer change of basis P; licence CC BY 4.0, `verify_X1.py` under MIT.
