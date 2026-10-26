# certificats_impairs.py (copie parametree de certificats_impairs_x1.py : classe J du depot) -- lot R112_X1_EFFORT_MAX_20261025 (agent Claude n° 116, 25 oct. 2026). Volet B3, F5a pour X1.
# X1 = {(x, v)/sqrt2 : x dans L, v dans L~ = L56, v = x f (mod 2)} (structure_x1.npz). Types a exclure (lemme 4.2 adapte) :
#   (6,6) et (6,10) : pour chaque representant r des orbites de S sur L_6, min(r f + 2 L56) >= 14   [cote phi]
#   (10,6) (et (6,6)) : pour chaque representant r~ des orbites sur L56_6, min(r~ f^-1 + 2 L) >= 14  [cote psi]
# Methode (roiban, § 6.6) : descente w -> w - 2u tant qu'un vecteur minimal u a <w, u> >= 7 (classe Descent de
# produce/descent.py du depot, LUE ; produits flottants exacts sous bornes verifiees), puis CONTROLE EXACT du certificat a la
# maniere de verify/v5 : w - (relevement) a coordonnees paires ; norme 14 ou 18 ; |<w, u>| <= 6 pour les 15 590 400 vecteurs
# minimaux (lib/shells.py : MinimalVectors, float32 exact sous borne verifiee). Toute descente qui s'arrete a une norme 6 ou 10
# donnerait un TEMOIN de norme < 10 dans X1 (ecrit alors avec ses coordonnees dans la base de X1, norme recalculee).
# Temoin positif (comme p4) : classes « norme 10 + 2L » plantees : la descente ne doit jamais rendre de faux certificat.
# Usage : python -I certificats_impairs.py RACINE_DEPOT STRUCTURE_NPZ DONNEES_L_NPZ MINREPS_L_NPZ DOSSIER J REDUCTION_L_NPZ
import os, sys, time, random, hashlib
import numpy as np
racine, fstruct, fdon, fmin, sortie, J, fred = sys.argv[1:8]
sys.path.insert(0, os.path.join(racine, "code")); sys.path.insert(0, os.path.join(racine, "code", "produce"))
from lib import certs, data, exact, group, shells
from lib.report import Report
from descent import Descent
os.makedirs(sortie, exist_ok=True)
rep = Report("certificats_impairs_X%s" % J, sortie)
st = np.load(fstruct, allow_pickle=False)
GL = st["G_L"].astype(np.int64); fz = st["f"].astype(np.int64); Y1c = st["Y1c"].astype(np.int64); Y2c = st["Y2c"].astype(np.int64)
SL = np.load(fdon, allow_pickle=False)["S"].astype(np.int16)
R6L = np.load(fmin, allow_pickle=False)["reps"].astype(np.int64)
G = data.gram(); S56 = group.sl2_29_mod_sign(data.generators())
R656 = certs.load("min_reps.npz", "reps").astype(np.int64)
GX = data.read_integers(os.path.join(racine, "certificates", "genus_class_%s.txt" % J), None).reshape(112, 112)
rep.check("G_X = Gram de la base [Y1; Y2]/2 coherente : Y1 G_X Y1^T = 2 G_L et Y2 G_X Y2^T = 2 G",
          (exact.i64_matmul(exact.i64_matmul(Y1c, GX), Y1c.T) == 2 * GL).all() and
          (exact.i64_matmul(exact.i64_matmul(Y2c, GX), Y2c.T) == 2 * G).all() and
          (exact.i64_matmul(exact.i64_matmul(Y1c, GX), Y2c.T) == 0).all())
# inverse de f modulo 2 (Gauss sur F_2)
def inv_mod2(F):
    n = len(F); A = np.concatenate([F % 2, np.eye(n, dtype=np.int64)], axis=1)
    r = 0
    for c in range(n):
        p = next(i for i in range(r, n) if A[i, c] % 2)
        A[[r, p]] = A[[p, r]]
        for i in range(n):
            if i != r and A[i, c] % 2:
                A[i] = (A[i] + A[r]) % 2
        r += 1
    return A[:, n:] % 2
fiz = inv_mod2(fz)
rep.check("f f^-1 = I (mod 2)", ((fz @ fiz) % 2 == np.eye(56, dtype=np.int64)).all())

# Bases reduites (lignes, unimodulaires) : L56 = reduction_L.txt du depot (BKZ-40) ; L = reduction BKZ-40 de reduction_L.py.
# Le point de depart de chaque descente est ramene dans sa classe modulo 2 par : coordonnees dans la base reduite prises
# modulo 2 (dans {0, 1}), puis plan le plus proche (Babai) sur 2 x base reduite (flottants pour CHOISIR y seulement ; le
# vecteur rendu est entier et reste dans la classe, ce qui est controle). Essai 1 sans reduction : normes de depart ~1e7.
B56 = certs.load_matrix("reduction_L.txt", 56).astype(np.int64)
BL = np.load(fred, allow_pickle=False)["U"].astype(np.int64)
def prep_reduction(B, Gd):
    Bi = exact.inverse_unimodular(B)
    Gr = exact.i64_matmul(exact.i64_matmul(B, Gd), B.T).astype(np.float64)
    Lc = np.linalg.cholesky(Gr)
    return Bi, Lc
def reduire(w, B, Bi, Lc):
    c = exact.i64_matmul(w[None, :], Bi)[0]
    c = c % 2
    x = c.astype(np.float64) @ Lc
    n = len(c)
    y = np.zeros(n, dtype=np.int64)
    for i in range(n - 1, -1, -1):
        reste = x[i] - 2.0 * float(y[i + 1:].astype(np.float64) @ Lc[i + 1:, i])
        y[i] = int(np.rint(reste / (2.0 * Lc[i, i])))
    c2 = c - 2 * y
    w2 = exact.i64_matmul(c2[None, :], B)[0]
    if ((w2 - w) % 2 != 0).any():
        raise RuntimeError("reduction hors de la classe")
    return w2
PRE56 = prep_reduction(B56, G)
PREL = prep_reduction(BL, GL)

def temoin(xL, v56, etiquette):
    """vecteur z = (x Y1 + v Y2)/2 de X1 (coordonnees entieres dans la base de X1) ; norme exacte."""
    z2 = exact.i64_matmul(xL[None, :], Y1c)[0] + exact.i64_matmul(v56[None, :], Y2c)[0]
    if (z2 % 2 != 0).any():
        return None
    z = z2 // 2
    q = int(z @ GX @ z)
    with open(os.path.join(sortie, "TEMOIN_X%s_%s.txt" % (J, etiquette)), "a") as h:
        h.write("%d : %s\n" % (q, " ".join(map(str, z.tolist()))))
    rep.log("!!! TEMOIN POTENTIEL (%s) : norme %d dans X%s" % (etiquette, q, J))
    return q

def campagne(nom, Gd, Sd, R6d, depart, R6src, coll_x, PRE, Bt):
    d = Descent(Gd, Sd, R6d)
    # temoin positif a la p4 : classes « norme 10 + 2L » plantees
    rng = random.Random(1)
    vec = lambda: R6d[rng.randrange(len(R6d))] @ Sd[rng.randrange(len(Sd))].astype(np.int64)
    ret = fausse = essais = 0
    while essais < 40:
        r, s = vec(), vec()
        ip = int(r @ Gd @ s)
        if abs(ip) != 1:
            continue
        w10 = r - s if ip == 1 else r + s
        shift = sum(rng.choice((-1, 1)) * vec() for _ in range(3))
        w, m, _ = d.descend(w10 + 2 * shift, 60)
        nw = int(w @ Gd @ w); essais += 1
        ret += nw == 10; fausse += (nw in (14, 18) and m <= 6)
    rep.value("%s : temoin positif, descentes revenues a la norme 10" % nom, "%d sur %d" % (ret, essais))
    rep.check("%s : temoin positif, aucun faux certificat" % nom, fausse == 0)
    W = np.zeros((len(R6src), 56), dtype=np.int64); tab = {}; ntem = 0
    for j, r in enumerate(R6src):
        w0 = exact.i64_matmul(r[None, :], depart)[0]
        w0 = reduire(w0, Bt, PRE[0], PRE[1])
        w, m, k = d.descend(w0, 400)
        if j % 50 == 0:
            rep.log("%s : %d / %d descentes (derniere : %d pas, norme finale %d)" % (nom, j, len(R6src), k, int(w @ Gd @ w)))
        nw = int(w @ Gd @ w)
        if not ((w - w0) % 2 == 0).all():
            rep.check("%s : la descente reste dans la classe" % nom, False)
        tab["norme %d, max %d" % (nw, m)] = tab.get("norme %d, max %d" % (nw, m), 0) + 1
        W[j] = w
        if nw < 14:
            ntem += 1
            if coll_x == "phi":
                temoin(r, w, nom)
            else:
                temoin(w, r, nom)
    rep.value("%s : (norme, max |<w,u>|) -> nombre" % nom, dict(sorted(tab.items())))
    rep.value("%s : descentes terminees sous la norme 14 (collisions)" % nom, ntem)
    # controle exact a la v5
    mv = shells.MinimalVectors(Gd, R6d, Sd)
    m = mv.max_abs_inner(W)
    norms = exact.norms(W, Gd)
    okc = np.isin(norms, (14, 18)) & (m <= 6)
    rep.value("%s : certificats valides (norme 14 ou 18, max <= 6)" % nom, int(okc.sum()))
    np.savez_compressed(os.path.join(sortie, "certificats_%s.npz" % nom), w0=W.astype(np.int16), norms=norms, maxip=m)
    return okc, norms, m

ok1, n1, m1 = campagne("phi_L_vers_L56", G, S56, R656, fz, R6L, "phi", PRE56, B56)
rep.check("type (6,6)/(6,10) : un certificat impair pour chacun des %d representants de L_6" % len(R6L), ok1.all())
ok2, n2, m2 = campagne("psi_L56_vers_L", GL, SL, R6L, fiz, R656, "psi", PREL, BL)
rep.check("type (10,6) : un certificat impair pour chacun des 656 representants de L56_6", ok2.all())
rep.finish()
