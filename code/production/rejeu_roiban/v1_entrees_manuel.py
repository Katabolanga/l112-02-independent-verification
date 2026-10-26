# v1_entrees_manuel.py -- agent 116 (25 oct. 2026). Rejeu de v1 (F1 : min L56 = 6) SANS le sous-processus de lib/enumerate.py
# (garde-fou : aucun script telecharge n'appelle de shell ni de subprocess). On utilise seulement les fonctions PURES du depot
# (data.gram, certs.load_matrix, exact.det_bareiss, exact.i64_matmul, enumerate.enumerator_input) pour ECRIRE les entrees du
# programme C enum_interval.c ; la compilation et l'execution sont faites a la main (rejouer_v1.sh), et la lecture des sorties
# par lire_v1.py.  Usage (depuis la racine de la copie) : python -I v1_entrees_manuel.py RACINE_COPIE DOSSIER_SORTIE
import os, sys
racine, sortie = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(racine, "code"))
import numpy as np
from lib import certs, data, exact
from lib.enumerate import enumerator_input
os.makedirs(sortie, exist_ok=True)
E8 = np.array([
    [2, 1, 1, -1, 1, 1, 1, 1], [1, 2, 1, 0, 1, 1, 0, 1], [1, 1, 2, -1, 1, 0, 1, 1], [-1, 0, -1, 2, 0, 0, -1, -1],
    [1, 1, 1, 0, 2, 0, 0, 0], [1, 1, 0, 0, 0, 2, 0, 1], [1, 0, 1, -1, 0, 0, 2, 1], [1, 1, 1, -1, 0, 1, 1, 2]], dtype=np.int64)
leech = data.read_integers(os.path.join(racine, "code", "verify", "controls", "leech.txt")).reshape(24, 24)
Z = lambda p, q: np.zeros((p, q), dtype=np.int64)
big = np.block([[leech, Z(24, 24), Z(24, 8)], [Z(24, 24), leech, Z(24, 8)], [Z(8, 24), Z(8, 24), E8]])
G = data.gram()
U = certs.load_matrix("reduction_L.txt", 56)
assert abs(exact.det_bareiss(U)) == 1
Gr = exact.i64_matmul(exact.i64_matmul(U, G), U.T)
for nom, M, R in (("E8", E8, 2), ("leech", leech, 4), ("leech2_e8", big, 4), ("L56", Gr, 4)):
    with open(os.path.join(sortie, nom + ".entree"), "w") as f:
        f.write(enumerator_input(M, R))
    print(nom, "dimension", len(M), "rayon", R, "diagonale min/max", int(np.diag(M).min()), int(np.diag(M).max()))
