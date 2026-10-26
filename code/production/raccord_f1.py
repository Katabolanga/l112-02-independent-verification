# raccord_f1.py -- lot R112_X1_FICHE_CATALOGUE_20261026 (agent Claude n° 119, 26 oct. 2026). Code ecrit ici (numpy pour lire les
# .npz ; arithmetique EXACTE en entiers et Fraction). RACCORD « entree de enum_interval <-> Gram du reseau » pour F1 (min = 6),
# reserve d'<REVIEWER> du 25 oct. (§ 4 : « raccord integral de cette entree non admis ») :
#   (1) la matrice de Gram ecrite dans l'entree est EXACTEMENT U G U^t, U unimodulaire (det +-1, Bareiss), G la Gram du reseau ;
#   (2) chaque intervalle [lo, hi] de l'entree contient EXACTEMENT le rationnel D_i ou V_ij de la decomposition G' = V^t diag(D) V
#       (LDL exacte en Fraction ; les bornes flottantes sont converties exactement par Fraction(float)) ;
#   (3) le rayon est 4 (enumeration des vecteurs de norme <= 4 ; une seule feuille = le vecteur nul => min >= 6, reseau pair).
# Usage : python -I raccord_f1.py ENTREE GRAM_RESEAU(.txt ou .npz:cle) PASSAGE(.txt ou .npz:cle)
import sys
from fractions import Fraction
import numpy as np


def charge(spec):
    if ".npz:" in spec:
        f, k = spec.split(".npz:")
        return [[int(t) for t in r] for r in np.load(f + ".npz", allow_pickle=False)[k]]
    return [[int(t) for t in l.split()] for l in open(spec, encoding="utf-8") if l.strip() and not l.strip().startswith("#")]


def mm(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(r, c)) for c in Bt] for r in A]


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


fe, fg, fu = sys.argv[1:4]
L = [l.split() for l in open(fe, encoding="ascii")]
n, rayon = int(L[0][0]), int(L[0][1])
Ge = [[int(t) for t in L[1 + i]] for i in range(n)]
ivD = [(float(L[1 + n + i][0]), float(L[1 + n + i][1])) for i in range(n)]
ivV = [(float(a), float(b)) for a, b in L[1 + 2 * n:]]
G = charge(fg)
U = charge(fu)
ok = True
def chk(lab, c):
    global ok
    print(("[ok]    " if c else "[ECHEC] ") + lab, flush=True)
    ok = ok and c
chk("entree : dimension %d, rayon %d (vecteurs de norme <= 4)" % (n, rayon), n == 56 and rayon == 4 and len(ivV) == n * (n - 1) // 2)
dU = det_bareiss(U)
chk("passage U : %d x %d, det = %d (unimodulaire)" % (len(U), len(U[0]), dU), abs(dU) == 1)
Gp = mm(mm(U, G), [list(c) for c in zip(*U)])
chk("Gram de l'entree = U G U^t (egalite exacte des %d coefficients)" % (n * n), Gp == Ge)
# LDL exacte : G' = V^t diag(D) V, V unipotente superieure (convention de lib/exact.ldl_exact : V[i][j], j > i)
A = [[Fraction(x) for x in r] for r in Ge]
D = []
V = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
for k in range(n):
    D.append(A[k][k])
    for j in range(k + 1, n):
        V[k][j] = A[k][j] / A[k][k]
    for i in range(k + 1, n):
        for j in range(k + 1, n):
            A[i][j] -= A[i][k] * A[k][j] / A[k][k]
chk("pivots D_i > 0 (Gram definie positive)", all(d > 0 for d in D))
inD = all(Fraction(lo) <= d <= Fraction(hi) for d, (lo, hi) in zip(D, ivD))
chk("les %d intervalles de D contiennent les D_i exacts" % n, inD)
vals = [V[i][j] for i in range(n) for j in range(i + 1, n)]
inV = all(Fraction(lo) <= v <= Fraction(hi) for v, (lo, hi) in zip(vals, ivV))
chk("les %d intervalles de V contiennent les V_ij exacts" % len(vals), inV)
# reconstruction : G' = V^t diag(D) V
R = [[sum(V[k][i] * D[k] * V[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
chk("controle : V^t diag(D) V = Gram de l'entree", all(R[i][j] == Ge[i][j] for i in range(n) for j in range(n)))
print("RACCORD :", "OK" if ok else "ECHEC", flush=True)
sys.exit(0 if ok else 1)
