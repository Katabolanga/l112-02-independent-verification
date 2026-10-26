# raccord_entrees_f1_rep_v1.py -- paquet de replication X1 pour MACHINE_B (agent Claude n° 121, 26 oct. 2026). Code ecrit ici.
# MEME CONTROLE que raccord_entrees_f1.py (Claude, 26 oct., journal raccord_entrees_f1.log, code 0) et que raccord_f1.py
# (agent 119), mais (1) en BIBLIOTHEQUE STANDARD SEULE (aucun numpy : les .npz sont lus par zipfile + en-tete .npy) et
# (2) avec les chemins en ARGUMENT (aucun chemin Windows en dur). Verifie EXACTEMENT (entiers et Fraction, aucun flottant
# dans les conclusions) que l'entree lue par enum_interval :
#   (1) porte une Gram M = U G U^T avec U entiere de det +-1, pour L (= L56,2(M) de X1, G_L de structure_x1.npz ; de plus
#       M = Gr de reduction_L_bkz40.npz) et pour L56 (Gram de roiban, U = certificates/reduction_L.txt) ;
#   (2) porte des intervalles [lo, hi] qui CONTIENNENT les D_i et V_ij exacts de M = V^T diag(D) V (format de lib/enumerate.py
#       de roiban : n rayon, n lignes de M, puis n intervalles D puis n(n-1)/2 intervalles V, rien d'autre), et D > 0.
# Usage : python3 -I raccord_entrees_f1_rep_v1.py DONNEES_FIGEES      (sortie 0 = BILAN : OK ; 1 = ECHEC ; 2 = donnee manquante)
import hashlib, os, re, sys, zipfile, ast, struct
from fractions import Fraction

if len(sys.argv) != 2:
    print("usage : raccord_entrees_f1_rep_v1.py DONNEES_FIGEES", flush=True); sys.exit(2)
DF = sys.argv[1]
F_EL = os.path.join(DF, "F1", "L_bkz40_rayon4.entree")
F_ST = os.path.join(DF, "X1", "structure_x1.npz")
F_RD = os.path.join(DF, "F1", "reduction_L_bkz40.npz")
F_E56 = os.path.join(DF, "F1", "L56.entree")
F_G56 = os.path.join(DF, "roiban_112", "data", "L56_gram.txt")
F_U56 = os.path.join(DF, "roiban_112", "certificates", "reduction_L.txt")
manq = [p for p in (F_EL, F_ST, F_RD, F_E56, F_G56, F_U56) if not os.path.isfile(p)]
if manq:
    print("DONNEES MANQUANTES (arret avant tout calcul) :", manq, flush=True); sys.exit(2)

_DT = {"<i8": ("q", 8), "<i4": ("i", 4), "<i2": ("h", 2), "|i1": ("b", 1), "<u8": ("Q", 8), "<u4": ("I", 4), "<u2": ("H", 2), "|u1": ("B", 1)}


def npz_tableau(p, cle):
    """lit le tableau entier `cle` d'un .npz (format .npy 1.0/2.0/3.0) en listes Python ; bibliotheque standard seule"""
    with zipfile.ZipFile(p) as z:
        raw = z.read(cle + ".npy")
    if raw[:6] != b"\x93NUMPY":
        raise ValueError("pas un .npy : %s/%s" % (p, cle))
    maj = raw[6]
    if maj == 1:
        hl = struct.unpack("<H", raw[8:10])[0]; deb = 10
    else:
        hl = struct.unpack("<I", raw[8:12])[0]; deb = 12
    h = ast.literal_eval(raw[deb:deb + hl].decode("latin1"))
    if h["descr"] not in _DT:
        raise ValueError("type non pris en charge : %r" % (h["descr"],))
    code, taille = _DT[h["descr"]]
    shape = tuple(h["shape"]); n = 1
    for s in shape:
        n *= s
    data = raw[deb + hl:]
    if len(data) != n * taille:
        raise ValueError("taille incoherente dans %s/%s" % (p, cle))
    vals = list(struct.unpack("<%d%s" % (n, code), data))
    if len(shape) == 0:
        return vals[0]
    if len(shape) != 2:
        raise ValueError("seuls les tableaux 0-d ou 2-d sont pris en charge ici")
    a, b = shape
    if h["fortran_order"]:
        return [[vals[j * a + i] for j in range(b)] for i in range(a)]
    return [vals[i * b:(i + 1) * b] for i in range(a)]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def lire_entree(p):
    L = open(p, encoding="utf-8").read().split("\n")
    n, rayon = map(int, L[0].split())
    M = [[int(t) for t in L[1 + i].split()] for i in range(n)]
    iv = [tuple(Fraction(float(t)) for t in L[1 + n + k].split()) for k in range(n + n * (n - 1) // 2)]
    reste = [l for l in L[1 + n + n + n * (n - 1) // 2:] if l.strip()]
    return n, rayon, M, iv, reste


def entiers(p):
    out = []
    for l in open(p, encoding="utf-8"):
        if l.lstrip().startswith("#"):
            continue
        out += [int(t) for t in re.findall(r"-?\d+", l)]
    return out


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def tr(A):
    return [list(r) for r in zip(*A)]


def det_bareiss(A):
    M = [list(r) for r in A]; n = len(M); s = 1; prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            for i in range(k + 1, n):
                if M[i][k] != 0:
                    M[k], M[i] = M[i], M[k]; s = -s; break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return s * M[n - 1][n - 1]


def ldl(G):   # G = V^T diag(D) V, V unitriangulaire superieure ; V[k][a] = Lw[a][k] ; tout en Fraction
    n = len(G); Lw = [[Fraction(0)] * n for _ in range(n)]; D = [Fraction(0)] * n
    for j in range(n):
        D[j] = Fraction(G[j][j]) - sum((Lw[j][k] ** 2 * D[k] for k in range(j)), Fraction(0))
        Lw[j][j] = Fraction(1)
        for i in range(j + 1, n):
            Lw[i][j] = (Fraction(G[i][j]) - sum((Lw[i][k] * Lw[j][k] * D[k] for k in range(j)), Fraction(0))) / D[j]
    return D, [[Lw[j][i] for j in range(n)] for i in range(n)]


def intervalles_ok(M, iv):
    n = len(M); D, V = ldl(M); vals = list(D) + [V[i][j] for i in range(n) for j in range(i + 1, n)]
    mauvais = [k for k, (v, (lo, hi)) in enumerate(zip(vals, iv)) if not (lo <= v <= hi)]
    return len(mauvais) == 0, len(vals), mauvais[:5], min(D) > 0


ok = True
# --- L = L56,2(M) ---
n, rayon, M, iv, reste = lire_entree(F_EL)
GL = npz_tableau(F_ST, "G_L"); U = npz_tableau(F_RD, "U"); Gr = npz_tableau(F_RD, "Gr")
c1 = (n, rayon, len(reste)) == (56, 4, 0); c2 = M == Gr; c3 = mul(mul(U, GL), tr(U)) == M; d = det_bareiss(U); c4 = abs(d) == 1
c5, nv, mv, pos = intervalles_ok(M, iv)
print("L   : %s (sha %s) n=%d rayon=%d ; entree == Gr : %s ; entree == U G_L U^T : %s ; det U = %d ; %d intervalles contiennent les valeurs exactes : %s %s ; D > 0 : %s" % (os.path.basename(F_EL), sha(F_EL)[:16], n, rayon, c2, c3, d, nv, c5, mv, pos), flush=True)
ok &= c1 and c2 and c3 and c4 and c5 and pos
# --- L56 (roiban) ---
n, rayon, M, iv, reste = lire_entree(F_E56)
G = entiers(F_G56); okG = len(G) == 56 * 56; G = [G[i * 56:(i + 1) * 56] for i in range(56)]
U = entiers(F_U56); okU = len(U) == 56 * 56; U = [U[i * 56:(i + 1) * 56] for i in range(56)]
c1 = (n, rayon, len(reste)) == (56, 4, 0) and okG and okU; c3 = mul(mul(U, G), tr(U)) == M; d = det_bareiss(U); c4 = abs(d) == 1
c5, nv, mv, pos = intervalles_ok(M, iv)
print("L56 : %s (sha %s) n=%d rayon=%d ; entree == U G U^T : %s ; det U = %d ; %d intervalles contiennent les valeurs exactes : %s %s ; D > 0 : %s ; G sha %s ; U sha %s" % (os.path.basename(F_E56), sha(F_E56)[:16], n, rayon, c3, d, nv, c5, mv, pos, sha(F_G56)[:16], sha(F_U56)[:16]), flush=True)
ok &= c1 and c3 and c4 and c5 and pos
print("BILAN : OK" if ok else "BILAN : ECHEC", flush=True)
sys.exit(0 if ok else 1)
