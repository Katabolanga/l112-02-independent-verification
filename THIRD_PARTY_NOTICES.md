# Third-party material

## Code of roiban1344 (MIT licence)

Some files of this repository contain code copied, ported or adapted from https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice (commit `3db9dac5ac13de4c90109bbdc4176b7b7a0a4ca1`). The header of each file states what it takes from that repository. In particular:

- `code/verification/enum_interval.c` is a verbatim copy of `code/verify/enum_interval.c` (SHA-256 `80d0ffcacd79863ac6fb55c4afa2ed3df1251339691209bf73f91a60ca897098`);
- `code/verification/raccord_entrees_f1_rep_v1.py` ports the construction of the input of `enum_interval` (`code/lib/enumerate.py`);
- `code/production/certificats_impairs.py`, `code/production/certificats_impairs_x1.py`, `code/production/collisions8_x1.py`, `code/production/collisions8_x1_v3.py`, `code/production/rejeu_roiban/` and `code/reduced_basis/groupe_x1.py` adapt or replay parts of roiban1344's programs;
- `lean/ChainX1.lean` and `lean/ChainX1_avec_axiomes.lean` are adapted from `lean/EEUL/L112/Chain.lean`.

Other programs of `code/production/` and `code/reduced_basis/` import roiban1344's library at run time (for example `code/lib/group.py`, `code/produce/p2_minimal_orbits.py`, `code/produce/p3_norm8_orbits.py`, `code/produce/descent.py`); they need a copy of his repository and do not contain it. The copyright notice and licence of roiban1344's code are:

```
MIT License

Copyright (c) 2026 roiban1344

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Data of roiban1344 (CC BY 4.0)

The data of roiban1344's repositories are distributed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). This repository does not redistribute them: `data/roiban/fetch_roiban_data.sh` downloads them from their sources. The following files of this repository are derived from them (changes by Ivan Gauvin, 2026):

- `data/frozen/`: computed from roiban1344's `certificates/genus_class_1.txt`, `certificates/genus_basis_1.txt`, `certificates/genus_class_4.txt`, `certificates/genus_basis_4.txt`, `certificates/commutant.npz`, `data/L56_gram.txt`, `data/sl2_29_generators.txt` and `certificates/reduction_L.txt` (decompositions of the gluings, orbit representatives, certificates, inputs of the enumerator; see `data/README.md`);
- `data/reduced_basis/`: the Gram matrix `lattices/L112.02/gram.txt` of https://github.com/roiban1344/sl-2-29-rank-112-extremal-lattice (commit `d868927ada7bfbbcc0d6fad88cb8a25c75de9155`), written in another basis by the integer matrix of `X1_passage_from_roiban.txt`, and generators of a subgroup of its automorphism group in that basis;
- `logs/`: some logs print values read from these data.

The lattices L₅₆,₂(𝔐) and L₅₆,₂(M̃) are due to G. Nebe, Some cyclo-quaternionic lattices, J. Algebra 199 (1998) 472–498.
