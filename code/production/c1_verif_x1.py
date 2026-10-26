# c1_verif_x1.py -- lot R112_X1_EFFORT_MAX_20261025 (agent Claude n° 116, 25 oct. 2026). Volet C1.
# Verification EXACTE des deux matrices de Gram de X1 : celle de l'agent 112 (X3_gram.txt, classe |U| = 12 de (29, Delta_2, 2))
# et celle de roiban (genus_class_1.txt) : entieres, symetriques, paires, rang 112, det 1 (Bareiss, entiers Python), definies
# positives (decomposition LDL exacte en rationnels). Action de G0 = S o U(Lambda_1) sur la base de roiban : generateurs de S
# (D diag(g, g) D^-1) et les 12 elements de U (paires (u, u') compatibles avec f) : matrices entieres, isometries, U commute a S,
# U abelien d'exposant 6, |<S, U>| = 24360 x 12 / 2 (S ∩ U = {+-1}). Action de S sur la base de l'agent 112 (X3_gens.txt) :
# isometries entieres, groupe d'ordre 24360 (parcours exact).
# Usage : python -I c1_verif_x1.py RACINE STRUCT_NPZ DONNEES_L_NPZ X3_GRAM X3_GENS DOSSIER
import os, sys, time, hashlib
import numpy as np
racine, fstruct, fdon, fx3, fg3, sortie = sys.argv[1:7]
sys.path.insert(0, os.path.join(racine, "code"))
from lib import certs, data, exact, group
os.makedirs(sortie, exist_ok=True)
LOG = open(os.path.join(sortie, "c1_verif_x1.txt"), "w")
T0 = time.time()
def log(*a):
    s = " ".join(str(x) for x in a); print("[%7.1f s] %s" % (time.time() - T0, s), flush=True); LOG.write(s + "\n"); LOG.flush()
def ok(label, cond):
    log("[ok]  " if cond else "[ECHEC]", label)
    if not cond:
        raise SystemExit("ECHEC : " + label)
def lit_gram(f):
    L = [l.split() for l in open(f) if l.strip() and not l.startswith("#")]
    if len(L[0]) == 2 and len(L) == int(L[0][0]) + 1:
        L = L[1:]
    return np.array([[int(t) for t in r] for r in L], dtype=np.int64)
for nom, f in (("agent 112 (X3_gram.txt)", fx3), ("roiban (genus_class_1.txt)", os.path.join(racine, "certificates", "genus_class_1.txt"))):
    G = lit_gram(f)
    log(nom, "sha256", hashlib.sha256(open(f, "rb").read()).hexdigest())
    ok(nom + " : 112 x 112 entiere symetrique", G.shape == (112, 112) and (G == G.T).all())
    ok(nom + " : paire (diagonale paire)", (np.diag(G) % 2 == 0).all())
    ok(nom + " : det = 1 (Bareiss exact)", exact.det_bareiss(G) == 1)
    ok(nom + " : definie positive (LDL exacte en rationnels) ; rang 112", exact.is_positive_definite(G))
# action de S sur la base de l'agent 112
G3 = lit_gram(fx3)
v = [int(t) for t in open(fg3).read().split()]
k, r, c = v[0], v[1], v[2]
gens3 = [np.array(v[3 + i * r * c: 3 + (i + 1) * r * c], dtype=np.int64).reshape(r, c) for i in range(k)]
for g in gens3:
    ok("agent 112 : generateur de S isometrie entiere de X3", (exact.i64_matmul(exact.i64_matmul(g, G3), g.T) == G3).all())
E3 = group.enumerate_group(gens3)
ok("agent 112 : |<generateurs>| = 24360 (SL_2(29))", len(E3) == 24360)
ok("agent 112 : -I dans le groupe", any((e == -np.eye(112, dtype=np.int16)).all() for e in E3))
del E3
# G0 sur la base de roiban (Sage pour les inverses exacts)
from sage.all import ZZ, QQ, matrix, identity_matrix
st = np.load(fstruct, allow_pickle=False)
fz = st["f"].astype(np.int64)
Q = matrix(ZZ, st["Y1c"].tolist()).stack(matrix(ZZ, st["Y2c"].tolist())); Qi = Q.inverse()
GX = matrix(ZZ, lit_gram(os.path.join(racine, "certificates", "genus_class_1.txt")).tolist())
CL = np.load(fdon, allow_pickle=False)["units"].astype(np.int64)
C56 = certs.load("centralizer.npz", "units").astype(np.int64)
gens = data.generators()
def surX(a, b):
    M = matrix(ZZ, 112, 112)
    M.set_block(0, 0, matrix(ZZ, a.tolist())); M.set_block(56, 56, matrix(ZZ, b.tolist()))
    return Qi * M * Q
U = []
for u in [s * x for x in CL for s in (1, -1)]:
    for w in [s * x for x in C56 for s in (1, -1)]:
        if (((u @ fz) - (fz @ w)) % 2 == 0).all():
            M = surX(u, w)
            if M.denominator() == 1 and M * GX * M.transpose() == GX:
                U.append(M.change_ring(ZZ))
ok("U(Lambda_1) : 12 isometries entieres de X1", len(U) == 12)
I = identity_matrix(ZZ, 112)
ok("U abelien", all(A * B == B * A for A in U for B in U))
ok("U d'exposant 6 (u^6 = 1)", all(A ** 6 == I for A in U))
Sg = [surX(st["h1"].astype(np.int64), gens[0]).change_ring(ZZ), surX(st["h2"].astype(np.int64), gens[1]).change_ring(ZZ)]
ok("S : isometries entieres de X1", all(g * GX * g.transpose() == GX for g in Sg))
ok("U commute a S", all(A * g == g * A for A in U for g in Sg))
ok("S ∩ U = {+-1} : seuls +-I de U sont dans le centre (U agit fidelement sur Lambda_1)", sum(1 for A in U if A == I or A == -I) == 2)
log("|G0| = |S| |U| / |S ∩ U| = 24360 x 12 / 2 =", 24360 * 12 // 2)
np.savez_compressed(os.path.join(sortie, "U_X1_base_roiban.npz"), U=np.array([np.array(A, dtype=np.int64) for A in U]))
log("ecrit U_X1_base_roiban.npz")
