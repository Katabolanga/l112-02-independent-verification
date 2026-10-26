# groupe_x1.py -- lot R112_X1_FICHE_CATALOGUE_20261026 (agent Claude n° 119, 26 oct. 2026). Code ecrit ici (SageMath 10.6,
# env sagefull de WSL), sur le modele de la methode du § 8 de roiban1344 (article, theoreme B) ; aucune bibliotheque du
# depot de roiban n'est importee : seuls ses FICHIERS DE DONNEES sont lus (SHA-256 controles par ailleurs).
#
# X1 = classe 1 du genre de roiban : base genus_basis_1.txt (D = d B, d = 5, coordonnees de (L56 (x) Q)^2, forme
# diag(G, G)/2), Gram genus_class_1.txt. S = SL_2(29) agit diagonalement : s = D diag(g, g) D^-1.
# (1) verifications exactes (Gram, S, U(Lambda_1) du lot X1) ;
# (2) CENTRALISATEUR EXACT : les endomorphismes de V commutant a S sont les matrices par blocs [[a, b], [c, d]],
#     a, b, c, d dans M' (x) Q (M' = commutant.npz, rang 8) : espace de dimension 32 ; ceux qui preservent X1 forment un
#     Z-reseau H de rang 32 (dual du Z-module engendre par les lignes de coefficients) ; sur H, Q(T) = tr(G_X^-1 T G_X T^t)
#     est definie positive et vaut 112 sur les isometries : on ENUMERE EXACTEMENT les T avec Q(T) <= 112 (enum_exact.py,
#     rationnels exacts ; recoupe par qfminim de PARI) et on teste T G_X T^t = G_X en entiers ;
# (3) AUTOMORPHISME EXTERIEUR : un entrelaceur tordu a (g a = a alpha(g)) est extrait du certificat de roiban
#     outer_automorphism_L112.txt (bloc de la matrice ambiante) ; l'espace tordu sur V est {[[m a, ...]] : m dans M'} ;
#     meme enumeration exacte ; T trouve est verifie : isometrie entiere de X1, T^-1 s T dans S, et EXTERIEUR (GAP :
#     l'automorphisme induit n'est pas interieur ; T hors de S C(S)) ;
# (4) GAP (reduction modulo 3, injective sur un groupe fini de matrices entieres, Minkowski) : ordre de <S, C(S), T>,
#     structure de C(S), de N/S, centre, scission, determinants ; nouveaux generateurs de S d'ordres 29 et 4 ;
# (5) controle « diagonal » de l'annexe F.4 (c) de roiban, transpose a X1 : pour chaque involution c != +-1 de C(S),
#     g -> P_- g + P_+ ne preserve pas X1.
# Usage : python -I groupe_x1.py ENTREES SORTIE
import os, sys, time, json, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[0])))
from enum_exact import vecteurs_courts
from sage.all import ZZ, QQ, GF, matrix, identity_matrix, zero_matrix, block_matrix, libgap, pari, lcm

ENT, SORTIE = sys.argv[1:3]
os.makedirs(SORTIE, exist_ok=True)
LOG = open(os.path.join(SORTIE, "groupe_x1.log"), "w")
T0 = time.time()
RES = {}


def log(*a):
    s = " ".join(str(x) for x in a)
    print("[%7.1f s] %s" % (time.time() - T0, s), flush=True)
    LOG.write("[%7.1f s] %s\n" % (time.time() - T0, s))
    LOG.flush()


def ok(label, cond):
    log("[ok]   " if cond else "[ECHEC]", label)
    if not cond:
        raise SystemExit("ECHEC : " + label)


def sha(f):
    return hashlib.sha256(open(f, "rb").read()).hexdigest()


def lignes(f):
    out = []
    for l in open(f):
        l = l.strip()
        if l and not l.startswith("#"):
            out.append([int(t) for t in l.split()])
    return out


def entier(M):
    return all(x in ZZ for x in M.list())


for nom in ("L56_gram.txt", "sl2_29_generators.txt", "commutant.npz", "genus_basis_1.txt", "genus_class_1.txt",
            "U_X1_base_roiban.npz", "outer_automorphism_L112.txt", "tau.txt"):
    log("entree", nom, "sha256", sha(os.path.join(ENT, nom)))

# ---------------------------------------------------------------- (1) donnees et verifications exactes
G = matrix(ZZ, lignes(os.path.join(ENT, "L56_gram.txt")))
r = lignes(os.path.join(ENT, "sl2_29_generators.txt"))
g1, g2 = matrix(ZZ, r[:56]), matrix(ZZ, r[56:112])
I56 = identity_matrix(ZZ, 56)
ok("L56 : Gram 56 x 56 symetrique paire de det 1", G.nrows() == 56 and G == G.transpose() and all(G[i, i] % 2 == 0 for i in range(56)) and G.det() == 1)
ok("g1, g2 : isometries de L56", all(g * G * g.transpose() == G for g in (g1, g2)))
ok("ordres de g1, g2 : 5 et 7", g1 ** 5 == I56 and g1 != I56 and g2 ** 7 == I56 and g2 != I56)
comm = [matrix(ZZ, m.tolist()) for m in np.load(os.path.join(ENT, "commutant.npz"), allow_pickle=False)["basis"]]
ok("M' : 8 matrices commutant a g1, g2", len(comm) == 8 and all(m * g == g * m for m in comm for g in (g1, g2)))
ok("M' : Q-libre de rang 8", matrix(QQ, [m.list() for m in comm]).rank() == 8)
rb = lignes(os.path.join(ENT, "genus_basis_1.txt"))
d = rb[0][0]
Dm = matrix(ZZ, rb[1:113])
GX = matrix(ZZ, lignes(os.path.join(ENT, "genus_class_1.txt")))
ok("G_X (genus_class_1) : 112 x 112 symetrique paire de det 1", GX.nrows() == 112 and GX == GX.transpose() and all(GX[i, i] % 2 == 0 for i in range(112)) and GX.det() == 1)
G2 = block_matrix(ZZ, [[G, 0], [0, G]], subdivide=False)
ok("D diag(G, G) D^t = 2 d^2 G_X (d = %d) : la base de genus_basis_1 realise G_X" % d, Dm * G2 * Dm.transpose() == 2 * d * d * GX)
Dq = Dm.change_ring(QQ)
Di = Dq.inverse()
GXi = GX.inverse()
ok("G_X^-1 entiere", entier(GXi))
GXi = GXi.change_ring(ZZ)
I112 = identity_matrix(ZZ, 112)


def surX(phi):
    """matrice ambiante (112 x 112, rationnelle) -> matrice dans la base de X1 (D phi D^-1)."""
    return Dq * phi.change_ring(QQ) * Di


S0 = []
for g in (g1, g2):
    M = surX(block_matrix(QQ, [[g, 0], [0, g]], subdivide=False))
    ok("D diag(g, g) D^-1 entiere (S preserve X1)", entier(M))
    M = M.change_ring(ZZ)
    ok("isometrie de X1", M * GX * M.transpose() == GX)
    S0.append(M)
U12 = [matrix(ZZ, u.tolist()) for u in np.load(os.path.join(ENT, "U_X1_base_roiban.npz"), allow_pickle=False)["U"]]
ok("U(Lambda_1) du lot X1 : 12 isometries entieres de X1 commutant a S", len(U12) == 12 and all(u * GX * u.transpose() == GX and all(u * s == s * u for s in S0) for u in U12))
setU = {tuple(u.list()) for u in U12}
ok("U(Lambda_1) : ferme par produit, 12 elements distincts", len(setU) == 12 and all(tuple((u * v).list()) in setU for u in U12 for v in U12))
ordres = sorted(int(next(k for k in range(1, 13) if u ** k == I112)) for u in U12)
log("ordres des elements de U(Lambda_1) :", ordres)
ok("U(Lambda_1) abelien, distribution des ordres de C2 x C6 [1,2,2,2,3,3,6,6,6,6,6,6]", all(u * v == v * u for u in U12 for v in U12) and ordres == [1, 2, 2, 2, 3, 3, 6, 6, 6, 6, 6, 6])
RES["ordres_U"] = ordres


# ---------------------------------------------------------------- (2) et (3) : enumeration sur le reseau H
def reseau_H(blocs8, etiquette):
    """blocs8 : 8 matrices 56 x 56 (rationnelles) engendrant un espace de blocs ; renvoie (Ts, 2Q) : base de H (matrices
    entieres dans la base de X1) et la forme 2Q(T) = 2 tr(G_X^-1 T G_X T^t) sur cette base."""
    Zq = zero_matrix(QQ, 56, 56)
    gens = []
    for t in blocs8:
        for pos in range(4):
            bl = [[Zq, Zq], [Zq, Zq]]
            bl[pos // 2][pos % 2] = t.change_ring(QQ)
            gens.append(surX(block_matrix(QQ, bl, subdivide=False)))
    k = len(gens)
    ok(etiquette + " : 32 generateurs Q-independants", matrix(QQ, [g.list() for g in gens]).rank() == k)
    lignesc = {tuple(col) for col in zip(*[g.list() for g in gens])}
    lignesc.discard(tuple([QQ(0)] * k))
    lignesc = [list(x) for x in lignesc]
    den = lcm([QQ(x).denominator() for l in lignesc for x in l])
    span = matrix(ZZ, 0, k)
    for i in range(0, len(lignesc), 200):
        span = span.stack(matrix(ZZ, [[int(den * x) for x in l] for l in lignesc[i:i + 200]])).hermite_form(include_zero_rows=False)
    ok(etiquette + " : lignes de coefficients de rang plein 32", span.nrows() == k)
    Hb = (span.change_ring(QQ) / den).inverse().transpose()
    Ts = []
    for row in Hb.rows():
        T = sum(c * g for c, g in zip(row, gens))
        ok(etiquette + " : element de base de H entier", entier(T)) if len(Ts) == 0 else None
        if not entier(T):
            raise SystemExit("element de base de H non entier")
        Ts.append(T.change_ring(ZZ))
    # contre-epreuve : H est exactement l'ensemble des combinaisons entieres -> Hb^-1 * (coefficients de chaque gen) entier
    Ys = [GXi * T * GX for T in Ts]
    Qm = matrix(ZZ, [Y.list() for Y in Ys]) * matrix(ZZ, [T.list() for T in Ts]).transpose()
    Q2 = Qm + Qm.transpose()
    ok(etiquette + " : 2Q definie positive sur H", Q2.is_positive_definite())
    return Ts, Q2


def enumerer(Ts, Q2, etiquette):
    """toutes les isometries de X1 (au signe pres) dans H : enumeration EXACTE de 2Q <= 224, recoupee par qfminim."""
    U = pari(Q2).qflllgram().sage()
    ok(etiquette + " : changement de base LLL unimodulaire", abs(U.det()) == 1)
    Qr = U.transpose() * Q2 * U
    t1 = time.time()
    exacts, noeuds = vecteurs_courts([[int(x) for x in row] for row in Qr.rows()], 224, QQ)
    t_ex = time.time() - t1
    vp = pari(Qr).qfminim(224, None, 0)[2]
    pl = [tuple(int(x) for x in c) for c in matrix(ZZ, vp).columns()] if vp.ncols() else []
    sgn = lambda w: tuple(w) if next(x for x in w if x) > 0 else tuple(-x for x in w)  # noqa: E731
    e_set = {sgn(v) for v, _ in exacts}
    p_set = {sgn(v) for v in pl}
    log(etiquette, ": vecteurs avec Q <= 112 (au signe pres) : exact", len(e_set), "(%d noeuds, %.1f s)" % (noeuds, t_ex), "; qfminim", len(p_set))
    ok(etiquette + " : enumeration exacte et qfminim de PARI donnent le meme ensemble", e_set == p_set)
    vals = sorted(v for _, v in exacts)
    log(etiquette, ": valeurs de 2Q des candidats :", vals)
    isos = []
    for v, _ in exacts:
        c = U * matrix(ZZ, len(v), 1, v)
        T = sum(int(c[i, 0]) * Ts[i] for i in range(len(Ts)))
        if T * GX * T.transpose() == GX:
            isos.append(T)
    return isos, len(e_set), noeuds


Ts_c, Q2_c = reseau_H(comm, "centralisateur")
iso_c, ncand_c, nn_c = enumerer(Ts_c, Q2_c, "centralisateur")
C12 = iso_c + [-T for T in iso_c]
log("|C_Aut(X1)(S)| =", len(C12), "(candidats Q <= 112 au signe pres :", ncand_c, ")")
ok("|C_Aut(X1)(S)| = 12 EXACTEMENT (enumeration exacte complete)", len(C12) == 12)
ok("C(S) calcule ici = U(Lambda_1) du lot X1 (meme ensemble de 12 matrices)", {tuple(T.list()) for T in C12} == setU)
ok("chaque element de C(S) commute a S", all(T * s == s * T for T in C12 for s in S0))
RES["centralisateur"] = {"ordre": len(C12), "candidats_Q_le_112_au_signe_pres": ncand_c, "noeuds_enumeration_exacte": nn_c}

# entrelaceur tordu extrait du certificat de roiban (L112)
tau = matrix(ZZ, lignes(os.path.join(ENT, "tau.txt")))
Xo = matrix(ZZ, lignes(os.path.join(ENT, "outer_automorphism_L112.txt")))
B112 = block_matrix(QQ, [[I56, tau], [zero_matrix(ZZ, 56, 56), 2 * I56]], subdivide=False)
G112 = B112 * block_matrix(QQ, [[G, 0], [0, G]], subdivide=False) / 2 * B112.transpose()
ok("L112 : Gram (3.1) entiere de det 1", entier(G112) and G112.det() == 1)
ok("outer_automorphism_L112.txt : isometrie de L112", Xo * G112.change_ring(ZZ) * Xo.transpose() == G112.change_ring(ZZ))
Xa = B112.inverse() * Xo.change_ring(QQ) * B112
blocs = [Xa[:56, :56], Xa[:56, 56:], Xa[56:, :56], Xa[56:, 56:]]
a0 = next(b for b in blocs if b.rank() == 56)
alpha = []
for g in (g1, g2):
    ga = a0.inverse() * g * a0
    ok("alpha(g) = a^-1 g a : matrice entiere, isometrie de L56", entier(ga) and ga.change_ring(ZZ) * G * ga.change_ring(ZZ).transpose() == G)
    alpha.append(ga.change_ring(ZZ))
ok("le certificat de roiban induit alpha sur S (X^-1 diag(g,g) X = diag(alpha(g), alpha(g)) en coordonnees ambiantes)",
   all(Xa.inverse() * block_matrix(QQ, [[g, 0], [0, g]], subdivide=False) * Xa == block_matrix(QQ, [[ga, 0], [0, ga]], subdivide=False) for g, ga in zip((g1, g2), alpha)))
ok("ordres de alpha(g1), alpha(g2) : 5 et 7", alpha[0] ** 5 == I56 and alpha[0] != I56 and alpha[1] ** 7 == I56 and alpha[1] != I56)
tw = [m.change_ring(QQ) * a0 for m in comm]
ok("espace tordu {m a} : 8 matrices Q-independantes, g (m a) = (m a) alpha(g)", matrix(QQ, [t.list() for t in tw]).rank() == 8 and all(g * t == t * ga for t in tw for g, ga in zip((g1, g2), alpha)))
Ts_t, Q2_t = reseau_H(tw, "tordu")
iso_t, ncand_t, nn_t = enumerer(Ts_t, Q2_t, "tordu")
log("isometries de X1 induisant alpha (au signe pres) :", len(iso_t), "(candidats :", ncand_t, ")")
ok("au moins une isometrie T de X1 induisant alpha", len(iso_t) > 0)
SX_alpha = [surX(block_matrix(QQ, [[ga, 0], [0, ga]], subdivide=False)) for ga in alpha]
ok("alpha(s) agit sur X1 (matrices entieres)", all(entier(M) for M in SX_alpha))
SX_alpha = [M.change_ring(ZZ) for M in SX_alpha]
Tsol = iso_t[0]
Tinv = Tsol.inverse().change_ring(ZZ)
ok("T : isometrie entiere de X1, det = +-1", Tsol * GX * Tsol.transpose() == GX and abs(Tsol.det()) == 1)
ok("T^-1 s T = alpha(s) pour les deux generateurs (T normalise S)", all(Tinv * s * Tsol == sa for s, sa in zip(S0, SX_alpha)))
ok("toutes les isometries trouvees induisent alpha", all(T.inverse() * s * T == sa for T in iso_t for s, sa in zip(S0, SX_alpha)))
RES["tordu"] = {"isometries_au_signe_pres": len(iso_t), "candidats_Q_le_112_au_signe_pres": ncand_t, "noeuds_enumeration_exacte": nn_t}

np.savez_compressed(os.path.join(SORTIE, "groupe_x1_base_roiban.npz"), GX=np.array(GX, dtype=np.int64),
                    S_g1g2=np.array([np.array(M, dtype=np.int64) for M in S0]),
                    C=np.array([np.array(M, dtype=np.int64) for M in C12]),
                    T_tous=np.array([np.array(M, dtype=np.int64) for M in iso_t]),
                    alpha_L56=np.array([np.array(M, dtype=np.int64) for M in alpha]))
log("ecrit groupe_x1_base_roiban.npz (point de reprise)")

# ---------------------------------------------------------------- (5) controle diagonal (annexe F.4 (c), transpose)
invs = [c for c in C12 if c * c == I112 and c != I112 and c != -I112]
surv = 0
traces = []
for c in invs:
    Pm = (I112 - c).change_ring(QQ) / 2
    Pp = (I112 + c).change_ring(QQ) / 2
    traces.append(int(c.trace()))
    surv += all(entier(Pm * s + Pp) for s in S0)
log("involutions != +-1 de C(S) :", len(invs), "; traces :", traces)
ok("controle diagonal : pour chaque involution c != +-1 de C(S), g -> P_- g + P_+ ne preserve pas X1", surv == 0 and len(invs) == 2)
RES["diagonal"] = {"involutions": len(invs), "traces": traces, "survivantes": surv}

# ---------------------------------------------------------------- (4) GAP, reduction modulo 3
F3 = GF(3)
L3 = lambda Ms: [libgap(M.change_ring(F3)) for M in Ms]  # noqa: E731
Gr = libgap.Group(L3([g1, g2]))
ok("<g1, g2> mod 3 : ordre 24360", int(Gr.Size()) == 24360)
hom = libgap.GroupHomomorphismByImages(Gr, Gr, L3([g1, g2]), L3(alpha))
ok("g -> alpha(g) definit un automorphisme de S", hom != libgap.eval("fail") and bool(libgap.IsBijective(hom)))
ok("alpha N'EST PAS interieur (GAP, IsInnerAutomorphism)", not bool(libgap.IsInnerAutomorphism(hom)))
# nouveaux generateurs d'ordres 29 et 4
epi = libgap.EpimorphismFromFreeGroup(Gr)
invg = [g1.inverse().change_ring(ZZ), g2.inverse().change_ring(ZZ)]


def relever(elt):
    mot = libgap.LetterRepAssocWord(libgap.PreImagesRepresentative(epi, elt)).sage()
    A = identity_matrix(ZZ, 56)
    for e in mot:
        A = A * ((g1, g2)[e - 1] if e > 0 else invg[-e - 1])
    return A, len(mot)


libgap.eval("function() Reset(GlobalMersenneTwister, 119); Reset(GlobalRandomSource, 119); return true; end")()
a29 = b4 = None
for essai in range(2000):
    x = libgap.PseudoRandom(Gr)
    o = int(libgap.Order(x))
    if a29 is None and o == 29:
        a29 = x
    if b4 is None and o == 4:
        b4 = x
    if a29 is not None and b4 is not None:
        if int(libgap.Size(libgap.Group([a29, b4]))) == 24360:
            break
        b4 = None
ok("generateurs d'ordres 29 et 4 engendrant S (mod 3)", a29 is not None and b4 is not None and int(libgap.Size(libgap.Group([a29, b4]))) == 24360)
A29, l29 = relever(a29)
B4, l4 = relever(b4)
ok("relevements entiers : reductions mod 3 egales aux elements choisis", libgap(A29.change_ring(F3)) == a29 and libgap(B4.change_ring(F3)) == b4)
ok("ordres exacts sur L56 : a^29 = 1 != a ; b^4 = 1, b^2 = -1", A29 ** 29 == I56 and A29 != I56 and B4 ** 4 == I56 and B4 ** 2 == -I56)
Snew = [surX(block_matrix(QQ, [[A, 0], [0, A]], subdivide=False)) for A in (A29, B4)]
ok("a, b agissent sur X1 (entiers, isometries)", all(entier(M) for M in Snew) and all(M.change_ring(ZZ) * GX * M.change_ring(ZZ).transpose() == GX for M in Snew))
Snew = [M.change_ring(ZZ) for M in Snew]
ok("ordres exacts sur X1 : 29 et 4", Snew[0] ** 29 == I112 and Snew[0] != I112 and Snew[1] ** 4 == I112 and Snew[1] ** 2 == -I112)
Sx = libgap.Group(L3(S0))
ok("<a, b> = <s1, s2> sur X1 (mod 3, ordre 24360)", int(Sx.Size()) == 24360 and int(libgap.Size(libgap.ClosureGroup(Sx, libgap.Group(L3(Snew))))) == 24360)
# generateurs de C(S) = C2 x C6
c6 = next(c for c in C12 if c ** 6 == I112 and c ** 3 != I112 and c ** 2 != I112)
c2 = next(c for c in C12 if c * c == I112 and c != I112 and c != -I112 and c != c6 ** 3)
Cg = libgap.Group(L3([c2, c6]))
ok("C(S) = <c2, c6> (ordres 2 et 6), d'ordre 12", int(Cg.Size()) == 12)
RES["C_structure"] = str(libgap.StructureDescription(Cg))
log("C(S) : StructureDescription =", RES["C_structure"], "; IdGroup =", libgap.IdGroup(Cg))
A = libgap.Group(L3(Snew + [c2, c6, Tsol]))
t1 = time.time()
ordre = int(A.Size())
log("|<a, b, c2, c6, T>| (GAP, mod 3) =", ordre, "(%.1f s)" % (time.time() - t1))
ok("ordre du groupe engendre = 292320 = 2 x 24360 x 12 / 2", ordre == 292320)
RES["ordre_N"] = ordre
SC = libgap.ClosureGroup(Sx, Cg)
ok("|S C(S)| = 146160", int(SC.Size()) == 146160)
Tg = libgap(Tsol.change_ring(F3))
ok("T hors de S C(S) (il induit l'automorphisme exterieur)", not bool(libgap.IN(Tg, SC)))
ok("T^2 dans S C(S)", bool(libgap.IN(Tg ** 2, SC)))
ZA = libgap.Centre(A)
RES["centre"] = int(ZA.Size())
log("|Z(N)| =", RES["centre"])
# N/S via K = <C, T> (petit), appartenance a S element par element
K = libgap.Group(L3([c2, c6, Tsol]))
Kel = list(K.AsList())
inS = [bool(libgap.IN(x, Sx)) for x in Kel]
homK = libgap.ActionHomomorphism(K, K.AsList(), libgap.OnRight)
Kp = libgap.Image(homK)
KSp = libgap.Group([libgap.Image(homK, x) for x, b in zip(Kel, inS) if b]) if any(inS) else libgap.TrivialSubgroup(Kp)
Qt = libgap.FactorGroup(Kp, KSp)
RES["N_sur_S"] = [int(Qt.Size()), str(libgap.StructureDescription(Qt))]
log("|K| =", len(Kel), "; N/S = KS/S : ordre et structure :", RES["N_sur_S"])
ok("N/S d'ordre 12", int(Qt.Size()) == 12)
# N / C(S) = PGL_2(29) attendu
# scission : un releve a = T s d'une involution de N/C(S) hors de S C(S) qui soit une involution ?
Cset = {tuple(M.change_ring(F3).list()) for M in C12}
trouve = None
for s in Sx.AsList():
    a_ = Tg * s
    if tuple(matrix(F3, (a_ * a_).sage()).list()) in Cset:
        trouve = matrix(F3, a_.sage())
        break
ok("un element a = T s avec a^2 dans C(S) existe", trouve is not None)
ordres_rel = sorted({int(libgap.Order(libgap(trouve * c.change_ring(F3)))) for c in C12})
RES["ordres_releves_a_c"] = ordres_rel
log("ordres des 12 releves a c (c dans C(S)) :", ordres_rel, "-> extension", "SCINDEE (involution hors de S C(S))" if 2 in ordres_rel else "NON SCINDEE au sens de roiban (aucune involution parmi les releves)")
RES["determinants"] = [sorted({int(M.det()) for M in Snew}), sorted({int(M.det()) for M in C12}), int(Tsol.det())]
log("determinants (S ; C(S) ; T) :", RES["determinants"])
np.savez_compressed(os.path.join(SORTIE, "generateurs_x1_base_roiban.npz"), GX=np.array(GX, dtype=np.int64),
                    s29=np.array(Snew[0], dtype=np.int64), s4=np.array(Snew[1], dtype=np.int64),
                    c2=np.array(c2, dtype=np.int64), c6=np.array(c6, dtype=np.int64), T=np.array(Tsol, dtype=np.int64),
                    a29_L56=np.array(A29, dtype=np.int64), b4_L56=np.array(B4, dtype=np.int64))
log("ecrit generateurs_x1_base_roiban.npz")
json.dump(RES, open(os.path.join(SORTIE, "groupe_x1.json"), "w"), indent=1, ensure_ascii=False)
log("FIN groupe_x1 : |N_Aut(X1)(S)| >= ", ordre, "; |C_Aut(X1)(S)| = 12 exactement")
