# orbites8_L.py -- lot R112_X1_EFFORT_MAX_20261025 (agent Claude n° 116, 25 oct. 2026). Volet B3, F3 pour L.
# Orbites de S* = S . C_L (|S*| = 24360 x 24 / 2 = 292 320) sur les vecteurs de norme 8 de L = Y1/sqrt2, par la fonction
# GENERIQUE norm8_orbits de produce/p3_norm8_orbits.py du depot roiban (LUE en entier : numpy seulement ; ecritures : points de
# reprise dans le dossier pdir donne ici), puis CONTROLE INDEPENDANT a la maniere de verify/v4 : toutes les paires x_i u_k
# (u_k dans C_L/{+-1}, 12 elements) ont la norme 8 ; leurs classes modulo 2L ont exactement 1 517 130 formes canoniques
# distinctes (orbites de S), toutes de taille 24 360, de somme |L_8| = 36 957 286 800 (serie theta extremale ; s'appuie sur F1
# pour L via le lemme du milieu). Ecrit K8_L.npy (formes canoniques triees) et norm8_reps_L.npz.
# Usage : python -I orbites8_L.py RACINE_DEPOT STRUCTURE_NPZ DONNEES_L_NPZ MINREPS_L_NPZ DOSSIER [TRIAL]
import os, sys, time, hashlib
import numpy as np
racine, fstruct, fdon, fmin, sortie = sys.argv[1:6]
trial = int(sys.argv[6]) if len(sys.argv) > 6 else None
sys.path.insert(0, os.path.join(racine, "code")); sys.path.insert(0, os.path.join(racine, "code", "produce"))
from lib import exact, mod2, shells, group
from lib.report import Report
from p3_norm8_orbits import norm8_orbits, fingerprint
import p3_norm8_orbits as _P3
if os.environ.get("SANS_REPRISE") == "1":
    # points de reprise desactives (memoire : la sauvegarde concatene les listes de hachages ; roiban annonce jusqu'a 5 Go
    # pendant les sauvegardes) ; ajout de l'agent 116, sans autre changement de l'algorithme
    _P3.State.save = lambda self, path: None
os.makedirs(sortie, exist_ok=True)
rep = Report("orbites8_L" + ("_trial%d" % trial if trial else ""), sortie)
GL = np.load(fstruct, allow_pickle=False)["G_L"].astype(np.int64)
don = np.load(fdon, allow_pickle=False)
S = don["S"].astype(np.int64)
Un = don["units"].astype(np.int64)
R6 = np.load(fmin, allow_pickle=False)["reps"].astype(np.int64)
rep.check("12 unites de C_L/{+-1}, isometries commutant a S (deux generateurs)",
          Un.shape == (12, 56, 56) and all((exact.i64_matmul(exact.i64_matmul(u, GL), u.T) == GL).all() for u in Un))
inputs = fingerprint(GL, S[:3], R6, Un)
pdir = os.path.join(sortie, "p3_trial" if trial else "p3")
t0 = time.time()
reps, sizes = norm8_orbits(GL, S, R6, Un, pdir, rep, trial=trial, inputs=inputs)
if reps is None:
    rep.finish(); sys.exit(0)
rep.value("duree de norm8_orbits (s)", round(time.time() - t0))
np.savez_compressed(os.path.join(sortie, "norm8_reps_L.npz"), reps=reps, sizes=sizes)
rep.log("ecrit norm8_reps_L.npz")
# controle a la v4
X = reps.astype(np.int64)
Y = np.stack([exact.i64_matmul(X, u) for u in Un], axis=1).reshape(-1, 56)
rep.value("paires x_i u_k", len(Y))
rep.check("toutes de norme 8", (exact.norms(Y, GL) == 8).all())
can = mod2.Canonical(S.astype(np.int16))
can.self_test(S.astype(np.int16), np.random.default_rng(2))
forms = np.empty(len(Y), dtype=np.uint64); osz = np.empty(len(Y), dtype=np.int64)
step = 1 << 15
for i in range(0, len(Y), step):
    forms[i:i + step], osz[i:i + step] = can.canon_and_orbit_size(mod2.pack(Y[i:i + step]))
    if (i // step) % 8 == 0:
        rep.log("formes canoniques : %d / %d" % (min(i + step, len(Y)), len(Y)))
K8, first = np.unique(forms, return_index=True)
rep.value("formes canoniques distinctes (= orbites de S)", len(K8))
rep.check("exactement 1517130 orbites de S", len(K8) == 1517130)
vs = 2 * osz[first]
rep.value("tailles {taille: nombre}", {int(k): int(v) for k, v in zip(*np.unique(vs, return_counts=True))})
rep.check("toutes regulieres (24360)", (vs == 24360).all())
rep.check("somme = |L_8| = 36957286800", int(vs.sum()) == shells.N8)
np.save(os.path.join(sortie, "K8_L.npy"), K8)
rep.value("SHA-256 de K8_L.npy", hashlib.sha256(open(os.path.join(sortie, "K8_L.npy"), "rb").read()).hexdigest())
rep.finish()
