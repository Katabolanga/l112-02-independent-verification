# reservoir_x1.py -- lot R112_X1_FICHE_CATALOGUE_20261026 (agent Claude n° 119, 26 oct. 2026). Code ecrit ici.
# Construit et ENREGISTRE le reservoir de vecteurs de norme 10 de X1 (meme code et meme graine que reduction2_x1.py), pour bkz_x1.py.
# Usage : python -I reservoir_x1.py ENTREES GROUPE_NPZ SORTIE
# (en-tete de reduction2_x1.py :)
# VERSION 2 de la reduction : la methode gloutonne pure (reduction_x1.py, essais 1 a 7) donne 111 vecteurs de norme 10 mais une
# base TRES MAL CONDITIONNEE (diagonale de G^-1 ~ 1e40, generateurs a coefficients ~ 1e21) : inutilisable pour le catalogue.
# Ici : « LLL a insertions » : on alterne (i) LLL de PARI (base reduite, donc bien conditionnee) et (ii) remplacement des
# vecteurs de base de norme > 10 par des vecteurs de norme 10 du reservoir de coefficient +-1 sur eux (la base reste une
# base), jusqu'a stabilite ; on garde la base LLL-reduite de plus petite somme diagonale.
# (en-tete de la version 1 :)
# reduction_x1.py -- lot R112_X1_FICHE_CATALOGUE_20261026 (agent Claude n° 119, 26 oct. 2026). Code ecrit ici
# (SageMath 10.6, env sagefull de WSL ; PARI pour LLL ; numpy pour les mises a jour, entiers exacts sous bornes verifiees).
# Objet : une base de X1 de DIAGONALE MINIMALE (lecon 20), partant de genus_class_1.txt (roiban).
# (1) graines de norme 10 : z = (x Y1 + v Y2)/2, x minimal de L (norme 6), v dans x f + 2 L56 de norme 14 (certificats
#     impairs du lot X1, cote phi), et symetriquement (cote psi) ; norme (6 + 14)/2 = 10, VERIFIEE en entiers ;
# (2) reservoir : marches aleatoires (graine fixe) des graines sous les generateurs de <S, C(S), T> (groupe_x1.py) ;
#     vecteurs distincts au signe pres, normes recalculees exactement ;
# (3) LLL de G_X (PARI qflllgram, passage unimodulaire verifie) ;
# (4) base gloutonne PRIMITIVE : a l'etape k, un vecteur p du reservoir de coefficient +-1 sur un vecteur de base
#     non encore choisi le remplace (la base reste une base) ; les coordonnees du reservoir sont mises a jour exactement ;
# (5) controles exacts (Sage, entiers) : P unimodulaire, G_new = P G_X P^t, diagonale, generateurs transportes
#     g' = P g P^-1 entiers et isometries (generateurs de groupe_x1_base_roiban.npz).
# Usage : python -I reduction_x1.py ENTREES GROUPE_NPZ SORTIE
import os, sys, time, json, hashlib
import numpy as np
from sage.all import ZZ, QQ, matrix, pari, identity_matrix, vector, gcd

ENT, FGR, SORTIE = sys.argv[1:4]
os.makedirs(SORTIE, exist_ok=True)
LOG = open(os.path.join(SORTIE, "reduction_x1.log"), "w")
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


def lignes(f):
    return [[int(t) for t in l.split()] for l in open(f) if l.strip() and not l.strip().startswith("#")]


def sha(f):
    return hashlib.sha256(open(f, "rb").read()).hexdigest()


for f in ("structure_x1.npz", "min_reps_L.npz", "min_reps.npz", "certificats_phi_L_vers_L56.npz",
          "certificats_psi_L56_vers_L.npz", "genus_class_1.txt", "L56_gram.txt"):
    log("entree", f, sha(os.path.join(ENT, f)))
log("entree", FGR, sha(FGR))
GXs = matrix(ZZ, lignes(os.path.join(ENT, "genus_class_1.txt")))
GX = np.array(GXs, dtype=np.int64)
G56 = np.array(lignes(os.path.join(ENT, "L56_gram.txt")), dtype=np.int64)
st = np.load(os.path.join(ENT, "structure_x1.npz"), allow_pickle=False)
GL, Y1c, Y2c = st["G_L"].astype(np.int64), st["Y1c"].astype(np.int64), st["Y2c"].astype(np.int64)
ok("Y1 G_X Y1^t = 2 G_L, Y2 G_X Y2^t = 2 G, Y1 G_X Y2^t = 0", (Y1c @ GX @ Y1c.T == 2 * GL).all() and (Y2c @ GX @ Y2c.T == 2 * G56).all() and (Y1c @ GX @ Y2c.T == 0).all())
R6L = np.load(os.path.join(ENT, "min_reps_L.npz"), allow_pickle=False)["reps"].astype(np.int64)
R656 = np.load(os.path.join(ENT, "min_reps.npz"), allow_pickle=False)["reps"].astype(np.int64)
cphi = np.load(os.path.join(ENT, "certificats_phi_L_vers_L56.npz"), allow_pickle=False)
cpsi = np.load(os.path.join(ENT, "certificats_psi_L56_vers_L.npz"), allow_pickle=False)
ok("656 representants minimaux de L (norme 6) et de L56 (norme 6)", len(R6L) == 656 and len(R656) == 656 and
   (np.einsum("ij,jk,ik->i", R6L, GL, R6L) == 6).all() and (np.einsum("ij,jk,ik->i", R656, G56, R656) == 6).all())


def norme(z):
    zz = [int(t) for t in z]
    return sum(zz[i] * int(GX[i, j]) * zz[j] for i in range(112) if zz[i] for j in range(112) if zz[j])


graines = []
for x, w, nw, cote in [(R6L[j], cphi["w0"][j].astype(np.int64), int(cphi["norms"][j]), "phi") for j in range(656)] + \
                      [(cpsi["w0"][j].astype(np.int64), R656[j], int(cpsi["norms"][j]), "psi") for j in range(656)]:
    if nw != 14:
        continue
    z2 = x @ Y1c + w @ Y2c
    if (z2 % 2 != 0).any():
        raise SystemExit("graine hors de X1")
    z = z2 // 2
    if norme(z) != 10:
        raise SystemExit("graine de norme != 10")
    graines.append(z)
graines = np.array(graines, dtype=np.int64)
log("graines de norme 10 (types (6,14) et (14,6)) :", len(graines))
RES["graines"] = len(graines)

gr = np.load(FGR, allow_pickle=False)
gens = [m.astype(np.int64) for m in gr["S_g1g2"]] + [m.astype(np.int64) for m in gr["C"]] + [m.astype(np.int64) for m in gr["T_tous"]]
GXi = np.array(GXs.inverse().change_ring(ZZ), dtype=np.int64)
gens = gens + [GX @ g.T @ GXi for g in gens]
ok("generateurs (et inverses) : isometries entieres de X1", all((g @ GX @ g.T == GX).all() for g in gens))
borne_g = max(int(np.abs(g).max()) for g in gens)
rng = np.random.default_rng(119)
bloc = graines.copy()
reservoir = [bloc]
for pas in range(160):
    g = gens[int(rng.integers(len(gens)))]
    if int(np.abs(bloc).max()) * borne_g * 112 >= 2 ** 62:
        raise SystemExit("borne int64")
    bloc = bloc @ g
    reservoir.append(bloc)
R = np.concatenate(reservoir)
sgn = np.sign(R[np.arange(len(R)), np.argmax(R != 0, axis=1)])
R = R * sgn[:, None]
R = np.unique(R, axis=0)
nr = np.einsum("ij,jk,ik->i", R.astype(np.float64), GX.astype(np.float64), R.astype(np.float64))
log("reservoir : %d vecteurs distincts au signe pres ; normes (flottant) min %.1f max %.1f" % (len(R), nr.min(), nr.max()))

# ---------------------------------------------------------------- LLL a insertions
np.save(os.path.join(SORTIE, "reservoir_norme10.npy"), R)
log("ecrit reservoir_norme10.npy :", R.shape)
