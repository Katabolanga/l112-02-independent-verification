# bkz_x1.py -- lot R112_X1_FICHE_CATALOGUE_20261026 (agent Claude n° 119, 26 oct. 2026). Code ecrit ici (fpylll, env g6k de WSL).
# But : une base de X1 COURTE et BIEN CONDITIONNEE (base duale courte, generateurs a petits coefficients), pour le catalogue.
# Constat (essais 1 a 7 de reduction_x1.py, essai de reduction2_x1.py) : les bases gloutonnes de vecteurs de norme 10 sont
# tres mal conditionnees (diagonale de G^-1 jusqu'a 1e40) ; LLL seul plafonne vers une diagonale de 10 a 30.
# Methode : (1) BKZ-beta (fpylll, plongement de Cholesky a l'echelle 2^40, comme g6k_x1.py de l'agent 116) depuis la base de
# roiban ; la base reduite est lue EXACTEMENT par la matrice de passage entiere U de fpylll (B_new = U B), G_new = U G U^t
# recalculee en entiers ; (2) REDUCTION DE SEYSEN exacte (entiers Python) : operations b_j <- b_j + l b_i qui font baisser
# S = sum_i G_ii (G^-1)_ii, l = round((Gi_ij/Gi_jj - G_ij/G_ii)/2), jusqu'a stabilite ; G et G^-1 mis a jour exactement.
# Les flottants ne servent qu'a CHOISIR la base ; tout est verifie en entiers (P unimodulaire, G = P G_X P^t, G Gi = I).
# Usage : python -I bkz_x1.py GRAM_ROIBAN_TXT SORTIE_NPZ [BETAS=20,24]
import sys, time
import numpy as np
from fpylll import IntegerMatrix, GSO, LLL, BKZ
from fpylll.algorithms.bkz2 import BKZReduction

fgx, fout = sys.argv[1:3]
betas = [int(b) for b in (sys.argv[3] if len(sys.argv) > 3 else "20,24").split(",")]
T0 = time.time()
n = 112


def log(*a):
    print("[%7.1f s] %s" % (time.time() - T0, " ".join(str(x) for x in a)), flush=True)


def lignes(f):
    return [[int(t) for t in l.split()] for l in open(f) if l.strip() and not l.strip().startswith("#")]


def mm(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(r, c)) for c in Bt] for r in A]


def tr(A):
    return [list(c) for c in zip(*A)]


def det_bareiss(M):
    A = [r[:] for r in M]
    m, s, prev = len(A), 1, 1
    for k in range(m - 1):
        if A[k][k] == 0:
            p = next((i for i in range(k + 1, m) if A[i][k]), None)
            if p is None:
                return 0
            A[k], A[p] = A[p], A[k]
            s = -s
        for i in range(k + 1, m):
            for j in range(k + 1, m):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return s * A[m - 1][m - 1]


def inverse_exacte(G):
    Gi = np.rint(np.linalg.inv(np.array(G, dtype=float))).astype(object)
    Gi = [[int(x) for x in r] for r in Gi]
    I = mm(G, Gi)
    if any(I[i][j] != (1 if i == j else 0) for i in range(n) for j in range(n)):
        raise SystemExit("inverse non exacte")
    return Gi


GX = lignes(fgx)
P = [[int(i == j) for j in range(n)] for i in range(n)]
G = [r[:] for r in GX]
# (1) BKZ
Lc = np.linalg.cholesky(np.array(G, dtype=float))
A0 = [[int(round(x * 2.0 ** 40)) for x in row] for row in Lc]
for i in range(n):
    for j in range(i + 1, n):
        A0[i][j] = 0
A = IntegerMatrix.from_matrix(A0)
M = GSO.Mat(A, U=IntegerMatrix.identity(n), UinvT=IntegerMatrix.identity(n), float_type="dd")
M.update_gso()
LLL.Reduction(M)()
best = None
for beta in betas:
    t1 = time.time()
    BKZReduction(M)(BKZ.EasyParam(beta, max_loops=8))
    U = [[M.U[i, j] for j in range(n)] for i in range(n)]
    Gn = mm(mm(U, GX), tr(U))
    d = [Gn[i][i] for i in range(n)]
    log("BKZ-%d (%.0f s) : diagonale exacte min %d max %d somme %d ; nombre de 10 : %d" % (beta, time.time() - t1, min(d), max(d), sum(d), d.count(10)))
    if best is None or (max(d), sum(d)) < best[0]:
        best = ((max(d), sum(d)), U, Gn)
_, P, G = best
Gi = inverse_exacte(G)
d, di = [G[i][i] for i in range(n)], [Gi[i][i] for i in range(n)]
log("apres BKZ : diag G min %d max %d ; diag G^-1 min %d max %d ; S = %d" % (min(d), max(d), min(di), max(di), sum(a * b for a, b in zip(d, di))))
np.savez_compressed(fout.replace(".npz", "_bkz.npz"), P=np.array(P, dtype=np.int64), G=np.array(G, dtype=np.int64))
# (2) Seysen
P = [r[:] for r in P]
balayages = 0
while balayages < 200:
    balayages += 1
    gain_total = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            # b_j <- b_j + l b_i  ;  dual : bv_i <- bv_i - l bv_j
            num = Gi[i][j] * G[i][i] - G[i][j] * Gi[j][j]
            den = 2 * G[i][i] * Gi[j][j]
            l = int(round(num / den)) if den else 0
            if l == 0:
                continue
            dS = 2 * l * (G[i][j] * Gi[j][j] - G[i][i] * Gi[i][j]) + 2 * l * l * G[i][i] * Gi[j][j]
            if dS >= 0:
                continue
            # mise a jour exacte de G (ligne et colonne j), de Gi (ligne et colonne i), de P (ligne j)
            Gjj = G[j][j] + 2 * l * G[i][j] + l * l * G[i][i]
            for k in range(n):
                if k != j:
                    G[j][k] += l * G[i][k]
                    G[k][j] = G[j][k]
            G[j][j] = Gjj
            Gii = Gi[i][i] - 2 * l * Gi[i][j] + l * l * Gi[j][j]
            for k in range(n):
                if k != i:
                    Gi[i][k] -= l * Gi[j][k]
                    Gi[k][i] = Gi[i][k]
            Gi[i][i] = Gii
            P[j] = [a + l * b for a, b in zip(P[j], P[i])]
            gain_total += -dS
    d, di = [G[i][i] for i in range(n)], [Gi[i][i] for i in range(n)]
    if balayages % 5 == 1 or gain_total == 0:
        log("Seysen balayage %d : gain %d ; diag G max %d ; diag G^-1 max %d ; S = %d" % (balayages, gain_total, max(d), max(di), sum(a * b for a, b in zip(d, di))))
    if gain_total == 0:
        break
# controles exacts
Gc = mm(mm(P, GX), tr(P))
if Gc != G:
    raise SystemExit("G incoherente apres Seysen")
I = mm(G, Gi)
if any(I[i][j] != (1 if i == j else 0) for i in range(n) for j in range(n)):
    raise SystemExit("G^-1 incoherente apres Seysen")
dt = det_bareiss(P)
if abs(dt) != 1:
    raise SystemExit("P non unimodulaire")
d, di = [G[i][i] for i in range(n)], [Gi[i][i] for i in range(n)]
log("RETENU (BKZ + Seysen) : diag G min %d max %d somme %d (nombre de 10 : %d) ; diag G^-1 min %d max %d ; max |G_ij| %d ; det P = %d"
    % (min(d), max(d), sum(d), d.count(10), min(di), max(di), max(abs(x) for r in G for x in r), dt))
np.savez_compressed(fout, P=np.array(P, dtype=np.int64), G=np.array(G, dtype=np.int64))
log("ecrit", fout)
