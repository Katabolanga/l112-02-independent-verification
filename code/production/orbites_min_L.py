# orbites_min_L.py -- lot R112_X1_EFFORT_MAX_20261025 (agent Claude n° 116, 25 oct. 2026). Volet B3, F2 pour L.
# Orbites de S = SL_2(29) sur les vecteurs minimaux (norme 6) de L = Y1/sqrt2, par la fonction GENERIQUE minimal_orbits de
# produce/p2_minimal_orbits.py du depot roiban (LUE en entier : numpy seulement, aucune ecriture hors du dossier de sortie),
# puis controle independant a la maniere de verify/v3 (developpement complet : 7 795 200 vecteurs distincts de norme 6 au signe
# pres, soit 15 590 400 = |L_6| (serie theta extremale, depend de F1 pour L) ; formes canoniques distinctes et somme des orbites).
# Les germes : vecteurs de norme 6 de la base BKZ-40 (reduction_L.py) et leurs sommes/differences de norme 6.
# Usage : python -I orbites_min_L.py RACINE_DEPOT STRUCTURE_NPZ DONNEES_L_NPZ REDUCTION_NPZ DOSSIER
import os, sys, time
import numpy as np
racine, fstruct, fdon, fred, sortie = sys.argv[1:6]
sys.path.insert(0, os.path.join(racine, "code")); sys.path.insert(0, os.path.join(racine, "code", "produce"))
from lib import exact, mod2, shells
from lib.report import Report
from p2_minimal_orbits import minimal_orbits
os.makedirs(sortie, exist_ok=True)
rep = Report("orbites_min_L", sortie)
GL = np.load(fstruct, allow_pickle=False)["G_L"].astype(np.int64)
S = np.load(fdon, allow_pickle=False)["S"].astype(np.int64)
red = np.load(fred, allow_pickle=False)
U = red["U"].astype(np.int64)
rep.check("S_L : 12180 elements", S.shape == (12180, 56, 56))
B6 = [u for u in U if int(u @ GL @ u) == 6]
seeds = B6 + [x + s * y for i, x in enumerate(B6) for y in B6[:i] for s in (1, -1) if int((x + s * y) @ GL @ (x + s * y)) == 6]
rep.value("germes (vecteurs minimaux)", len(seeds))
R = minimal_orbits(GL, S.astype(np.int16), seeds, rep)
rep.value("representants", len(R))
# controle a la v3 (A) : developpement
V = shells.expand_half_shell(R, S.astype(np.int16))
rep.value("vecteurs r s au signe pres", len(V))
rep.check("2 x |V| = 15590400 = |L_6| (theta extremale)", 2 * len(V) == shells.N6)
rep.check("tous distincts (hachages 64 bits distincts)", shells.count_distinct_rows(V) == len(V))
rep.check("tous de norme 6", (exact.norms(V, GL) == 6).all())
del V
# (B) formes canoniques
can = mod2.Canonical(S.astype(np.int16))
can.self_test(S.astype(np.int16), np.random.default_rng(1))
forms, sizes = can.canon_and_orbit_size(mod2.pack(R))
rep.check("formes canoniques distinctes", len(set(forms.tolist())) == len(R))
vs = 2 * sizes
dist = {int(k): int(v) for k, v in zip(*np.unique(vs, return_counts=True))}
rep.value("tailles d'orbites {taille: nombre}", dist)
rep.check("somme des tailles = 15590400", int(vs.sum()) == shells.N6)
np.savez_compressed(os.path.join(sortie, "min_reps_L.npz"), reps=R.astype(np.int16))
rep.log("ecrit min_reps_L.npz")
rep.finish()
