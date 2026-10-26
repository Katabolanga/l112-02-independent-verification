# structure_x1.py -- lot R112_X1_EFFORT_MAX_20261025 (agent Claude n° 116, 25 oct. 2026). Volet B2.
# Structure de X1 (classe 1 de roiban = classe 3 de l'agent 112, |U| = 12) comme RECOLLEMENT MODULO 2 de deux reseaux de rang 56,
# calcule ICI de facon independante (code ecrit pour ce lot ; SageMath 10.6 de l'env sagefull pour l'algebre lineaire exacte),
# dans les coordonnees du depot roiban (donnees LUES seulement : data/L56_gram.txt, data/sl2_29_generators.txt,
# certificates/commutant.npz, certificates/genus_basis_1.txt, certificates/genus_class_1.txt).
#
# Notations. L~ = L56 du depot (Gram G, S = <g1, g2> = SL_2(29)), M' = End_S(L~) (base m_0..m_7, action a droite), Q = M' (x) Q.
#   X1 est donne par une base B = D/d dans (L~ (x) Q)^2 muni de diag(G, G)/2.
#   Lambda~ = Hom_S(L~, X1) = { (a, b) dans Q^2 : (x a, x b) dans X1 pour tout x dans L~ } (M'-module a gauche, rang 2),
#   h~((a,b),(a,b)) = (a a^+ + b b^+)/2 (a^+ = G a^T G^-1 : adjoint ; c'est un element central de Q, i.e. de K = Q(sqrt 29)).
#   Un vecteur mu = (a, b) de Lambda~ avec h~(mu, mu) = 2 donne Y2 = { (x a, x b) : x dans L~ } ~ sqrt2 L~ (si Y2 est primitif) ;
#   Y1 = X1 ∩ Y2^perp ; si Gram(Y1)/2 est pair unimodulaire, X1 est le recollement modulo 2 de L := Y1/sqrt2 et de L~ :
#   X1 = { (y1 + y2)/2 : y1 = x.Y1, y2 = v.Y2, v = x f (mod 2) }, de norme (<x,x>_L + <v,v>_L~)/2.
# Sorties (DOSSIER) : structure_x1.npz (G_L, h1, h2 [action de g1, g2 sur L], f [0/1, x -> x f], Y1c, Y2c [coordonnees dans la
#   base de X1], mu, base de Lambda~, Gram de la forme T), structure_x1.txt (journal des controles).
# Usage : python -I structure_x1.py RACINE_DEPOT DOSSIER_SORTIE   (PATH doit contenir l'env sagefull pour SageMath)
import os, sys, hashlib, time
import numpy as np
from sage.all import QQ, ZZ, GF, matrix, block_matrix, identity_matrix, zero_matrix, lcm, pari, vector

racine, sortie = sys.argv[1], sys.argv[2]
os.makedirs(sortie, exist_ok=True)
LOG = open(os.path.join(sortie, "structure_x1.txt"), "w")
T0 = time.time()
def log(*a):
    s = " ".join(str(x) for x in a)
    print("[%7.1f s] %s" % (time.time() - T0, s), flush=True)
    LOG.write("[%7.1f s] %s\n" % (time.time() - T0, s)); LOG.flush()
def ok(label, cond):
    log("[ok]  " if cond else "[ECHEC]", label)
    if not cond:
        raise SystemExit("ECHEC : " + label)
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
def entiers(p):
    v = []
    for l in open(p):
        if l.startswith("#"):
            continue
        v.extend(int(t) for t in l.split())
    return v

fG = os.path.join(racine, "data", "L56_gram.txt"); fgen = os.path.join(racine, "data", "sl2_29_generators.txt")
fB = os.path.join(racine, "certificates", "genus_basis_1.txt"); fX = os.path.join(racine, "certificates", "genus_class_1.txt")
fC = os.path.join(racine, "certificates", "commutant.npz")
for p in (fG, fgen, fB, fX, fC):
    log("entree", os.path.relpath(p, racine), "sha256", sha(p))
G = matrix(ZZ, 56, 56, entiers(fG))
v = entiers(fgen); g1 = matrix(ZZ, 56, 56, v[:3136]); g2 = matrix(ZZ, 56, 56, v[3136:])
v = entiers(fB); d = v[0]; D = matrix(ZZ, 112, 112, v[1:])
GX = matrix(ZZ, 112, 112, entiers(fX))
with np.load(fC, allow_pickle=False) as z:
    mk = [matrix(ZZ, [[int(t) for t in r] for r in m]) for m in z["basis"]]
ok("8 elements de base de M'", len(mk) == 8)
Ginv = G.inverse()
ok("G pair, det 1", G == G.transpose() and all(G[i, i] % 2 == 0 for i in range(56)) and G.det() == 1)
ok("G_X pair, det 1", GX == GX.transpose() and all(GX[i, i] % 2 == 0 for i in range(112)) and GX.det() == 1)
for g in (g1, g2):
    ok("g G g^T = G", g * G * g.transpose() == G)
for m in mk:
    ok("m_k commute a g1, g2", m * g1 == g1 * m and m * g2 == g2 * m)
Z56 = zero_matrix(ZZ, 56)
GG = block_matrix([[G, Z56], [Z56, G]])
ok("D diag(G,G) D^T = 2 d^2 G_X (d = %d)" % d, D * GG * D.transpose() == 2 * d * d * GX)
B = D.change_ring(QQ) / d
P = B.inverse()
gX = []
for g in (g1, g2):
    M = B * block_matrix([[g, Z56], [Z56, g]]) * P
    ok("diag(g, g) agit sur X1 (matrice entiere, isometrie)", M.denominator() == 1 and M * GX * M.transpose() == GX)
    gX.append(M.change_ring(ZZ))

# --- Lambda~ = Hom_S(L~, X1) ---
Phi = []
for k in range(16):
    m = mk[k % 8]
    blk = block_matrix([[m, Z56]]) if k < 8 else block_matrix([[Z56, m]])
    Phi.append((blk.change_ring(QQ) * P).list())
M16 = matrix(QQ, Phi)                       # 16 x 6272 ; c dans Lambda~ <=> c M16 entier
den = M16.denominator()
A = (den * M16).change_ring(ZZ)
Sat = A.saturation()                         # base Z de (Q-espace des lignes) ∩ Z^6272
ok("rang 16", A.rank() == 16 and Sat.nrows() == 16)
LamB = M16.solve_left(Sat.change_ring(QQ))  # 16 x 16 : lignes = base Z de Lambda~ (coordonnees sur (m_k,0),(0,m_k))
ok("Lambda~ : base exacte (c M16 entier pour chaque ligne)", (LamB * M16).denominator() == 1)
log("Lambda~ : denominateur de la base", LamB.denominator(), " ; |det| =", abs(LamB.det()))
def AB(c):
    a = sum(c[k] * mk[k] for k in range(8)); b = sum(c[8 + k] * mk[k] for k in range(8))
    return a, b
def adj(X):
    return G * X.transpose() * Ginv
def H(c):
    a, b = AB(c)
    return (a * adj(a) + b * adj(b)) / 2
# forme T(c, c') = tr((a G a'^T + b G b'^T) G^-1) / 56  (= Tr_{K/Q} h~ sur la diagonale)
basesAB = [AB(LamB.row(i)) for i in range(16)]
def Tb(i, j):
    a, b = basesAB[i]; a2, b2 = basesAB[j]
    return ((a * G * a2.transpose() + b * G * b2.transpose()) * Ginv).trace() / 56
TG = matrix(QQ, 16, 16, lambda i, j: Tb(i, j))
ok("forme T symetrique", TG == TG.transpose())
log("forme T : denominateur", TG.denominator(), "; diagonale", [TG[i, i] for i in range(16)])
TGz = (TG.denominator() * TG).change_ring(ZZ)
ok("forme T definie positive", TGz.is_positive_definite())
borne = 4 * TG.denominator()
res = pari(TGz).qfminim(borne, 10000)
nb = int(res[0]); vecs = matrix(ZZ, res[2].sage())
ok("qfminim : 2 x colonnes = compte", vecs.ncols() == nb // 2)
log("vecteurs de T <= 4 (un par paire) :", nb // 2)
cands = []
for j in range(nb // 2):
    cc = vecs.column(j)
    c = cc * LamB
    Hc = H(c)
    t = (cc * TG * cc)
    if Hc == 2 * identity_matrix(QQ, 56):
        cands.append((cc, c))
    elif Hc == identity_matrix(QQ, 56):
        log("  vecteur avec h~ = 1 (inattendu pour la classe 1) :", list(cc))
log("candidats mu avec h~(mu, mu) = 2 :", len(cands), "(paires)")
ok("au moins un mu avec h~ = 2", len(cands) > 0)

choix = None
for cc, c in cands:
    a, b = AB(c)
    Y2W = block_matrix([[a, b]])             # 56 x 112 dans (L~ (x) Q)^2
    Y2c = Y2W * P
    if Y2c.denominator() != 1:
        continue
    Y2c = Y2c.change_ring(ZZ)
    if Y2c.elementary_divisors() != [1] * 56:
        log("  mu non primitif :", list(cc)); continue
    choix = (cc, c, a, b, Y2c); break
ok("un mu donne Y2 primitif dans X1", choix is not None)
cc, c, a, b, Y2c = choix
log("mu choisi (coordonnees dans la base de Lambda~) :", list(cc))
ok("Gram(Y2) = 2 G", Y2c * GX * Y2c.transpose() == 2 * G)
Mk = GX * Y2c.transpose()                    # 112 x 56
K1 = Mk.left_kernel().basis_matrix()         # base Z (saturee) de Y1 = X1 ∩ Y2^perp
ok("Y1 de rang 56", K1.nrows() == 56)
GY1 = K1 * GX * K1.transpose()
ok("Gram(Y1) a coefficients pairs", all(t % 2 == 0 for t in GY1.list()))
GL = GY1 / 2
GL = GL.change_ring(ZZ)
ok("G_L = Gram(Y1)/2 pair, det 1", all(GL[i, i] % 2 == 0 for i in range(56)) and GL.det() == 1)
# reduction LLL de la base de Y1 (PARI qflllgram, colonnes)
Ucol = matrix(ZZ, pari(GL).qflllgram().sage())   # colonnes = nouvelle base en fonction de l'ancienne
ok("U unimodulaire", Ucol.nrows() == 56 and Ucol.ncols() == 56 and abs(Ucol.det()) == 1)
Y1c = Ucol.transpose() * K1                         # lignes = nouvelle base de Y1
GL = Y1c * GX * Y1c.transpose() / 2
GL = GL.change_ring(ZZ)
log("G_L reduite : diagonale min/max", min(GL.diagonal()), max(GL.diagonal()))
ok("G_L pair det 1", all(GL[i, i] % 2 == 0 for i in range(56)) and GL.det() == 1)
# actions de S
hs = []
for k, M in enumerate(gX):
    ok("Y2 . g_X = g . Y2 (g = g%d agit comme sur L~)" % (k + 1), Y2c * M == (g1 if k == 0 else g2) * Y2c)
    h = Y1c.change_ring(QQ).solve_left((Y1c * M).change_ring(QQ))
    ok("action de g%d sur L entiere, isometrie" % (k + 1), h.denominator() == 1 and h * GL * h.transpose() == GL)
    hs.append(h.change_ring(ZZ))
# recollement
Qm = Y1c.stack(Y2c)
ok("|det [Y1; Y2]| = 2^56", abs(Qm.det()) == 2 ** 56)
C2 = 2 * Qm.inverse()
ok("2 [Y1; Y2]^-1 entiere", C2.denominator() == 1)
C2 = C2.change_ring(ZZ)
F2 = GF(2)
Gam = C2.change_ring(F2)                     # lignes (x_j | v_j) mod 2
ok("Gamma de rang 56", Gam.rank() == 56)
E = Gam.echelon_form()
E = E.matrix_from_rows(range(56))
ok("projection sur x bijective (pivots dans les 56 premieres colonnes)", E.pivots() == tuple(range(56)))
f = E.matrix_from_columns(range(56, 112))   # x -> x f
ok("f inversible", f.rank() == 56)
for k in range(2):
    g = g1 if k == 0 else g2
    ok("f equivariante : h%d f = f g%d (mod 2)" % (k + 1, k + 1), hs[k].change_ring(F2) * f == f * g.change_ring(F2))
# parite : q_L(x) = q_L~(x f) sur une base et sur des sommes
fz = f.change_ring(ZZ)
rng = np.random.default_rng(116)
okp = True
for _ in range(200):
    x = vector(ZZ, [int(t) for t in rng.integers(-2, 3, size=56)])
    y = (x * fz)
    okp &= ((x * GL * x) // 2 - (y * G * y) // 2) % 2 == 0
ok("f preserve la parite (200 tests aleatoires)", okp)
# reconstruction : chaque vecteur de base de X1 = (x.Y1 + v.Y2)/2 avec v = x f mod 2
recon = True
for j in range(112):
    x = C2.row(j)[:56]; vv = C2.row(j)[56:]
    recon &= (vector(F2, list(x)) * f == vector(F2, list(vv)))
    recon &= ((x * Y1c + vv * Y2c) == 2 * vector(ZZ, [int(i == j) for i in range(112)]))
ok("X1 = {(x Y1 + v Y2)/2 : v = x f mod 2} sur la base de X1", recon)
np.savez_compressed(os.path.join(sortie, "structure_x1.npz"),
    G_L=np.array(GL, dtype=np.int64), h1=np.array(hs[0], dtype=np.int64), h2=np.array(hs[1], dtype=np.int64),
    f=np.array(fz, dtype=np.int64), Y1c=np.array(Y1c, dtype=np.int64), Y2c=np.array(Y2c, dtype=np.int64),
    mu=np.array([int(t) for t in cc], dtype=np.int64),
    Lambda_num=np.array(LamB * LamB.denominator(), dtype=np.int64), Lambda_den=np.int64(LamB.denominator()),
    T_num=np.array(TGz, dtype=np.int64), T_den=np.int64(TG.denominator()))
log("ecrit", os.path.join(sortie, "structure_x1.npz"))
log("FIN structure_x1 : X1 est le recollement modulo 2 de L = Y1/sqrt2 (G_L) et de L~ = L56 (G) le long de f")
