# verif_phi_L56_int64_v3.py -- COPIE CORRIGEE (agent Claude n° 119, 26 oct. 2026) de
#   lots/R112_X1_EFFORT_MAX_20261025/scripts/independant/verif_phi_L56_int64.py (SHA-256 53526cdc4678977a27f14f3f9a0dff1377e52c86e37a524ca8e9353ecd14831f),
# l'original restant INTACT. Corrections demandees par <REVIEWER> (message du 25 oct. 23 h 14 UTC, § 5 a ; rappel du 26 oct. 08:12 UTC) :
#   (1) DONNEES OBLIGATOIRES : les quatre arguments sont exiges ; chaque fichier est verifie AVANT tout calcul (sortie 2 sinon) ;
#       le chargement de la source des certificats (representants minimaux de L, min_reps_L.npz) n'est plus dans un
#       try/except qui avalait l'erreur : le test de classe ne peut plus etre omis ;
#   (2) la ligne sans effet « with np.load(sys.argv[4] if ... else fstruct) as z: pass » est retiree ;
#   (3) les « assert » (inoperants sous python -O) deviennent des controles explicites qui ECHOUENT ;
#   (4) le BILAN exige que la liste COMPLETE des controles attendus ait ete executee (pas seulement l'absence d'echec).
# L'algorithme et les donnees lues sont inchanges (stockage int16 borne, normes int64, produits float64 sous borne 2^53).
# Version 2 de l'original (23 h 05) : stockage int16 avec borne verifiee, distinction par hachage, normes en int64 par blocs,
# produits scalaires en float64 avec borne d'exactitude 2^53 verifiee.
# Usage : python -I verif_phi_L56_int64_v3.py RACINE_DEPOT STRUCTURE_NPZ DOSSIER_CERTIFICATS MINREPS_L_NPZ
# (pour X1 : RACINE_DEPOT = copie_execution/roiban_112, STRUCTURE_NPZ = sorties/structure_x1/structure_x1.npz,
#  DOSSIER_CERTIFICATS = sorties/certificats_X1, MINREPS_L_NPZ = sorties/orbites_min_L/min_reps_L.npz)
import os, sys
import numpy as np

if len(sys.argv) != 5:
    print("usage : python -I verif_phi_L56_int64_v3.py RACINE_DEPOT STRUCTURE_NPZ DOSSIER_CERTIFICATS MINREPS_L_NPZ", flush=True)
    sys.exit(2)
racine, fstruct, dcert, fminL = sys.argv[1:5]
REQUIS = [os.path.join(racine, "data", "L56_gram.txt"), os.path.join(racine, "data", "sl2_29_generators.txt"),
          os.path.join(racine, "certificates", "min_reps.npz"), fstruct,
          os.path.join(dcert, "certificats_phi_L_vers_L56.npz"), fminL]
manquants = [p for p in REQUIS if not os.path.isfile(p)]
if manquants:
    print("DONNEES MANQUANTES (arret avant tout calcul) :", manquants, flush=True)
    sys.exit(2)


def stop(msg):
    print("[ECHEC] " + msg, flush=True)
    print("BILAN : ECHEC (arret)", flush=True)
    sys.exit(1)


def entiers(p):
    return [int(t) for l in open(p) if not l.startswith("#") for t in l.split()]


G = np.array(entiers(REQUIS[0]), dtype=np.int64).reshape(56, 56)
gg = np.array(entiers(REQUIS[1]), dtype=np.int64).reshape(2, 56, 56)
with np.load(REQUIS[2], allow_pickle=False) as z:
    M56 = z["reps"].astype(np.int64)
with np.load(fstruct, allow_pickle=False) as z:
    fz = z["f"].astype(np.int64)
with np.load(REQUIS[4], allow_pickle=False) as z:
    W = z["w0"].astype(np.int64)
with np.load(fminL, allow_pickle=False) as z:
    src = z["reps"].astype(np.int64)
if len(W) != len(src) or len(src) != 656:
    stop("tailles : %d certificats pour %d representants (656 attendus)" % (len(W), len(src)))
ATTENDUS = ["generateurs isometries de L56", "|<g1, g2>| = 24360", "distincts", "tous de norme 6",
            "normes des certificats dans {14, 18}", "classe", "max |<w0, u>| <= 6"]
FAITS, ECHECS = [], []


def ok(cle, lab, c):
    print(("[ok]   " if c else "[ECHEC] ") + lab, flush=True)
    FAITS.append(cle)
    if not c:
        ECHECS.append(lab)


ok(ATTENDUS[0], "generateurs isometries de L56", all((g @ G @ g.T == G).all() for g in gg))
I = np.eye(56, dtype=np.int64)
seen = {I.tobytes()}
fr = [I]
E = [I]
while fr:
    nf = []
    for A in fr:
        for g in gg:
            B = A @ g
            k = B.tobytes()
            if k not in seen:
                seen.add(k)
                nf.append(B)
                E.append(B)
    fr = nf
E = np.stack(E)
ok(ATTENDUS[1], "|<g1, g2>| = 24360", len(E) == 24360)
print("max |entree| du groupe :", int(np.abs(E).max()), flush=True)
parts = []
mxc = 0
for r in M56:
    Y = np.einsum("j,ajk->ak", r, E)
    f = (Y != 0).argmax(axis=1)
    sg = np.sign(Y[np.arange(len(Y)), f])
    Y = Y * sg[:, None]
    mxc = max(mxc, int(np.abs(Y).max()))
    if mxc > 32767:
        stop("coordonnees hors int16")
    parts.append(np.unique(Y.astype(np.int16), axis=0))
del E
V = np.concatenate(parts)
del parts
print("max |coordonnee| des vecteurs minimaux de L56 (base du depot) :", mxc, "; int8 suffisait :", mxc <= 127, flush=True)
w = np.random.default_rng(116).integers(1, 2 ** 61, size=56, dtype=np.int64) | 1
h = np.concatenate([V[i:i + (1 << 20)].astype(np.int64) @ w for i in range(0, len(V), 1 << 20)])
ok(ATTENDUS[2], "%d vecteurs minimaux au signe pres, distincts (hachage), 2 x = |L_6| = 15590400" % len(V),
   2 * len(V) == 15590400 and len(np.unique(h)) == len(V))
del h
if int(np.abs(V).max()) * int(np.abs(G).max()) * 56 >= 2 ** 62:
    stop("borne int64 des normes")
nV = np.concatenate([np.einsum("ij,jk,ik->i", V[i:i + (1 << 18)].astype(np.int64), G, V[i:i + (1 << 18)].astype(np.int64))
                     for i in range(0, len(V), 1 << 18)])
ok(ATTENDUS[3], "tous de norme 6 (int64 exact)", (nV == 6).all())
del nV
nW = np.einsum("ij,jk,ik->i", W, G, W)
ok(ATTENDUS[4], "normes des certificats dans {14, 18}", np.isin(nW, (14, 18)).all())
ok(ATTENDUS[5], "chaque certificat est dans la classe de son representant (w0 = r f mod 2)", (((W - (src @ fz)) % 2) == 0).all())
A = W @ G
if int(np.abs(A).sum(axis=1).max()) * mxc >= 2 ** 53:
    stop("borne d'exactitude float64")
Af = A.astype(np.float64)
mx = np.zeros(len(W), dtype=np.int64)
for i in range(0, len(V), 1 << 16):
    P = Af @ V[i:i + (1 << 16)].astype(np.float64).T
    mx = np.maximum(mx, np.rint(np.abs(P).max(axis=1)).astype(np.int64))
ok(ATTENDUS[6], "max |<w0, u>| <= 6 sur tous les vecteurs minimaux (int64 exact)", (mx <= 6).all())
print("max |<w0,u>| observe :", int(mx.max()), flush=True)
complet = FAITS == ATTENDUS
if not complet:
    ECHECS.append("liste des controles incomplete : %s" % FAITS)
print("controles executes : %d / %d attendus" % (len(FAITS), len(ATTENDUS)), flush=True)
print("BILAN :", "OK" if not ECHECS else "ECHECS : %s" % ECHECS, flush=True)
sys.exit(0 if not ECHECS else 1)
