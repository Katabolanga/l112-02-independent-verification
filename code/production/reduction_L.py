# reduction_L.py -- lot R112_X1_EFFORT_MAX_20261025 (agent Claude n° 116, 25 oct. 2026). Volet B3, F1 pour L.
# Base BKZ-40 de L = Y1/sqrt2 (Gram G_L de structure_x1.npz) par fpylll (env g6k), comme p6_reduction.py du depot (Cholesky x 2^40
# arrondie, LLL puis BKZ-40, 4 tours, transformation accumulee) ; U verifiee EXACTEMENT (entiere, det +-1 par Bareiss), puis
# G' = U G_L U^T en entiers, et ecriture de l'entree du programme C enum_interval.c (fonction PURE enumerator_input du depot,
# rayon 4) : l'execution du programme est faite a part (shell), pas par Python.
# Usage : python -I reduction_L.py RACINE_DEPOT STRUCTURE_NPZ DOSSIER [BLOC=40]
import os, sys, time, hashlib
import numpy as np
racine, fstruct, sortie = sys.argv[1], sys.argv[2], sys.argv[3]
bloc = int(sys.argv[4]) if len(sys.argv) > 4 else 40
sys.path.insert(0, os.path.join(racine, "code"))
from lib import exact
from lib.enumerate import enumerator_input
from fpylll import BKZ, GSO, LLL, IntegerMatrix
from fpylll.algorithms.bkz2 import BKZReduction
os.makedirs(sortie, exist_ok=True)
GL = np.load(fstruct, allow_pickle=False)["G_L"].astype(np.int64)
n = len(GL)
t0 = time.time()
C = np.linalg.cholesky(GL.astype(float))
A = IntegerMatrix.from_matrix([[int(round(v * 2 ** 40)) for v in row] for row in C])
U = IntegerMatrix.identity(n)
M = GSO.Mat(A, U=U, float_type="mpfr")
LLL.Reduction(M)()
BKZReduction(M)(BKZ.EasyParam(bloc, max_loops=4))
Un = np.array([[U[i, j] for j in range(n)] for i in range(n)], dtype=np.int64)
d = exact.det_bareiss(Un)
assert abs(d) == 1, "U non unimodulaire"
Gr = exact.i64_matmul(exact.i64_matmul(Un, GL), Un.T)
assert (Gr == Gr.T).all() and exact.det_bareiss(Gr) == 1
print("BKZ-%d en %.0f s ; det U = %d ; diagonale de U G U^T : min %d max %d ; normes 6 dans la base : %d" %
      (bloc, time.time() - t0, d, int(np.diag(Gr).min()), int(np.diag(Gr).max()), int((np.diag(Gr) == 6).sum())), flush=True)
np.savez_compressed(os.path.join(sortie, "reduction_L_bkz%d.npz" % bloc), U=Un, Gr=Gr)
with open(os.path.join(sortie, "L_bkz%d_rayon4.entree" % bloc), "w") as f:
    f.write(enumerator_input(Gr, 4))
print("ecrit", os.path.join(sortie, "L_bkz%d_rayon4.entree" % bloc), flush=True)
