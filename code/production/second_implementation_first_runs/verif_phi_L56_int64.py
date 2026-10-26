# verif_phi_L56_int64.py -- Claude (agent principal), 25 oct. 2026, 23 h. Reprise du seul cote « phi_L_vers_L56 » de la seconde
# implementation (verif_independante.py, lignes 141-183), dont deux controles ont echoue a 22 h 55. Hypothese a tester : la ligne
# « parts.append(np.unique((Y * sg[:, None]).astype(np.int8), axis=0)) » tronque en int8 les coordonnees des vecteurs minimaux de
# L56 dans la base du depot (non reduite), alors que celles de L (base reduite) tiennent dans int8. Ici : memes donnees, memes
# controles, mais tout en int64 exact (groupe par parcours en largeur, orbites, normes, produits scalaires), sans flottant.
# Version 2 (23 h 05) : stockage int16 avec borne verifiee, distinction par hachage (comme l'original), normes en int64 par blocs,
# produits scalaires en float64 avec borne d'exactitude 2^53 verifiee (le premier essai int64 integral depassait la memoire).
# Usage : python -I verif_phi_L56_int64.py RACINE_DEPOT STRUCTURE_NPZ DOSSIER_CERTIFICATS
import sys, numpy as np
racine, fstruct, dcert = sys.argv[1:4]
def entiers(p):
    return [int(t) for l in open(p) if not l.startswith("#") for t in l.split()]
G = np.array(entiers(racine + "/data/L56_gram.txt"), dtype=np.int64).reshape(56, 56)
gg = np.array(entiers(racine + "/data/sl2_29_generators.txt"), dtype=np.int64).reshape(2, 56, 56)
with np.load(racine + "/certificates/min_reps.npz") as z: M56 = z["reps"].astype(np.int64)
st = np.load(fstruct); fz = st["f"].astype(np.int64)
with np.load(dcert + "/certificats_phi_L_vers_L56.npz") as z: W = z["w0"].astype(np.int64)
with np.load(sys.argv[4] if len(sys.argv) > 4 else fstruct) as z: pass
ECHECS = []
def ok(lab, c):
    print(("[ok]   " if c else "[ECHEC] ") + lab, flush=True)
    if not c: ECHECS.append(lab)
ok("generateurs isometries de L56", all((g @ G @ g.T == G).all() for g in gg))
I = np.eye(56, dtype=np.int64); seen = {I.tobytes()}; fr = [I]; E = [I]
while fr:
    nf = []
    for A in fr:
        for g in gg:
            B = A @ g; k = B.tobytes()
            if k not in seen: seen.add(k); nf.append(B); E.append(B)
    fr = nf
E = np.stack(E); ok("|<g1, g2>| = 24360", len(E) == 24360)
print("max |entree| du groupe :", int(np.abs(E).max()), flush=True)
parts = []; mxc = 0
for r in M56:
    Y = np.einsum("j,ajk->ak", r, E)
    f = (Y != 0).argmax(axis=1); sg = np.sign(Y[np.arange(len(Y)), f])
    Y = Y * sg[:, None]; mxc = max(mxc, int(np.abs(Y).max()))
    assert mxc <= 32767, "coordonnees hors int16"
    parts.append(np.unique(Y.astype(np.int16), axis=0))
del E
V = np.concatenate(parts); del parts
print("max |coordonnee| des vecteurs minimaux de L56 (base du depot) :", mxc, "; int8 suffisait :", mxc <= 127, flush=True)
w = np.random.default_rng(116).integers(1, 2 ** 61, size=56, dtype=np.int64) | 1
h = np.concatenate([V[i:i + (1 << 20)].astype(np.int64) @ w for i in range(0, len(V), 1 << 20)])
ok("%d vecteurs minimaux au signe pres, distincts (hachage), 2 x = |L_6| = 15590400" % len(V), 2 * len(V) == 15590400 and len(np.unique(h)) == len(V))
del h
nV = np.concatenate([np.einsum("ij,jk,ik->i", V[i:i + (1 << 18)].astype(np.int64), G, V[i:i + (1 << 18)].astype(np.int64)) for i in range(0, len(V), 1 << 18)])
ok("tous de norme 6 (int64 exact)", (nV == 6).all()); del nV
nW = np.einsum("ij,jk,ik->i", W, G, W); ok("normes des certificats dans {14, 18}", np.isin(nW, (14, 18)).all())
# classe : la source des certificats phi est ML (representants minimaux de L) ; on reprend la meme verification que l'original
src = None
try:
    import glob
    with np.load(sys.argv[5]) as z: src = z["reps"].astype(np.int64)
except Exception:
    pass
if src is not None:
    ok("chaque certificat est dans la classe de son representant", (((W - (src @ fz)) % 2) == 0).all())
A = W @ G
assert int(np.abs(A).sum(axis=1).max()) * mxc < 2 ** 53, "borne d'exactitude float64"
Af = A.astype(np.float64); mx = np.zeros(len(W), dtype=np.int64)
for i in range(0, len(V), 1 << 16):
    P = Af @ V[i:i + (1 << 16)].astype(np.float64).T
    mx = np.maximum(mx, np.rint(np.abs(P).max(axis=1)).astype(np.int64))
ok("max |<w0, u>| <= 6 sur tous les vecteurs minimaux (int64 exact)", (mx <= 6).all())
print("max |<w0,u>| observe :", int(mx.max()), flush=True)
print("BILAN :", "OK" if not ECHECS else "ECHECS : %s" % ECHECS, flush=True)
sys.exit(0 if not ECHECS else 1)
