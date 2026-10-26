# seysen_pondere_x1.py -- VARIANTE PONDEREE de seysen_insertion_x1.py (agent 119, 26 oct. 2026) : objectif F_K = K sum_i G_ii + sum_i (G^-1)_ii
# (K grand : priorite a la base primale courte, la base duale n'etant que contenue). Pas b_j <- b_j + l b_i :
# l = round((Gi_ij - K G_ij)/(K G_ii + Gi_jj)), dF = K(2 l G_ij + l^2 G_ii) - 2 l Gi_ij + l^2 Gi_jj ; insertion : dF = K(10 - G_jj) +
# sum_{k != j} (a_k^2 Gi_jj - 2 a_k a_j Gi_kj). Usage : python -I seysen_pondere_x1.py DEPART_NPZ RESERVOIR_NPY GRAM_ROIBAN_TXT SORTIE_NPZ K [TOURS]
# (en-tete de la version non ponderee :)
# seysen_insertion_x1.py -- lot R112_X1_FICHE_CATALOGUE_20261026 (agent Claude n° 119, 26 oct. 2026). Code ecrit ici (numpy +
# entiers Python exacts). Recherche locale sur la mesure de Seysen S(B) = sum_i |b_i|^2 |b_i^v|^2 (b^v : base duale ; X1 etant
# unimodulaire, la base duale est aussi une base de X1, et les coefficients des isometries sont bornes par |b_i| |b_j^v|) :
#   (a) INSERTION : un vecteur p de norme 10 du reservoir, de coordonnee a_j = +-1 sur b_j, remplace b_j si S baisse ;
#       nouvelle base duale : b'_j^v = a_j b_j^v, b'_k^v = b_k^v - a_k a_j b_j^v (k != j) ; G, G^-1 mis a jour EXACTEMENT ;
#   (b) SEYSEN : operations b_j <- b_j + l b_i (l = round((Gi_ij/Gi_jj - G_ij/G_ii)/2)) tant que S baisse ;
# jusqu'a stabilite. Depart : la base BKZ + Seysen (bkz_x1.py). Controles exacts a la fin : P unimodulaire (Bareiss),
# G = P G_X P^t, G G^-1 = I, normes du reservoir.
# Usage : python -I seysen_insertion_x1.py DEPART_NPZ RESERVOIR_NPY GRAM_ROIBAN_TXT SORTIE_NPZ [TOURS=60]
import sys, time
import numpy as np

fdep, fres, fgx, fout = sys.argv[1:5]
K = int(sys.argv[5])
tours = int(sys.argv[6]) if len(sys.argv) > 6 else 60
T0 = time.time()
n = 112


def log(*a):
    print("[%7.1f s] %s" % (time.time() - T0, " ".join(str(x) for x in a)), flush=True)


def lignes(f):
    return [[int(t) for t in l.split()] for l in open(f, encoding="utf-8") if l.strip() and not l.strip().startswith("#")]


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


GX = lignes(fgx)
GXn = np.array(GX, dtype=np.int64)
dep = np.load(fdep, allow_pickle=False)
P = [[int(t) for t in r] for r in dep["P"]]
G = mm(mm(P, GX), tr(P))
if [[int(t) for t in r] for r in dep["G"]] != G:
    raise SystemExit("Gram de depart incoherente")
Gi = np.rint(np.linalg.inv(np.array(G, dtype=float))).astype(np.int64).tolist()
if mm(G, Gi) != [[int(i == j) for j in range(n)] for i in range(n)]:
    raise SystemExit("inverse de depart non exacte")
R = np.load(fres, allow_pickle=False).astype(np.int64)
nR = np.einsum("ij,jk,ik->i", R, GXn, R)
if not (nR == 10).all():
    raise SystemExit("reservoir : normes != 10")


def S_of(G, Gi):
    return K * sum(G[i][i] for i in range(n)) + sum(Gi[i][i] for i in range(n))


def coords(P, Gi):
    Pn = np.array(P, dtype=np.int64)
    IP = R @ (GXn @ Pn.T)                      # <p, b_l>
    if int(np.abs(IP).max()) * int(np.abs(np.array(Gi)).max()) * n >= 2 ** 62:
        raise SystemExit("borne int64")
    A = IP @ np.array(Gi, dtype=np.int64)      # a_k = <p, b_k^v>
    if not (A @ Pn == R).all():
        raise SystemExit("coordonnees inexactes")
    return IP, A


def seysen(P, G, Gi, max_bal=100):
    for bal in range(max_bal):
        gain = 0
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                den = K * G[i][i] + Gi[j][j]
                l = int(round((Gi[i][j] - K * G[i][j]) / den))
                if l == 0:
                    continue
                dS = K * (2 * l * G[i][j] + l * l * G[i][i]) - 2 * l * Gi[i][j] + l * l * Gi[j][j]
                if dS >= 0:
                    continue
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
                gain -= dS
        if gain == 0:
            break
    return P, G, Gi


log("depart : diag G min %d max %d ; diag G^-1 max %d ; S = %d" % (min(G[i][i] for i in range(n)), max(G[i][i] for i in range(n)), max(Gi[i][i] for i in range(n)), S_of(G, Gi)))
for tour in range(1, tours + 1):
    IP, A = coords(P, Gi)
    Gd = np.array([G[k][k] for k in range(n)], dtype=np.int64)
    Gin = np.array(Gi, dtype=np.int64)
    ins = 0
    for j in sorted(range(n), key=lambda j: -G[j][j]):
        if G[j][j] == 10:
            continue
        cand = np.nonzero(np.abs(A[:, j]) == 1)[0]
        if len(cand) == 0:
            continue
        Ac = A[cand].astype(object)
        aj = Ac[:, j]
        # dS = (10 - G_jj) Gi_jj + sum_{k != j} G_kk (a_k^2 Gi_jj - 2 a_k a_j Gi_kj)
        Gdo = Gd.astype(object)
        col = Gin[:, j].astype(object)
        t1 = (Ac * Ac) @ Gdo - (aj * aj) * Gd[j]
        t2 = (Ac * (Gdo * col)) @ np.ones(n, dtype=object) - aj * Gd[j] * Gin[j, j]
        t1b = (Ac * Ac) @ np.ones(n, dtype=object) - aj * aj
        t2b = Ac @ col - aj * Gin[j, j]
        dS = K * (10 - G[j][j]) + Gi[j][j] * t1b - 2 * aj * t2b
        b = int(np.argmin(np.array([int(x) for x in dS])))
        if int(dS[b]) >= 0:
            continue
        q = int(cand[b])
        a = [int(x) for x in A[q]]
        e = a[j]
        # mise a jour exacte de G, Gi, P
        newrow = [sum(a[m] * G[m][k] for m in range(n)) for k in range(n)]      # <p, b_k> (anciens b)
        Gi_old_j = Gi[j][:]
        Gjj_old = Gi[j][j]
        Gi_new = [[0] * n for _ in range(n)]
        for k in range(n):
            for l2 in range(k, n):
                if k == j and l2 == j:
                    v = Gjj_old
                elif k == j:
                    v = e * Gi_old_j[l2] - a[l2] * Gjj_old
                elif l2 == j:
                    v = e * Gi_old_j[k] - a[k] * Gjj_old
                else:
                    v = Gi[k][l2] - a[l2] * e * Gi[k][j] - a[k] * e * Gi_old_j[l2] + a[k] * a[l2] * Gjj_old
                Gi_new[k][l2] = Gi_new[l2][k] = v
        Gi = Gi_new
        for k in range(n):
            if k != j:
                G[j][k] = G[k][j] = newrow[k]
        G[j][j] = 10
        P[j] = [int(x) for x in R[q]]
        ins += 1
        # coordonnees du reservoir : mise a jour de rang 1 (exacte)
        colj = A[:, j].copy()
        p_ = A[q].copy()
        A -= np.outer(colj * e, p_)
        A[:, j] = colj * e
        Gd = np.array([G[k][k] for k in range(n)], dtype=np.int64)
        Gin = np.array(Gi, dtype=np.int64)
    P, G, Gi = seysen(P, G, Gi)
    d = [G[i][i] for i in range(n)]
    di = [Gi[i][i] for i in range(n)]
    log("tour %d : %d insertions ; diag G min %d max %d somme %d (nombre de 10 : %d) ; diag G^-1 max %d ; S = %d"
        % (tour, ins, min(d), max(d), sum(d), d.count(10), max(di), S_of(G, Gi)))
    if ins == 0:
        break
# controles exacts
if mm(mm(P, GX), tr(P)) != G:
    raise SystemExit("G incoherente")
if mm(G, Gi) != [[int(i == j) for j in range(n)] for i in range(n)]:
    raise SystemExit("G^-1 incoherente")
dt = det_bareiss(P)
if abs(dt) != 1:
    raise SystemExit("P non unimodulaire")
d = [G[i][i] for i in range(n)]
di = [Gi[i][i] for i in range(n)]
log("RETENU : diag G min %d max %d somme %d (nombre de 10 : %d) ; diag G^-1 min %d max %d ; max |G_ij| %d ; det P = %d"
    % (min(d), max(d), sum(d), d.count(10), min(di), max(di), max(abs(x) for r in G for x in r), dt))
np.savez_compressed(fout, P=np.array(P, dtype=np.int64), G=np.array(G, dtype=np.int64))
log("ecrit", fout)
