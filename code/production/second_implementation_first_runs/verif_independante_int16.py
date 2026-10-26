# verif_independante_int16.py -- copie de verif_independante.py (agent 116) avec UNE correction (Claude, 25 oct. 23 h 15) : stockage int16 au lieu de int8
# des vecteurs minimaux (coordonnee maximale 135 pour L56 dans la base du depot). Rien d autre ne change.
# verif_independante.py -- lot R112_X1_EFFORT_MAX_20261025 (agent Claude n° 116, 25 oct. 2026).
# SECONDE IMPLEMENTATION (code ecrit ici, sans importer lib/ ni produce/ de roiban) des controles decisifs F3, F5b et F5a :
#   (G)   groupes : parcours en largeur EXACT des groupes engendres par les generateurs (entiers 56 x 56), et de leurs images mod 2 ;
#   (F3)  pour L56 (representants de roiban x unites) et pour L (sortie de p3 x unites) : normes 8 (entiers exacts), formes
#         canoniques modulo 2 par formes_canoniques.c (ecrit ici), 1 517 130 orbites, toutes regulieres, somme = |L_8| ;
#   (F5b) pour chaque paire x de L(8) : forme canonique (sous S sur L56/2L56) de la classe x f, cherchee dans K8(L56) recalcule ici ;
#   (F5a) certificats impairs (certificats_*.npz) : classe, norme 14 ou 18, |<w0, u>| <= 6 sur TOUS les vecteurs minimaux,
#         developpes ici a partir des representants et du groupe entier enumere ici (produits flottants sous bornes d'exactitude).
# Donnees partagees avec la premiere implementation : les fichiers d'entree seulement (Gram, generateurs, representants,
# certificats, structure du recollement).
# Usage : python -I verif_independante.py RACINE STRUCT_NPZ DONNEES_L_NPZ NORM8_REPS_L_NPZ MINREPS_L_NPZ CERTIFS_DIR BIN_FORMES DOSSIER [J]
import os, sys, time, struct, subprocess
import numpy as np
(racine, fstruct, fdon, f8L, fminL, dcert, binformes, sortie) = sys.argv[1:9]
J = sys.argv[9] if len(sys.argv) > 9 else "1"
os.makedirs(sortie, exist_ok=True)
LOG = open(os.path.join(sortie, "verif_independante_X%s.txt" % J), "w")
T0 = time.time()
ECHECS = []
def log(*a):
    s = " ".join(str(x) for x in a); print("[%7.1f s] %s" % (time.time() - T0, s), flush=True); LOG.write(s + "\n"); LOG.flush()
def ok(label, cond):
    log("[ok]  " if cond else "[ECHEC]", label)
    if not cond:
        ECHECS.append(label)
    return cond
def entiers(p):
    return [int(t) for l in open(p) if not l.startswith("#") for t in l.split()]
def charger_npz(p, k):
    with np.load(p, allow_pickle=False) as z:
        return z[k]
N6, N8 = 15590400, 36957286800
BITS = np.uint64(1) << np.arange(56, dtype=np.uint64)
G = np.array(entiers(os.path.join(racine, "data", "L56_gram.txt")), dtype=np.int64).reshape(56, 56)
gg = np.array(entiers(os.path.join(racine, "data", "sl2_29_generators.txt")), dtype=np.int64).reshape(2, 56, 56)
st = np.load(fstruct, allow_pickle=False)
GL = st["G_L"].astype(np.int64); fz = st["f"].astype(np.int64)
hL = [st["h1"].astype(np.int64), st["h2"].astype(np.int64)]
UL = charger_npz(fdon, "units").astype(np.int64)
U56 = charger_npz(os.path.join(racine, "certificates", "centralizer.npz"), "units").astype(np.int64)
R56 = charger_npz(os.path.join(racine, "certificates", "norm8_reps.npz"), "reps").astype(np.int64)
M56 = charger_npz(os.path.join(racine, "certificates", "min_reps.npz"), "reps").astype(np.int64)
XL = charger_npz(f8L, "reps").astype(np.int64)
ML = charger_npz(fminL, "reps").astype(np.int64)
def normes(V, Gm, bloc=1 << 18):
    out = np.empty(len(V), dtype=np.int64)
    for i in range(0, len(V), bloc):
        B = V[i:i + bloc].astype(np.int64)
        if np.abs(B).max() * np.abs(Gm).max() * 56 >= 2 ** 31:
            raise RuntimeError("borne")
        W = B @ Gm
        out[i:i + bloc] = (W * B).sum(axis=1)
    return out
def paquet(V, bloc=1 << 18):
    out = np.empty(len(V), dtype=np.uint64)
    for i in range(0, len(V), bloc):
        out[i:i + bloc] = ((V[i:i + bloc] % 2).astype(np.uint64) * BITS).sum(axis=1)
    return out
def parcours(gens, ordre_max=30000):
    """groupe engendre (parcours en largeur exact, entiers) -> tableau int16 (ordre, n, n)"""
    n = gens[0].shape[0]
    I = np.eye(n, dtype=np.int64)
    vus = {I.astype(np.int16).tobytes()}; L = [I.astype(np.int16)]; i = 0
    while i < len(L):
        X = L[i].astype(np.int64); i += 1
        for g in gens:
            Y = X @ g
            if np.abs(Y).max() >= 2 ** 15:
                raise RuntimeError("coefficient hors de int16")
            Y = Y.astype(np.int16); k = Y.tobytes()
            if k not in vus:
                vus.add(k); L.append(Y)
                if len(L) > ordre_max:
                    raise RuntimeError("groupe trop gros")
    return np.stack(L)
def groupe_mod2(E, fichier):
    lst = {}
    for X in E:
        m = tuple(int(t) for t in ((X.astype(np.int64) % 2).astype(np.uint64) * BITS).sum(axis=1))
        lst[m] = 1
    with open(fichier, "wb") as h:
        h.write(struct.pack("<Q", len(lst)))
        for m in lst:
            h.write(struct.pack("<56Q", *m))
    return len(lst)
def formes(classes, fgroupe, nom):
    fc = os.path.join(sortie, nom + ".classes.bin"); fo = os.path.join(sortie, nom + ".formes.bin")
    with open(fc, "wb") as h:
        h.write(struct.pack("<Q", len(classes))); h.write(np.asarray(classes, dtype="<u8").tobytes())
    r = subprocess.run([binformes, fgroupe, fc, fo], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("formes_canoniques : " + r.stderr)
    raw = open(fo, "rb").read(); N = len(classes)
    return np.frombuffer(raw[:8 * N], dtype="<u8").copy(), np.frombuffer(raw[8 * N:], dtype="<u4").copy()
# (G) groupes
log("parcours du groupe entier sur L56 ...")
E56 = parcours([gg[0], gg[1]])
ok("|<g1, g2>| = 24360 sur L56", len(E56) == 24360)
ok("generateurs isometries de L56", all((g @ G @ g.T == G).all() for g in gg))
ok("image modulo 2 d'ordre 12180 sur L56/2L56", groupe_mod2(E56, os.path.join(sortie, "groupe56_mod2.bin")) == 12180)
log("parcours du groupe entier sur L ...")
EL = parcours(hL)
ok("|<h1, h2>| = 24360 sur L", len(EL) == 24360)
ok("generateurs isometries de L", all((g @ GL @ g.T == GL).all() for g in hL))
ok("image modulo 2 d'ordre 12180 sur L/2L", groupe_mod2(EL, os.path.join(sortie, "groupeL_mod2.bin")) == 12180)
ok("f equivariante modulo 2 (generateurs)", all((((h @ fz) - (fz @ g)) % 2 == 0).all() for h, g in zip(hL, gg)))
# (F3) L56
P56 = np.stack([R56 @ u for u in U56], axis=1).reshape(-1, 56)
ok("L56 : %d paires de norme 8" % len(P56), (normes(P56, G) == 8).all())
c56, o56 = formes(paquet(P56), os.path.join(sortie, "groupe56_mod2.bin"), "L56_norme8")
del P56
K8, first = np.unique(c56, return_index=True)
ok("L56 : 1517130 orbites distinctes", len(K8) == 1517130)
ok("L56 : toutes regulieres (12180 classes, 24360 vecteurs)", (o56[first] == 12180).all())
ok("L56 : somme des tailles = |L_8|", int(2 * o56[first].astype(np.int64).sum()) == N8)
del c56, o56
# (F3) L
PL = np.stack([XL @ u for u in UL], axis=1).reshape(-1, 56)
ok("L : %d paires de norme 8" % len(PL), (normes(PL, GL) == 8).all())
cL, oL = formes(paquet(PL), os.path.join(sortie, "groupeL_mod2.bin"), "L_norme8")
KL, firstL = np.unique(cL, return_index=True)
ok("L : 1517130 orbites distinctes", len(KL) == 1517130)
ok("L : toutes regulieres", (oL[firstL] == 12180).all())
ok("L : somme des tailles = |L_8|", int(2 * oL[firstL].astype(np.int64).sum()) == N8)
# (F5b) type (8,8)
cls = np.empty(len(PL), dtype=np.uint64)
for i in range(0, len(PL), 1 << 18):
    cls[i:i + (1 << 18)] = paquet(PL[i:i + (1 << 18)] @ fz)
cX, _ = formes(cls, os.path.join(sortie, "groupe56_mod2.bin"), "X_88")
touches = np.isin(cX, K8)
nb = int(touches.sum())
log("type (8,8) : paires x de L(8) dont la classe x f contient un vecteur de norme 8 de L56 :", nb)
if nb:
    orbs = len(np.unique(cL[touches]))
    log("  orbites de S sur L(8) en collision :", orbs, "; vecteurs de norme 8 de X :", 2 * 24360 * orbs)
np.save(os.path.join(sortie, "touches_88_X%s.npy" % J), np.nonzero(touches)[0])
del PL, cls, cX
# (F5a) certificats impairs
def vecteurs_minimaux(M, E):
    S = E.astype(np.float32)
    parts = []
    for r in M:
        assert int(np.abs(r).sum()) * int(np.abs(E).max()) < 2 ** 24
        Y = np.rint(r.astype(np.float32) @ S).astype(np.int64)          # (24360, 56), exact
        f = (Y != 0).argmax(axis=1); sg = np.sign(Y[np.arange(len(Y)), f])
        parts.append(np.unique((Y * sg[:, None]).astype(np.int16), axis=0))
    V = np.concatenate(parts)
    w = np.random.default_rng(116).integers(1, 2 ** 61, size=56, dtype=np.int64) | 1
    h = np.concatenate([V[i:i + (1 << 20)].astype(np.int64) @ w for i in range(0, len(V), 1 << 20)])
    return V, len(np.unique(h))
def max_ip(W, V, Gm):
    A = (W @ Gm).astype(np.int64)
    assert np.abs(A).sum(axis=1).max() * int(np.abs(V).max()) < 2 ** 24
    Af = A.astype(np.float32); best = np.zeros(len(W), dtype=np.int64)
    for i in range(0, len(V), 1 << 15):
        P = Af @ V[i:i + (1 << 15)].T.astype(np.float32)
        best = np.maximum(best, np.rint(np.abs(P).max(axis=1)).astype(np.int64))
    return best
def inv_mod2(F):
    n = len(F); A = np.concatenate([F % 2, np.eye(n, dtype=np.int64)], axis=1)
    for c in range(n):
        q = next(i for i in range(c, n) if A[i, c] % 2); A[[c, q]] = A[[q, c]]
        for i in range(n):
            if i != c and A[i, c] % 2:
                A[i] = (A[i] + A[c]) % 2
    return A[:, n:] % 2
for cote, nomf, Gd, Mreps, E, src, F in (("phi_L_vers_L56", "certificats_phi_L_vers_L56.npz", G, M56, E56, ML, fz),
                                        ("psi_L56_vers_L", "certificats_psi_L56_vers_L.npz", GL, ML, EL, M56, None)):
    p = os.path.join(dcert, nomf)
    if not os.path.exists(p):
        log("certificats absents :", p); continue
    if F is None:
        F = inv_mod2(fz)
    W = charger_npz(p, "w0").astype(np.int64)
    V, nd = vecteurs_minimaux(Mreps, E)
    ok("%s : %d vecteurs minimaux au signe pres, distincts (hachage), 2 x = |L_6|" % (cote, len(V)), 2 * len(V) == N6 and nd == len(V))
    ok("%s : tous de norme 6" % cote, (normes(V, Gd) == 6).all())
    nW = normes(W, Gd)
    ok("%s : normes des certificats dans {14, 18}" % cote, np.isin(nW, (14, 18)).all())
    ok("%s : chaque certificat est dans la classe de son representant" % cote, (((W - (src @ F)) % 2) == 0).all())
    mx = max_ip(W, V, Gd)
    ok("%s : max |<w0, u>| <= 6 sur tous les vecteurs minimaux" % cote, (mx <= 6).all())
    del V
log("BILAN :", "OK" if not ECHECS else "ECHECS : %s" % ECHECS)
sys.exit(0 if not ECHECS else 1)
