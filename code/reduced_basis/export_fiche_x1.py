# export_fiche_x1.py -- lot R112_X1_FICHE_CATALOGUE_20261026 (agent Claude n° 119, 26 oct. 2026). Code ecrit ici (SageMath 10.6).
# Fabrique les fichiers de la fiche de X1 a partir de :
#   * la base reduite (reduction_x1.py : G_new = P G_roiban P^t, P unimodulaire) ;
#   * les generateurs (groupe_x1.py : s29, s4 de S = SL_2(29), c2, c6 de C(S) = C2 x C6, T exterieur ; base de roiban) ;
# et ecrit, apres controles EXACTS (entiers Sage) :
#   X1_gram.txt (matrice complete), X1_gram_gap_magma.txt ([[...],...]), X1_passage_from_roiban.txt (P),
#   X1_generators.txt et X1_generators_gap.txt (s29, s4, c2, c6, T dans la base reduite),
#   X1_112.std (format du catalogue de Nebe et Sloane : sections dans l'ordre des fiches « SUBGROUP_* »),
# avec les relations T^-1 s29 T = mot(s29, s4) et T^-1 s4 T = mot(s29, s4) (mots les plus courts, GAP Factorization sur
# la reduction modulo 3 de l'action sur L56, puis VERIFIES en entiers sur X1).
# Les textes NOTES et REFERENCES sont lus dans des fichiers a part (anglais).
# Usage : python -I export_fiche_x1.py ENTREES REDUCTION_NPZ GROUPE_NPZ GENERATEURS_NPZ NOTES_TXT REFS_TXT SORTIE
import os, sys, time, hashlib
import numpy as np
from sage.all import ZZ, QQ, GF, matrix, identity_matrix, block_matrix, libgap

ENT, FRED, FGR, FGEN, FNOTES, FREFS, SORTIE = sys.argv[1:8]
os.makedirs(SORTIE, exist_ok=True)
LOG = open(os.path.join(SORTIE, "export_fiche_x1.log"), "w")
T0 = time.time()


def log(*a):
    s = " ".join(str(x) for x in a)
    print("[%7.1f s] %s" % (time.time() - T0, s), flush=True)
    LOG.write("[%7.1f s] %s\n" % (time.time() - T0, s))
    LOG.flush()


def ok(label, cond):
    log("[ok]   " if cond else "[ECHEC]", label)
    if not cond:
        raise SystemExit("ECHEC : " + label)


def lignes(f):
    return [[int(t) for t in l.split()] for l in open(f) if l.strip() and not l.strip().startswith("#")]


def sha(f):
    return hashlib.sha256(open(f, "rb").read()).hexdigest()


for f in (FRED, FGR, FGEN, os.path.join(ENT, "genus_class_1.txt"), FNOTES, FREFS):
    log("entree", f, sha(f))
GX = matrix(ZZ, lignes(os.path.join(ENT, "genus_class_1.txt")))
red = np.load(FRED, allow_pickle=False)
P0 = red["P"].astype(np.int64)
G0 = red["G"].astype(np.int64)
perm = sorted(range(112), key=lambda i: (int(G0[i, i]), i))          # vecteurs ranges par norme croissante
P = matrix(ZZ, P0[perm].tolist())
Gn = matrix(ZZ, G0[perm][:, perm].tolist())
log("base rangee par norme croissante ; diagonale :", [int(Gn[i, i]) for i in range(112)])
ok("P unimodulaire", abs(P.det()) == 1)
ok("G_new = P G_roiban P^t", P * GX * P.transpose() == Gn)
ok("G_new symetrique, paire, det 1, definie positive", Gn == Gn.transpose() and all(Gn[i, i] % 2 == 0 for i in range(112)) and Gn.det() == 1 and Gn.is_positive_definite())
Pi = P.inverse().change_ring(ZZ)
gz = np.load(FGEN, allow_pickle=False)
noms = ["s29", "s4", "c2", "c6", "T"]
ordres_attendus = {"s29": 29, "s4": 4, "c2": 2, "c6": 6}
I = identity_matrix(ZZ, 112)
gens = {}
for nm in noms:
    g = matrix(ZZ, gz[nm].tolist())
    ok("%s : isometrie de G_roiban" % nm, g * GX * g.transpose() == GX)
    h = P * g * Pi
    ok("%s : transporte P g P^-1 entier, isometrie de G_new" % nm, all(x in ZZ for x in h.list()) and h * Gn * h.transpose() == Gn)
    gens[nm] = h.change_ring(ZZ)
for nm, o in ordres_attendus.items():
    g = gens[nm]
    ok("ordre exact de %s : %d" % (nm, o), g ** o == I and all(g ** d != I for d in range(1, o) if o % d == 0))
oT = next(k for k in range(1, 400) if gens["T"] ** k == I)
log("ordre de T :", oT)
ok("s4^2 = -1", gens["s4"] ** 2 == -I)
ok("c2, c6 commutent a s29, s4 et entre eux", all(gens[c] * gens[s] == gens[s] * gens[c] for c in ("c2", "c6") for s in ("s29", "s4")) and gens["c2"] * gens["c6"] == gens["c6"] * gens["c2"])
mx = max(int(abs(x)) for nm in noms for x in gens[nm].list())
log("max |coefficient| des generateurs dans la base reduite :", mx)
# relations T^-1 s T = mot(s29, s4), mots les plus courts (GAP, sur L56 modulo 3 ; Factorization)
A29 = matrix(ZZ, gz["a29_L56"].tolist())
B4 = matrix(ZZ, gz["b4_L56"].tolist())
gr = np.load(FGR, allow_pickle=False)
F3 = GF(3)
Ga = libgap.Group([libgap(A29.change_ring(F3)), libgap(B4.change_ring(F3))])
ok("<a29, b4> sur L56 (mod 3) : ordre 24360", int(Ga.Size()) == 24360)
Ti = gens["T"].inverse().change_ring(ZZ)
rels = []
for nm in ("s29", "s4"):
    cible = Ti * gens[nm] * gens["T"]           # = alpha(s) sur X1 ; on cherche son image sur L56 via l'action diagonale
    # sur X1 (base de roiban), cible_roiban = Pi cible P = D diag(x, x) D^-1 : on lit x dans la base ambiante
    cible_r = Pi * cible * P
    rb = lignes(os.path.join(ENT, "genus_basis_1.txt"))
    Dm = matrix(ZZ, rb[1:113]).change_ring(QQ)
    amb = Dm.inverse() * cible_r.change_ring(QQ) * Dm
    x = amb[:56, :56]
    ok("%s : T^-1 %s T est diagonal (diag(x, x)) en coordonnees ambiantes" % (nm, nm), amb[56:, 56:] == x and amb[:56, 56:] == 0 and amb[56:, :56] == 0 and all(t in ZZ for t in x.list()))
    w = libgap.Factorization(Ga, libgap(x.change_ring(ZZ).change_ring(F3)))
    lettres = libgap.LetterRepAssocWord(w).sage()
    mot = "".join({1: "a", -1: "A", 2: "b", -2: "B"}[e] for e in lettres)
    M = I
    inv = {"a": gens["s29"], "b": gens["s4"], "A": gens["s29"] ** 28, "B": gens["s4"] ** 3}
    for ch in mot:
        M = M * inv[ch]
    ok("relation T^-1*%s*T = mot de longueur %d en s29, s4 : VERIFIEE en entiers sur X1" % (nm, len(mot)), M == cible)
    rels.append(("T^-1*%s*T" % nm, mot))
T2 = gens["T"] ** 2
log("T^2 : ordre", next(k for k in range(1, 400) if T2 ** k == I))


# ---- ecriture des fichiers
def ecrire_matrice(h, M):
    for i in range(M.nrows()):
        h.write(" ".join(str(int(t)) for t in M.row(i)) + "\n")


with open(os.path.join(SORTIE, "X1_gram.txt"), "w", newline="\n") as h:
    h.write("# X1 (dimension 112, even unimodular, minimum 10): Gram matrix (112 rows) in a basis of minimal vectors where possible.\n")
    h.write("# GRAM = P * G_roiban * P^T, G_roiban = certificates/genus_class_1.txt of github.com/roiban1344 (CC BY 4.0), P = X1_passage_from_roiban.txt.\n")
    ecrire_matrice(h, Gn)
with open(os.path.join(SORTIE, "X1_gram_gap_magma.txt"), "w", newline="\n") as h:
    h.write("[" + ",\n".join("[" + ",".join(str(int(t)) for t in Gn.row(i)) + "]" for i in range(112)) + "]\n")
with open(os.path.join(SORTIE, "X1_passage_from_roiban.txt"), "w", newline="\n") as h:
    h.write("# P (112 x 112, integer, det +-1): rows = the basis of X1_gram.txt written in the basis of genus_class_1.txt (roiban1344).\n")
    h.write("# X1_gram = P * G_roiban * P^T.\n")
    ecrire_matrice(h, P)
with open(os.path.join(SORTIE, "X1_generators.txt"), "w", newline="\n") as h:
    h.write("# Generators of a subgroup of Aut(X1), in the basis of X1_gram.txt, row convention: g * GRAM * g^T = GRAM.\n")
    for nm in noms:
        h.write("# %s\n" % nm)
        ecrire_matrice(h, gens[nm])
with open(os.path.join(SORTIE, "X1_generators_gap.txt"), "w", newline="\n") as h:
    for nm in noms:
        M = gens[nm]
        h.write("%s := [" % nm + ",\n".join("[" + ",".join(str(int(t)) for t in M.row(i)) + "]" for i in range(112)) + "];\n")
notes = open(FNOTES, encoding="utf-8").read().rstrip("\n")
refs = open(FREFS, encoding="utf-8").read().rstrip("\n")
for t in (notes, refs):
    t.encode("ascii")                          # le fichier .std reste en ASCII
with open(os.path.join(SORTIE, "X1_112.std"), "w", newline="\n", encoding="ascii") as h:
    h.write("%NAME\nX1_112\n%DIMENSION\n112\n%DET\n1\n%GRAM\n112 0\n")
    for i in range(112):
        h.write(" ".join(str(int(Gn[i, j])) for j in range(i + 1)) + "\n")
    h.write("%DIVISORS\n1\n%MINIMAL_NORM\n10\n%KISSING_NUMBER\n10888335360\n%HERMITE_NUMBER\n10\n")
    h.write("%SUBGROUP_ORDER\n2^5*3^2*5*7*29\n%SUBGROUP_NAME\n(SL_2(29) o (C2 x C6)).2\n%SUBGROUP_GENERATORS\n5\n")
    for nm in noms:
        h.write("112\t112\n")
        ecrire_matrice(h, gens[nm])
    h.write("%PROPERTIES\nUnimodular=1\n%REFERENCES\n" + refs + "\n%NOTES\n" + notes + "\n")
    for lhs, mot in rels:
        h.write("RELATION: %s = %s\n" % (lhs, mot))
    h.write("%LAST_LINE\n")
ok("2^5*3^2*5*7*29 = 292320", 2 ** 5 * 3 ** 2 * 5 * 7 * 29 == 292320)
for f in ("X1_gram.txt", "X1_gram_gap_magma.txt", "X1_passage_from_roiban.txt", "X1_generators.txt", "X1_generators_gap.txt", "X1_112.std"):
    log("ecrit", f, sha(os.path.join(SORTIE, f)))
log("FIN export_fiche_x1")
