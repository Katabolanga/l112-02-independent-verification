# isometrie_L4_L1.py -- lot R112_X1_EFFORT_MAX_20261025 (agent Claude n° 116, 25 oct. 2026). Temoin positif X4 (volet B3).
# Isometrie S-EQUIVARIANTE T : L4 -> L1 entre le facteur « type b » de X4 (L4 = Y1/sqrt2 de structure_X4.npz) et celui de X1
# (L1 = Y1/sqrt2 de structure_x1.npz), pour TRANSPORTER les donnees de L1 (orbites, unites) vers L4.
# Methode (code ecrit ici) : les deux groupes <h1, h2> sont enumeres par le meme parcours en largeur (lib/group.py du depot, LU) ;
# comme les deux representations sont fideles et que les generateurs se correspondent, le i-eme element de l'une correspond au
# i-eme de l'autre (controle : memes relations constatees, ordres identiques). Les entrelaceurs h4 T = T h1 s'obtiennent par
# moyennes exactes T = sum_i (E4_i)^-1 M E1_i ; saturation (SageMath) ; puis enumeration exacte (Fincke-Pohst rationnel, apres
# LLL) des T avec q(T) = tr(T G1 T^T G4^-1) = 56, et test exact T G1 T^T = G4.
# Usage : python -I isometrie_L4_L1.py RACINE_DEPOT STRUCT_X1_NPZ STRUCT_X4_NPZ DOSSIER
import os, sys, time
from fractions import Fraction
import math
import numpy as np
racine, f1, f4, sortie = sys.argv[1:5]
sys.path.insert(0, os.path.join(racine, "code"))
from lib import group, exact
from sage.all import ZZ, QQ, matrix, pari, vector
os.makedirs(sortie, exist_ok=True)
LOG = open(os.path.join(sortie, "isometrie_L4_L1.txt"), "w")
T0 = time.time()
def log(*a):
    s = " ".join(str(x) for x in a); print("[%7.1f s] %s" % (time.time() - T0, s), flush=True); LOG.write(s + "\n"); LOG.flush()
def ok(label, cond):
    log("[ok]  " if cond else "[ECHEC]", label)
    if not cond:
        raise SystemExit("ECHEC : " + label)
s1 = np.load(f1, allow_pickle=False); s4 = np.load(f4, allow_pickle=False)
G1 = s1["G_L"].astype(np.int64); G4 = s4["G_L"].astype(np.int64)
a1, b1 = s1["h1"].astype(np.int64), s1["h2"].astype(np.int64)
a4, b4 = s4["h1"].astype(np.int64), s4["h2"].astype(np.int64)
E1 = group.enumerate_group([a1, b1]); E4 = group.enumerate_group([a4, b4])
ok("deux groupes d'ordre 24360", len(E1) == len(E4) == 24360)
# correspondance : meme parcours ; controle par les traces (caractere rationnel identique element par element)
tr1 = np.einsum("kii->k", E1.astype(np.int64)); tr4 = np.einsum("kii->k", E4.astype(np.int64))
ok("traces identiques element par element (correspondance du parcours)", (tr1 == tr4).all())
G4i = exact.inverse_unimodular(G4)
E4inv = np.stack([exact.i64_matmul(exact.i64_matmul(G4, e.astype(np.int64).T), G4i) for e in E4])
rng = np.random.default_rng(4116)
mats = []
for t in range(10):
    Mr = rng.integers(-1, 2, size=(56, 56)).astype(np.int64)
    acc = np.zeros((56, 56), dtype=np.float64)
    bound = len(E1) * 56 * 56 * int(np.abs(E4inv).max()) * int(np.abs(E1).max())
    ok("borne d'exactitude float64 (%d)" % t, bound < 2 ** 53)
    for k in range(0, len(E1), 2000):
        acc += np.einsum("kab,bc,kcd->ad", E4inv[k:k + 2000].astype(np.float64), Mr.astype(np.float64),
                         E1[k:k + 2000].astype(np.float64), optimize=True)
    R = np.rint(acc).astype(np.int64)
    ok("moyenne entiere", np.abs(acc - R).max() == 0)
    mats.append(R)
Mq = matrix(ZZ, [list(m.reshape(-1)) for m in mats])
ok("entrelaceurs : rang 8", Mq.rank() == 8)
Sat = Mq.saturation()
Bt = [matrix(ZZ, 56, 56, list(Sat.row(i))) for i in range(Sat.nrows())]
Bt = [b for b in Bt if b != 0]
A4 = matrix(ZZ, a4.tolist()); B4 = matrix(ZZ, b4.tolist()); A1 = matrix(ZZ, a1.tolist()); B1 = matrix(ZZ, b1.tolist())
for b in Bt:
    ok("h4 T = T h1", A4 * b == b * A1 and B4 * b == b * B1)
G1s = matrix(ZZ, G1.tolist()); G4s = matrix(ZZ, G4.tolist()); G4si = G4s.inverse()
Q = matrix(QQ, 8, 8, lambda i, j: (Bt[i] * G1s * Bt[j].transpose() * G4si).trace())
Q = (Q + Q.transpose()) / 2
ok("forme q entiere definie positive", Q.denominator() == 1 and Q.change_ring(ZZ).is_positive_definite())
Qz = Q.change_ring(ZZ)
Ucol = matrix(ZZ, pari(Qz).qflllgram().sage())
Qr = Ucol.transpose() * Qz * Ucol
def fp(Qm, borne):
    nq = Qm.nrows(); A = [[Fraction(int(Qm[i, j])) for j in range(nq)] for i in range(nq)]
    d = [Fraction(0)] * nq; m = [[Fraction(0)] * nq for _ in range(nq)]
    for i in range(nq):
        d[i] = A[i][i] - sum(m[k][i] ** 2 * d[k] for k in range(i))
        for j in range(i + 1, nq):
            m[i][j] = (A[i][j] - sum(m[k][i] * m[k][j] * d[k] for k in range(i))) / d[i]
    out = []; x = [0] * nq
    def rec(i, reste):
        c = -sum(m[i][j] * x[j] for j in range(i + 1, nq))
        r = math.isqrt(int(reste / d[i]) + 1) + 1
        for xi in range(math.floor(c - r), math.ceil(c + r) + 1):
            t = (xi - c) ** 2 * d[i]
            if t <= reste:
                x[i] = xi
                if i == 0:
                    out.append(list(x))
                else:
                    rec(i - 1, reste - t)
        x[i] = 0
    rec(nq - 1, Fraction(borne)); return out
cands = [list(Ucol * vector(ZZ, v)) for v in fp(Qr, 56) if any(v)]
log("entrelaceurs entiers avec q <= 56 :", len(cands))
isos = []
for c in cands:
    T = sum(int(c[i]) * Bt[i] for i in range(8))
    if T * G1s * T.transpose() == G4s:
        isos.append(T)
log("isometries T avec T G1 T^T = G4 :", len(isos))
ok("au moins une isometrie S-equivariante L4 -> L1", len(isos) > 0)
T = isos[0]
ok("|det T| = 1", abs(T.det()) == 1)
np.savez_compressed(os.path.join(sortie, "isometrie_L4_L1.npz"), T=np.array(T, dtype=np.int64),
                    Tinv=np.array(T.inverse().change_ring(ZZ), dtype=np.int64), nb_isometries=np.int64(len(isos)))
log("ecrit isometrie_L4_L1.npz (x4 T = x1 ; x1 T^-1 = x4)")
