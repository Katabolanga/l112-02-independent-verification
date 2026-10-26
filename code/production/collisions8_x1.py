# collisions8_x1.py -- lot R112_X1_EFFORT_MAX_20261025 (agent Claude n° 116, 25 oct. 2026). Volet B3, F5b (type (8,8)).
# Recollement X = {(x, v)/sqrt2 : x dans L, v dans L56, v = x f (mod 2)} (structure_*.npz). Type (8,8) : il faut que, pour
# TOUT x de norme 8 de L, la classe x f + 2 L56 ne contienne aucun vecteur de norme 8 de L56. Par F3 pour L (orbites des paires
# x_i u_k, u_k dans C_L/{+-1}) et l'equivariance de f (f(x h) = f(x) g mod 2), il suffit de tester les 1 527 984 paires.
# Test : forme canonique (sous S = SL_2(29) agissant sur L56/2L56) de la classe de (x_i u_k) f, cherchee dans la table K8 de
# L56 (out/K8.npy ecrite par MON rejeu de verify/v4 ; lue par lib.report.load_output_of, qui controle le JSON « passed » et les
# SHA-256). Proposition 6.3 de roiban : can(c) dans K8 <=> c contient un vecteur de norme 8 (via F3 pour L56).
# Toute touche est une COLLISION : on reconstruit alors le vecteur w de norme 8 de L56 dans la classe et le TEMOIN
# z = (x Y1 + w Y2)/2 de X (norme 8), ecrit en coordonnees de la base de X.
# Option : TRANSPORT (pour le temoin positif X4) : fichier d'isometrie avec Tinv ; les donnees de L1 sont transportees par
#   x4 = x1 Tinv.
# Usage : python -I collisions8_x1.py RACINE STRUCT_NPZ DONNEES_L_NPZ NORM8_REPS_L_NPZ DOSSIER CLASSE [ISOMETRIE_NPZ]
import os, sys, time, hashlib
import numpy as np
racine, fstruct, fdon, freps, sortie, classe = sys.argv[1:7]
fiso = sys.argv[7] if len(sys.argv) > 7 else None
sys.path.insert(0, os.path.join(racine, "code"))
from lib import certs, data, exact, group, mod2
from lib.report import Report
os.makedirs(sortie, exist_ok=True)
rep = Report("collisions8_X%s" % classe, sortie)
st = np.load(fstruct, allow_pickle=False)
GL = st["G_L"].astype(np.int64); fz = st["f"].astype(np.int64); Y1c = st["Y1c"].astype(np.int64); Y2c = st["Y2c"].astype(np.int64)
Un = np.load(fdon, allow_pickle=False)["units"].astype(np.int64)
X = np.load(freps, allow_pickle=False)["reps"].astype(np.int64)
if fiso:
    Ti = np.load(fiso, allow_pickle=False)["Tinv"].astype(np.int64)
    T = np.load(fiso, allow_pickle=False)["T"].astype(np.int64)
    X = exact.i64_matmul(X, Ti)
    Un = np.stack([exact.i64_matmul(exact.i64_matmul(T, u), Ti) for u in Un])     # u4 = T u1 T^-1 (x4 u4 = (x4 T) u1 T^-1)
    rep.log("donnees de L1 transportees vers L%s par l'isometrie" % classe)
rep.check("unites : isometries de L", all((exact.i64_matmul(exact.i64_matmul(u, GL), u.T) == GL).all() for u in Un))
G = data.gram()
gens = data.generators()
S = group.sl2_29_mod_sign(gens)
GX = data.read_integers(os.path.join(racine, "certificates", "genus_class_%s.txt" % classe), None).reshape(112, 112)
# K8 de L56 : ecrite par MON rejeu de verify/v4 dans RACINE/out ; controles explicites (JSON « passed », SHA-256 du fichier et
# des entrees identiques a ceux qu'a enregistres v4).
import json
dout = os.path.join(racine, "out")
res = json.load(open(os.path.join(dout, "v4_norm8_orbits.json")))
pK8 = os.path.join(dout, "K8.npy")
rep.check("rejeu de v4 : passed", res.get("passed") is True)
rep.check("rejeu de v4 : memes fichiers d'entree (SHA-256)", res["values"].get("SHA-256 of the inputs") == certs.file_hashes(certs.K8_INPUTS))
rep.check("K8.npy : SHA-256 enregistre par v4", res["values"].get("SHA-256 of out/K8.npy") == hashlib.sha256(open(pK8, "rb").read()).hexdigest())
K8 = np.load(pK8, allow_pickle=False)
rep.check("K8 de L56 : 1517130 formes canoniques (rejeu de v4)", len(K8) == 1517130)
can = mod2.Canonical(S)
can.self_test(S, np.random.default_rng(5))
h1 = st["h1"].astype(np.int64); h2 = st["h2"].astype(np.int64)
if fiso:
    rep.log("(generateurs de S sur L%s : ceux de la structure)" % classe)
rep.check("f equivariante modulo 2 sur les generateurs : h f = f g", all((((exact.i64_matmul(h, fz) - exact.i64_matmul(fz, g)) % 2) == 0).all()
                                                               for h, g in ((h1, gens[0]), (h2, gens[1]))))
Y = np.stack([exact.i64_matmul(X, u) for u in Un], axis=1).reshape(-1, 56)
rep.value("paires x_i u_k testees", len(Y))
rep.check("toutes de norme 8 dans L", (exact.norms(Y, GL) == 8).all())
# temoin positif de la table : les classes des representants de L56 eux-memes sont dans K8
X56 = certs.load("norm8_reps.npz", "reps").astype(np.int64)[:2000]
rep.check("temoin positif : can(x~_j + 2 L56) dans K8 (2000 premiers representants de L56)",
          np.isin(can.canon(mod2.pack(X56)), K8).all())
hits = []
step = 1 << 14
t0 = time.time()
for i in range(0, len(Y), step):
    B = Y[i:i + step]
    c = mod2.pack(exact.i64_matmul(B, fz))
    f_ = can.canon(c)
    idx = np.nonzero(np.isin(f_, K8))[0]
    for j in idx.tolist():
        hits.append(i + j)
    if (i // step) % 10 == 0:
        rep.log("%d / %d paires ; touches %d ; %.0f s" % (min(i + step, len(Y)), len(Y), len(hits), time.time() - t0))
rep.value("type (8,8) : classes (x_i u_k) f + 2 L56 contenant un vecteur de norme 8", len(hits))
if hits:
    # nombre d'orbites de S distinctes parmi les paires touchees (formes canoniques dans L/2L sous S agissant sur L)
    SL = np.load(fdon, allow_pickle=False)["S"].astype(np.int16)
    canL = mod2.Canonical(SL)
    fL = canL.canon(mod2.pack(Y[np.array(hits)]))
    k_orb = len(np.unique(fL))
    rep.value("orbites de S sur L(8) en collision (8,8)", k_orb)
    rep.value("nombre de vecteurs de norme 8 de X (2 x 24360 par orbite : x dans l'orbite, +-v)", 2 * 24360 * k_orb)
    # reconstruction des temoins : chercher s dans S/{+-1} et un representant x~ u~ de L56 avec la meme classe
    R56 = certs.load("norm8_reps.npz", "reps").astype(np.int64)
    U56 = certs.load("centralizer.npz", "units").astype(np.int64)
    P56 = np.stack([exact.i64_matmul(R56, u) for u in U56], axis=1).reshape(-1, 56)
    # K8_first.npy (rejeu de v4, SHA controle) : pour chaque forme canonique de K8 (triee), l'indice 6i + k d'une paire de L56
    pK8f = os.path.join(dout, "K8_first.npy")
    rep.check("K8_first.npy : SHA-256 enregistre par v4", res["values"].get("SHA-256 of out/K8_first.npy") == hashlib.sha256(open(pK8f, "rb").read()).hexdigest())
    K8first = np.load(pK8f, allow_pickle=False)
    with open(os.path.join(sortie, "TEMOINS_X%s_type88.txt" % classe), "w") as h:
        h.write("# temoins de norme 8 (type (8,8)) dans X%s : norme : coordonnees dans la base de genus_class_%s.txt\n" % (classe, classe))
        for t in hits[:50]:
            x = Y[t]; c = mod2.pack(exact.i64_matmul(x[None, :], fz))[0]
            fc = can.canon(np.array([c], dtype=np.uint64))[0]
            pos = int(np.searchsorted(K8, fc))
            if pos >= len(K8) or K8[pos] != fc:
                rep.log("reconstruction : forme canonique absente de K8 (inattendu)"); continue
            j = int(K8first[pos])
            img = can.images(mod2.pack(P56[j:j + 1]))[0]
            s = int(np.nonzero(img == c)[0][0])
            w = exact.i64_matmul(P56[j:j + 1], S[s].astype(np.int64))[0]
            z2 = exact.i64_matmul(x[None, :], Y1c)[0] + exact.i64_matmul(w[None, :], Y2c)[0]
            if (z2 % 2).any():
                rep.log("reconstruction : vecteur non entier (inattendu)"); continue
            z = z2 // 2
            q = int(z @ GX @ z)
            h.write("%d : %s\n" % (q, " ".join(map(str, z.tolist()))))
            rep.log("TEMOIN type (8,8) : norme %d (x de norme %d, w de norme %d)" % (q, int(x @ GL @ x), int(w @ G @ w)))
rep.finish()
