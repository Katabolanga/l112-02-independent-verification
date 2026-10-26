# donnees_L.py -- lot R112_X1_EFFORT_MAX_20261025 (agent Claude n° 116, 25 oct. 2026). Volet B3, etape « donnees de L ».
# L = Y1/sqrt2 (structure_x1.npz : Gram G_L, generateurs h1, h2 de S = SL_2(29) agissant sur L).
# Calcule : (1) le groupe S_L (24 360 elements, BFS exact, via lib/group.py du depot, LU) ; (2) l'anneau End_S(L) (rang 8) par
#   moyennes de Reynolds EXACTES (entiers) puis saturation (SageMath) ; (3) le centralisateur C_L = elements de norme reduite 1
#   (forme q(X) = tr(X X^+)/56 sur End_S(L) ; enumeration EXACTE en dimension 8 par un Fincke-Pohst en rationnels (code ecrit ici),
#   recoupee par qfminim de PARI) ; (4) un controle de maximalite (discriminant de la forme trace) ; (5) la classe de L :
#   |C_L| = 24 attendu pour L_{56,2}(M) (roiban, S6).
# Sorties : DOSSIER/donnees_L.npz (S_L mod +-1 en int16, commutant, unites C_L mod +-1), DOSSIER/donnees_L.txt.
# Usage : python -I donnees_L.py RACINE_DEPOT STRUCTURE_NPZ DOSSIER   (PATH avec l'env sagefull)
import os, sys, time, hashlib
from fractions import Fraction
import numpy as np
racine, fstruct, sortie = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.join(racine, "code"))
from lib import group, exact
from sage.all import ZZ, QQ, matrix, pari
os.makedirs(sortie, exist_ok=True)
LOG = open(os.path.join(sortie, "donnees_L.txt"), "w")
T0 = time.time()
def log(*a):
    s = " ".join(str(x) for x in a)
    print("[%7.1f s] %s" % (time.time() - T0, s), flush=True); LOG.write("[%7.1f s] %s\n" % (time.time() - T0, s)); LOG.flush()
def ok(label, cond):
    log("[ok]  " if cond else "[ECHEC]", label)
    if not cond:
        raise SystemExit("ECHEC : " + label)

z = np.load(fstruct, allow_pickle=False)
GL = z["G_L"].astype(np.int64); h1 = z["h1"].astype(np.int64); h2 = z["h2"].astype(np.int64)
log("structure", fstruct, "sha256", hashlib.sha256(open(fstruct, "rb").read()).hexdigest())
n = 56
GLinv = exact.inverse_unimodular(GL)
E = group.enumerate_group([h1, h2])
ok("|<h1, h2>| = 24360", len(E) == group.ORDER)
S = group.elements_mod_sign(E)
ok("12180 elements modulo +-1", len(S) == group.ORDER_MOD_SIGN)
log("max |coefficient| des elements de S_L :", int(np.abs(S).max()))
del E

# (2) commutant par Reynolds exacte : R(Ei) = sum_{s in S/+-1} s^-1 Ei s  (s^-1 = G s^T G^-1) ; entiers, bornes controlees.
Sinv = np.stack([exact.i64_matmul(exact.i64_matmul(GL, s.astype(np.int64).T), GLinv) for s in S])
smax = int(np.abs(S).max()); simax = int(np.abs(Sinv).max())
log("max |coefficient| des inverses :", simax)
rng = np.random.default_rng(20261025)
mats = []
for t in range(14):
    Ei = np.zeros((n, n), dtype=np.int64)
    for _ in range(3):
        Ei[rng.integers(n), rng.integers(n)] += int(rng.choice([-1, 1]))
    # borne : |sum_s (s^-1 Ei s)_{ab}| <= |S| * n^2 * simax * max|Ei| * smax
    require_ok = len(S) * n * n * simax * int(np.abs(Ei).max()) * smax < 2 ** 53
    ok("borne d'exactitude float64 de la moyenne (%d)" % t, require_ok)
    acc = np.zeros((n, n), dtype=np.float64)
    Ef = Ei.astype(np.float64)
    for k in range(0, len(S), 2000):
        A = Sinv[k:k + 2000].astype(np.float64); Bm = S[k:k + 2000].astype(np.float64)
        acc += np.einsum("kab,bc,kcd->ad", A, Ef, Bm, optimize=True)
    R = np.rint(acc).astype(np.int64)
    ok("moyenne entiere (float64 exact)", np.abs(acc - R).max() == 0)
    mats.append(R)
# (les moyennes d'elements a trace nulle sont de trace nulle : elles n'engendrent que l'hyperplan Tr trd = 0, de rang 7 ;
#  on ajoute l'identite, qui est dans le commutant -- essai 1 range dans essais/essai1_donnees_L_rang7_trace_nulle)
mats.append(np.eye(n, dtype=np.int64))
Mq = matrix(ZZ, [list(m.reshape(-1)) for m in mats])
r = Mq.rank()
log("rang de l'espace engendre par les moyennes :", r)
ok("commutant de rang 8", r == 8)
Sat = Mq.saturation()                       # lignes : base Z de (Q-espace) ∩ Z^3136 = End_S(L)
Bc = [matrix(ZZ, n, n, list(Sat.row(i))) for i in range(Sat.nrows())]
Bc = [b for b in Bc if b != 0]
ok("8 elements de base", len(Bc) == 8)
H1 = matrix(ZZ, h1.tolist()); H2 = matrix(ZZ, h2.tolist()); GLs = matrix(ZZ, GL.tolist()); GLi = GLs.inverse()
for b in Bc:
    ok("element du commutant (commute a h1, h2)", b * H1 == H1 * b and b * H2 == H2 * b)
# l'identite est dans le Z-module ?
Bm8 = matrix(QQ, [b.list() for b in Bc])
cI = Bm8.solve_left(matrix(QQ, [matrix.identity(n).list()]))
ok("1 dans End_S(L) (coordonnees entieres)", cI.denominator() == 1)
# stabilite par produit (ordre)
okprod = True
for a in Bc:
    for b in Bc:
        c = Bm8.solve_left(matrix(QQ, [(a * b).list()]))
        okprod &= (c.denominator() == 1)
ok("End_S(L) stable par produit (ordre)", okprod)
adjm = [GLs * b.transpose() * GLi for b in Bc]
Q = matrix(QQ, 8, 8, lambda i, j: (Bc[i] * adjm[j]).trace())
Q = (Q + Q.transpose()) / 2
ok("forme q entiere, definie positive", Q.denominator() == 1 and Q.change_ring(ZZ).is_positive_definite())
Qz = Q.change_ring(ZZ)
# forme trace t(x y) = tr(x y)/14 (t = Tr_{K/Q} trd sur W de dimension 56 sur Q = 7 x 8) : discriminant
Tt = matrix(QQ, 8, 8, lambda i, j: (Bc[i] * Bc[j]).trace() / 14)
log("forme trace Tr trd(xy) : det =", Tt.det(), "(ordre maximal : +-29^4 = %d)" % 29 ** 4)

# (3) unites : enumeration exacte des c avec c Q c^T = 56 (q = 1), Fincke-Pohst en rationnels
def fincke_pohst(Qm, borne):
    nq = Qm.nrows()
    A = [[Fraction(int(Qm[i, j])) for j in range(nq)] for i in range(nq)]
    # decomposition de Cholesky rationnelle (LDL) : q(x) = sum_i d_i (x_i + sum_{j>i} m_ij x_j)^2
    d = [Fraction(0)] * nq; m = [[Fraction(0)] * nq for _ in range(nq)]
    for i in range(nq):
        d[i] = A[i][i] - sum(m[k][i] ** 2 * d[k] for k in range(i))
        for j in range(i + 1, nq):
            m[i][j] = (A[i][j] - sum(m[k][i] * m[k][j] * d[k] for k in range(i))) / d[i]
    out = []
    x = [0] * nq
    def rec(i, reste):
        c = -sum(m[i][j] * x[j] for j in range(i + 1, nq))
        # (x_i - c)^2 d_i <= reste
        import math
        rad2 = reste / d[i]
        lo = math.floor(c - Fraction(math.isqrt(int(rad2) + 1) + 1)); hi = math.ceil(c + Fraction(math.isqrt(int(rad2) + 1) + 1))
        for xi in range(lo, hi + 1):
            t = (xi - c) ** 2 * d[i]
            if t <= reste:
                x[i] = xi
                if i == 0:
                    out.append(list(x))
                else:
                    rec(i - 1, reste - t)
        x[i] = 0
    rec(nq - 1, Fraction(borne))
    return out
# reduction LLL de la forme avant l'enumeration (essai 2 sans reduction : trop lent, range dans essais/)
Ucol = matrix(ZZ, pari(Qz).qflllgram().sage())
ok("reduction LLL de q unimodulaire", abs(Ucol.det()) == 1)
Qr = Ucol.transpose() * Qz * Ucol
from sage.all import vector as _vec
vecs = [list(Ucol * _vec(ZZ, v)) for v in fincke_pohst(Qr, 56)]
vecs = [v for v in vecs if any(v)]
vals = [int((matrix(ZZ, [v]) * Qz * matrix(ZZ, [v]).transpose())[0, 0]) for v in vecs]
log("enumeration exacte : vecteurs avec q <= 56 :", len(vecs), " valeurs :", sorted(set(vals)))
units = []
for v, val in zip(vecs, vals):
    X = sum(int(v[i]) * Bc[i] for i in range(8))
    if X * GLs * X.transpose() == GLs:
        units.append(X)
log("isometries trouvees (deux signes) :", len(units))
pv = pari(Qz).qfminim(56, None, 0)
ok("qfminim de PARI : meme nombre de vecteurs (q <= 56)", int(pv[0]) == len(vecs))
ok("|C_L| = 24 (L = L_{56,2}(M), centralisateur d'ordre 24)", len(units) == 24)
half = []
seen = set()
for X in units:
    Xn = np.array(X, dtype=np.int64)
    k = group.sign_normalize(Xn).tobytes()
    if k not in seen:
        seen.add(k); half.append(group.sign_normalize(Xn))
ok("12 elements de C_L modulo +-1", len(half) == 12)
np.savez_compressed(os.path.join(sortie, "donnees_L.npz"), S=S.astype(np.int16),
                    commutant=np.array([np.array(b, dtype=np.int64) for b in Bc]), units=np.stack(half).astype(np.int64))
log("ecrit", os.path.join(sortie, "donnees_L.npz"))
