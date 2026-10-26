# test_formes.py -- agent 116 : test unitaire de la seconde implementation (formes_canoniques.c + groupe modulo 2 enumere ici)
# contre lib/mod2.py de roiban, sur les 656 classes des representants minimaux de L56 : les formes canoniques (minimum sur l'orbite)
# doivent etre IDENTIQUES (meme ensemble de 12180 matrices modulo 2), ainsi que les tailles d'orbites.
# Usage : python -I test_formes.py RACINE BIN_FORMES DOSSIER
import os, sys, struct, subprocess
import numpy as np
racine, binf, sortie = sys.argv[1:4]
os.makedirs(sortie, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BITS = np.uint64(1) << np.arange(56, dtype=np.uint64)
def entiers(p):
    return [int(t) for l in open(p) if not l.startswith("#") for t in l.split()]
gg = np.array(entiers(os.path.join(racine, "data", "sl2_29_generators.txt")), dtype=np.int64).reshape(2, 56, 56)
with np.load(os.path.join(racine, "certificates", "min_reps.npz"), allow_pickle=False) as z:
    M = z["reps"].astype(np.int64)
# groupe modulo 2 (parcours en largeur sur les matrices modulo 2, code ici)
I = np.eye(56, dtype=np.int64)
vus = {I.tobytes()}; L = [I]; i = 0
g2 = [g % 2 for g in gg]
while i < len(L):
    X = L[i]; i += 1
    for g in g2:
        Y = (X @ g) % 2
        k = Y.tobytes()
        if k not in vus:
            vus.add(k); L.append(Y)
print("ordre de l'image modulo 2 :", len(L))
fg = os.path.join(sortie, "test_groupe.bin"); fc = os.path.join(sortie, "test_classes.bin"); fo = os.path.join(sortie, "test_formes.bin")
with open(fg, "wb") as h:
    h.write(struct.pack("<Q", len(L)))
    for X in L:
        h.write(struct.pack("<56Q", *[int(t) for t in (X.astype(np.uint64) * BITS).sum(axis=1)]))
cls = ((M % 2).astype(np.uint64) * BITS).sum(axis=1)
with open(fc, "wb") as h:
    h.write(struct.pack("<Q", len(cls))); h.write(cls.astype("<u8").tobytes())
r = subprocess.run([binf, fg, fc, fo], capture_output=True, text=True); print(r.stderr.strip())
raw = open(fo, "rb").read(); N = len(cls)
mine = np.frombuffer(raw[:8 * N], dtype="<u8"); orb = np.frombuffer(raw[8 * N:], dtype="<u4")
# reference : lib/mod2.py de roiban (lue)
sys.path.insert(0, os.path.join(racine, "code"))
from lib import group, mod2
S = group.sl2_29_mod_sign(gg)
ref, refo = mod2.Canonical(S).canon_and_orbit_size(mod2.pack(M))
print("formes identiques :", bool((mine == ref).all()), "; tailles identiques :", bool((orb.astype(np.int64) == refo).all()),
      "; distribution des tailles :", {int(k): int(v) for k, v in zip(*np.unique(orb, return_counts=True))})
sys.exit(0 if (mine == ref).all() and (orb.astype(np.int64) == refo).all() else 1)
